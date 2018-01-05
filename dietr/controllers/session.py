from flask import request, session

from .. import app, login_required
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

        # Check if the passwords (hashes) match
        if pbkdf2_sha256.verify(password, user['hash']):
            # Add user session key
            session['id']=user['id']
            #Return de template van de userpage
        else:
            errors={'login': 'Password or username is incorect'}
            #Return de template van de inlogpage (als die er is)
    else:
        #Return de template van de inlogpage (als die er is)

@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    '''The logout action allows user to logout.'''

    # Remove user sessin key
    session.pop('id', None)
    # Redirect user
    #Return de template van de uitlogpage (als die er is), of de homepage

@app.route('/join', methods = ['GET', 'POST'])
def join():
    '''The join action allows user to register.'''

    errors = {}

    if request.method == 'POST':
        # Get form data
        user = {}
        user['name']=request.form('name')
        user['username']=request.form('username')
        user['password']=request.form('password')
        user['confirm_password']=request.form('confirm_password')
        user['email']=request.form('email')

        count = model.does_user_exist(user['email'], user['username'])

        if count['email']:
            errors['email'] = 'There already is a user with this email address.'

        if count['username']:
            errors['username'] = 'This user name is already in use.'

        if len(user['name'].split(' '))==0:
            errors['name']='You have not entered a name.'
        elif user['name'][0]==' ':
            errors['name']='You have not entered a first name.'
        elif user['name'][len(user['name'])-1]==' ':
            errors['name']='You have not entered a last name.'

        if len(user['password'])<8 or len(user['password'])>20:
            errors['password']='Your password is not the required length.'
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
                errors['password']='Your password does not contain a letter, number and special character.'

        if not (user['password']==user['confirm_password']):
            errors['confirm_password']='Your entered passwords are not the same.'

        if len(user['email'].split(' '))==0 or len(user['email'].split('@'))!=2 or len(user['email'].split('.'))<2:
            errors['email']='You have not entered a valid E-mailadress.'

        if len(errors)==0:
            hash=[pbkdf2_sha256.hash(user['password'])]
            model.add_user(user['username'], user['name'], hash, user['email'])
            #Return naar de geregistreerdpagina
        else:
            #Return naar de registreerpagina

    else:
        # Return naar de registreerpagina
        pass
