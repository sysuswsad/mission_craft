import functools
import random
import os
import re
import datetime

from flask import (
    Blueprint, g, request, session, current_app, send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.db import get_db
from app.response_code import bad_request, unauthorized, ok, created
from app.verification import verify_istrue
from app.api import bp

from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth()
