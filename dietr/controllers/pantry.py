from .. import app
from ..models.pantry import PantryModel

model = PantryModel()

@app.route('/pantry/add')
def add_pantry():
    '''The add action allows users to add an ingredient to their pantry.'''

    pass

@app.route('/pantry/<int:index>/edit')
def edit_pantry(index):
    '''The edit action allows users to change an ingredient in their pantry.'''

    pass

@app.route('/pantry/<int:index>/delete')
def delete_pantry(index):
    '''The delete action allows users to remove an ingredient their pantry. '''

    pass

@app.route('/pantry/<int:index>')
def view_pantry(index):
    '''The view action allows users to view an ingredient in their pantry.'''

    pass

@app.route('/pantry')
def overview_pantry():
    '''The view action allows users to view their pantry.'''

    pass