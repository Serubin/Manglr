from flask import Blueprint
import api

from api.controllers import auth, url
from api.models.user import User
from api.db import init_db
from api.util import APIResp, APIErrorResp, Defines


api_root = Blueprint('api', __name__, url_prefix='/api')

init_db()

def api_init(app):

    # key for testing only
    app.secret_key = 'y3cmApSMwYBznrMK6MS74SesyufUYVVLMp3Azk2KHW4LzmqaF4evZ4dk6PYJEywg' # TODO move to config
    app.register_blueprint(api_root)
    app.register_blueprint(url.api_url)
    app.register_blueprint(auth.api_auth)
    
    @app.before_request 
    def require_json(request):
        if request.method != 'GET' and not request.get_json():
            return APIErrorResp(ERROR_PARAM, "JSON unreadable")

@api_root.route('/')
def api_index():
    return APIResp(200, None)



