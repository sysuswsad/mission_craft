import os
import json
import pytest
from werkzeug.security import check_password_hash

from app.db import get_db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


def get_basic_auth_headers():
    '''创建Basic Auth认证的headers'''
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def get_token_auth_headers(client, app, username_or_email, password):
    '''创建JSON Web Token认证的headers'''
    headers = get_basic_auth_headers()
    response = client.post('/api/token/', headers=headers, data=json.dumps({'username_or_email':username_or_email, 'password':password}))
    assert response.status_code == 201
    response = json.loads(response.get_data(as_text=True))
    token = response.get('token')
    assert token is not None
    return {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


# 有个地方非常坑，request.get_json(force=True)中force=True必须设置，否则就一直出错，建议后续写一个函数来添加header，防止出现类似错误
# 下面这个测过了，不用测了
# @pytest.mark.parametrize(('email', 'status_code', 'message'), (
#     ('', 400, 'Email is required'),
#     ('1473595322', 400, 'Email format error'),
#     ('123@qq.com', 400, 'Email 123@qq.com is already registered.'),
#     ('ou@mail2.sysu.edu.cn', 201, 'Generate and send token successfully'),
# ))
# def test_code(client, app, email, status_code, message):
#     response = client.post('/api/code/', headers=get_basic_auth_headers(), data=json.dumps({'email':email}))
#     assert response.status_code == status_code
#     response = json.loads(response.get_data(as_text=True))
#     assert response.get('message') == message


# 下面这个测过了，不用测了
@pytest.mark.parametrize(('username', 'password', 'email', 'sid', 'code', 'status_code', 'message'), (
    ('', '', '', '', '', 400, 'Username is required'),
    ('test1', '', '', '', '', 400, 'Password is required'),
    ('test1', '123456', '', '', '', 400, 'Email is required'),
    ('test1', '123456', '123@qq.com', '', '', 400, 'Sid is required'),
    ('test1', '123456', '123@qq.com', '16340001', '', 400, 'Verification code is required'),
    ('test1', '123456', '123@qq.com', '16340001', '111111', 400, 'User test1 is already registered.'),
    ('test2', '123456', '123@qq.com', '16340001', '111111', 400, 'Email 123@qq.com is already registered.'),
    ('test2', '123456', '1234@qq.com', '16340001', '111111', 400, 'Sid 16340001 is already registered.'),
    ('test2', '123456', '1234@qq.com', '16340002', '111111', 400, 'Verification code is not correct'),
    ('test2', '123456', '12345@qq.com', '16340002', '123456', 400, 'Verification code is out of time')
))
def test_register_validate_input(client, app, username, password, email, sid, code, status_code, message):
    response = client.post('/api/user/', headers=get_basic_auth_headers(), data=json.dumps({
        'username':username,'password':password,'email':email,'sid':sid,'code':code}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


# 下面这个测过了，不用测了
@pytest.mark.parametrize(('username', 'password', 'email', 'sid', 'code', 'status_code', 'message'), (
    ('test2', '123456', '1234@qq.com', '16340002', '123456', 201, 'Register successfully'),
))
def test_register(client, app, username, password, email, sid, code, status_code, message):
    response = client.post('/api/user/', headers=get_basic_auth_headers(), data=json.dumps({
        'username':username,'password':password,'email':email,'sid':sid,'code':code}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    with app.app_context():
        person = get_db().execute('SELECT * FROM User  WHERE username = ?', (username,)).fetchone()
        assert person is not None
        assert person['username'] == username
        assert person['email'] == email
        assert person['sid'] == sid
        assert check_password_hash(person['password'], password)
        

@pytest.mark.parametrize(('username_or_email', 'password', 'status_code', 'message'), (
    ('', '', 400, 'Username or email is required'),
    ('test', '', 400, 'Password is required'),
    ('test', '123', 400, 'Incorrect username or email'),
    ('12@qq.com', '123', 400, 'Incorrect username or email'),
    ('test1', '123', 400, 'Incorrect password'),
    ('123@qq.com', '123', 400, 'Incorrect password'),
))
def test_login_validate_input(client, app, username_or_email, password, status_code, message):
    response = client.post('/api/token/', headers=get_basic_auth_headers(), data=json.dumps({
        'username_or_email':username_or_email,'password':password}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


#下面这个测过了，不用测了
@pytest.mark.parametrize(('username_or_email', 'password', 'status_code', 'message'), (
    ('test1', '123456', 201, 'Login successfully'),
    ('123@qq.com', '123456', 201, 'Login successfully')
))
def test_login(client, app, username_or_email, password, status_code, message):
    response = client.post('/api/token/', headers=get_basic_auth_headers(), data=json.dumps({
        'username_or_email':username_or_email,'password':password}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    with app.app_context():
        person = get_db().execute('SELECT * FROM User  WHERE username = ?', (username_or_email,)).fetchone()
        if person is None:
            person = get_db().execute('SELECT * FROM User  WHERE email = ?', (username_or_email,)).fetchone()
        assert person is not None
        s = Serializer(app.config['SECRET_KEY'])
        token = s.loads(response_data.get('token'))
        assert token is not None
        assert token['idUser'] == person['idUser']
        assert token['email'] == person['email']


@pytest.mark.parametrize(('status_code', 'message'), (
    (401, 'Unauthorized Access'),
))
def test_get_info_without_login(client, app, status_code, message):
    response = client.get('/api/user/', headers=get_basic_auth_headers())
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


@pytest.mark.parametrize(('username_or_email', 'password', 'status_code', 'message'), (
    ('test1', '123456', 200, 'Get user info successfully'),
    ('123@qq.com', '123456', 200, 'Get user info successfully')
))
def test_get_info(client, app, username_or_email, password, status_code, message):
    response = client.get('/api/user/', headers=get_token_auth_headers(client, app, username_or_email, password))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    person_info = response_data.get('data')
    with app.app_context():
        person = get_db().execute('SELECT * FROM User  WHERE idUser = ?', (person_info['idUser'],)).fetchone()
        assert person is not None
        for key in person_info:
            assert person[key] == person_info[key]


@pytest.mark.parametrize(('origin_username', 'password', 'username', 'realname', 'id_card_num', 'university', 'school', 'grade', 'gender', 'phone', 'qq', 'wechat', 'status_code', 'message'), (
    ('test1', '123456', '', 'oooooo', '123234435', 'Sysu', '', '', '', '', '', '', 400, 'Username is required'),
    ('test1', '123456', 'test10', 'oooooo', '123234435', 'Sysu', '', '', '', '', '', '', 400, 'User test10 is already registered.')
))
def test_update_info_validate_input(client, app, origin_username, password, username, realname, id_card_num, university, school, grade, gender, phone, qq, wechat, status_code, message):
    response = client.put('/api/user/', headers=get_token_auth_headers(client, app, origin_username, password), data=json.dumps({
        'username':username,'realname':realname,'id_card_num':id_card_num,'university':university,
        'school':school,'grade':grade,'gender':gender,'phone':phone,'qq':qq,'wechat':wechat}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


@pytest.mark.parametrize(('status_code', 'message'), (
    (401, 'Unauthorized Access'),
))
def test_update_info_without_login(client, app, status_code, message):
    response = client.put('/api/user/', headers=get_basic_auth_headers(), data=json.dumps({}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


@pytest.mark.parametrize(('origin_username', 'password', 'username', 'realname', 'id_card_num', 'university', 'school', 'grade', 'gender', 'phone', 'qq', 'wechat', 'status_code', 'message'), (
    ('test1', '123456', 'test1', 'ooooox', '1232344', 'Berkeley', '', '', '', '', '', '', 200, 'Update user info successfully'),
    ('test1', '123456', 'test50', 'ooooos', '123234435f4365', 'Berkeley', 'software', '3', 'male', '1239087', 'dasu', 'dakl', 200, 'Update user info successfully')
))
def test_update_info(client, app, origin_username, password, username, realname, id_card_num, university, school, grade, gender, phone, qq, wechat, status_code, message):
    response = client.put('/api/user/', headers=get_token_auth_headers(client, app, origin_username, password), data=json.dumps({
        'username':username,'realname':realname,'id_card_num':id_card_num,'university':university,
        'school':school,'grade':grade,'gender':gender,'phone':phone,'qq':qq,'wechat':wechat}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    with app.app_context():
        person = get_db().execute('SELECT * FROM User  WHERE username = ?', (username,)).fetchone()
        assert person is not None
        assert person['realname'] == realname
        assert person['id_card_num'] == id_card_num
        assert person['university'] == university
        assert person['school'] == school
        assert person['grade'] == grade
        assert person['gender'] == gender
        assert person['phone'] == phone
        assert person['qq'] == qq
        assert person['wechat'] == wechat


@pytest.mark.parametrize(('username', 'password', 'old_password', 'new_password', 'status_code', 'message'), (
    ('test1', '123456', None, None, 400, 'Old password is required'),
    ('test1', '123456', '12345', None, 400, 'New password is required'),
    ('test1', '123456', '12345', '12345678', 400, 'Old password wrong'),
))
def test_change_password_validate_input(client, app, username, password, old_password, new_password, status_code, message):
    response = client.post('/api/password/', headers=get_token_auth_headers(client, app, username, password), data=json.dumps({
        'old_password':old_password,'new_password':new_password}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


@pytest.mark.parametrize(('status_code', 'message'), (
    (401, 'Unauthorized Access'),
))
def test_change_password_without_login(client, app, status_code, message):
    response = client.post('/api/password/', headers=get_basic_auth_headers(), data=json.dumps({}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message


@pytest.mark.parametrize(('username', 'old_password', 'new_password', 'status_code', 'message'), (
    ('test1', '123456', '12345678', 200, 'Change password successfully'),
))
def test_change_password(client, app, username, old_password, new_password, status_code, message):
    response = client.post('/api/password/', headers=get_token_auth_headers(client, app, username, old_password), data=json.dumps({
        'old_password':old_password,'new_password':new_password}))
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    with app.app_context():
        password = get_db().execute('SELECT password FROM User  WHERE username = ?', (username,)).fetchone()
        assert password is not None
        assert check_password_hash(password['password'], new_password)
