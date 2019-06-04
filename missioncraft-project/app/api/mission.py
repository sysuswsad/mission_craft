from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.api.user import auth
from app.db import get_db
from app.api import bp


@bp.route('/mission/')
@auth.login_required
class Login():
    def get(self):
        return {'data': 'test'}