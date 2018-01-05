from functools import wraps

from flask import Flask, session, redirect, url_for
from flask_session import Session
from passlib.hash import pbkdf2_sha256

import pymysql as sql

connection = sql.connect(host        = '185.182.57.56',
                         user        = 'renswnc266_dietr',
                         password    = 'qvuemzxu',
                         db          = 'renswnc266_dietr',
                         cursorclass = sql.cursors.DictCursor)

app = Flask(__name__)
app.config.from_object('config')
app.secret_key='\x95\x9d\xceq\x81=M\xa4y\xea\xfd\x10\x15\x12\x138"\xcdh\xcah\x83\xa4\x85'

Session(app)

'''
@app.teardown_appcontext
def teardown(exception):
    # Close database
    connection.close()
'''

def login_required(action):
    '''Decorator for the login required method. This decorator will check if the
    user is logged in. If not it will redirect to the login page.
    '''
    @wraps(action)
    def login_decorator(*arg, **kwargs):
        print(session.get('user_id'))

        # Check if user is logged in
        if 'user_id' in session:
            return action(*arg, **kwargs)
        return redirect(url_for('login'))
    return login_decorator

from .controllers import ingredient, overview, pantry, person, session
