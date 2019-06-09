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



@bp.route('/notification/', methods=('get'))
@auth.login_required
def get_notification():
    """返回对应通知id的通知item
    """
    # data = request.get_json()
	# if not data:
	# 	return bad_request('ERROR DATA AT GET NOTIFICATION')
    notifications = get_db().execute(
        'SELECT n_id, mission_id, message, create_time, has_read'
        ' FROM Notification n'
        ' WHERE n.n_id = ?',
        (g.user['idUser'],)
    ).fetchone()

    return ok('Get notifications successfully', data={'notifications': notifications})


def get_unread_num(user_id):
    """获取未读通知读数量
    """
    db = get_db()
    notifications = db.execute(
        'SELECT *'
        ' FROM Notification'
        ' WHERE user_id = ? AND has_read = 1',
        (user_id, )
    ).fetchone()
    return len(notifications)

def has_created(n_type, user_id, mission_id):
    """判定该通知是否已创建过，若是，则返回True，否则范围False
    """
    db = get_db()
    notification = db.execute(
        'SELECT *'
        ' FROM Notification'
        ' WHERE user_id = ? AND mission_id = ? AND type = ?',
        (user_id, mission_id, n_type,)
    ).fetchone()
    # None 表示还没创建过，非None表示已经创建过了
    has_created = False if notification is None else True
    return has_created

def create_notification_type_1(user_id, mission_id, time):
    """
    若最后一个人填完问卷，立即对发布人生成通知！（通知1）
    @params: 
        user_id, 待生成通知的user的id
        mission_id, 待生成通知所对应的mission的id
        time, 最后一个人填完的时间
    """
    n_type = 1
    db = get_db()

    # 判断是否为最后一个人填写了问卷
    info = db.execute(
        'SELECT u.username, m.create_time, m.title, m.fin_num, m.max_num'
        ' FROM User u JOIN MissionInfo m ON u.idUser = m.publisher_id'
        ' WHERE m.idMissionInfo = ? AND m.fin_num = m.max_num',
        (mission_id,)
    ).fetchone()
    if info is None:  # 不是最后一人填完问卷，不生成通知
        return

    # 生成新通知
    now_time = datetime.datetime.now()
    massage = "{}：您于 {} 发布的问卷 {} 已于 {} 全部填写完成。".format(
        info[0][0], info[0][1], info[0][2], time
    )

    # 插入数据库
    db.execute(
        'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
        ' VALUES (?, ?, ?, ?, ?)',
        (user_id, mission_id, message, now_time, n_type,)
    )
    db.commit()


def create_notification_type_2(user_id):
    """用户上线时！检查该用户是否有**已过期、且未填完**的问卷，
    若有，则对发布人生成通知（如何处理唯一性？）！（通知2）
    @params: 
        user_id, 待检查的user的id
    """
    n_type = 2
    now_time = datetime.datetime.now()
    db = get_db()

    info = db.execute(
        'SELECT m.idMissionInfo, u.username, m.create_time, m.deadline, m.title, m.fin_num'
        ' FROM User u JOIN MissionInfo m ON u.idUser = m.publisher_id'
        ' WHERE u.idUser = ? AND m.deadline  > ? AND m.type = 0 AND m.fin_num < m.max_num',
        (user_id, now_time,)
    ).fetchone()
    for i in range(len(info)):
        # 若这条通知已经创建过，则声明无需创建声明
        mission_id = info[i][0]
        if has_created(n_type, user_id, mission_id):
            continue

        # 生成通知
        message = "{}：您于 {} 发布的问卷 {} 已于 {} 过期，已有{}人填写了您的问卷。".format(
            info[i][1], info[i][2], info[i][4], info[i][3], info[i][5]
        )
        # 插入数据库
        db.execute(
            'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
            ' VALUES (?, ?, ?, ?, ?)',
            (user_id, mission_id, message, now_time, n_type,)
        )
        db.commit()


