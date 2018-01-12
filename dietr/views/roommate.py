import json

from flask import Blueprint, redirect, render_template, request, url_for

from dietr import login_required
from dietr.models.roommate import RoommateModel

blueprint = Blueprint('', __name__)

model = RoommateModel()


@blueprint.route('/person/add', methods=['GET', 'POST'])
@login_required
def add_person():
    '''The add action allows users to add an person.'''
    if request.method == 'POST':
        name = request.form['name']

        # Get account specific indentifier
        handle = model.get_count()

        person = {
            'handle': handle,
            'name': name
        }

        model.add_person(person)

        # Redirect to person page
        return redirect(f'person/{handle}')

    return render_template('/person/add.html')


@blueprint.route('/person/<int:handle>/edit', methods=['GET', 'POST'])
@login_required
def edit_person(handle):
    '''The edit action allows users to change a person.'''
    person = model.get_person(handle)

    # Check if person exists
    if not person:
        return render_template('error/not_found.html'), 404

    person['allergies'] = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    if request.method == 'POST':
        if 'name' in request.form.values():
            person['name'] = request.form['name']

    return render_template('/person/edit.html', person=person)


@blueprint.route('/person/<int:handle>/remove', methods=['GET', 'POST'])
@login_required
def remove_person(handle):
    '''The remove action allows users to remove a person.'''
    person = model.get_person(handle)

    # Check if person exists
    if not person:
        return render_template('error/not_found.html'), 404

    if request.method == 'POST':
        print(person['id'])

        model.remove_person(person['id'])

        return redirect('persons')

    return render_template('/person/remove.html', person=person)


@blueprint.route('/person/<int:handle>')
@login_required
def view_person(handle):
    '''The view action allows users to view a person.'''
    person = model.get_person(handle)

    # Check if person exists
    if not person:
        return render_template('error/not_found.html'), 404

    # Fetch allergies of said person
    person['allergies'] = model.get_allergies(person['id'])
    person['ingredients'] = model.get_ingredients(person['id'])

    return render_template('/person/view.html', person=person)


@blueprint.route('/persons')
@login_required
def overview_person():
    '''The overview action allows users to view all their persons.'''
    persons = model.get_persons()

    return render_template('/person/overview.html', persons=persons)