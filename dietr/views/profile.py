from flask import Blueprint, request

from .. import login_required
from ..models.profile import ProfileModel

blueprint = Blueprint('profile', __name__)

model = ProfileModel()


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    error = {}

    if request.method == 'POST':
        form = request.form.values()
        user = model.get_user(sessions['user'])

        if all(item in form for item in ['first_name', 'middle_name', 'last_name']):
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

            model.update_name(name)

        if 'email' in form:
            email = request.form['email']

            '''
            # @TODO move to model
            # Check if email adress is valid
            if PATTERN_EMAIL.match(user['email']):
                error['email'] = 'You have not entered a valid mail address.'
            '''

            user['email'] = email

            model.update_email(email)

        if 'username' in form:
            pass

        if all(item in form for item in ['password-current', 'password', 'password-verify']):
            pass

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
                    error['password'] = 'New passwords do not match.'
            else:
                model.update_user_without_password(new_user)
        else:
            error['password'] = 'Invalid password.'

        return render_template('/profile', error=error, user=user)

    else:
        user = model.get_user(sessions['user'])

    return render_template('/profile', error=error, user=user)
