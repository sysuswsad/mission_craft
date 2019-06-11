from flask import (
    Blueprint, g, request
)
from werkzeug.exceptions import abort
import datetime

from app.auth import auth
from app.db import get_db
from app.api import bp
from app.response_code import bad_request, unauthorized, ok, created, forbidden, error_response
from app.statistics import statistics_ana

from app.api.notification import create_notification_type_8, get_unread_num

import json
import re

# ????????????需要有一个机制处理过期任务
@bp.route('/mission/', methods=['POST'])
@auth.login_required
def create_mission():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT CREATE MISSION')

    mission_type = data.get('type')
    deadline = data.get('deadline')
    title = data.get('title')
    description = data.get('description')
    qq = data.get('qq')
    wechat = data.get('wechat')
    phone = data.get('phone')
    other_way = data.get('other_way')
    bounty = data.get('bounty')
    max_num = data.get('max_num', 1)
    problems = data.get('problems')

    # bounty等于0也会报错Missing some necessary parameter
    if (not mission_type and mission_type != 0) or (not deadline) or (not title) or (not description) or (not bounty):
        return bad_request('Missing some necessary parameter')
    elif (not qq) and (not wechat) and (not phone) and (not other_way):
        return bad_request('Missing contact info')
    elif not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', deadline):
        return bad_request('Deadline format error')
    elif datetime.datetime.now() > datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S'):
        return bad_request('Deadline should be in future')

    try:
        mission_type = int(mission_type)
        bounty = float(bounty)
        max_num = int(max_num)
    except Exception:
        return bad_request('Parse parameter error')
    deadline = datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')

    db = get_db()
    db.execute(
        'INSERT INTO MissionInfo (publisher_id, type, deadline, title, description, qq, wechat, phone, other_way, bounty, max_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (g.user['idUser'], mission_type, deadline, title, description, qq, wechat, phone, other_way, bounty, max_num)
    )
    db.commit()
    # 这里可以通过type(fetchone())来查看列值；通过fetchone().keys()查看列名
    mission_id = db.execute('SELECT last_insert_rowid() FROM MissionInfo').fetchone()[0]
    # 该用户发布任务数量+1
    db.execute(
        'UPDATE User SET mission_pub_num=mission_pub_num+1 WHERE idUser = ?', 
        (g.user['idUser'],)
    )
    # 处理问卷任务
    if mission_type == 0:
        # 创建任务之前检查金额，金额足够才能创建????????????待完成
        if not problems:
            return bad_request('Questionare should have problems')
        problems = json.loads(problems)
        # 建议debug的时候注释掉这些try，便于看到错误
        try:
            for problem in problems:
                db.execute('INSERT INTO Problem (mission_id, type, problem_stem, problem_detail) VALUES (?, ?, ?, ?)', 
                    (mission_id, int(problem['type']), problem['question'], json.dumps(problem.get('choices', '')))
                )
        except Exception:
            return bad_request('Parse problems error')

    db.commit()
    return created('Create mission successfully', data={'mission_id':mission_id})


@bp.route('/mission/', methods=['get'])
@auth.login_required
def get_mission():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT GET MISSION')

    limit = data.get('limit')
    mission_type = data.get('type')
    return_problems = data.get('return_problems')
    return_statistics = data.get('return_statistics')

    bounty = data.get('bounty')
    create_time = data.get('create_time')
    if not bounty:
        bounty = 0.0
    if not create_time:
        create_time = '2000-01-01 00:00:00'

    personal = data.get('personal')
    mission_id = data.get('mission_id')

    db = get_db()
    mission_array = []
    col_name = [name_list[1] for name_list in db.execute('PRAGMA table_info(MissionInfo)').fetchall()]
    col_name.remove('phone');col_name.remove('qq');col_name.remove('wechat');col_name.remove('other_way')
    # 若missionid不为空，说明是通过missionid查询特定订单信息，不需要提供任何其他信息
    if mission_id or mission_id == 0:
        try:
            mission_id = int(mission_id)
        except Exception:
            return bad_request('Parse mission id error')
        mission_info = db.execute(
            'SELECT * FROM MissionInfo WHERE idMissionInfo = ?', (mission_id,)
        ).fetchone()
        if not mission_info:
            return bad_request('No such mission')
        mission_json = {}
        for item in col_name:
            mission_json[item] = mission_info[item]
        mission_array.append(mission_json)
    elif personal or personal == 0:
        try:
            create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
            bounty = float(bounty)
            personal = int(personal)
        except Exception:
            return bad_request('Parse create_time, bounty or personal error')
        # personal为0时表示广场查询，为1时表示私人查询
        if personal == 0:
            mission_info = db.execute(
                'SELECT * FROM MissionInfo WHERE bounty > ? AND create_time > ?', 
                (bounty, create_time)
            ).fetchall()
        elif personal == 1:
            mission_info = db.execute(
                'SELECT * FROM MissionInfo WHERE publisher_id = ? AND bounty > ? AND create_time > ?', 
                (g.user['idUser'], bounty, create_time)
            ).fetchall()
        for row in mission_info:
            mission_json = {}
            for item in col_name:
                mission_json[item] = row[item]
            mission_array.append(mission_json)
    else:
        return bad_request('Personal or mission_id are required')
    # 根据mission_type筛选
    if mission_type or mission_type == 0:
        try:
            mission_type = int(mission_type)
        except Exception:
            return bad_request('Parse mission type error')
        mission_temp = []
        for item in mission_array:
            if item['type'] == mission_type:
                mission_temp.append(item)
        mission_array = mission_temp

    if len(mission_array) == 0:
        return bad_request('No search result for the param')

    # 使用问题表完善missioninfo信息
    for item in mission_array:
        item['problems'] = ''
        if item['type'] == 0 and return_problems:
            problem_info = db.execute(
                'SELECT * FROM Problem WHERE mission_id = ?', (item['idMissionInfo'],)
            ).fetchall()
            problems = []
            for row in problem_info:
                problem_json = {}
                problem_json['type'] = row['type']
                problem_json['question'] = row['problem_stem']
                problem_json['choices'] = json.loads(row['problem_detail'])
                problems.append(problem_json)
            item['problems'] = problems
            # 如果问卷任务还需要返回答案统计信息
            if item['publisher_id'] != g.user['idUser'] or (not return_statistics):
                continue
            for num in range(0, len(problems)):
                item['problems'][num]['answer'] = statistics_ana(problem_info[num]['type'], problem_info[num]['problem_detail'], problem_info[num]['idProblem'])

    # 讨论过后发现不需要接单人信息
    # 使用订单表完善missioninfo信息，如果是其他任务需要先检查任务是否被接受，如果是那么就需要返回接收人任务人信息    
    for item in mission_array:
        item['receiver_id'] = ''
        item['receiver_time'] = ''
        user_info = db.execute(
            'SELECT username, avatar FROM User WHERE idUser = ?', (item['publisher_id'],)
        ).fetchone()
        item['avatar'] = user_info['avatar']
        item['username'] = user_info['username']
        # 暂时只考虑快递任务，如果有人接单且查询人是发布者，返回接单人信息
        if item['type'] == 1 and item['rcv_num'] == 1 and item['publisher_id'] == g.user['idUser']:
            mission_order = db.execute(
                'SELECT receiver_id, receive_time FROM MissionOrder WHERE mission_id = ?', (item['idMissionInfo'],)
            ).fetchone()
            item['receiver_id'] = mission_order['receiver_id']
            item['receiver_time'] = mission_order['receive_time']

    # 选出后limit个
    if limit and int(limit) < len(mission_array):
        limit = int(limit)
        mission_array = mission_array[len(mission_array)-limit:len(mission_array)]

    # notification
    # return ok('Get missions successfully', data={'missions':mission_array})
    return ok('Get missions successfully', data={'missions': mission_array, 'notification_num': get_unread_num(g.user['idUser'])})


