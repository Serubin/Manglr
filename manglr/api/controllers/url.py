from flask import Blueprint, request
from flask_login import current_user, login_required
from api.models.user import User
from api.models.url import Url
from api.util import APIResp, APIErrorResp, Defines

api_url = Blueprint('api_url', __name__, url_prefix='/api/url')

@api_url.route('', methods=['POST'])
@api_url.route('/', methods=['POST'])
def api_url_create():
    
    data = request.get_json()

    if not data.get('url'): # If no URL is provided
        return APIErrorResp(Defines.ERROR_PARAM, '"url" not provided') 

    data_url = data.get('url')
    data_aliases = data.get('aliases')

    #Get current user's id
    user_id = None 
    if current_user.is_authenticated:
        user_id = current_user.getInteralId()
    
    # Create new short
    url = Url()
    res = url.create(data_url, request.remote_addr, user_id=user_id)
    
    if not res: # If URL exists TODO, should return existing url if it belongs to user
        return APIErrorResp(Defines.ERROR_EXISTS, "Url exists")

    failed_aliases = []

    for alias in data_aliases:
        if not url.addAlias(alias):
            failed_aliases.append(alias)
    
    # Return values
    retval = {
        'id': str(url.getID()),
        'url': url.getURL(),
        'alias': url.getAliases()
    }
    
    if len(failed_aliases) >= 1:
        retval.update({'failed_alias': failed_aliases})

    return APIResp(Defines.SUCCESS_CREATED, retval) 

@api_url.route('', methods=['GET'])
@api_url.route('/')
@login_required
def api_url_get_all():

    user_id = current_user.getInteralId()

    urls = Url.getUrlForUser(user_id)
    
    return APIResp(Defines.SUCCESS_OK, {'urls': urls})
    
@api_url.route('/<alias>', methods=['GET'])
@api_url.route('/<alias>/', methods=['GET'])
def api_url_get(alias):
    
    url = Url(alias=alias)
    
    if not url.getURL():
        return APIErrorResp(Defines.ERROR_NOT_FOUND, "url or alias does not exist")

    retval = {
        'id': url.getID(),
        'url': url.getURL(),
        'aliases': url.getAliases(),
        'created': url.getTimestamp()
    }

    return APIResp(Defines.SUCCESS_OK, retval)

@api_url.route('/<url_id>', methods=['DELETE'])
@api_url.route('/<url_id>/', methods=['DELETE'])
def api_url_delete(url_id):
    url = Url(id=url_id)
    url.remove()
 
    retval = {
        'removed': True
        }

    return APIResp(Defines.SUCCESS_NO_CONTENT, retval)

@api_url.route('/<url_id>/alias', methods=['POST'])
@api_url.route('/<url_id>/alias/', methods=['POST'])
def api_url_alias_add(url_id):

    data = request.get_json()
    
    if not data.get('alias'): # If no Alias is provided
        return APIErrorResp(Defines.ERROR_PARAM, '"alias" not provided')

    alias = data.get('alias')

    url = Url(id=url_id)
    
    res = url.addAlias(alias)

    if not res:
        return APIErrorResp(Defines.ERROR_EXISTS, "Alias already exists")
    
    retval = {
        'id': str(url.getID()),
        'alias': alias
    }

    return APIResp(Defines.SUCCESS_CREATED, retval)

@api_url.route('/<url_id>/alias', methods=['DELETE'])
@api_url.route('/<url_id>/alias/', methods=['DELETE'])
def api_url_alias_rem(url_id):
    
    data = request.get_json()

    if not data.get('alias'): # If no Alias is provided
        return APIErrorResp(Defines.ERROR_PARAM, '"alias" not provided')

    alias = data.get('alias')

    if url_id == alias:
        return APIErrorResp(Defines.ERROR_FORBIDDEN, "url id cannot be removed")

    url = Url(id=url_id)
    
    res = url.delAlias(alias)

    if not res:
        return APIErrorResp(Defines.ERROR_NOT_FOUND, "Alias doesn't exist")
    
    retval = {
        'id': str(url.getID()),
        'alias': alias
    }

    return APIResp(Defines.SUCCESS_CREATED, retval)


@api_url.route('/<url_id>/alias', methods=['GET'])
@api_url.route('/<url_id>/alias/', methods=['GET'])
def api_alias_get(url_id):
    
    url = Url(id=url_id)
    
    if not url.getURL():
        return APIErrorResp(Defines.ERROR_NOT_FOUND, "Url does not exist")

    retval = {
        'aliases': url.getAliases()
    }

    return APIResp(Defines.SUCCESS_OK, retval)

