from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from api.models.user import User
from api.util import APIResp, APIErrorResp, Defines

import hashlib, base64, random

api_login = Blueprint('api_login', __name__, url_prefix='/api/login')


@api_login.route('/', methods=['GET', 'POST'])
def login():

    if not request.values.get('email') or not request.values.get('password'): # If email and password is provided
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "email" or "password"  not provided') 

    user = User(email=request.values.get('email'))

    retval = {
        'success': False
    }

    if user.verifyPassword(request.values.get('password')):
        user.is_authenticated = True

        login_user(user)
        retval = {
            'success': True
        }

    return APIResp(Defines.SUCCESS_OK, retval)

@api_login.route('/logout')
@api_login.route('/logout/')
@login_required
def logout():
    logout_user()
    return APIResp(Defines.SUCCESS_OK, {'success': True})

@api_login.route('/create', methods=['GET', 'POST'])
@api_login.route('/create/', methods=['GET', 'POST'])
def create():
    
    if not request.values.get('email'):
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "email" not provided')

    if not request.values.get('password'):
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "password" not provided')

    new_user = User()
    if new_user.create(request.values.get('email'), request.values.get('password')):
        return APIResp(Defines.SUCCESS_CREATED, { 'email': request.values.get('email') })
    return APIErrorResp(Defines.ERROR_EXISTS, { 'email': request.values.get('email') })

def generate_hash_key(username, timestamp):
    """ @return: A hashkey for use to authenticate agains the API. """
    return base64.b64encode(
            hashlib.sha256(str(random.getrandbits(256)) + str(timestamp) + username).digest(),
            random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')

