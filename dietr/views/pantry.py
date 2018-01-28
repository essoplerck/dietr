from flask import Blueprint

blueprint = Blueprint('pantry', __name__)


@blueprint.route('/pantry')
def view():
    """Allow users to view their pantry."""
    pass
