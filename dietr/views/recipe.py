from flask import Blueprint, request, render_template, url_for, redirect, \
                  session

from dietr.models import model
from dietr.models.recipe import Order
from dietr.pagination import Pagination
from dietr.utils import login_required

blueprint = Blueprint('recipe', __name__)


@blueprint.route('/recipes', methods=['GET', 'POST'], defaults={
    'page': 1,
    'limit':  20
})
@blueprint.route('/recipes/page/<int:page>/show<int:limit>')
@login_required
def view(page, limit):
    # Checks if the url doesn't ask for a non-excistent limit
    if limit not in [20, 40, 100]:
        return redirect(url_for('recipe.view', page=1, limit=20))

    start = limit * (page - 1)
    order = 'ASC'

    user_id = session['user']
    user = model.user.get_user(user_id)

    user.allergies = model.user.get_allergies(user.id)
    user.preferences = model.user.get_preferences(user.id)

    # Make a list of allergy and ingredient ids
    allergies = [allergy.id for allergy in user.allergies]
    preferences = [ingredient.id for ingredient in user.preferences]

    user.roommates = model.roommate.get_roommates(user.id)

    roommates = []

    tags = []

    if request.method == 'POST':
        sort = request.form['sort']

        for roommate in user.roommates:
            if request.form['roommate_' + str(roommate.handle)]:
                roommates.append(roommate.id)

                roommate.allergies = model.roommate.get_allergies(user.id, roommate.handle)
                roommate.preferences = model.roommate.get_preferences(user.id, roommate.handle)

                # Append list of allergies to list
                allergies += [allergy.id for allergy in roommate.allergies]
                preferences += [ingredient.id for ingredient in roommate.preferences]

        if request.form.get('course_3'):
            tags.append(3)

        if request.form.get('course_4'):
            tags.append(4)

        if request.form.get('course_5'):
            tags.append(5)

        if request.form.get('diet_6'):
            tags.append(6)

        if request.form.get('diet_7'):
            tags.append(7)

    recipe_count = model.recipe.get_recipe_count(allergies, preferences, tags)

    # Add pagination
    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recipes/page/{page}/show{limit}')

    recipes = model.recipe.get_recipes(allergies, preferences, tags,
                                       order, start, limit)

    # Add information to the recipes
    for recipe in recipes:
        recipe.allergies = model.recipe.get_allergies(recipe.id)
        recipe.ingredients = model.recipe.get_ingredients(recipe.id)
        recipe.tags = model.recipe.get_tags(recipe.id)

        print(recipe)

    return render_template('/recipe/view.jinja', recipes=recipes, user=user,
                           pagination=pagination, roommates=roommates,
                           tags=tags, order=order)
