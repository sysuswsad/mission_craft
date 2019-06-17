import os
import json
import pytest
import datetime
from werkzeug.security import check_password_hash

from app.db import get_db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from tests.test_user import get_token_auth_headers


@pytest.mark.parametrize(('type', 'deadline', 'title', 'description', 'qq', 'wechat', 'phone', 'other_way', 'bounty', 'max_num', 'problems', 'status_code', 'message'), (
    (None, '', '', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    # (0, '', '', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', '', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', 'title1', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', 'title1', 'description1', '', '', '', '', None, '', '', 400, 'Missing some necessary parameter'),
    (1, '2019-01-01 01:01:01', 'title1', 'description1', '', '', '', '', 10, '', '', 400, 'Missing contact info'),
    (0, '2019-01-01 01:01:0', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '', '', 400, 'Deadline format error'),
    (0, '2019-01-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '', '', 400, 'Deadline should be in future'),
    (0, '2019-10-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '10', '', 400, 'Questionare should have problems'),
    (0, '2019-10-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '10', json.dumps({'test':'error'}), 400, 'Parse problems error'),
    (0, '2019-10-01 01:01:01', 'title1', 'description1', '', '', '', '', 10, '10', 
        json.dumps([
                { 'type': 0, 'question': 'are you pj', 'choices': ['yes', 'no'] },
                { 'type': 1, 'question': 'what do you like', 'choices': ['money', 'happiness'] },
                { 'type': 2, 'question': 'how do you feel' }]), 
        201, 'Create mission successfully'),
))
def test_create_mission(client, app, type, deadline, title, description, qq, wechat, phone, other_way, bounty, max_num, problems, status_code, message):
    response = client.post('/api/mission/', headers=get_token_auth_headers(client, app, 'test1', '123456'), data=json.dumps({
        'type':type, 'deadline':deadline, 'title':title, 'description':description, 'qq':qq, 'wechat':wechat, 'phone':phone, 
        'other_way':other_way, 'bounty':bounty, 'max_num':max_num, 'problems':problems
        }))
    # assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if response.status_code == 201:
        mission_info = response_data.get('data')
        with app.app_context():
            mission = get_db().execute('SELECT * FROM MissionInfo WHERE idMissionInfo = ?', (mission_info['mission_id'],)).fetchone()
            assert mission['type'] == int(type)
            assert mission['deadline'] == deadline
            assert mission['title'] == title
            assert mission['description'] == description
            assert mission['qq'] == qq
            assert mission['wechat'] == wechat
            assert mission['phone'] == phone
            assert mission['other_way'] == other_way
            assert mission['bounty'] == int(bounty)
            assert mission['max_num'] == int(max_num)
            _problems = get_db().execute('SELECT * FROM Problem WHERE mission_id = ?', (mission_info['mission_id'],)).fetchall()
            problems = json.loads(problems)
            for i in range(0, len(problems)):
                assert problems[i]['type'] == _problems[i]['type']
                assert problems[i]['question'] == _problems[i]['problem_stem']
                assert problems[i].get('choices', '') == json.loads(_problems[i]['problem_detail'])


@pytest.mark.parametrize(('limit', 'type', 'bounty', 'create_time', 'personal', 'mission_id', 'status_code', 'message', 'res_num'), (
    (None, None, None, None, None, None, 400, 'Personal or mission_id are required', 0),
    (None, None, None, None, None, 'sd', 400, 'Parse mission id error', 0),
    (None, None, None, None, None, 100, 400, 'No such mission', 0),
    (None, 1, None, None, None, 10, 400, 'No search result for the param', 0),
    # get by mission id
    (None, 0, None, None, None, 10, 200, 'Get missions successfully', 0),
    (None, None, None, None, 'test', None, 400, 'Parse create_time, bounty or personal error', 0),
    (None, None, None, '2020:10:11 00:00:00', 0, None, 400, 'Parse create_time, bounty or personal error', 0),
    (None, None, 'None', '2020-10-11 00:00:00', 0, None, 400, 'Parse create_time, bounty or personal error', 0),
    # get through square
    (4, 0, 9, None, 0, None, 200, 'Get missions successfully', 3),
    (3, 1, -1, None, 0, None, 200, 'Get missions successfully', 3),
    # get by user id
    (4, 0, 1, '2019-06-07 11:20:12', 1, None, 200, 'Get missions successfully', 1),
))
def test_get_mission(client, app, limit, type, bounty, create_time, personal, mission_id, status_code, message, res_num):
    response = client.get('/api/mission/', headers=get_token_auth_headers(client, app, 'test1', '123456'), data=json.dumps({
        'limit':limit, 'type':type, 'bounty':bounty, 'create_time':create_time, 'personal':personal, 'mission_id':mission_id}))
    # assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if response.status_code == 200 and (mission_id or mission_id == 0):
        mission_info = response_data.get('data').get('missions')[0]
        assert mission_info['publisher_id'] == 1
        assert not mission_info.get('phone')
        assert not mission_info.get('qq')
        assert not mission_info.get('wechat')
        assert not mission_info.get('other_way')
        assert mission_info['avatar'] == ''
        assert mission_info['username'] == 'test1'
        assert mission_info['type'] == 0
        assert mission_info['create_time'] == ('2019-06-08 11:20:12')
        assert mission_info['deadline'] == ('2019-07-08 11:20:12')
        assert mission_info['title'] == 'test mission title'
        assert mission_info['description'] == 'test mission description'
        assert mission_info['bounty'] == 10
        assert mission_info['max_num'] == 10
        assert mission_info['rcv_num'] == 2
        assert mission_info['fin_num'] == 1
        assert mission_info['state'] == 0
    elif response.status_code == 200 and personal == 0:
        mission_info = response_data.get('data').get('missions')
        assert len(mission_info) == res_num
        for item in mission_info:
            assert item['bounty'] > bounty
            # if item['type'] == 1:
                # assert not item['receiver_id']
                # assert not item['receiver_time']
    elif response.status_code == 200 and personal == 1:
        mission_info = response_data.get('data').get('missions')
        assert len(mission_info) == res_num
        for item in mission_info:
            assert item['create_time'] > create_time


@pytest.mark.parametrize(('personal', 'mission_id', 'return_problems', 'return_statistics', 'message'), (
    (0, None, 0, 0, 'Get missions successfully'),
    (0, None, 1, 0, 'Get missions successfully'),
    (0, None, 1, 1, 'Get missions successfully'),
))
def test_get_mission_with_problems(client, app, personal, mission_id, return_problems, return_statistics, message):
    response = client.get('/api/mission/', headers=get_token_auth_headers(client, app, 'test10', '123456'), data=json.dumps({
        'bounty':16, 'personal':personal, 'mission_id':mission_id, 'return_problems':return_problems, 'return_statistics':return_statistics}))
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    missions = response_data.get('data').get('missions')
    assert len(missions) == 1
    problems = missions[0].get('problems')
    if not return_problems:
        assert not problems
    elif return_problems:
        assert problems[0]['choices'] == ['yes', 'no', 'pardon']
        assert problems[1]['choices'] == ['apple', 'banana', 'watermelon']
        assert not problems[2]['choices']
        if return_statistics:
            assert problems[0]['answer'] == [1, 1, 1]
            assert problems[1]['answer'] == [2, 1, 3]
            assert problems[2]['answer'] == ['ousuixin', 'pj', 'pjh']


@pytest.mark.parametrize(('username', 'password','mission_id', 'rcv_num','mission_state', 'order_state', 'response_code', 'message'), (
    ('test1', '123456', 14, 1, 1, 2, 200, 'cancel successfully'),
    ('pj', '123456', 15, 49, 0, 2, 200, 'cancel successfully'),
    ('pj', '123456', 16, 99, 0, 2, 200, 'cancel successfully'),
    ('test1', '123456', 17, 0, 1, 0, 200, 'cancel successfully'),
    ('test1', '123456', 18, 1, 1, 0, 400, 'Should not cancel a mission already received'),
    ('pj', '123456', 19, 0, 0, 2, 200, 'cancel successfully'),
    ('pj2', '123456', 16, 100, 1, 0, 403, 'The operation is forbidden'),
    ('pj2', '123456', 19, 1, 1, 0, 403, 'The operation is forbidden'),

))
def test_cancel_mission(client, app, username, password, mission_id, rcv_num, mission_state, order_state, response_code, message):
    response = client.put('api/mission/',headers=get_token_auth_headers(client, app, username, password),data=json.dumps({'mission_id':mission_id}))
    assert response
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message

    with app.app_context():
        db = get_db()
        mission_info = db.execute(
            'SELECT * FROM MissionInfo WHERE idMissionInfo = ?', (mission_id,)
        ).fetchone()
        assert mission_info['state'] == mission_state
        assert mission_info['rcv_num'] == rcv_num
        # 领取者额外查看
        if username == 'pj':
            order_info = db.execute(
                'SELECT * FROM MissionOrder WHERE mission_id = ?', (mission_id,)
            ).fetchone()
            assert order_info['order_state'] == order_state