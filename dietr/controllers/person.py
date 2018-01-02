from .. import app
from ..models.person import PersonModel

model = PersonModel()

@app.route('/persons/add')
def add_person(self):
    pass

@app.route('/persons/<string:name>/edit')
def edit_person(self, name):
    pass

@app.route('/persons/<string:name>/delete')
def delete_person(self, name):
    pass

@app.route('/persons/<string:name>')
def view_person(self, name):
    pass

@app.route('/persons')
def overview_person(self):
    pass
