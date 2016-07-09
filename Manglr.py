import time, hashlib # for ip hashing

from bson.objectid import ObjectId

import ManglrDB

class Mangl:
    
    self._id = None
    self._url = None
    self._user_id = None
    self._user_ip = None
    self._aliases = []
    self._redirects = []
    self._timestamp = None

    def init(self):
        pass
    
    def create(self, url, ip, aliases=[], user_id=None):
        """ Creates new link to be mangl'd
        Parameters:
            url         -- Valid url
            ip          -- Owners ip (for tracking)
            aliases     -- Aliases if any. Will generate default
            user_id     -- User that owns link
        """
        self._url = url
        self._user_ip = ip
        

        self._aliases = aliases

    def load(self, alias=None, id=None):
        """ Loads existing mangl using id or alias
        Note: Does not load redirects into memory
        Parameters:
            alias   -- Single alias
            id      -- Object id
        """
        
        res = None # Res init

        # Fetch results
        if id != None:
            res = self._db.urls.find({ 
                '_id': ObjectId(id)
            }, { "redirects": 0 }).limit(1)

        if alias != None:
            res = self._db.urls.find({ 'aliases': { 
                    '$in': [ alias ] 
                } 
                }, { "redirects": 0 }).limit(1)

        # Process results

        if res == None or res.count() < 1:
            return False
        
        url = res[0] # Index 0 is guaranteed to exist
        
        # Save info to object
        self._id            = url._id
        self._url           = url._url
        self._user_id       = url.user_id
        self._user_ip       = url.user_ip
        self._aliases       = url.aliases
        self._timestamp     = url.timestamp

        return True

    def getID(self):
        """ Getter for id """
        return self._id

    def getURL(self):
        """ Getter for url """
        return self._url

    def getUserID(self):
        """ Getter for user id """
        return self._user_id

    def getAliases(self):
        """ Getter for aliases """
        return self._aliases

    def setAliases(self, aliases):
        """ Setter for aliases 
            Note: A valid ID must be saved to the object
            Parameters:
                aliases     -- Modifed array of aliases
        """
        if self._id == None:
            return False

        self._aliases = aliases

        url = self._db.urls.find_one_and_update({
                '_id': self._id
            },
            {
                '$set': self._aliases
            })

        return True
    
    def getRedirects(self):
        """ Getter for Redirects
            Note: Not prefetched, requires a valid id
        """
        pass

    def addRedirect(self, ip, user=None):
        """ Adds rediect to database """
        pass

    def _createRandomHash(self, url, ip, attempt):
        """ Creates a random hash from the url, ip, and unix timestamp.
            Acts recursively until a unique id is created
        """
        # IN PROGRESS
        pre_hash_str = url + str(ip) + str(time.time()) # String to be hashed

        # Create hex hash
        hasher = hashlib.sha224() 
        hasher.update(pre_hash_str)
        hash_str = hasher.hexdigest()
        
        # Takes x characters from a random starting 
        # point in the string

        self._db.find()

    def _constructObject(self):
        """ Constructs database object to be inserted """
        pass
