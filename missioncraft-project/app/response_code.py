from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def fine_response(status_code, message=None, token=None, data=None):
    payload = {}
    if message:
        payload['message'] = message
    if token:
        payload['token'] = token
    if data:
        payload['data'] = data
    response = jsonify(payload)
    response.status_code = status_code
    return response


def ok(message, data=None):
    return fine_response(status_code=200, message=message, data=data)

def created(message, token=None, data=None):
    return fine_response(status_code=201, message=message, token=token, data=data)


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    '''最常用的错误 400：错误的请求'''
    return error_response(status_code=400, message=message)


def unauthorized(message):
    '''401:未授权错误'''
    return error_response(status_code=401, message=message)

# with app.app_context():
#     res = jsonify(pyload)
#     print(res.status_code)
#     print(json.loads(res.get_data(as_text=True))['message'])
#     print(json.loads(res.get_data(as_text=True))['data'])