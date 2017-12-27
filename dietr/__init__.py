from flask import Flask

import pymysql as sql

connection = sql.connect(host        = '185.182.57.56',
                         user        = 'renswnc266_dietr',
                         password    = 'qvuemzxu',
                         db          = 'renswnc266_dietr',
                         cursorclass = sql.cursors.DictCursor)

app = Flask(__name__)
app.config.from_object('config')

'''
@app.teardown_appcontext
def teardown(exception):
    # Close database
    connection.close()
'''

from .controllers import ingredient, session
