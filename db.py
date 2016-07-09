
class ManglrDB():
    
    # TEMPORARY CLIENT
    self._HOST = 'localhost'
    self._PORT = 27017
    self._DB   = 'manglr'
    
    def __init__(self):
        """ Creates client and database connections/objects """
        self._client = MangoClient(self._HOST, self._PORT)
        self._db     = self._client[self._DB]

    def getDB(self):
        return self._db
