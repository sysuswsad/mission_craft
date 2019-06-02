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
    headers = get_basic_auth_headers(username_or_email, password)
    response = client.post('/token/', headers=headers, data=json.dumps({'username_or_email':username_or_email, 'password':password}))
    assert response.status_code == 201
    response = json.loads(response.get_data(as_text=True))
    assert (response.get('token') is not None)
    token = response['token']
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
#     ('ousx@mail2.sysu.edu.cn', 201, 'Generate and send token successfully'),
# ))
# def test_code(client, app, email, status_code, message):
#     response = client.post('/code/', headers=get_basic_auth_headers(), data=json.dumps({'email':email}))
#     assert response.status_code == status_code
#     response = json.loads(response.get_data(as_text=True))
#     assert response.get('message') == message


# 下面这个测过了，不用测了
# @pytest.mark.parametrize(('username', 'password', 'email', 'sid', 'code', 'status_code', 'message'), (
#     ('', '', '', '', '', 400, 'Username is required'),
#     ('test1', '', '', '', '', 400, 'Password is required'),
#     ('test1', '123456', '', '', '', 400, 'Email is required'),
#     ('test1', '123456', '123@qq.com', '', '', 400, 'Sid is required'),
#     ('test1', '123456', '123@qq.com', '16340001', '', 400, 'Verification code is required'),
#     ('test1', '123456', '123@qq.com', '16340001', '111111', 400, 'User test1 is already registered.'),
#     ('test2', '123456', '123@qq.com', '16340001', '111111', 400, 'Email 123@qq.com is already registered.'),
#     ('test2', '123456', '1234@qq.com', '16340001', '111111', 400, 'Sid 16340001 is already registered.'),
#     ('test2', '123456', '1234@qq.com', '16340002', '111111', 400, 'Verification code is not correct')

# ))
# def test_register_validate_input(client, app, username, password, email, sid, code, status_code, message):
#     response = client.post('/user/', headers=get_basic_auth_headers(), data=json.dumps({
#         'username':username,'password':password,'email':email,'sid':sid,'code':code}))
#     assert response.status_code == status_code
#     response_data = json.loads(response.get_data(as_text=True))
#     assert response_data.get('message') == message


# 下面这个测过了，不用测了
# @pytest.mark.parametrize(('username', 'password', 'email', 'sid', 'code', 'status_code', 'message'), (
#     ('test2', '123456', '1234@qq.com', '16340002', '123456', 201, 'Register successfully'),
# ))
# def test_register(client, app, username, password, email, sid, code, status_code, message):
#     response = client.post('/user/', headers=get_basic_auth_headers(), data=json.dumps({
#         'username':username,'password':password,'email':email,'sid':sid,'code':code}))
#     assert response.status_code == status_code
#     response_data = json.loads(response.get_data(as_text=True))
#     assert response_data.get('message') == message
#     with app.app_context():
#         person = get_db().execute('SELECT * FROM User  WHERE username = ?', (username,)).fetchone()
#         assert person is not None
#         assert person['username'] == username
#         assert person['email'] == email
#         assert person['sid'] == sid
#         assert check_password_hash(person['password'], password)
        

# @pytest.mark.parametrize(('username_or_email', 'password', 'status_code', 'message'), (
#     ('', '', 400, 'Username or email is required'),
#     ('test', '', 400, 'Password is required'),
#     ('test', '123', 400, 'Incorrect username or email'),
#     ('12@qq.com', '123', 400, 'Incorrect username or email'),
#     ('test1', '123', 400, 'Incorrect password'),
#     ('123@qq.com', '123', 400, 'Incorrect password'),
# ))
# def test_login_validate_input(client, app, username_or_email, password, status_code, message):
#     response = client.post('/token/', headers=get_basic_auth_headers(), data=json.dumps({
#         'username_or_email':username_or_email,'password':password}))
#     assert response.status_code == status_code
#     response_data = json.loads(response.get_data(as_text=True))
#     assert response_data.get('message') == message


#下面这个测过了，不用测了
# 注意token解析出来后的id字段不是叫'idUser'！！这一点和数据库不同
# @pytest.mark.parametrize(('username_or_email', 'password', 'status_code', 'message'), (
#     ('test1', '123456', 201, 'Login successfully'),
#     ('123@qq.com', '123456', 201, 'Login successfully')
# ))
# def test_login(client, app, username_or_email, password, status_code, message):
#     response = client.post('/token/', headers=get_basic_auth_headers(), data=json.dumps({
#         'username_or_email':username_or_email,'password':password}))
#     assert response.status_code == status_code
#     response_data = json.loads(response.get_data(as_text=True))
#     assert response_data.get('message') == message
#     with app.app_context():
#         person = get_db().execute('SELECT * FROM User  WHERE username = ?', (username_or_email,)).fetchone()
#         if person is None:
#             person = get_db().execute('SELECT * FROM User  WHERE email = ?', (username_or_email,)).fetchone()
#         s = Serializer(app.config['SECRET_KEY'])
#         token = s.loads(response_data.get('token'))
#         assert token['id'] == person['idUser']
#         assert token['email'] == person['email']


