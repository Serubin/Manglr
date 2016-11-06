from flask import Blueprint

from api.controllers import login, url, user
from api.db import init_db
from api.util import *

api = Blueprint('api', __name__, url_prefix='/api')

init_db()


@api.route('/')
def api_index():
    return APIResp(200, None)

def register_blueprints(app):
    app.register_blueprint(api)
    app.register_blueprint(url.api_url)
    app.register_blueprint(user.api_user)
    app.register_blueprint(login.api_login)


