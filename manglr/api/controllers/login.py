from flask import Blueprint

api_login = Blueprint('api_login', __name__, url_prefix='/api/login')


@api_login('/')
def login():
    if not request.values.get('email') or request.values.get('password'): # If email and password is provided
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "email" or "password"  not provided') 
    user = User(email=request.values.get('email'))

    if user.verifyPassword(request.values.get('password')):
        login_user(user)
        retval = {
            'success': True
        }
        return APIResp(Defines.SUCCESS_OK, retval)
    retval = {
        'success': False
    }

    return APIResp(Defines.SUCCESS_OK, retval)

@api_login('/create')
def create():
    pass

def generate_hash_key(username, timestamp):
    """ @return: A hashkey for use to authenticate agains the API. """
    return base64.b64encode(
            hashlib.sha256(str(random.getrandbits(256)) + str(timestamp) + username).digest(),
            random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')

