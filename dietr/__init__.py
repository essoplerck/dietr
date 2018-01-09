from functools import wraps

from flask import Flask, session

from .connection import connection
from .sessions import RedisSessionInterface
from .utils import login_required

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config.from_object('config')
app.session_interface = RedisSessionInterface()

'''
@app.teardown_appcontext
def teardown(exception):
    # Close database
    connection.close()
'''

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
