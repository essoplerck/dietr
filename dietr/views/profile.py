from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for)

from dietr.models.profile import ProfileModel
from dietr.utils import login_required

blueprint = Blueprint('profile', __name__)

model = ProfileModel()


@blueprint.route('/profile')
@login_required
def view():
    user = g.user

    return render_template('/profile/view.jinja', user=user)


@blueprint.route('/profile/edit')
@login_required
def edit():
    user = g.user

    return render_template('/profile/edit.jinja', error=None, user=user)


@blueprint.route('/profile/edit/name', methods=['POST'])
@login_required
def edit_name():
    error = {}
    user = g.user

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
        model.set_name(user.id, first_name, middle_name, last_name)

        return redirect(url_for('profile.edit'))
    return render_template('/profile/edit.jinja', error=error, user=user)


@blueprint.route('/profile/edit/email', methods=['POST'])
@login_required
def edit_email():
    error = {}
    user = g.user

    email = request.form['email']

    # Check for errors
    if not error:
        model.set_email(id, email)

        return redirect(url_for('profile.edit'))
    return render_template('/profile/edit.jinja', error=error, user=user)


@blueprint.route('/profile/edit/username', methods=['POST'])
@login_required
def edit_username():
    error = {}
    user = g.user

    username = request.form['username']

    # Check for errors
    if not error:
        model.set_username(user.id, username)

        return redirect(url_for('profile.edit'))
    return render_template('/profile/edit.jinja', error=error, user=user)


@blueprint.route('/profile/edit/password', methods=['POST'])
@login_required
def edit_password():
    error = {}
    user = g.user

    current_password = request.form['current-password']

    password = request.form['password']
    password_verify = request.form['password-verify']

    print(model.verify_password(current_password, user.hash))

    if not model.verify_password(current_password, user.hash):
        error['current_password'] = 'Incorrect password'

    # Check password length
    if len(password) < 8:
        error['password'] = 'Your password is too short.'

    if not password == password_verify:
        error['password_verify'] = 'Passwords do not match'

    # Check for errors
    if not error:
        model.set_password(user.id, password)

        # Log the user out
        session.pop('user', None)

        return redirect(url_for('authentication.login'))
    return render_template('/profile/edit.jinja', error=error, user=user)
