from flask import Flask

from api import api

VERSION_HASH = ""

app = Flask(__name__)


api.register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
