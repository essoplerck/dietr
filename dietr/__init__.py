from datetime import datetime

from flask import Flask, g, session, request
from htmlmin.main import minify

from dietr.models.user import User
from dietr.connection import Database
from dietr.sessions import RedisSessionInterface
from dietr.utils import login_required

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config.from_object('config')
app.session_interface = RedisSessionInterface()

database = Database()


@app.teardown_request
def teardown(exception):
    database.close()


@app.before_request
def connect():
    database.connect()

    if 'user' in session:
        user_id = session['user']

        query = '''SELECT username,
                          email,
                          first_name, middle_name, last_name,
                          hash
                     FROM users
                    WHERE id = %s'''

        (username, email, first_name, middle_name, last_name, hash) = database.fetch(query, id)

        g.user = User(id, username, email, first_name, middle_name, last_name, hash)


@app.context_processor
def context():
    date = datetime.now()
    year = date.year

    return dict(user=g.user, year=year)


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
