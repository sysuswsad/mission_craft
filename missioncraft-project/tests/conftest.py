import os
import tempfile
import time
# import redis

import pytest
from app import create_app
# from app import redis_db
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# 在后面的每个test_文件中，pytest会将fixture下的函数运行，然后将返回值赋值给同名（和该函数同名）的变量，然后直接在test_文件中使用该变量即可
# 这中间的工作都是pytest做的
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config['DATABASE'] = db_path

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
        # redis_db = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['VERIFICATION_CODE_FILE'])
        # redis_db.set('Email:123@qq.com', '111111', 1800)
        # redis_db.set('Email:1234@qq.com', '123456', 1800)
    
    yield app   

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
