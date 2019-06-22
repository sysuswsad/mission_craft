from flask_cors import CORS
import os
# import redis
# redis_db = None

from flask import Flask
from config import Config
from flask_mail import Mail
from flask_cors import *
from threading import Timer
import datetime
from app.currency import refund_overdue

mail = Mail()
# 每隔1分钟扫一次数据库，把过期任务找出来标记state=1
def check_mission_out_of_state(db):
    # 为publisher返还金额
    refund_overdue()

    # 扫描数据库并更新：
    db.execute('UPDATE MissionInfo SET state = 2 WHERE state == 0 AND deadline < datetime(CURRENT_TIMESTAMP,"localtime")')
    db.execute('UPDATE MissionOrder SET order_state = 2 WHERE order_state == 0 AND mission_id == (SELECT idMissionInfo FROM MissionInfo WHERE deadline < datetime(CURRENT_TIMESTAMP,"localtime"))')
    db.commit()

    t = Timer(60, check_mission_out_of_state, (db,))
    t.start()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    
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

    # 扫描数据库更新过期任务
    # with app.app_context():
    #     check_mission_out_of_state(db.get_db())

    return app
