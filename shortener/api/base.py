from flask import Blueprint, request
import api

from api.util import APIResp, APIErrorResp, Defines


api_root = Blueprint('api_root', __name__)

def api_init(app):
    """ Init api
        Register all routes and app functions
        @params app - flask app
    """
    app.register_blueprint(api_root)

    @app.before_request
    def require_json():
        """ Handle unreadable json
        """
        if request.method != 'GET' and not request.get_json():
            return APIErrorResp(Defines.ERROR_PARAM, "JSON unreadable")


@api_root.route('/')
def api_index():
    return APIResp(200, None)




