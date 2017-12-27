from flask import Flask

import MySQLdb as MySQL

app = Flask(__name__)
app.config.from_object('config')

database = MySQL.connect(host   = '185.182.57.56',
                         user   = 'renswnc266_dietr',
                         passwd = 'qvuemzxu',
                         db     = 'renswnc266_dietr')

from .controllers import ingredient, session