def create_notification_type_3(mission_id):
    """若有人接收任务，立即对发布人生成通知！（通知3）
    @params: 
        user_id, 接收任务的
        mission_id, 待生成通知所对应的mission的id
    """
    n_type = 3
    now_time = datetime.datetime.now()
    db = get_db()
    
    info = db.execute(
        'SELECT u.username, m.create_time, m.title, tu.username, o.receive_time, m.publisher_id'
        ' FROM (SELECT * FROM User) AS tu, User u, MissionInfo m, MissionOrder o'
        ' WHERE u.idUser = m.publisher_id AND tu.idUser = o.receiver_id AND m.idMissionInfo = o.mission_id'
        ' AND m.idMissionInfo = ?',
        (mission_id,)
    ).fetchone()

    # 生成通知
    message = "{发布人}：您于 {时间} 发布的任务 {任务号} 已被 {接收人} 于 {时间} 确认接收。".format(
        info[0][0], info[0][1], info[0][2], info[0][3], info[0][4]
    )
    # 插入数据库
    db.execute(
        'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
        ' VALUES (?, ?, ?, ?, ?)',
        (info[0][6], mission_id, message, now_time, n_type,)
    )
    db.commit()


def create_notification_type_4(mission_id):
    """若发布人确定任务完成，立即对接收人发送通知！（通知4）
    @params: 
        user_id, 待检查的user的id
        mission_id, 待生成通知所对应的mission的id
        time, 接收时间
    """
    n_type = 4
    now_time = datetime.datetime.now()
    db = get_db()

    info = db.execute(
        'SELECT u.username, m.title, tu.username, o.finish_time, o.receiver_id'
        ' FROM (SELECT * FROM User) AS tu, User u, MissionInfo m, MissionOrder o'
        ' WHERE u.idUser = m.publisher_id AND tu.idUser = o.receiver_id AND m.idMissionInfo = o.mission_id'
        ' AND m.idMissionInfo = ?',
        (mission_id,)
    ).fetchone()

    # 生成通知
    message = "{接收人}：您接收的任务 {任务号} 以被 {发布人} 于 {时间} 确认完成。".format(
        info[0][2], info[0][1], info[0][0], info[0][3]
    )
    # 插入数据库
    db.execute(
        'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
        ' VALUES (?, ?, ?, ?, ?)',
        (info[0][4], mission_id, message, now_time, n_type,)
    )
    db.commit()


def create_notification_type_5(user_id):
    """用户上线时！检查该用户是否有**已过期、且无人接收**的任务，
    若有，则对发布人生成通知！（通知5）
    @params: 
        user_id, 待检查的user的id
    """
    n_type = 5
    now_time = datetime.datetime.now()
    db = get_db()

    info = db.execute(
        'SELECT m.idMissionInfo, u.username, m.create_time, m.deadline, m.title'
        ' FROM User u JOIN MissionInfo m ON u.idUser = m.publisher_id'
        ' WHERE u.idUser = ? AND m.deadline  > ? AND m.type = 1 AND m.rcv_num = 0',
        (user_id, now_time,)
    ).fetchone()
    for i in range(len(info)):
        # 若这条通知已经创建过，则声明无需创建声明
        mission_id = info[i][0]
        if has_created(n_type, user_id, mission_id):
            continue
        # 生成通知
        message = "{}：您于 {} 发布的任务 {} 于 {} 过期，无人接收该任务，请重新发布任务。".format(
            info[i][1], info[i][2], info[i][4], info[i][3], 
        )
        # 插入数据库
        db.execute(
            'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
            ' VALUES (?, ?, ?, ?, ?)',
            (user_id, mission_id, message, now_time, n_type,)
        )
        db.commit()


