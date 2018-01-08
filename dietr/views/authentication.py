from flask import Blueprint, request, redirect, render_template, url_for, \
                  session

import re

from .. import login_required
from ..models.authentication import AuthenticationModel

PATTERN_EMAIL = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')

blueprint = Blueprint('authentication', __name__)

model = AuthenticationModel()

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    '''The login action allows user to login.'''
    error = {}

    print('user_id' in session)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get the user from the database
        user = model.get_user(username)

        # Check if the password matches the hash
        if model.verify_hash(password, user['hash']):
            # Add user session key
            session['user_id'] = user['id']

            return redirect('/dashboard'), 302

        else:
            error['login']: 'Password or username is incorect'
    return render_template('/authentication/login.html', error = error)

@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    '''The logout action allows users to logout.'''
    if request.method == 'POST':
        # Remove user sessin key
        session.pop('user_id', None)

        # Redirect user
        return redirect(url_for('/dashboard')), 302
    return render_template('/authentication/logout.html')

# @TODO move validation to model
@blueprint.route('/join', methods = ['GET', 'POST'])
def join():
    '''The join action allows users to register.'''
    error = {}

    if request.method == 'POST':
        # Get form data
        user = {
            'username': request.form['username'],
            'email':    request.form['email']
        }

        '''
        # @TODO move to model
        # Check if email adress is valid
        if PATTERN_EMAIL.match(user['email']):
            error['email'] = 'You have not entered a valid mail address.'
        '''

        first_name  = request.form['first-name']
        middle_name = request.form['middle-name']
        last_name   = request.form['last-name']

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
        password        = request.form['password']
        password_verify = request.form['confirm-password']

        if password == password_verify:
            # Get hash
            user['hash'] = model.generate_hash(password)

        else:
            error['password'] = 'Passwords do not match'

        # Check for errors
        if error:
            # Show errors
            print(error)
            return render_template('/authentication/join.html', error=error,
                                                                user=user)

        # Check password length
        if len(password) < 8:
            error['password'] = 'Your password is too short.'

        '''
        # @TODO replace with regex
        # Check if password is valid
        else:
            lets=0
            nums=0
            chars=0
            for char in user['password']:
                if char.isdigit():
                    nums+=1
                elif char.isalpha():
                    lets+=1
                else:
                    chars+=1

            if lets==0 or nums==0 or chars==0:
                error['password']='Your password does not contain a letter, number and special character.'
        '''

        # Check for errors
        if error:
            # Show errors
            print(error)
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
            print(error)
            return render_template('/authentication/join.html', error=error,
                                                                user=user)

        else:
            # Register user
            model.add_user(user)

            user = model.get_user(user['username'])

            # Add user id to sesson
            sessions['user_id'] = user['id']

            return redirect(url_for('dashboard')), 302

    # Return template
    return render_template('/authentication/join.html', error=error)

@blueprint.route('/user', methods=['GET', 'POST'])
def user():
    if request.method=='POST':
        new_first_name=request.form['first_name']
        new_middle_name=request.form['middle_name']
        new_last_name=request.form['last_name']
        new_username=request.form['username']
        current_password=request.form['current_password']
        new_password=request.form['new_password']
        new_password_confirm=request.form['new_password_confirm']
        new_email=request.form['email']

        userdata=model.get_user(sessions['user_id'])

        errors={}

        name=new_firstname
        if new_firstname and new_last_name:
            name+=new_middle_name+' '+new_last_name
        else:
            errors['name']='You have not entered a valid name.'

        if not new_email:
            errors['email']='You have not entered a valid E-mailaddress.'

        if not new_username:
            errors['username']='You have not entered a valid username.'

        if model.verify_hash(current_password, userdata['hash']):
            new_user={'name': name,
                      'username': new_username,
                      'hash': model.generate_hash(new_password),
                      'email': new_email,
                      'id': userdata['id']}
            if new_password:
                if new_password_confirm==new_password:
                    model.update_user_with_password(new_user)
                else:
                    errors['password']='New passwords do not match.'
            else:
                model.update_user_without_password(new_user)
        else:
            errors['password']='Invalid password.'

        return render_template(url_for('userpage'), error=errors, userdata=model.get_user(userdata['id']))

    else:
        userdata=model.get_user(sessions['user_id'])
        return render_template(url_for('userpage'), user=userdata)
