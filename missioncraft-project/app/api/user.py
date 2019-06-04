import functools
import random
import os
import re
import datetime

from flask import (
    Blueprint, g, request, session, current_app, send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.db import get_db
from app.response_code import bad_request, unauthorized, ok, created
from app.email import send_verification_code
from app.verification import  verify_istrue
from app.api import bp
# from app import redis_db

from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth()


# 下面这句@的作用就是：将url'/register'绑定到register视图函数，同时设置app.view_func['auth.register']=register
# 也就是说url'/register'、register视图函数、endpoint'auth.register'被绑定在一起，通过任意一个可以找到其他两个
# 通过url_for(endpoint)可以得到url'/register'，通过浏览器的url可以得到register视图函数
@bp.route('/user/', methods=['POST'])
def register():
    # 这里返回code 400 表示bad request，请求失败
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT REGISTERING')

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    sid = data.get('sid')
    code = data.get('code')

    db = get_db()

    if not username:
        return bad_request('Username is required')
    elif not password:
        return bad_request('Password is required')
    elif not email:
        return bad_request('Email is required')
    elif not sid:
        return bad_request('Sid is required')
    elif not code:
        return bad_request('Verification code is required')
    elif db.execute(
        'SELECT idUser FROM User WHERE username = ?', (username,)
    ).fetchone() is not None:
        return bad_request('User {} is already registered.'.format(username))
    elif db.execute(
        'SELECT idUser FROM User WHERE email = ?', (email,)
    ).fetchone() is not None:
        return bad_request('Email {} is already registered.'.format(email))
    elif db.execute(
        'SELECT idUser FROM User WHERE sid = ?', (sid,)
    ).fetchone() is not None:
        return bad_request('Sid {} is already registered.'.format(sid))
    # 检查验证码，使用redis时是这样的
    # elif redis_db.get('Email:'+email).decode('utf-8') != str(code):
    #     return bad_request('Verification code is not correct')
    # 检查验证码，使用sqlite数据库是这样的
    else:
        code_info = db.execute(
            'SELECT code, send_time FROM Verification WHERE email = ?', (email,)
        ).fetchone()
        if code_info['code'] != str(code):
            return bad_request('Verification code is not correct')
        elif abs(code_info['send_time'] - datetime.datetime.now()).seconds > 1800:
            return bad_request('Verification code is out of time')

    db.execute(
        'INSERT INTO User (username, password, email, sid) VALUES (?, ?, ?, ?)',
        (username, generate_password_hash(password), email, sid)
    )
    db.commit()

    return created('Register successfully')


@bp.route('/token/', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT LOGIN')

    username_or_email = data.get('username_or_email')
    password = data.get('password')
    db = get_db()

    if not username_or_email:
        return bad_request('Username or email is required')
    elif not password:
        return bad_request('Password is required')

    user = db.execute(
        'SELECT * FROM User WHERE username = ?', (username_or_email,)
    ).fetchone()
    if user is None:
        user = db.execute(
            'SELECT * FROM User WHERE email = ?', (username_or_email,)
        ).fetchone()

    if user is None:
        return bad_request('Incorrect username or email')
    elif not check_password_hash(user['password'], password):
        return bad_request('Incorrect password')

    # 登录成功，服务器生成token并返回给用户端
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    return created('Login successfully', token=s.dumps({'idUser': user['idUser'], 'email': user['email'], 'randnum': random.randint(0, 1000000)}).decode('utf-8'))


@bp.route('/code/', methods=['POST'])
def get_code():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT CODE')

    email = data.get('email')
    if not email:
        return bad_request('Email is required')


    if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
        return bad_request('Email format error')

    db = get_db()
    if db.execute(
        'SELECT idUser FROM User WHERE email = ?', (email,)
    ).fetchone() is not None:
        return bad_request('Email {} is already registered.'.format(email))

    code = random.randint(100000, 999999)
    # 使用sqlite数据库的情况：
    # try:
    db.execute(
        'REPLACE INTO Verification VALUES (?,?,?)',
        (email, code, datetime.datetime.now())
    )
    # except Exception as e:
    #     current_app.logger.debug(e)
    #     return bad_request('Redis storing error '+str(e))
    # 使用redis情况的代码如下：
    # try:
    #     redis_db.set('Email:'+email, code, 1800)    # 有效期半小时
    # except Exception as e:
    #     current_app.logger.debug(e)
    #     return bad_request('Redis storing error '+str(e))

    # 邮箱真实性验证，有点慢，不知道是否真的需要
    # if not verify_istrue(email):
    #     return bad_request('Email does not exist')
    send_verification_code(email, code)
    return created('Generate and send token successfully')


@auth.error_handler
def error_handler():
    return unauthorized('Unauthorized Access')


@auth.verify_token
def verify_token(token):
    g.user = None
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        # token正确但是过期了
        return False
    except BadSignature:
        # token错误
        return False
    if 'idUser' in data:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM User WHERE idUser = ?', (data['idUser'],)
        ).fetchone()
        return True
    return False


@bp.route('/user/', methods=['GET'])
@auth.login_required
def get_info():
    db = get_db()
    user_table = db.execute('SELECT * FROM User')
    name_list = [tuple[0] for tuple in user_table.description]
    user = {}
    for item in tuple(name_list):
        user[item] = g.user[item]

    return ok('Get user info successfully', data=user)


@bp.route('/user/', methods=['PUT'])
@auth.login_required
def update_info():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT UPDATE')

    username = data.get('username')
    realname = data.get('realname', '')
    id_card_num = data.get('id_card_num', '')
    university = data.get('university', '')
    school = data.get('school', '')
    grade = data.get('grade', '')
    gender = data.get('gender', 0)
    phone = data.get('phone', '')
    qq = data.get('qq', '')
    wechat = data.get('wechat', '')

    db = get_db()

    if not username:
        return bad_request('Username is required')
    elif db.execute(
        'SELECT idUser FROM User WHERE username = ? AND username != ?', (username, g.user['username'],)
    ).fetchone() is not None:
        return bad_request('User {} is already registered.'.format(username))

    db.execute(
        'UPDATE User SET username = ?, realname = ?, id_card_num = ?, university = ?, school = ?, grade = ?, gender = ?, phone = ?, qq = ?, wechat = ?'
        ' WHERE idUser = ?',
        (username, realname, id_card_num, university, school, grade, gender, phone, qq, wechat, g.user['idUser'])
    )
    db.commit()

    return ok('Update user info successfully')


@bp.route('/avatar/', methods=['GET'])
@auth.login_required
def get_avatar_url():
    db = get_db()
    avatar = db.execute(
        'SELECT avatar FROM User WHERE idUser = ?', (g.user['idUser'],)
    ).fetchone()
    if avatar['avatar'] is not None:
        return ok('Get user avatar successfully', data={'avatar':avatar['avatar']})      
    else:
        return bad_request('User avatar is not available')



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/image/<filename>')
def get_uploaded_file(filename):

    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)

import tempfile
@bp.route('/avatar/', methods=['POST'])
@auth.login_required
def change_avatar():
    # 先得到文件
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = file.filename
        extention = filename.rsplit('.', 1)[1]

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], str(g.user['idUser']) + '.' + extention))
        
        avatar = os.path.join(current_app.config['BASE_STATIC_URL'], str(g.user['idUser']) + '.' + extention)
        db = get_db()
        db.execute(
            'UPDATE User SET avatar = ? WHERE idUser = ?', (avatar, g.user['idUser'])
        )
        db.commit()
        return ok('change avatar successfully', data={'avatar':avatar})
    else:
        return bad_request('file is supposed to be jpg or png')


@bp.route('/password/', methods=['POST'])
@auth.login_required
def change_password():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT CHANGING PASSWORD')

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if not old_password:
        return bad_request('Old password is required')
    elif not new_password:
        return bad_request('New password is required')

    if not check_password_hash(g.user['password'], old_password):
        return bad_request('Old password wrong')

    db = get_db()
    db.execute(
        'UPDATE User SET password = ? WHERE idUser = ?', (generate_password_hash(new_password), g.user['idUser'])
    )
    db.commit()
    return ok('Change password successfully')
