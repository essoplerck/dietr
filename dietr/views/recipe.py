from flask import Blueprint

blueprint = Blueprint('recipe', __name__)


@blueprint.route('/recipes')
def recipes():
    pass
