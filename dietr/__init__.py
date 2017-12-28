from functools import wraps

from flask import Flask, session, redirect, url_for

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

#from .controllers import ingredient, session

@app.route('/')
@login_required
def index():
    return 'Hello, world!'

@app.route('/login')
def login():
    return 'Login'

@app.route('/set')
def set():
    session['user_id'] = 1

    return session.get('user_id')
