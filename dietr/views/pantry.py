from flask import Blueprint

from dietr.models.pantry import PantryModel

blueprint = Blueprint('pantry', __name__)

model = PantryModel()


@blueprint.route('/pantry')
def overview_pantry():
    '''The view action allows users to view their pantry.'''
    pass
