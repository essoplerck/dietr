from flask import render_template

from .. import app
from ..models.person import PersonModel

model = PersonModel()

@app.route('/persons/add')
def add_person():
    pass

@app.route('/persons/<string:name>/edit')
def edit_person(name):
    pass

@app.route('/persons/<string:name>/delete')
def delete_person(name):
    pass

@app.route('/persons/<string:name>')
def view_person(name):
    pass

@app.route('/persons')
def overview_person():
    persons = model.get_persons()

    return render_template('/person/overview.html', persons = persons)
