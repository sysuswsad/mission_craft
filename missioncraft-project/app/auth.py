import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


bp = Blueprint('auth', __name__)


# 下面这句@的作用就是：将url'/register'绑定到register视图函数，同时设置app.view_func['auth.register']=register
# 也就是说url'/register'、register视图函数、endpoint'auth.register'被绑定在一起，通过任意一个可以找到其他两个
# 通过url_for(endpoint)可以得到url'/register'，通过浏览器的url可以得到register视图函数
@bp.route('/register')
class Register():
    def get(self):
        pass

    # 这里返回code 400 表示bad request，请求失败
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'ERROR DATA AT REGISTERING'}, 400

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        db = get_db()

        if not username:
            return {'message': 'Username is required'}, 400
        elif not password:
            return {'message': 'Password is required'}, 400
        elif not email:
            return {'message': 'Password is required'}, 400
        elif db.execute(
            'SELECT idUser FROM User WHERE username = ?', (username,)
        ).fetchone() is not None:
            return {'message': 'User {} is already registered.'.format(username)}, 400

        db.execute(
            'INSERT INTO User (username, password, email) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), email)
        )
        db.commit()
        # 返回状态码200表示创建成功
        return {'message': 'Create successfully'}, 200


@bp.route('/login')
class Login():
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'ERROR DATA AT REGISTERING'}, 400

        username = data.get('username')
        password = data.get('password')
        db = get_db()

        user = db.execute(
            'SELECT * FROM User WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            return {'message': 'Incorrect username'}, 400
        elif not check_password_hash(user['password'], password):
            return {'message': 'Incorrect password'}, 400

        # session是服务器这一端的变量，而cookie则是用户端的变量，由浏览器设置，是前端的工作
        session.clear()
        session['user_id'] = user['id']
        return {'message': 'Login successfully'}, 200


@bp.before_app_request
def load_logged_in_user():
	# bp.before_app_request注册了一个函数，这个函数在每一次request后，调用对应视图函数之前 调用
    user_id = session.get('user_id')

    if user_id is None:
    	# g在调用request之时记录，在request完成之后消失
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM User WHERE idUser = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    # 之所以直接通过/index就能访问主页，因为它的蓝图没有设置前缀
    # 但是这样还不够，url_for仍然需要通过blog.index才能得到对应的url，因为index是blog的视图
    # 这时还需要额外操作：app.add_url_rule将/和index字符串关联
    # 这样url_for('index')时，字符串index被翻译为/，从而将页面导向主页
    return {'message': 'Logout successfully'}, 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
