from flask import url_for, redirect, request, render_template

import json
import re

from .. import app
from ..models.person import PersonModel

model = PersonModel()

@app.route('/person/add', methods = ['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        person = {
            'name': request.form['name']
        }

        url = []

        valid_characters = re.compile('([a-z0-9])')

        # Replace non valid characters
        for character in person['name']:
            match = valid_characters.search(character.lower())
            print(character.lower())

            if match:
                url.append(character)

            else:
                url.append('_')

        url = ''.join(url)

        person['url'] = url

        '''
        ingredients = json.loads(request.form['ingredients'])

        for ingredient in ingredients:
            print(ingredient['id'])
        '''

        model.add_person(person)

        return redirect(f'person/{url}')

    return render_template('/person/add.html')

@app.route('/person/<string:url>/edit', methods = ['GET', 'POST'])
def edit_person(url):
    errors = {}

    person = model.get_person(url)

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

@app.route('/person/<string:url>/remove', methods = ['GET', 'POST'])
def remove_person(url):
    person = model.get_person(url)

    if not person:
        return render_template('error/not_found.html'), 404

    if request.method == 'POST':
        print(person['id'])
        model.remove_person(person['id'])

        return redirect('persons')

    return render_template('/person/remove.html', person = person)

@app.route('/person/<string:url>')
def view_person(url):
    person = model.get_person(url)

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
