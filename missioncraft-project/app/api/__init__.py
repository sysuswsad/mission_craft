from flask import Blueprint


bp = Blueprint('api', __name__, url_prefix='/api')

# Import resources to ensure view is registered
from app.api.user import *
# from app.api.mission import *
