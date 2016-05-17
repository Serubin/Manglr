from flask import Flask
from flask_restful import Resource, Api


VERSION = "0.0.1-dev"
VERSION_HASH = ""

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    """ Index Handler """
    def get(self):
        return {'code': '200', 'version': getVersionHash()}

api.add_resource(HelloWorld, '/')


def APIResponse():
    pass


def getVersionHash():
    """ Retrieves Version Hash 
        Checks saved version hash first
    """    
    if VERSION_HASH == "":
        VERSION_HASH = subprocess.call(["git", "log", "--format='%h'", "-n" "1"])

    return VERSION_HASH

if __name__ == '__main__':
    app.run(debug=True)
