from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for)

from dietr.models.diet import DietModel

blueprint = Blueprint('diet', __name__)

model = DietModel()


@blueprint.route('/diet')
def view():
    user = model.get_user()
    user.allergies = model.get_allergies()
    user.preferences = model.get_preferences()

    print(user)
    pass
