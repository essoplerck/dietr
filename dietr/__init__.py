from functools import wraps

from flask import Flask, session, redirect, url_for

from .connection import connection
from .sessions import RedisSessionInterface

app = Flask(__name__,
            template_folder = 'templates',
            static_folder   = 'static')

app.config.from_object('config')
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

from .api import blueprint as api

app.register_blueprint(api)

from .views import authentication
from .views import ingredient
from .views import overview
from .views import pantry
from .views import person

app.register_blueprint(authentication.blueprint)
app.register_blueprint(ingredient.blueprint)
app.register_blueprint(overview.blueprint)
app.register_blueprint(pantry.blueprint)
app.register_blueprint(person.blueprint)
