from flask import (
    Blueprint, g, request
)
from werkzeug.exceptions import abort
import datetime

from app.auth import auth
from app.db import get_db
from app.api import bp
from app.response_code import bad_request, unauthorized, ok, created, forbidden
from app.currency import get_by_confirm

import json

from app.api.notification import (
    create_notification_type_1, create_notification_type_3, 
    create_notification_type_4, create_notification_type_8)

# 查看个人领取订单
@bp.route('/order/', methods=['GET'])
@auth.login_required
def get_rcv_order():
    db = get_db()
    orders = db.execute(
        'SELECT * FROM MissionOrder WHERE receiver_id = ?', (g.user['idUser'],)
    ).fetchall()
    
    data = {}
    l = []
    for order in orders:
        mission_id = order['mission_id']
        # 查publisher_id
        mission_info = db.execute(
            'SELECT publisher_id, title, type, phone, qq, wechat, other_way FROM MissionInfo WHERE idMissionInfo = ?', (mission_id,)
        ).fetchone()

        obj = {}
        obj['order_id'] = order['idMissionOrder']
        obj['receiver_id'] = order['receiver_id']
        # modified by ousx
        obj['publisher_id'] = mission_info['publisher_id']
        obj['mission_id'] = order['mission_id']
        obj['title'] = mission_info['title']
        obj['type'] = mission_info['type']
        obj['phone'] = mission_info['phone']
        obj['qq'] = mission_info['qq']
        obj['wechat'] = mission_info['wechat']
        obj['other_way'] = mission_info['other_way']
        # end modified

        obj['order_state'] = order['order_state']
        obj['publisher_confirm'] = order['publisher_confirm']
        obj['receiver_confirm'] = order['receiver_confirm']
        obj['receive_time'] = order['receive_time']
        obj['finish_time'] = order['finish_time']
        l.append(obj)
    data['orders'] = l
    return ok('return successfully', data=data)


# 创建个人订单
@bp.route('/order/', methods=['POST'])
@auth.login_required
def create_order():
    data = request.get_json()
    # 得到json Data
    if not data:
        return bad_request('ERROR PARAM AT CREATING ORDER')
    # 得到任务ID
    mission_id = data.get('mission_id')
 
    db = get_db()
    mission = db.execute(
        'SELECT * FROM MissionInfo WHERE idMissionInfo = ?', (mission_id,)
    ).fetchone()
    # id不存在
  
    if(mission is None):
        return bad_request('mission_id is invalid')
  
    # 已经结束
    if(mission['state'] == 1):
        return bad_request('Mission is closed') 
    # 达最大接单数
    rcv_num = mission['rcv_num']
    max_num = mission['max_num']
    deadline = mission['deadline']
    # 达最大接收量

    if(rcv_num >= max_num):
        db.execute(
        'UPDATE MissionInfo SET state = ? WHERE idMissionInfo = ?',
            (1, mission_id)
        )
        db.commit()
        return bad_request('mission reached its max rcv num')
    # 时间过期

    # if(datetime.datetime.now() > datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')):
    #     db.execute(
    #     'UPDATE MissionInfo SET state = ? WHERE idMissionInfo = ?',
    #         (1,mission_id)
    #     )
    #     db.commit()
    #     return bad_request('mission reached its dealine')

    # 任务正常关闭
    state = 1 if rcv_num + 1 == max_num else 0

    db.execute(
        'UPDATE MissionInfo SET state = ? , rcv_num = ? WHERE idMissionInfo = ?',(state, rcv_num + 1, mission_id)
    )

    # 添加订单
    db.execute(
      'INSERT INTO MissionOrder (mission_id, receiver_id, receive_time) VALUES (?, ?, ?)',
        (mission_id, g.user['idUser'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
 
    # 得到订单id
    order_id = db.execute(
        'select last_insert_rowid() from MissionOrder'
    ).fetchone()
    db.commit()

    obj = {
        'order_id': order_id[0]
    }
    
    # notification
    if mission['type'] != 0: # 对于非问卷类任务
        create_notification_type_3(mission['idMissionInfo'])

    return created('Create order successfully', data=obj)


@bp.route('/order/', methods=['PUT'])
@auth.login_required
def confirm_order():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT CREATE MISSION')

    db = get_db()

    order_id = data.get('order_id')	
    try:
        order_id = int(order_id)
    except Exception:
        return bad_request('Parse order id error')
    order_info = db.execute(
        'SELECT mission_id, receiver_id, order_state FROM MissionOrder WHERE idMissionOrder = ?', (order_id,)
    ).fetchone()
    if not order_info:
        return bad_request('No such mission')

    mission_info = db.execute(
        'SELECT publisher_id, type, bounty, max_num FROM MissionInfo WHERE idMissionInfo = ?', (order_info['mission_id'],)
    ).fetchone()

    # 确认过的/过期的 订单不能再确认，防止再次生成答案表
    if order_info['order_state'] == 1:
        return bad_request('The order has been confirmed')

    # 分成两类，问卷由接收人确认即可，其他任务由发布人确认
    if mission_info['type'] == 0:
        if order_info['receiver_id'] != g.user['idUser']:
            return forbidden('You can not submit for other receivers')
        answers = json.loads(data.get('answers'))
        problem_ids = db.execute(
            'SELECT idProblem FROM Problem WHERE mission_id = ?', (order_info['mission_id'],)
        ).fetchall()
        try:
            for i in range(0, len(answers)):
                db.execute('INSERT INTO Answer (order_id, problem_id, result) VALUES (?, ?, ?)', 
                    (order_id, problem_ids[i]['idProblem'], json.dumps(answers[i]))
                )
            db.commit()
        except Exception:
            return bad_request('Parse answers error')
    elif mission_info['type'] == 1:
        if mission_info['publisher_id'] != g.user['idUser']:
            return forbidden('You can not submit for other publishers')

    # 为接单人发钱
    get_by_confirm(mission_info['bounty']/mission_info['max_num'], 
    	g.user['idUser'] if mission_info['type'] == 0 else order_info['receiver_id'])
    
    # 更新其它表
    db.execute(
        'UPDATE MissionOrder SET publisher_confirm = ?, receiver_confirm = ?, order_state = ?, finish_time = ? WHERE idMissionOrder = ?', 
        (1, 1, 1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), order_id,)
    )
    db.execute(
        'UPDATE User SET mission_fin_num = mission_fin_num + 1 WHERE idUser = ?', 
        (order_info['receiver_id'],)
    )
    db.execute(
        'UPDATE MissionInfo SET fin_num = fin_num + 1 WHERE idMissionInfo = ?', 
        (order_info['mission_id'],)
    )
    db.commit()
    db.execute(
        'UPDATE MissionInfo SET state = 1 WHERE idMissionInfo = ? AND fin_num==max_num', 
        (order_info['mission_id'],)
    )
    db.commit()

    # notification
    if mission_info['type'] == 0:
        create_notification_type_1(order_info['mission_id'])
    elif mission_info['type'] == 1:
        create_notification_type_4(order_info['mission_id'])


    return ok('Confirm order successfully')
