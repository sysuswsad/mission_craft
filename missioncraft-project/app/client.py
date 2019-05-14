""" Client App """

import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

client_bp = Blueprint('client_app', __name__,
                      url_prefix='',
                      static_url_path='',
                      static_folder='./dist/static/',
                      template_folder='./dist/',
                      )

