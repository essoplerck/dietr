from flask import Flask, session

from dietr.connection import Database, connection
from dietr.sessions import RedisSessionInterface
from dietr.utils import login_required

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config.from_object('config')
app.session_interface = RedisSessionInterface()

database = Database()

'''
@app.teardown_appcontext
def teardown(exception):
    # Close database
    connection.close()
'''

from dietr.api import blueprint as api

app.register_blueprint(api)

from dietr.views import authentication
from dietr.views import ingredient
from dietr.views import overview
from dietr.views import pantry
from dietr.views import person
from dietr.views import profile

app.register_blueprint(authentication.blueprint)
app.register_blueprint(ingredient.blueprint)
app.register_blueprint(overview.blueprint)
app.register_blueprint(pantry.blueprint)
app.register_blueprint(person.blueprint)
app.register_blueprint(profile.blueprint)
