import time, hashlib, json # for ip hashing
import api

from bson.objectid import ObjectId
from pymongo import collection

class Url:
    
    
    def __init__(self, id=None, alias=None):
        self._id = None
        self._url = None
        self._user_id = None
        self._user_ip = None
        self._aliases = []
        self._redirects = []
        self._timestamp = None
    
        if id:
            self.setID(id)
            self.load(id=id)

        if alias:
            self.load(alias=alias)
    
    def create(self, url, ip, aliases=[], user_id=None):
        """ Creates new link to be mangl'd
        Parameters:
            url         -- Valid url
            ip          -- Owners ip (for tracking)
            aliases     -- Aliases if any. Will generate default
            user_id     -- User that owns link
        """

        alias = self._createRandomHash(url, ip, 0)
        self._id = alias
        self._url = url
        self._aliases = [ alias ] 

        self._user_ip = ip
        self._user_id = user_id

        res = api.DB.urls.find({
            'id': self._id,
            'user_id': self._user_id
            }).limit(1)

        if res.count() >= 1:
            return False
        
        if len(aliases) > 0:
            self._aliases = self._aliases + aliases

        dbres = api.DB.urls.insert_one({ # dump to db
                'id': self._id,
                'url': self._url,
                'user_id': self._user_id,
                'user_ip': self._user_ip,
                'aliases': self._aliases,
                'redirects': [],
                'timestamp': int(time.time())
            })
        
        return True
    
    def load(self, alias=None, id=None):
        """ Loads existing mangl using id or alias
        Note: Does not load redirects into memory
        Parameters:
            alias   -- Single alias
            id      -- Object id
        """
        
        res = None # Res init

        # Fetch results
        if id:
            res = api.DB.urls.find({ 
                    'id': id
                }, { "redirects": 0 }).limit(1)

        if alias:
            res = api.DB.urls.find({ 'aliases': { 
                    '$in': [ alias ] 
                } 
                }, { "redirects": 0 }).limit(1)

        # Process results
        if res == None or res.count() < 1:
            return False
        
        url = res[0] # Index 0 is guaranteed to exist

        # Save info to object
        self._id            = url.get('id')
        self._url           = url.get('url')
        self._user_id       = url.get('user_id')
        self._user_ip       = url.get('user_ip')
        self._aliases       = url.get('aliases')
        self._timestamp     = url.get('timestamp')
        
        return True

    def getID(self):
        """ Getter for id """
        return self._id

    def setID(self, id):
        """ Setting for id """
        self._id = id

    def getURL(self):
        """ Getter for url """
        return self._url

    def getUserID(self):
        """ Getter for user id """
        return self._user_id

    def getAliases(self):
        """ Getter for aliases """
        return self._aliases
    
    def addAlias(self, alias):
        if self._id == None:
            return False
        
        res = api.DB.urls.find({ 'aliases': { 
                '$in': [ alias ]
            }
        }, 
        {
            'aliases': 1
        }).limit(1)
        
        # If database returns result, try again
        if res.count() >= 1:
            return False
        
        res = api.DB.urls.find_one_and_update({
                'id': self._id
            },{
                '$push': { 'aliases': alias  }
            })

        print(json.dumps(res, default=lambda x: str(x)))

        return True

    def delAlias(self, alias):
        if self._id == None:
            return False

        res = api.DB.urls.find_one_and_update({
                'id': self._id
            },{
                '$pull': { 'aliases': [ alias ] }
            })
    
        return True

    def setAliases(self, aliases):
        """ Setter for aliases 
            Note: A valid ID must be saved to the object
            Parameters:
                aliases     -- Modifed array of aliases
        """
        if self._id == None:
            return False

        self._aliases = aliases

        url = api.DB.urls.find_one_and_update({
                'id': self._id
            },
            {
                '$set': self._aliases
            }, 
            return_document=ReturnDocument.AFTER
        )

        return True
    
    def getRedirects(self):
        """ Getter for Redirects
            Note: Not prefetched, requires a valid id
        """
        url = api.DB,find({
            'id': self._id
                },
                { 
                    'redirects': 1
                })
        if url == None:
            return False

        return url

    def addRedirect(self, ip, user=None):
        """ Adds rediect to database """
        if self._id == None:
            return False
        
        # Push redirect
        url = api.DB.urls.find_one_and_update({
                'id': self._id
            },
            {
                '$push': {
                    'redirects' : {'ip': ip, 'user_id': user}
                }
            }, return_document=ReturnDocument.AFTER)

        
        if url == None or url.count < 1: # Check for result
            return False
        
        return url # Return result

    def _createRandomHash(self, url, ip, attempt):
        """ Creates a random hash from the url, ip, and unix timestamp.
            Acts recursively until a unique id is created
        """
        # IN PROGRESS
        pre_hash_str = url + str(ip) + str(time.time()) # String to be hashed
        pre_hash_str = pre_hash_str.encode('utf-8')

        # Create hex hash
        hasher = hashlib.sha224() 
        hasher.update(pre_hash_str)
        hash_str = hasher.hexdigest()
        
        # Takes x characters from a random starting 
        # point in the string
        hash_final = hash_str[0:5] # TODO Add size to config
        
        # Ensures alias doesn't previously exist
        res = api.DB.urls.find({ 'aliases': { 
                    '$in': [ hash_final ]
                }
            }, 
            {
                'aliases': 1
            }).limit(1)
        
        # If database returns result, try again
        if res.count() >= 1:
            return self._createRandomHash(url, ip, attempt + 1)

        # return final
        return hash_final


    def _constructObject(self):
        """ Constructs database object to be inserted """
        pass
