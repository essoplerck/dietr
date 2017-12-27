from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from . import database

from .controllers.ingredient import *
from .controllers.session import *
