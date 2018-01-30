from flask import Blueprint, redirect, render_template, request, session, \
                  url_for

from dietr.models import model
from dietr.utils import login_required

blueprint = Blueprint('roommate', __name__)


@blueprint.route('/roommate/add', methods=['GET', 'POST'])
@login_required
def add():
    """The add action allows users to add an roommate."""
    user_id = session['user']

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
            model.roommate.add_roommate(user_id, first_name, middle_name,
                                        last_name)

            # Redirect to roommate page
            return redirect(url_for('roommate.overview'))
    return render_template('/roommate/add.jinja', error=error)


@blueprint.route('/roommate/<int:handle>/edit', methods=['GET', 'POST'])
@login_required
def edit(handle):
    """The edit action allows users to change a roommate."""
    user_id = session['user']

    error = {}

    roommate = model.roommate.get_roommate(user_id, handle)

    # Check if roommate exists
    if not roommate:
        return render_template('error/not_found.html'), 404

    if request.method == 'POST':
        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        # Check if user has enterd a name
        if not first_name:
            error['first_name'] = 'You have not entered a first name.'

        if not middle_name:
            middle_name = None

        if not last_name:
            error['last_name'] = 'You have not entered a last name.'

        # Check for errors
        if not error:
            model.roommate.set_roommate(roommate.id, first_name,
                                        middle_name, last_name)

            return redirect(url_for('roommate.view', handle=roommate.handle))
    return render_template('/roommate/edit.jinja', roommate=roommate,
                                                   error=error)


@blueprint.route('/roommate/<int:handle>/remove', methods=['GET', 'POST'])
@login_required
def remove(handle):
    """The remove action allows users to remove a roommate."""
    user_id = session['user']

    roommate = model.roommate.get_roommate(user_id, handle)

    # Check if roommate exists
    if not roommate:
        return abort(404)

    if request.method == 'POST':
        model.roommate.delete_roommate(roommate.id)

        return redirect(url_for('roommate.overview'))
    return render_template('/roommate/remove.jinja', roommate=roommate)


@blueprint.route('/roommate/<int:handle>')
@login_required
def view(handle):
    """The view action allows users to view a roommate."""
    user_id = session['user']

    roommate = model.roommate.get_roommate(user_id, handle)

    # Check if roommate exists
    if not roommate:
        return render_template('error/not_found.html'), 404

    # Fetch allergies of said roommate
    roommate.allergies = model.roommate.get_allergies(roommate.id)
    roommate.preferences = model.roommate.get_preferences(roommate.id)

    return render_template('/roommate/view.jinja', roommate=roommate)


@blueprint.route('/roommates')
@login_required
def overview():
    """The overview action allows users to view all their roommates."""
    user_id = session['user']

    roommates = model.roommate.get_roommates(user_id)

    return render_template('/roommate/overview.jinja', roommates=roommates)
