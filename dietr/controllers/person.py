from flask import url_for, redirect, request, render_template

import json
import urllib

from .. import app
from ..models.person import PersonModel

model = PersonModel()

@app.route('/person/add', methods = ['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        person = {
            'name': request.form['name']
        }

        # @FIXME unsafe
        #  Encode url
        url = urllib.parse.quote(person['name'].lower())

        person['url'] = url

        '''
        ingredients = json.loads(request.form['ingredients'])

        for ingredient in ingredients:
            print(ingredient['id'])
        '''

        model.add_person(person)

        return redirect(f'person/{url}')

    return render_template('/person/add.html')

@app.route('/person/<string:name>/edit', methods = ['GET', 'POST'])
def edit_person(name):
    errors = {}

    person = model.get_person(name)

    person['allergies']   = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    data = {
        'allergies':   json.dumps(person['allergies']),
        'ingredients': json.dumps(person['ingredients'])
    }

    if request.method == 'POST':
        ingredients = json.loads(request.form['ingredients'])

        for ingredient in ingredients:
            print(ingredient['id'])

    return render_template('/person/edit.html', errors = errors,
                                                person = person,
                                                data   = data)

@app.route('/person/<string:name>/remove', methods = ['GET', 'POST'])
def remove_person(name):
    person = model.get_person(name)

    if not person:
        return render_template('error/not_found.html'), 404

    if request.method == 'POST':
        print(person['id'])
        model.remove_person(person['id'])

        return redirect('persons')

    return render_template('/person/remove.html', person = person)

@app.route('/person/<string:name>')
def view_person(name):
    person = model.get_person(name)

    if not person:
        return render_template('error/not_found.html'), 404

    # Fetch allergies of said person
    person['allergies']   = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    return render_template('/person/view.html', person = person)

@app.route('/persons')
def overview_person():
    persons = model.get_persons()

    return render_template('/person/overview.html', persons = persons)