@bp.route('/mission/', methods=['put'])
@auth.login_required
def cancel_mission():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT CANCEL MISSION')

    db = get_db()
    mission_id = data.get('mission_id')
    if (mission_id is None):
        return bad_request('Mission_id is required')
    mission_info = db.execute('SELECT * FROM MissionInfo WHERE idMissionInfo = ?',
        (mission_id,) 
    ).fetchone()
    if(mission_info is None):
        return bad_request('Mission_id is invalid')
    
    rcv_num = mission_info['rcv_num']
    max_num = mission_info['max_num']
    # 问卷
    # 发布者可以取消
    if(mission_info['type'] == 0):
        if(mission_info['publisher_id'] == g.user['idUser']):
            db.execute('UPDATE MissionInfo SET state = ? WHERE idMissionInfo = ?', (1, mission_id))
            db.commit()
            return ok('cancel successfully')
        else:
            order_info = db.execute('SELECT * FROM MissionOrder WHERE mission_id = ?', (mission_id,)).fetchone()
            if order_info['receiver_id'] == g.user['idUser']:
                # 如果问卷原本是满人了,就重新开放
                if rcv_num == max_num:
                    db.execute('UPDATE MissionInfo SET state = ? WHERE idMissionInfo = ?', (0, mission_id))         
                # 修改接单人数
                db.execute('UPDATE MissionInfo SET rcv_num = ? WHERE idMissionInfo = ?', (rcv_num - 1, mission_id))
                # 订单取消
                db.execute('UPDATE MissionOrder SET order_state = ? WHERE mission_id = ?', (2, mission_id))
                db.commit()
                return ok('cancel successfully')
            else:
                return error_response(403, 'The operation is forbidden')
    # 取快递
    # 没人接，发布者可以取消
    # 领取者主动放弃
    elif(mission_info['type'] == 1):
        if(mission_info['publisher_id'] == g.user['idUser']):
            if rcv_num != 0:
                return error_response(400, 'Should not cancel a mission already received')
            else:
                db.execute('UPDATE MissionInfo SET state = ? WHERE idMissionInfo = ?', (1, mission_id))
                db.commit()
                return ok('cancel successfully')        
        else:
            order_info = db.execute('SELECT * FROM MissionOrder WHERE mission_id = ?', (mission_id,)).fetchone()
            if order_info['receiver_id'] == g.user['idUser']:
                db.execute('UPDATE MissionInfo SET rcv_num = ?, state = ? WHERE idMissionInfo = ?', (rcv_num - 1, 0, mission_id))
                # 订单取消
                db.execute('UPDATE MissionOrder SET order_state = ? WHERE mission_id = ?', (2, mission_id))
                db.commit()

                # notification
                create_notification_type_8(
                    mission_id=mission_info['idMissionInfo'], 
                    receiver_id=order_info['receiver_id'], 
                    cancel_time=datetime.datetime.now())
                
                return ok('cancel successfully')
            else:
                return error_response(403, 'The operation is forbidden')
            
    else:
        return error_response(500, 'Server Internal error')

    # 取消任务之后返回部分或全部金额，????????????待完成
