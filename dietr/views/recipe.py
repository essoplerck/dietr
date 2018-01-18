from flask import Blueprint

blueprint = Blueprint('recipe', __name__)


@blueprint.route('/recipe/<int:id>')
def view():
    pass


@blueprint.route('/recipes')
def overview():
    pass
