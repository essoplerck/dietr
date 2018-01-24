from flask import Blueprint, render_template, request

from dietr.models.diet import DietModel
from dietr.utils import login_required

blueprint = Blueprint('diet', __name__)

model = DietModel()


@blueprint.route('/diet')
@login_required
def view():
    user = model.get_user()
    user.allergies = model.get_allergies()
    user.preferences = model.get_preferences()

    return render_template('diet/view.jinja', user=user)
