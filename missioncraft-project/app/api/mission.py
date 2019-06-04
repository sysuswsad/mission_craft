from flask import (
    Blueprint, g, request
)
from werkzeug.exceptions import abort
import datetime

from app.api.user import auth
from app.db import get_db
from app.api import bp
from app.response_code import bad_request, unauthorized, ok, created


@bp.route('/mission/')
@auth.login_required
def create_mission():
	data = request.get_json()
	if not data:
		return bad_request('ERROR DATA AT CREATE MISSION')

	mission_type = data.get('type')
	deadline = data.get('deadline')
	title = data.get('title')
	description = data.get('description')
	bounty = data.get('bounty')
	max_num = data.get('max_num')
	problems = data.get('problems')

	db = get_db()

	if (not mission_type) or (not deadline) or (not title) or (not description) or (not bounty):
		return bad_request('Missing some necessary parameter')
	elif not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', deadline):
		return bad_request('Deadline format error')
	elif datetime.datetime.now() < datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S'):
		return bad_request('Deadline should be in future')

	# 处理问卷任务, detail到底还要不要
	if mission_type == 0:
		db.execute(
			'INSERT INTO MissionInfo (publisher_id, type, deadline, title, description, bounty, max_num)'
			' VALUES (?, ?, ?, ?, ?, ?, ?)',
			(g.user['idUser'], mission_type, deadline, title, description, bounty, max_num)
		)
		return created('Create mission successfully')
