from flask import render_template

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
        format = re.compile('^(allergy|ingredient)-([0-9])$')

        for key, value in request.form.items():
            # Check if form name starts with allergy or ingredient
            match = format.search(key)

            if not match:
                break

            type  = match.group(1)
            index = int(match.group(2)) - 1

            print(type, index)

    return render_template('/person/edit.html', errors = errors,
                                                person = person)

@app.route('/person/<string:name>/delete', methods = ['GET', 'POST'])
def delete_person(name):
    pass

@app.route('/person/<string:name>')
def view_person(name):
    person = model.get_person(name)

    person['allergies']   = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    return render_template('/person/view.html', person = person)

@app.route('/persons')
def overview_person():
    persons = model.get_persons()

    return render_template('/person/overview.html', persons = persons)
