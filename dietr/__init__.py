from datetime import datetime

from flask import Flask, g, render_template, session
from htmlmin.main import minify
from flask import redirect
from flask import request, url_for

from dietr.sessions import RedisSessionInterface
from dietr.models.user import UserModel
from dietr.database import database

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config.from_object('config')
app.session_interface = RedisSessionInterface()

model = UserModel()


@app.teardown_request
def teardown(exception):
    """Close database connection."""
    database.close()


@app.after_request
def minify_response(response):
    """Minify response to save bandwith."""
    if response.mimetype == u'text/html':
        data = response.get_data(as_text=True)

        response.set_data(minify(data, remove_comments=True,
                                       remove_empty_space=True,
                                       reduce_boolean_attributes=True))

    return response


@app.before_request
def connect():
    """Connect to the database."""
    database.connect()

    # @TODO move to seperate method
    if 'user' in session:
        g.user = model.get_user()


@app.context_processor
def add_context():
    """Pass user and current year to templating engine."""
    date = datetime.now()
    year = date.year

    # Check if user is logged in
    user = g.user if 'user' in session else None

    return dict(user=user, year=year)


@app.errorhandler(403)
def forbidden(error):
    return render_template('error/forbidden.jinja'), 403


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/internal_server_error.jinja'), 500


@app.errorhandler(404)
def not_found(error):
    return render_template('error/not_found.jinja'), 404


from dietr.views import api

app.register_blueprint(api.blueprint)

from dietr.views import allergy
from dietr.views import authentication
from dietr.views import diet
from dietr.views import ingredient
from dietr.views import overview
from dietr.views import pantry
from dietr.views import profile
from dietr.views import recipe
from dietr.views import roommate

app.register_blueprint(allergy.blueprint)
app.register_blueprint(authentication.blueprint)
app.register_blueprint(diet.blueprint)
app.register_blueprint(ingredient.blueprint)
app.register_blueprint(overview.blueprint)
app.register_blueprint(pantry.blueprint)
app.register_blueprint(profile.blueprint)
app.register_blueprint(recipe.blueprint)
app.register_blueprint(roommate.blueprint)
