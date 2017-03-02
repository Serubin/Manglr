from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from api.models.user import User
from api.util import APIResp, APIErrorResp, Defines

import time, hashlib, base64, codecs, os, random

api_auth = Blueprint('api_auth', __name__, url_prefix='/api/auth')


@api_auth.route('/login', methods=['POST'])
@api_auth.route('/login/', methods=['POST'])
def api_auth_login():


    data = request.get_json()

    if not data.get('email'):
        return APIErrorResp(Defines.ERROR_PARAM, '"email" not provided')

    if not data.get('password'):
        return APIErrorResp(Defines.ERROR_PARAM, '"password" not provided')

    user = User(email=data.get('email'))

    retval = {
        'success': False
    }

    if user.verifyPassword(data.get('password')):
        user.is_authenticated = True

        login_user(user)
        retval = {
            'success': True
        }

    return APIResp(Defines.SUCCESS_OK, retval)

@api_auth.route('/logout', methods=['GET'])
@api_auth.route('/logout/', methods=['GET'])
@login_required
def auth_api_logout():
    logout_user()
    return APIResp(Defines.SUCCESS_OK, {'success': True})

@api_auth.route('/account', methods=['GET'])
@api_auth.route('/account/', methods=['GET'])
def auth_api_account_view():
    pass

@api_auth.route('/account', methods=['POST'])
@api_auth.route('/account/', methods=['POST'])
def auth_api_account_create():
    
    data = request.get_json()

    if not data.get('email'):
        return APIErrorResp(Defines.ERROR_PARAM, '"email" not provided')

    if not data.get('password'):
        return APIErrorResp(Defines.ERROR_PARAM, '"password" not provided')

    new_user = User()
    if new_user.create(data.get('email'), data.get('password')):
        return APIResp(Defines.SUCCESS_CREATED, { 'email': data.get('email') })
    return APIErrorResp(Defines.ERROR_EXISTS, { 'email': data.get('email') })

@api_auth.route('/key', methods=['POST'])
@api_auth.route('/key/', methods=['POST'])
def auth_api_key_create():
    
    data = request.get_json()

    if not data.get('name'):
        return APIErrorResp(Defines.ERROR_PARAM, '"name" not provided')
    
    data_name = data.get('name')

    api_token = generate_hash_key(current_user.getEmail(), time.time(), data_name)
    
    current_user.load() 
    if not current_user.add_api_token(data_name, api_token):
        return APIErrorResp(Defines.ERROR_EXISTS, '"' + data_name + '" exists')

    retval = { 
        'name': data_name,
        'token': api_token
    }

    return APIResp(Defines.SUCCESS_CREATED, retval)
    
        
@api_auth.route('/key', methods=['DELETE'])
@api_auth.route('/key/', methods=['DELETE'])
def auth_api_key_delete():
    
    data = request.get_json()

    if not data.get('name'):
        return APIErrorResp(Defines.ERROR_PARAM, '"name" not provided')

    data_name = data.get('name')
    
    api_token = generate_hash_key(current_user.getEmail(), time.time(), data_name)
    
    current_user.load() 
    current_user.remove_api_token(data_name)
    
    retval = { 
        'name': data_name
    }

    return APIResp(Defines.SUCCESS_NO_CONTENT, retval)
    
#TODO accept ip restriction, accept expire date

def generate_hash_key(username, timestamp, name):
    """ @return: A hashkey for use to authenticate agains the API. """
    
    rand = str(codecs.encode(os.urandom(256), 'hex'), 'utf-8')

    char_pair = random.choice([b'rA', b'aZ', b'gQ', b'hH', b'hG', b'aR', b'DD'])
    
    hash_str = (rand  + str(timestamp) + username + name).encode('utf-8')

    hash512 = hashlib.sha512(hash_str).digest()

    base64_hash = base64.urlsafe_b64encode(hash512)

    return str(base64_hash, 'utf-8').rstrip('=')

