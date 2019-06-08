from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


<<<<<<< HEAD
def fine_response(status_code, message=None, token=None, data=None):
=======
def fine_response(status_code, message=None, data=None):
>>>>>>> 61dfbb4bf5393e25ecff354c84dadeb9cdf7f4ba
    payload = {}
    if message:
        payload['message'] = message
    if data:
        payload['data'] = data
    response = jsonify(payload)
    response.status_code = status_code
    return response


def ok(message, data=None):
    return fine_response(status_code=200, message=message, data=data)

<<<<<<< HEAD
def created(message, token=None, data=None):
    return fine_response(status_code=201, message=message, token=token, data=data)
=======
def created(message, data=None):
    return fine_response(status_code=201, message=message, data=data)
>>>>>>> 61dfbb4bf5393e25ecff354c84dadeb9cdf7f4ba


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


def forbidden(message):
    return error_response(status_code=403, message=message)
# with app.app_context():
#     res = jsonify(pyload)
#     print(res.status_code)
#     print(json.loads(res.get_data(as_text=True))['message'])
#     print(json.loads(res.get_data(as_text=True))['data'])