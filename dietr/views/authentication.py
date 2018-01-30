from flask import Blueprint, redirect, render_template, request, session, \
                  url_for

from dietr.models import model
from dietr.models.user import User
from dietr.utils import login_required

blueprint = Blueprint('authentication', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Allow users to login. Will add user id to session and redirect to
    dashboard.
    """
    error = {}

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get the user from the database
        user = model.user.get_user_by_username(username)

        # Check if the password matches the hash
        if model.user.verify_password(password, user.hash):
            # Add user session key
            session['user'] = user.id

            return redirect(url_for('overview.dashboard'))

        else:
            error['password'] = 'Wachtwoord of gebruikers naam is onjuist'
    return render_template('/authentication/login.jinja', error=error)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Allow users to logout. Will redirect to dashboard."""
    if request.method == 'POST':
        # Remove user sessin key
        session.pop('user', None)

        return redirect(url_for('overview.dashboard'))
    return render_template('/authentication/logout.jinja')


@blueprint.route('/join', methods=['GET', 'POST'])
def join():
    """Allow users to register."""
    error = {}
    user = None

    if request.method == 'POST':
        # Get username and email adress
        username = request.form['username']
        email = request.form['email']

        # Check if email is in use
        if model.user.verify_email(email):
            error['username'] = 'Deze gebruikernaam is al in gebruik.'

        # Check if username is in use
        if model.user.verify_username(username):
            error['email'] = 'Er is al een gebruiker met dit email adress.'

        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        # Check if user has enterd a name
        if not first_name:
            error['first-name'] = 'U heeft geen voornaam ingevuld.'

        if not last_name:
            error['last-name'] = 'U heeft geen achternaam ingevuld.'

        # Fetch the passwords
        password = request.form['password']
        password_verify = request.form['password-verify']

        # Check password length
        if len(password) < 8:
            error['password'] = 'Uw wachtwoord is te kort, minimaal 8 tekens.'

        if not password == password_verify:
            error['password_verify'] = 'Wachtwoorden komen niet overeen'

        # Check for errors
        if not error:
            # Register user
            model.user.add_user(username, email, first_name, middle_name,
                                last_name, password)

            user = model.user.get_user_by_username(username)

            # Add user id to sesson
            session['user'] = user.id

            return redirect(url_for('overview.dashboard'))

        # Pass all data to template so the user does not have to refill it
        user = User(0, username, email, first_name, middle_name, last_name, 0)
    return render_template('/authentication/join.jinja', error=error,
                                                         user=user)


@blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
    """Allow users to reset their password via email."""
    error = {}

    if request.method == 'POST':
        email = request.form['email']

        # Expand if the future if we have more time
        pass
    return render_template('/authentication/reset.jinja', error=error)
