from flask import Blueprint, request

from api.models.url import Url
from api.util import *

api_url = Blueprint('api_url', __name__, url_prefix='/api/url')

@api_url.route('/create')
def api_url_create():
    
    if not request.values.get('url'): # If no URL is provided
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "url" not provided') 

    url_str = request.values.get('url')
    # END no URL

    # Create new short
    url = Url()
    res = url.create(url_str, request.remote_addr)
    
    if not res: # If URL exists
        return APIErrorResp(Defines.ERROR_EXISTS, "Url exists")
    
    # Return values
    retval = {
        'id': str(url.getID()),
        'url': url.getURL(),
        'alias': url.getAliases()
    }
    
    return APIResp(Defines.SUCCESS_CREATED, retval) 

@api_url.route('/<alias>')
def api_url_get(alias):
    
    url = Url(alias=alias)
    
    if not url.getURL():
        return APIErrorResp(Defines.ERROR_NOT_FOUND, "Url does not exist")

    retval = {
        'id': url.getID(),
        'url': url.getURL(),
        'created': url.getTimestamp()
    }

    return APIResp(Defines.SUCCESS_OK, retval)


@api_url.route('/<url_id>/alias/add')
def api_url_alias_add(url_id):
    
    if not request.values.get('alias'): # If no Alias is provided
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "alias" not provided')

    alias = request.values.get('alias')

    url = Url(id=url_id)
    
    res = url.addAlias(alias)

    if not res:
        return APIErrorResp(Defines.ERROR_EXISTS, "Alias already exists")
    
    retval = {
        'id': str(url.getID()),
        'alias': alias
    }

    return APIResp(Defines.SUCCESS_CREATED, retval)

@api_url.route('/<url_id>/alias/rem')
def api_url_alias_rem(url_id):
    
    if not request.values.get('alias'): # If no Alias is provided
        return APIErrorResp(Defines.ERROR_PARAM, 'Param "alias" not provided')

    alias = request.values.get('alias')

    url = Url(id=url_id)
    
    res = url.delAlias(alias)

    if not res:
        return APIErrorResp(Defines.ERROR_NOT_FOUND, "Alias doesn't exist")
    
    retval = {
        'id': str(url.getID()),
        'alias': alias
    }

    return APIResp(Defines.SUCCESS_CREATED, retval)


@api_url.route('/<url_id>/alias/')
def api_alias_get(url_id):
    
    url = Url(id=url_id)
    
    if not url.getURL():
        return APIErrorResp(Defines.ERROR_NOT_FOUND, "Url does not exist")

    retval = {
        'id': url.getID(),
        'aliases': url.getAliases()
    }

    return APIResp(Defines.SUCCESS_OK, retval)

