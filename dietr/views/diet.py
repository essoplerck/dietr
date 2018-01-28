from flask import Blueprint, render_template, request, session

from dietr.models import model
from dietr.utils import login_required

blueprint = Blueprint('diet', __name__)


@blueprint.route('/diet')
@login_required
def view():
    # Get user id from session
    user_id = session['user']

    user = model.user.get_user(user_id)

    user.allergies = model.user.get_allergies(user.id)
    user.roommates = model.roommate.get_roommates(user.id)
    user.preferences = model.user.get_preferences(user.id)

    return render_template('diet/view.jinja', user=user)
