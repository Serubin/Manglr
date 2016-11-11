from flask import Flask

from api import base as api_base
from ui import base as ui_base

VERSION_HASH = ""

app = Flask(__name__)


api_base.api_init(app)
ui_base.ui_init(app)

if __name__ == '__main__':
    app.run(debug=True)
