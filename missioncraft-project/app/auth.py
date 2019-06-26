

from flask import (
    g, current_app
)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.db import get_db
from app.response_code import bad_request, unauthorized, ok, created, forbidden

from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth()


@auth.error_handler
def error_handler():
    return unauthorized('401 Unauthorized Access')


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
