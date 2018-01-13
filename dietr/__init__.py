from datetime import datetime

from flask import Flask, g, session
from htmlmin.main import minify

from dietr.sessions import RedisSessionInterface
from dietr.utils import login_required
from dietr.models.user import UserModel

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config.from_object('config')
app.session_interface = RedisSessionInterface()

model = UserModel()


@app.teardown_request
def teardown(exception):
    database.close()


@app.after_request
def minify_response(response):
    if response.mimetype == u'text/html':
        response.set_data(minify(response.get_data(as_text=True)))

    return response


@app.before_request
def connect():
    database.connect()

    if 'user' in session:
        g.user = model.get_user(session['user'])


@app.context_processor
def context():
    date = datetime.now()
    year = date.year

    if 'user' in session:
        user = g.user

    else:
        user = None

    return dict(user=user, year=year)


from dietr.views import api
from dietr.views import authentication
from dietr.views import ingredient
from dietr.views import overview
from dietr.views import pantry
from dietr.views import profile
from dietr.views import roommate

app.register_blueprint(api.blueprint)
app.register_blueprint(authentication.blueprint)
app.register_blueprint(ingredient.blueprint)
app.register_blueprint(overview.blueprint)
app.register_blueprint(pantry.blueprint)
app.register_blueprint(profile.blueprint)
app.register_blueprint(roommate.blueprint)
