import functools
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from .db import get_db
from .response_code import bad_request, ok, created

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


bp = Blueprint('auth', __name__)


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
    db = get_db()

    if not username:
        return bad_request('Username is required')
    elif not password:
        return bad_request('Password is required')
    elif not email:
        return bad_request('Email is required')
    elif not sid:
        return bad_request('Sid is required')
    elif db.execute(
        'SELECT idUser FROM User WHERE username = ?', (username,)
    ).fetchone() is not None:
        return bad_request('User {} is already registered.'.format(username))

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
        or db.execute(
        'SELECT * FROM User WHERE email = ?', (username_or_email,)
    ).fetchone()

    if user is None:
        return bad_request('Incorrect username or email')
    elif not check_password_hash(user['password'], password):
        return bad_request('Incorrect password')

    # 登录成功，服务器生成token并返回给用户端
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    return created('Login successfully', s.dumps({'id': user['idUser'], 'email': user['email'], 'randnum': random.randint(0, 1000000)}).decode('utf-8'))


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
    return ok('Get user info successfully', g.user)


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
        'SELECT idUser FROM User WHERE username = ?', (username,)
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
def get_avatar():
    db = get_db()
    avatar = db.execute(
        'SELECT avatar FROM User WHERE idUser = ?', (g.user['idUser'],)
    ).fetchone()
    return ok('Get user avatar successfully', {'avatar':avatar})


@bp.route('/avatar/', methods=['POST'])
@auth.login_required
def change_avatar():
    data = request.get_json()
    if not data:
        return bad_request('ERROR DATA AT CHANGING AVATAR')


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
        'UPDATE User SET password = ? WHERE idUser = ?', (new_password, g.user['idUser'])
    )
    db.commit()
    return ok('Change password successfully')
