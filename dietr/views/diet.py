from flask import Blueprint

blueprint = Blueprint('diet', __name__)


@blueprint.route('/diet')
def view():
    pass
