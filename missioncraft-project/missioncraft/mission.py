# coding: utf-8
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from missioncraft.auth import login_required
from missioncraft.db import get_db

bp = Blueprint('mission', __name__)


@bp.route('/')
def index():
    
    return render_template('mission/index.html')