def create_notification_type_6(user_id):
    """用户上线时！检查该用户是否有**发布的，已过期、且已被接受、未确定完成**的任务，
    若有，则对发布人生成通知！（通知6）
    @params: 
        user_id, 待检查的user的id
    """
    n_type = 6
    now_time = datetime.datetime.now()
    db = get_db()

    info = db.execute(
        'SELECT m.idMissionInfo, u.username, m.create_time, m.deadline, m.title'
        ' FROM User u, MissionInfo m, MissionOrder o'
        ' WHERE u.idUser = m.publisher_id AND m.idMissionInfo = o.mission_id'
        ' AND u.idUser = ? AND m.deadline  > ? AND m.type = 1 AND o.publisher_confirm = 0',
        (user_id, now_time,)
    ).fetchone()
    for i in range(len(info)):
        # 若这条通知已经创建过，则声明无需创建声明
        mission_id = info[i][0]
        if has_created(n_type, user_id, mission_id):
            continue
        # 生成通知
        message = "{发布人}：您于 {时间} 发布的任务 {任务号} 于 {时间} 过期，请按时确认完成任务。".format(
            info[i][1], info[i][2], info[i][4], info[i][3],
        )
        # 插入数据库
        db.execute(
            'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
            ' VALUES (?, ?, ?, ?, ?)',
            (user_id, mission_id, message, now_time, n_type,)
        )
        db.commit()


def create_notification_type_7(user_id):
    """用户上线时！检查该用户是否有**接受的，已过期、且未确定完成**的任务，
    若有，则对接收人生成通知！（通知7）
    @params: 
        user_id, 待检查的user的id
    """
    n_type = 7
    now_time = datetime.datetime.now()
    db = get_db()

    info = db.execute(
        'SELECT m.idMissionInfo, u.username, m.create_time, m.deadline, m.title'
        ' FROM (SELECT * FROM User) AS tu, User u, MissionInfo m, MissionOrder o'
        ' WHERE u.idUser = m.publisher_id AND tu.idUser = o.receiver_id AND m.idMissionInfo = o.mission_id'
        ' AND o.receiver_id = ? AND m.deadline  > ? AND m.type = 1 AND o.publisher_confirm = 0',
        (user_id, now_time,)
    ).fetchone()
    for i in range(len(info)):
        # 若这条通知已经创建过，则声明无需创建声明
        mission_id = info[i][0]
        if has_created(n_type, user_id, mission_id):
            continue
        # 生成通知
        message = "{接收人}：您接收的任务 {任务号} 于{时间} 过期，发布人 {发布人} 未确认任务完成，您将无法获得对应奖励，请提醒发布人按时确认完成任务。如需投诉，请联系客服。".format(
            info[i][1], info[i][2], info[i][4], info[i][3],
        )
        # 插入数据库
        db.execute(
            'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
            ' VALUES (?, ?, ?, ?, ?)',
            (user_id, mission_id, message, now_time, n_type,)
        )
        db.commit()

def create_notification_type_8(mission_id, receiver_id, cancel_time):
    """若接受人放弃任务，立即对发布人生成通知！（通知8）
    @params: 
        mission_id, 待生成通知所对应的mission的id
        receiver_id, 取消接收任务的user的id
        cancel_time, 取消接收时间
    """
    n_type = 8
    now_time = datetime.datetime.now()
    db = get_db()

    info = db.execute(
        'SELECT u.username, m.create_time, m.title, u.idUser'
        ' FROM User u, MissionInfo m'
        ' WHERE u.idUser = m.publisher_id'
        ' AND m.idMissionInfo = ?',
        (mission_id,)
    ).fetchone()

    # 生成通知
    message = "{发布人}：您于 {时间} 发布的任务 {任务号} 于 {时间} 被接收人 {接收人} 取消接收任务。 ".format(
        info[0][0], info[0][1], info[0][2], cancel_time, receiver_id
    )
    # 插入数据库
    db.execute(
        'INSERT INTO Notification (user_id, mission_id, message, create_time, notification_type)'
        ' VALUES (?, ?, ?, ?, ?)',
        (info[0][3], mission_id, message, now_time, n_type,)
    )
    db.commit()

# def get_a_notification(idNotification):
#     """返回对应通知id的通知item
#     """
#     notification = get_db().execute(
#         'SELECT idNotification, mission_id, message, create_time, has_read'
#         ' FROM Notification'
#         ' WHERE idNotification = ?',
#         (idNotification,)
#     ).fetchone()
    
#     if notification is None:
#         abort(404, "Notification id {0} doesn't exist.".format(idNotification))

#     return notification


