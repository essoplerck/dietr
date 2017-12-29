from flask import Blueprint
from flask_restful import Api

from .. import connection

app = Blueprint('api', __name__)
api = Api(app)

from .resources import ingredient
