from flask import Blueprint, redirect, render_template, request, url_for

from dietr.models.roommate import RoommateModel
from dietr.utils import login_required

blueprint = Blueprint('roommate', __name__)

model = RoommateModel()


@blueprint.route('/roommate/add', methods=['GET', 'POST'])
@login_required
def add():
    """The add action allows users to add an roommate."""
    error = {}

    if request.method == 'POST':
        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        # Check if user has enterd a name
        if not first_name:
            error['first-name'] = 'You have not entered a first name.'

        if not last_name:
            error['last-name'] = 'You have not entered a last name.'

        # Check for errors
        if not error:
            # Get account specific indentifier
            handle = model.get_count()

            model.add_roommate(handle, first_name, middle_name, last_name)

            # Redirect to roommate page
            return redirect(url_for('roommate.roommate', handle=handle))
    return render_template('/roommate/add.jinja', error=error)


@blueprint.route('/roommate/<int:handle>/edit', methods=['GET', 'POST'])
@login_required
def edit(handle):
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
    return render_template('/roommate/edit.jinja', roommate=roommate)


@blueprint.route('/roommate/<int:handle>/remove', methods=['GET', 'POST'])
@login_required
def remove(handle):
    """The remove action allows users to remove a roommate."""
    roommate = model.get_roommate(handle)

    # Check if roommate exists
    if not roommate:
        return abort(404)

    if request.method == 'POST':
        model.remove_roommate(roommate.id)

        return redirect(url_for('roommate.overview'))
    return render_template('/roommate/remove.jinja', roommate=roommate)


@blueprint.route('/roommate/<int:handle>')
@login_required
def view(handle):
    """The view action allows users to view a roommate."""
    roommate = model.get_roommate(handle)

    # Check if roommate exists
    if not roommate:
        return render_template('error/not_found.html'), 404

    # Fetch allergies of said roommate
    roommate.allergies = model.get_allergies(roommate.id)
    roommate.preferences = model.get_preferences(roommate.id)

    return render_template('/roommate/view.jinja', roommate=roommate)


@blueprint.route('/roommates')
@login_required
def overview():
    """The overview action allows users to view all their roommates."""
    roommates = model.get_roommates()

    return render_template('/roommate/overview.jinja', roommates=roommates)
