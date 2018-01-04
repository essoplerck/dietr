import json
import re

from flask import url_for, redirect, request, render_template

from .. import app
from ..models.person import PersonModel

model = PersonModel()

# List of invalid characters. Negated, all but a-z are invalid
invalid_characters = re.compile('[^a-z]')

@app.route('/person/add', methods = ['GET', 'POST'])
def add_person():
    '''The add action allows users to add an person.'''
    if request.method == 'POST':
        name = request.form['name']

        # Replace all non alphanumeric characters with a underscore
        url  = invalid_characters.sub('_', name.lower())

        person = {
            'name': name,
            'url':  url
        }

        model.add_person(person)

        # @TODO check for possible exploits
        # Redirect to person page
        return redirect(f'person/{url}')

    return render_template('/person/add.html')

@app.route('/person/<string:url>/edit', methods = ['GET', 'POST'])
def edit_person(url):
    '''The edit action allows users to change a person.'''
    person = model.get_person(url)

    # Check if person exists
    if not person:
        return render_template('error/not_found.html'), 404

    person['name']        = request.form['name']
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

    return render_template('/person/edit.html', person = person,
                                                data   = data)

@app.route('/person/<string:url>/remove', methods = ['GET', 'POST'])
def remove_person(url):
    '''The remove action allows users to remove a person.'''
    person = model.get_person(url)

    # Check if person exists
    if not person:
        return render_template('error/not_found.html'), 404

    if request.method == 'POST':
        print(person['id'])
        model.remove_person(person['id'])

        return redirect('persons')

    return render_template('/person/remove.html', person = person)

@app.route('/person/<string:url>')
def view_person(url):
    '''The view action allows users to view a person.'''
    person = model.get_person(url)

    # Check if person exists
    if not person:
        return render_template('error/not_found.html'), 404

    # Fetch allergies of said person
    person['allergies']   = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    return render_template('/person/view.html', person = person)

@app.route('/persons')
def overview_person():
    '''The overview action allows users to view all their persons.'''
    persons = model.get_persons()

    return render_template('/person/overview.html', persons = persons)
