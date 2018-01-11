from flask import Blueprint, request, redirect, render_template, session

import re

from dietr import login_required
from dietr.models.authentication import AuthenticationModel

PATTERN_EMAIL = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')

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
        if model.verify_hash(password, user['hash']):
            # Add user session key
            session['user'] = user['id']

            return redirect('/dashboard'), 302

        else:
            error['login']: 'Password or username is incorect'
    return render_template('/authentication/login.html', error=error)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    '''The logout action allows users to logout.'''
    if request.method == 'POST':
        # Remove user sessin key
        session.pop('user', None)

        # Redirect user
        return redirect('/dashboard'), 302
    return render_template('/authentication/logout.html')


# @TODO move validation to model
@blueprint.route('/join', methods=['GET', 'POST'])
def join():
    '''The join action allows users to register.'''
    error = {}

    if request.method == 'POST':
        # Get form data
        user = {
            'username': request.form['username'],
            'email': request.form['email']
        }

        '''
        # @TODO move to model
        # Check if email adress is valid
        if PATTERN_EMAIL.match(user['email']):
            error['email'] = 'You have not entered a valid mail address.'
        '''

        first_name = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name = request.form['last-name']

        # Check if user has enterd a name
        if not first_name:
            error['name'] = 'You have not entered a first name.'

        if not last_name:
            error['name'] = 'You have not entered a last name.'

        # Concat names
        if middle_name:
            user['name'] = f'{first_name} {middle_name} {last_name}'

        else:
            user['name'] = f'{first_name} {last_name}'

        # Fetch the passwords
        password = request.form['password']
        password_verify = request.form['password-verify']

        if password == password_verify:
            # Get hash
            user['hash'] = model.generate_hash(password)

        else:
            error['password'] = 'Passwords do not match'

        # Check for errors
        if error:
            # Show errors
            return render_template('/authentication/join.html', error=error,
                                                                user=user)

        # Check password length
        if len(password) < 8:
            error['password'] = 'Your password is too short.'

        # Check for errors
        if error:
            # Show errors
            return render_template('/authentication/join.html', error=error,
                                                                user=user)

        # Check if user exit
        count = model.does_user_exist(user['email'], user['username'])

        if count['email']:
            error['email'] = 'There already is a user with this email address.'

        if count['username']:
            error['username'] = 'This user name is already in use.'

        # Check for errors
        if error:
            # Show errors
            return render_template('/authentication/join.html', error=error,
                                                                user=user)

        else:
            # Register user
            model.add_user(user)

            user = model.get_user(user['id'])

            # Add user id to sesson
            sessions['user'] = user['id']

            return redirect('/dashboard'), 302

    # Return template
    return render_template('/authentication/join.html', error=error)
