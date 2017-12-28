from .. import app
from ..models.pantry import PantryModel

model = PantryModel()

@app.route('/pantry/add')
def add_pantry(self):

    pass

@app.route('/pantry/<int:index>/edit')
def edit_pantry(self, index):

    pass

@app.route('/pantry/<int:index>/delete')
def delete_pantry(self, index):

    pass

@app.route('/pantry/<int:index>')
def view_pantry(self, index):

    pass

@app.route('/pantry')
def overview_pantry(self):

    pass
