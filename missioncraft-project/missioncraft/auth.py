# coding: utf-8
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from missioncraft.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username      = request.form['username']    # 登陆身份
        password      = request.form['password']

        realname      = request.form['realname']    # 真实身份
        IDcard_number = request.form['IDcard_number']
        sex           = request.form['sex']
        
        usertype      = request.form['usertype']    # 账户类型
        
        university    = request.form['university']  # 所属组织
        school        = request.form['school']
        major         = request.form['major']
        grade         = request.form['grade']
        
        email         = request.form['email']       # 联系方式
        tel           = request.form['tel']
        
        tags          = request.form['tags']        # 兴趣标签

        # 完善其他信息
        nickname      = '新人用户'                   # 昵称

        # debug
        print("username", type(username), username)
        print("password", type(password), password)
        print("realname", type(realname), realname)
        print("IDcard_number", type(IDcard_number), IDcard_number)
        print("sex", type(sex), sex)
        print("usertype", type(usertype), usertype)
        print("university", type(university), university)
        print("school", type(school), school)
        print("major", type(major), major)
        print("grade", type(grade), grade)
        print("email", type(email), email)
        print("tel", type(tel), tel)
        print("tags",type(tags), tags)

        # 获取数据库
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, nickname, \
                realname, IDcard_number, sex, usertype, university, \
                school, major, grade, email, tel, tags) VALUES (?, ?, ?, ?, \
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), nickname,
                 realname, IDcard_number, sex, usertype, university,
                 school, major, grade, email, tel, tags)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('mission.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
