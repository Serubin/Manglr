from flask import Blueprint
from flask_login import LoginManager

import api
from api.controllers import login, url, user
from api.db import init_db
from api.util import *

api = Blueprint('api', __name__, url_prefix='/api')

init_db()

login = Blueprint('login', __name__, url_prefix='/login')

api.LOGIN_MANAGER = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User(email=user_id)

def login_init(app):
    app.register_blueprint(api)
    app.register_blueprint(url.api_url)
    app.register_blueprint(user.api_user)
    app.register_blueprint(login.api_login)
    api.LOGIN_MANAGER.init_app(app)

@api.route('/')
def api_index():
    return APIResp(200, None)

