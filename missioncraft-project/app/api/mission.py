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
	bounty = data.get('bounty')
	max_num = data.get('max_num')
	problems = json.loads(data.get('problems'))

	if (not mission_type) or (not deadline) or (not title) or (not description) or (not bounty):
		return bad_request('Missing some necessary parameter')
	elif not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', deadline):
		return bad_request('Deadline format error')
	elif datetime.datetime.now() > datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S'):
		return bad_request('Deadline should be in future')

	mission_type = int(mission_type)
	bounty = float(bounty)
	max_num = int(max_num)
	deadline = datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')

	db = get_db()
	# 处理问卷任务
	if mission_type == 0:
		db.execute(
			'INSERT INTO MissionInfo (publisher_id, type, deadline, title, description, bounty, max_num)'
			' VALUES (?, ?, ?, ?, ?, ?, ?)',
			(g.user['idUser'], mission_type, deadline, title, description, bounty, max_num)
		)
		mission_id = db.execute('SELECT last_insert_rowid() FROM MissionInfo')
		try:
			for problem in problems:
				db.execute('INSERT INTO Problem (mission_id, type, problem_stem, problem_detail)'
					'VALUES (?, ?, ?, ?)', (mission_id, int(problem['type']), problem['question'], json.dumps(problem['choices']))
				)
		except Exception:
			return bad_request('Parse problems error')
		db.commit()
		return created('Create mission successfully', mission_id=mission_id)


@bp.route('/mission/', methods=['get'])
@auth.login_required
def get_mission():
	data = request.get_json()
	if not data:
		return bad_request('ERROR DATA AT GET MISSION')

	create_time = data.get('create_time')
	limit = data.get('limit')
	mission_type = data.get('type')
	bounty = data.get('bounty')
	mission_id = data.get('mission_id')

	if create_time and re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', create_time):
		
	elif 
		
	create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')

	db = get_db()
	# 首先根据参数判断查询类型，然后根据mission_type判断任务类型：

