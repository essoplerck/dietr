import pymysql as sql

from functools import wraps
from flask import Flask, session, redirect, url_for

connection = sql.connect(host        = '185.182.57.56',
                         user        = 'renswnc266_dietr',
                         password    = 'qvuemzxu',
                         db          = 'renswnc266_dietr',
                         cursorclass = sql.cursors.DictCursor)

app = Flask(__name__,
            template_folder = 'templates',
            static_folder   = 'static')

app.config.from_object('config')

from .sessions import RedisSessionInterface

app.session_interface = RedisSessionInterface()

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
        # Check if user is logged in
        if 'user_id' in session:
            return action(*arg, **kwargs)
        return redirect(url_for('login'))
    return login_decorator

from .api import app as api

app.register_blueprint(api, url_prefix = '/api')

from .controllers import authentication, ingredient, overview, pantry, person
