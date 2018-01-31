from flask import Blueprint, redirect, render_template, request, session, \
                  url_for

from dietr.models import model
from dietr.utils import login_required

blueprint = Blueprint('profile', __name__)


@blueprint.route('/profile')
@login_required
def view():
    user_id = session['user']
    user = model.user.get_user(user_id)

    return render_template('/profile/view.jinja', user=user)


@blueprint.route('/profile/edit')
@login_required
def edit():
    user_id = session['user']
    user = model.user.get_user(user_id)

    return render_template('/profile/edit.jinja', error=None, user=user)


@blueprint.route('/profile/edit/name', methods=['POST'])
@login_required
def edit_name():
    error = {}

    user_id = session['user']
    user = model.user.get_user(user_id)

    first_name = request.form['first-name']
    middle_name = request.form['middle-name']
    last_name = request.form['last-name']

    # Check if user has enterd a name
    if not first_name:
        error['first_name'] = 'U heeft geen voornaam ingevuld.'

    if not middle_name:
        middle_name = None

    if not last_name:
        error['last_name'] = 'U heeft geen achternaam ingevuld.'

    # Check for errors
    if not error:
        model.user.set_name(user.id, first_name, middle_name, last_name)

        return redirect(url_for('profile.edit'))
    return render_template('/profile/edit.jinja', error=error, user=user)


@blueprint.route('/profile/edit/email', methods=['POST'])
@login_required
def edit_email():
    error = {}

    user_id = session['user']
    user = model.user.get_user(user_id)

    email = request.form['email']

    # Check for errors
    if not error:
        model.user.set_email(id, email)

        return redirect(url_for('profile.edit'))
    return render_template('/profile/edit.jinja', error=error, user=user)


@blueprint.route('/profile/edit/username', methods=['POST'])
@login_required
def edit_username():
    error = {}

    user_id = session['user']
    user = model.user.get_user(user_id)

    username = request.form['username']

    # Check for errors
    if not error:
        model.user.set_username(user.id, username)

        return redirect(url_for('profile.edit'))
    return render_template('/profile/edit.jinja', error=error, user=user)


@blueprint.route('/profile/edit/password', methods=['POST'])
@login_required
def edit_password():
    error = {}

    user_id = session['user']
    user = model.user.get_user(user_id)

    current_password = request.form['current-password']

    password = request.form['password']
    password_verify = request.form['password-verify']

    if not model.user.verify_password(current_password, user.hash):
        error['current_password'] = 'U heeft een fout wachtwoord ingevuld'

    # Check password length
    if len(password) < 8:
        error['password'] = 'Uw wachtwoord is te kort, minimaal 8 tekens.'

    if not password == password_verify:
        error['password_verify'] = 'Wachtwoorden komen niet overeen'

    # Check for errors
    if not error:
        model.user.set_password(user.id, password)

        # Log the user out
        session.pop('user', None)

        return redirect(url_for('authentication.login'))
    return render_template('/profile/edit.jinja', error=error, user=user)
