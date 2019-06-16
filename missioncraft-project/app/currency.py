from flask import g
from app.db import get_db
import json


# 根据发布人给出的订单总赏金扣钱(这里如果是问卷，bounty应该是所有问卷赏金之和)
def pay_for_create(bounty):
	db = get_db()
	db.execute('UPDATE User SET balance = ? WHERE idUser = ?', (balance - bounty, g.user['idUser']))
	db.commit()


# 根据发布人给出的单笔订单给接单人发钱，传入的bounty是单笔赏金，idUser是接单人id
def get_by_confirm(bounty, idUser):
	db = get_db()
	db.execute('UPDATE User SET balance = ? WHERE idUser = ?', (balance + bounty, idUser))
	db.commit()


# 发布人取消订单，赏金退回，这里bounty是单笔订单赏金，refund_num是退款单数
def refund_by_cancel(bounty, refund_num):
	db = get_db()
	db.execute('UPDATE User SET balance = ? WHERE idUser = ?', (balance + bounty*refund_num, g.user['idUser']))
	db.commit()


# 处理过期任务，返回剩下金额给发布者
def refund_overdue():
	db = get_db()
	missions_overdue = db.execute('SELECT * FROM MissionInfo WHERE state == 0 AND deadline < datetime(CURRENT_TIMESTAMP,"localtime")')
	for row in missions_overdue:
		db.execute('UPDATE User SET balance = balance + ? WHERE idUser = ?', 
			(row['bounty']/row['max_num']*(row['max_num']-row['rcv_num']), row['publisher_id'])
		)
	db.commit()
