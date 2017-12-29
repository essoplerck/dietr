from flask import Blueprint
from flask_restful import Api

import pymysql as sql

app = Blueprint('api', __name__)
api = Api(app)

connection = sql.connect(host        = '185.182.57.56',
                         user        = 'renswnc266_dietr',
                         password    = 'qvuemzxu',
                         db          = 'renswnc266_dietr',
                         cursorclass = sql.cursors.DictCursor)

from .resources import ingredient
