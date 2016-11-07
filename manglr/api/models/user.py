

class User():
    
    def __init__(self, email=None):
        self._name = None
        self._email = None
        self._api_keys = []
        self._timestamp = None
        self.is_active = None # Flask-Login (is active account)

        self.is_authenticated = False
        self.is_anonymous = None

    def create(self, email, password):
        res = api.DB.users.find({
            'email': email
            }).limit(1)

        if res.count() >= 1:
            return False

        self._email = email
        self._password_hash = bcrypt.hashpw(
                base64.b64encode(hashlib.sha256(password).digest()),
                bcrypt.gensalt()
            )
        self._timestamp = int(time.time())

        res = api.DB.users.insert_one({
            'email': self._email,
            'password_hash': self._password_hash,
            'api_keys': self._api_keys,
            'timestamp': self._timestamp
        })
        
        return True
    
    def load(self, email=None):

        res = None
        if email or self._email:
            res = api.DB.users.find({
                'email': self._email
            }, { 'password_hash': 0 }).limit(1)
        
        # Process results
        if not res or res.count() < 1:
            return False

        user = res[0] # Index 0 is guaranteed to exist

        # Save info to object
        self._email = user.get('email')
        self._name = user.get('name')
        self._api_keys = user.get('api_keys')
        self._timestamp = user.get('timestamp')

        return True
    
    def getName(self):
        """ Returns username """
        return self._name
    
    def getEmail(self):
        """ Returns email """
        return self._email

    def get_id(self):
        """ Flask Login, get username """
        return self.getEmail()

    def verifyPassword(self, password):
        if not self._email:
            return False
        res = api.DB.users.find({
                'email': self._email
            }, {
                'email': 1,
                'password_hash': 1 
            }).limit(1)

        # Process results
        if not res or res.count() < 1:
            return False

        user = res[0] # Index 0 is guaranteed to exist
        password_hash = user.get('password_hash')

        if bcrypt.checkpw(password, password_hash):
            self.is_authenticated = True
            return True

        return False

    
