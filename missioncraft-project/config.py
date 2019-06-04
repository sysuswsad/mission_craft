import os


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')

    # 为了安全起见不应该在程序中原文存储密码，建议在运行服务器之前使用set FLASK_SECRET=os.urandom(16)动态生成随机秘钥并存储
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    # 设置发送验证码的邮箱信息，必须自己手动设置，保证自己邮箱的隐私安全，防止自己忘了授权码，这里记一下授权码：hzqjtpbdpdxyfejd
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('FLASK_EMAIL', '1473595322@qq.com')
    MAIL_PASSWORD = os.getenv('FLASK_EMAIL_PASSWORD', 'hzqjtpbdpdxyfejd')
    MAIL_DEFAULT_SENDER = 'MissionCraft <' + str(MAIL_USERNAME) + '>'
    # 上传到的文件夹
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static')
    BASE_STATIC_URL = 'localhost:5000/api/image/'
    

    # 配置redis数据库
    # REDIS_HOST = '127.0.0.1'
    # REDIS_PORT = 6379
    # VERIFICATION_CODE_FILE = 0 # 这里要用0-15，不然就会报错
    