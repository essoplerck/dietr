from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from dietr.models.authentication import AuthenticationModel
from dietr.models.user import User
from dietr.utils import login_required

blueprint = Blueprint('authentication', __name__)

model = AuthenticationModel()


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    '''The login action allows user to login.'''
    error = {}

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get the user from the database
        user = model.get_user(username)

        # Check if the password matches the hash
        if model.verify_password(password, user.hash):
            # Add user session key
            session['user'] = user.id

            return redirect(url_for('overview.dashboard'))

        else:
            error['password'] = 'Password or username is incorect'
            print(error)
    return render_template('/authentication/login.jinja', error=error)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    '''The logout action allows users to logout.'''
    if request.method == 'POST':
        # Remove user sessin key
        session.pop('user', None)

        # Redirect user
        return redirect(url_for('overview.dashboard'))
    return render_template('/authentication/logout.jinja')


@blueprint.route('/join', methods=['GET', 'POST'])
def join():
    '''The join action allows users to register.'''
    error = {}
    user = None

    if request.method == 'POST':
        # Get username and email adress
        username = request.form['username']
        email = request.form['email']

        # Check if user exit
        count = model.does_user_exist(username, email)

        if count['username_count']:
            error['username'] = 'This username is already in use.'

        if count['email_count']:
            error['email'] = 'There already is a user with this email address.'

        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        # Check if user has enterd a name
        if not first_name:
            error['first-name'] = 'You have not entered a first name.'

        if not last_name:
            error['last-name'] = 'You have not entered a last name.'

        # Fetch the passwords
        password = request.form['password']
        password_verify = request.form['password-verify']

        # Check password length
        if len(password) < 8:
            error['password'] = 'Your password is too short.'

        if not password == password_verify:
            error['password_verify'] = 'Passwords do not match'

        # Check for errors
        if not error:
            # Register user
            model.add_user(username, email, first_name, middle_name, last_name,
                           password)

            user = model.get_user(username)

            # Add user id to sesson
            session['user'] = user.id

            return redirect(url_for('overview.dashboard'))

        # Pass all data to template so the user does not have to refill it
        user = User(0, username, email, first_name, middle_name, last_name, 0)
    return render_template('/authentication/join.jinja', error=error, user=user)


@blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
    """Allow users to reset their password via email."""
    error = {}

    if request.method == 'POST':
        email = request.form['email']

        # Expand if the future if we have more time
        pass
    return render_template('/authentication/reset.jinja', error=error)
