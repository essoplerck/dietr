from functools import wraps

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

def login_required():
    '''Decorator for the login required method. This decorator will check if the
    user is logged in. If not it will redirect to the login page.
    '''
    def login_decorator(action):
        @wraps
        def wrapper(*arg, **kwargs):
            # Check if user is logged in
            if session['user_id']:
                return action

            else:
                return redirect('/login')

        return wrapper
    return login_decorator

from .controllers import ingredient, session
