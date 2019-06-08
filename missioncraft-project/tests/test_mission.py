import os
import json
import pytest
from werkzeug.security import check_password_hash

from app.db import get_db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


def get_basic_auth_headers(ContentType='application/json'):
    '''创建Basic Auth认证的headers'''
    return {
        'Accept': 'application/json',
        'Content-Type': ContentType
    }


def get_token_auth_headers(client, app, username_or_email, password, content_type = 'application/json'):
    '''创建JSON Web Token认证的headers'''
    headers = get_basic_auth_headers()
    response = client.post('/api/token/', headers=headers, data=json.dumps({'username_or_email':username_or_email, 'password':password}))
    assert response.status_code == 201
    response = json.loads(response.get_data(as_text=True))
    token = response.get('token')
    assert token is not None
    return {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': content_type
    }


@pytest.mark.parametrize((), (
))
def test_create_mission(client, app):
    response = client.post('/api/mission/', headers=get_basic_auth_headers(), data=json.dumps())
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if response.status_code == 201:
        with app.app_context():
            assert get_db().execute('SELECT code FROM Verification WHERE email = ?', (email,)).fetchone() is not None

