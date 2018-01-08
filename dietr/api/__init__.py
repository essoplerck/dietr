from flask import Blueprint
from flask_restful import Api

from .. import connection


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)

from .resources import ingredient
