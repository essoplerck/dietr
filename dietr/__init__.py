from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

database = MySQL(app)
database.init_app(app)

from .controllers import ingredient, session
