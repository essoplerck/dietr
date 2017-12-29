from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from dietr import app as blueprint
from dietr_api import app as blueprint_api

app.register_blueprint(blueprint)
app.register_blueprint(blueprint_api, url_prefix = '/api')

if __name__=='__main__':
    app.run(host = 'localhost', port = 80)
