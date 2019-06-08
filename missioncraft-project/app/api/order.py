from flask import (
    Blueprint, g, request
)
from werkzeug.exceptions import abort
import datetime

from app.api.user import auth
from app.db import get_db
from app.api import bp
from app.response_code import bad_request, unauthorized, ok, created

import json

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
        publisher_id = db.execute(
            'SELECT publisher_id FROM MissionInfo WHERE idMissionInfo = ?', (mission_id,)
        ).fetchone()
        obj = {}
        obj['order_id'] = order['idMissionOrder']
        obj['receiver_id'] = order['receiver_id']
        obj['publisher_id'] = publisher_id['publisher_id']
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
    
    if(datetime.datetime.now() > datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')):
        db.execute(
        'UPDATE MissionInfo SET state = ? WHERE idMissionInfo = ?',
            (1,mission_id)
        )
        db.commit()
        return bad_request('mission reached its dealine')

    # 任务正常关闭
    state = 1 if rcv_num + 1 == max_num else 0

    db.execute(
        'UPDATE MissionInfo SET state = ? , rcv_num = ? WHERE idMissionInfo = ?',(state, rcv_num + 1, mission_id)
    )

    # 添加订单
    db.execute(
      'INSERT INTO MissionOrder (mission_id, receiver_id, receive_time) VALUES (?, ?, ?)',
        (mission_id, g.user['idUser'], datetime.datetime.now())
    )
 
    # 得到订单id
    order_id = db.execute(
        'select last_insert_rowid() from MissionOrder'
    ).fetchone()
    db.commit()

    obj = {
        'order_id': order_id[0]
    }
  
    return created('Create order successfully', data=obj)

    
# 确认个人订单
@bp.route('/order/', methods=['PUT'])
@auth.login_required
def confirm_order():
    return ''