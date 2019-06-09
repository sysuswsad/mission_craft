import os
import json
import pytest
from werkzeug.security import check_password_hash

from app.db import get_db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


def get_basic_auth_headers(content_type='application/json'):
    '''创建Basic Auth认证的headers'''
    return {
        'Accept': 'application/json',
        'Content-Type': content_type
    }


def get_token_auth_headers(client, app, username_or_email, password, content_type = 'application/json'):
    '''创建JSON Web Token认证的headers'''
    headers = get_basic_auth_headers()
    response = client.post('/api/token/', headers=headers, data=json.dumps({'username_or_email':username_or_email, 'password':password}))
    assert response.status_code == 201
    response = json.loads(response.get_data(as_text=True))
    token = response.get('data')['token']
    assert token is not None
    return {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': content_type
    }


@pytest.mark.parametrize(('type', 'deadline', 'title', 'description', 'qq', 'wechat', 'phone', 'other_way', 'bounty', 'max_num', 'questions', 'status_code', 'message'), (
    (None, '', '', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '', '', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', '', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', 'title1', '', '', '', '', '', '', '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', 'title1', 'description1', '', '', '', '', None, '', '', 400, 'Missing some necessary parameter'),
    (0, '2019-01-01 01:01:01', 'title1', 'description1', '', '', '', '', 10, '', '', 400, 'Missing contact info'),
    (0, '2019-01-01 01:01:0', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '', '', 400, 'Deadline format error'),
    (0, '2019-01-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '', '', 400, 'Deadline should be in future'),
    (0, '2019-10-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '10', '', 400, 'Questionare should have problems'),
    (0, '2019-10-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '10', json.dumps({'test':'error'}), 400, 'Parse problems error'),
    (0, '2019-10-01 01:01:01', 'title1', 'description1', '1473595322@qq.com', '', '', '', 10, '10', 
        json.dumps([
                { 'type': 0, 'question': 'are you pj', 'choices': ['yes', 'no'] },
                { 'type': 1, 'question': 'what do you like', 'choices': ['money', 'happiness'] },
                { 'type': 2, 'question': 'how do you feel' }]), 
        201, 'Create mission successfully'),
))
def test_create_mission(client, app, type, deadline, title, description, qq, wechat, phone, other_way, bounty, max_num, questions, status_code, message):
    response = client.post('/api/mission/', headers=get_token_auth_headers(client, app, 'test1', '123456'), data=json.dumps({
        'type':type, 'deadline':deadline, 'title':title, 'description':description, 'qq':qq, 'wechat':wechat, 'phone':phone, 
        'other_way':other_way, 'bounty':bounty, 'max_num':max_num, 'questions':questions
        }))
    # assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if response.status_code == 201:
        mission_info = response_data.get('data')
        assert mission_info['mission_id'] == 10

