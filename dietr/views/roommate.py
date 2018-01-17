import json

from flask import Blueprint, redirect, render_template, request, url_for

from dietr.utils import login_required
from dietr.models.roommate import RoommateModel

blueprint = Blueprint('roommate', __name__)

model = RoommateModel()


@blueprint.route('/roommate/add', methods=['GET', 'POST'])
@login_required
def add_roommate():
    """The add action allows users to add an roommate."""
    if request.method == 'POST':
        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        # Get account specific indentifier
        handle = model.get_count()

        model.add_roommate(handle, first_name, middle_name, last_name)

        # Redirect to roommate page
        return redirect(url_for('roommate.roommate', handle=handle))
    return render_template('/roommate/add.html')


@blueprint.route('/roommate/<int:handle>/edit', methods=['GET', 'POST'])
@login_required
def edit_roommate(handle):
    """The edit action allows users to change a roommate."""
    roommate = model.get_roommate(handle)

    # Check if roommate exists
    if not roommate:
        return render_template('error/not_found.html'), 404

    roommate.allergies = model.get_allergies(roommate.id)
    roommate.preferences = model.get_preferences(roommate.id)

    if request.method == 'POST':
        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        model.set_roommate(handle, first_name, middle_name, last_name)
    return render_template('/roommate/edit.html', roommate=roommate)


@blueprint.route('/roommate/<int:handle>/remove', methods=['GET', 'POST'])
@login_required
def remove_roommate(handle):
    """The remove action allows users to remove a roommate."""
    roommate = model.get_roommate(handle)

    # Check if roommate exists
    if not roommate:
        return render_template('error/not_found.html'), 404

    if request.method == 'POST':
        model.remove_roommate(roommate.id)

        return redirect(url_for('roommate.roommates'))
    return render_template('/roommate/remove.html', roommate=roommate)


@blueprint.route('/roommate/<int:handle>')
@login_required
def roommate(handle):
    """The view action allows users to view a roommate."""
    roommate = model.get_roommate(handle)

    # Check if roommate exists
    if not roommate:
        return render_template('error/not_found.html'), 404

    # Fetch allergies of said roommate
    roommate.allergies = model.get_allergies(roommate.id)
    roommate.preferences = model.get_preferences(roommate.id)

    return render_template('/roommate/view.html', roommate=roommate)


@blueprint.route('/roommates')
@login_required
def roommates():
    """The overview action allows users to view all their roommates."""
    roommates = model.get_roommates()

    return render_template('/roommate/overview.html', roommates=roommates)
