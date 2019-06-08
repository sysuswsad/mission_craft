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
		'SELECT publisher_id, type FROM MissionInfo WHERE idMissionInfo = ?', (order_info['mission_id'],)
	).fetchone()

	# 确认过的订单不能再确认，防止再次生成答案表
	if order_info['order_state'] == 1:
		return bad_request('The order has been confirmed')

	# 分成两类，问卷由接收人确认即可，其他任务由发布人确认
	if mission_info['type'] == 0:
		if order_info['receiver_id'] != g.user['idUser']:
			return unauthorized('You can not submit for other receivers')
		answers = json.loads(data.get('answers'))
		problem_ids = db.execute(
			'SELECT idProblem FROM Problem WHERE mission_id = ?', (order_info['mission_id'])
		).fetchall()
		try:
			for i in range(0, len(answers)):
				db.execute('INSERT INTO ANSWER (order_id, problem_id, result)', 
					(order_id, problem_ids[i]['idProblem'], answers[i])
				)
			db.commit()
		except Exception:
			return bad_request('Parse answers error')
	elif mission_info['type'] == 1:
		if mission_info['publisher_id'] != g.user['idUser']:
			return unauthorized('You can not submit for other publishers')
		# 注意进行修改通知表？？？？？？？？？？后续完成
	# 为接单人发钱

	# 更新其它表
	db.execute(
		'UPDATE MissionOrder SET publisher_confirm = ?, receiver_confirm = ?, order_state = ?, finish_time = ? WHERE idMissionOrder = ?', 
		(1, 1, 1, datetime.datetime.now(), order_id,)
	)
	db.execute(
		'UPDATE User SET mission_fin_num = mission_fin_num + 1 WHERE idUser = ?', 
		(order_info['receiver_id'])
	)
	db.execute(
		'UPDATE MissionInfo SET fin_num = fin_num + 1 WHERE idMissionInfo = ?', 
		(order_id['mission_id'],)
	)
	db.commit()
	db.execute(
		'UPDATE MissionInfo SET state = fin_num/max_num WHERE idMissionInfo = ? and state < 1', 
		(order_id['mission_id'],)
	)
	db.commit()
	
	return ok('Confirm order successfully')
