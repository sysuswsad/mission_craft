from flask import (
    Blueprint, g, request
)
from werkzeug.exceptions import abort
import datetime

from app.api.user import auth
from app.db import get_db
from app.api import bp
from app.response_code import bad_request, unauthorized, ok, created

import json


@bp.route('/notification/', methods=('get','post'))
@auth.login_required
def index():
	db = get_db()
    notifications = db.execute(
        'SELECT idNotification, mission_id, message, create_time, has_read'
        ' FROM Notification'
    ).fetchall()

    return notifications


def get_notification(idNotification):
    """返回对应通知id的通知item
    """
    notification = get_db().execute(
        'SELECT idNotification, mission_id, message, create_time, has_read'
        ' FROM Notification'
        ' WHERE idNotification = ?',
        (idNotification,)
    ).fetchone()
    
    if notification is None:
        abort(404, "Notification id {0} doesn't exist.".format(idNotification))

    return notification


