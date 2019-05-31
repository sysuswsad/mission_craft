from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import auth
from .db import get_db

bp = Blueprint('mission', __name__)


@bp.route('/login')
class Login():
    def get(self):
        return {'data': 'test'}