from flask import request, render_template

from .. import app
from ..models.person import PersonModel

model = PersonModel()

@app.route('/person/add', methods = ['GET', 'POST'])
def add_person():
    pass

@app.route('/person/<string:name>/edit', methods = ['GET', 'POST'])
def edit_person(name):
    errors = {}

    person = model.get_person(name)

    person['allergies']   = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    if request.method == 'POST':
        ingredients = request.form['ingredients']

        for ingredient in ingredients.split(','):
            print(ingredient)

    return render_template('/person/edit.html', errors = errors,
                                                person = person)

@app.route('/person/<string:name>/delete', methods = ['GET', 'POST'])
def delete_person(name):
    pass

@app.route('/person/<string:name>')
def view_person(name):
    person = model.get_person(name)

    # Fetch allergies of said person
    person['allergies']   = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    return render_template('/person/view.html', person = person)

@app.route('/persons')
def overview_person():
    persons = model.get_persons()

    return render_template('/person/overview.html', persons = persons)
