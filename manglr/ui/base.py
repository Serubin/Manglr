from flask import Blueprint, request, redirect
from flask_login import current_user

from api.models.url import Url

ui_root = Blueprint('ui', __name__)

def ui_init(app):
    app.register_blueprint(ui_root)

@ui_root.route('/')
def index():
    return "index"

@ui_root.route('/<string:alias>')
@ui_root.route('/<string:alias>/')
def url_redirect(alias):
    if not alias:
        return redirect('/')

    url = Url(alias=alias)

    user_id = None
    if current_user:
        user_id = current_user.getInteralId()

    url.addRedirect(request.remote_addr, user_id)

    return redirect(url.getURL())
