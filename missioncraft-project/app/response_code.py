from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app.api import bp
from app.extensions import db


def fine_response(status_code, message=None, token=None):
    payload = {}
    if message:
        payload['message'] = message
    if token:
        payload['token'] = token
    response = jsonify(payload)
    response.status_code = status_code
    return response


def ok(message):
    return fine_response(200, message)

def created(message, token=None):
    return fine_response(201, message, token)


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    '''最常用的错误 400：错误的请求'''
    return error_response(400, message)
