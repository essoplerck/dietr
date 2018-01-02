from flask import render_template

from .. import app
from ..models.person import PersonModel

model = PersonModel()

@app.route('/person/add')
def add_person():
    pass

@app.route('/person/<string:name>/edit')
def edit_person(name):
    pass

@app.route('/person/<string:name>/delete')
def delete_person(name):
    pass

@app.route('/person/<string:name>')
def view_person(name):
    person = model.get_person(name)

    return render_template('/person/view.html', person = person)

@app.route('/persons')
def overview_person():
    persons = model.get_persons()

    return render_template('/person/overview.html', persons = persons)
