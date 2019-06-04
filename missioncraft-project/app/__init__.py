import os
# import redis
# redis_db = None

from flask import Flask
from config import Config
from flask_mail import Mail
mail = Mail()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # 设置数据库
    app.config.from_mapping(
        DATABASE = os.path.join(app.instance_path, 'mission_craft.sqlite')
    )

    # 加载环境变量（包括邮箱，密码等信息）
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 创建数据库
    from app import db
    db.init_app(app)

    # 创建并添加邮箱实例
    mail.init_app(app)

    # 使用redis数据库将验证码存储在内存
    # global redis_db
    # redis_db = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['VERIFICATION_CODE_FILE'])

    # 添加用户蓝图
    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app
