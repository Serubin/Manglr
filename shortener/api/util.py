import json, subprocess
import api

""" UTIL """
class Defines():
    SUCCESS_OK          = 200
    SUCCESS_CREATED     = 201
    SUCCESS_ACCEPTED    = 202
    SUCCESS_NO_CONTENT  = 204

    ERROR_CLIENT        = 400
    ERROR_EXISTS        = 401
    ERROR_PARAM         = 402
    ERROR_FORBIDDEN     = 403
    ERROR_NOT_FOUND     = 404
    ERROR_LEGAL         = 451

    ERROR_SERVER        = 500
    ERROR_DB            = 501


def APIErrorResp(result, msg):
    retval = {
        'error': msg
    }

    return APIResp(result, retval)

def APIResp(result, data):
    retval = {'result': result, 'version': getVersionHash() }
    if data != None:
        retval.update(data)

    return json.dumps(retval, sort_keys=True)

def getVersionHash():
    """ Retrieves Version Hash 
        Checks saved version hash first
    """
    print(api.VERSION_HASH)
    if not api.VERSION_HASH or api.VERSION_HASH == "":
        api.VERSION_HASH = subprocess.check_output(["git", "describe"])

    return api.VERSION_HASH



