from flask import Blueprint

api_login = Blueprint('api_login', __name__, url_prefix='/api/login')




def generate_hash_key(username, timestamp):
    """ @return: A hashkey for use to authenticate agains the API. """
    return base64.b64encode(
            hashlib.sha256(str(random.getrandbits(256)) + str(timestamp) + username).digest(),
            random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')

