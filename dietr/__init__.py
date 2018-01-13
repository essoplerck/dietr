from datetime import datetime

from flask import Flask, session, request
from htmlmin.main import minify

from dietr.connection import Database
from dietr.sessions import RedisSessionInterface
from dietr.utils import login_required

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config.from_object('config')
app.session_interface = RedisSessionInterface()

database = Database()

from dietr.models.user import UserModel

model = UserModel()


@app.teardown_request
def teardown(exception):
    database.close()


@app.before_request
def connect():
    database.connect()


@app.context_processor
def context():
    date = datetime.now()
    year = date.year

    if 'user' in session:
        user = model.get_user(session['user'])

    else:
        user = None

    return dict(user=user, year=year)


from dietr.api import blueprint as api

app.register_blueprint(api)

from dietr.views import authentication
from dietr.views import ingredient
from dietr.views import overview
from dietr.views import pantry
from dietr.views import profile
from dietr.views import roommate

app.register_blueprint(authentication.blueprint)
app.register_blueprint(ingredient.blueprint)
app.register_blueprint(overview.blueprint)
app.register_blueprint(pantry.blueprint)
app.register_blueprint(profile.blueprint)
app.register_blueprint(roommate.blueprint)
