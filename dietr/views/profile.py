from flask import Blueprint, request

from dietr import login_required
from dietr.models.profile import ProfileModel

blueprint = Blueprint('profile', __name__)

model = ProfileModel()


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    id = session['user']

    error = {}
    user = model.get_user_by_id(id)

    if request.method == 'POST':
        form = request.form.values()

        if all(item in form for item in ['first-name', 'middle-name', 'last-name']):
            first_name = request.form['first-name']
            middle_name = request.form['middle-name']
            last_name = request.form['last-name']

            # Check if user has enterd a name
            if not first_name:
                error['name'] = 'You have not entered a first name.'

            if not last_name:
                error['name'] = 'You have not entered a last name.'

            if not error:
                model.set_name(id, first_name, middle_name, last_name)

        if 'mail' in form:
            email = request.form['email']

            if not error:
                model.set_email(id, email)

        if 'handle' in form:
            username = request.form['username']

            if not error:
                model.set_username(id, username)

        if all(item in form for item in ['password-current', 'password', 'password-verify']):
            password = request.form['password']
            password_verify = request.form['password-verify']

            # Check password length
            if len(password) < 8:
                error['password'] = 'Your password is too short.'

            if not password == password_verify:
                error['password'] = 'Passwords do not match'

            if not error:
                model.set_password(id, password)

    return render_template('/profile', error=error, user=user)
