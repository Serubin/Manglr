from flask import Blueprint
from flask_login import LoginManager
import api

from api.controllers import login, url
from api.db import init_db
from api.util import APIResp, APIErrorResp, Defines

api_root = Blueprint('api', __name__, url_prefix='/api')

init_db()


api.LOGIN_MANAGER = LoginManager()

@api.LOGIN_MANAGER.user_loader
def load_user(user_id):
    return User(email=user_id)

def api_init(app):
    app.register_blueprint(api_root)
    app.register_blueprint(url.api_url)
    app.register_blueprint(login.api_login)
    api.LOGIN_MANAGER.init_app(app)

@api_root.route('/')
def api_index():
    return APIResp(200, None)

