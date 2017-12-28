from flask import Blueprint, Flask

import pymysql as sql

connection = sql.connect(host        = '185.182.57.56',
                         user        = 'renswnc266_dietr',
                         password    = 'qvuemzxu',
                         db          = 'renswnc266_dietr',
                         cursorclass = sql.cursors.DictCursor)

api = Blueprint('api', __name__)

app = Flask(__name__,
            template_folder = 'templates',
            static_folder   = 'static')

app.config.from_object('config')
app.register_blueprint(api, url_prefix = '/api')
