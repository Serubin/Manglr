from flask import Blueprint, request
from flask_login import LoginManager
import api

from api.controllers import auth, url
from api.models.user import User
from api.db import init_db
from api.util import APIResp, APIErrorResp, Defines


api_root = Blueprint('api', __name__, url_prefix='/api')

init_db()

api.LOGIN_MANAGER = LoginManager()

@api.LOGIN_MANAGER.user_loader
def load_user(user_id):
    user = User(email=user_id, load=False)

    user.is_anonymous = False
    user.is_authenticated = True

    return user

@api.LOGIN_MANAGER.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_token')
    
    if api_key:
        return User.loadFromToken(api_key)

    api_key = request.headers.get('Authorization')
    api_key = api_key.replace('Basic ', '', 1)
    try:
        api_key = base64.b64decode(api_key)
    except TypeError:
        api_key = None

    if api_key:
        return User.loadFromToken(api_key)

    return None


def api_init(app):

    # key for testing only
    app.secret_key = 'y3cmApSMwYBznrMK6MS74SesyufUYVVLMp3Azk2KHW4LzmqaF4evZ4dk6PYJEywg' # TODO move to config
    app.register_blueprint(api_root)
    app.register_blueprint(url.api_url)
    app.register_blueprint(auth.api_auth)
    api.LOGIN_MANAGER.init_app(app)
    
    @app.before_request 
    def require_json():
        if request.method != 'GET' and not request.get_json():
            return APIErrorResp(Defines.ERROR_PARAM, "JSON unreadable")



@api_root.route('/')
def api_index():
    return APIResp(200, None)



