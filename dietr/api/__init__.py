from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


from dietr.api.resources import ingredient, person
