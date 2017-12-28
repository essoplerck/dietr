from flask import request

from .. import app
from ..models.session import SessionModel

model = SessionModel()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''The login action allows user to login.'''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get the user from the database
        user = model.get_user(username)

        salt = user['salt']
        hash = model.get_hash(password, salt)

        # Check if the passwords (hashes) match
        if hash == user['hash']:
            # Add user session key

            pass

        else:
            error['password'] = 'Password or username is incorect'

            pass

        # Return template

        pass

    else:
        # Return template

        pass

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    '''The logout action allows user to logout.'''

    if request.method == 'POST':
        # Remove user sessin key

        # Redirect user

        pass

    else:
        # Return template

        pass

@app.route('/join', methods = ['GET', 'POST'])
def join():
    '''The join action allows user to register.'''

    if request.method == 'POST':
        # Get form data
        user = {}

        (email, username) = model.does_user_exist(user['email'],
                                                  user['username'])

        # Redirect

        pass

    else:
        # return template

        pass
