from flask import Blueprint, request, render_template, url_for, redirect, \
                  session

from dietr.models import model
from dietr.models.recipe import Order
from dietr.pagination import Pagination
from dietr.utils import login_required

blueprint = Blueprint('recipe', __name__)


@blueprint.route('/recipes', methods=['GET', 'POST'], defaults={
    'page': 1
})
@blueprint.route('/recipes/page/<int:page>')
@login_required
def view(page):
    limit = request.args.get('limit', default=20, type=int)
    sort = request.args.get('sort', default='A-Z', type=str)

    # Checks if the url doesn't ask for a non-excistent limit
    if limit not in [20, 40, 100]:
        return redirect(url_for('recipe.view', page=page, limit=20, sort=sort))

    start = limit * (page - 1)

    if sort == 'A-Z':
        order = 'ASC'
    else:
        order = 'DESC'

    user_id = session['user']
    user = model.user.get_user(user_id)

    user.allergies = model.user.get_allergies(user.id)
    user.preferences = model.user.get_preferences(user.id)

    # Make a list of allergy and ingredient ids
    allergies = [allergy.id for allergy in user.allergies ] if user.allergies else []
    preferences = [ingredient.id for ingredient in user.preferences] if user.preferences else []

    user.roommates = model.roommate.get_roommates(user.id)

    roommates = []

    tags = []

    if request.method == 'POST':
        for roommate in user.roommates:
            if 'roommate-' + str(roommate.handle) in request.form:
                roommates.append(roommate.handle)

                roommate.allergies = model.roommate.get_allergies(roommate.id)
                roommate.preferences = model.roommate.get_preferences(roommate.id)

                # Append list of allergies to list
                allergies += [allergy.id for allergy in roommate.allergies]
                preferences += [ingredient.id for ingredient in roommate.preferences]

        if 'tag-3' in request.form:
            tags.append(3)

        if 'tag-4' in request.form:
            tags.append(4)

        if 'tag-5' in request.form:
            tags.append(5)

        if 'tag-6' in request.form:
            tags.append(6)

        if 'tag-7' in request.form:
            tags.append(7)

    recipe_count = model.recipe.get_recipe_count(allergies, preferences, tags)

    # Add pagination
    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(url_for('recipe.view', page=page, limit=limit, sort=sort))

    recipes = model.recipe.get_recipes(allergies, preferences, tags,
                                       order, start, limit)

    # Add information to the recipes
    for recipe in recipes:
        recipe.allergies = model.recipe.get_allergies(recipe.id)
        recipe.ingredients = model.recipe.get_ingredients(recipe.id)
        recipe.tags = model.recipe.get_tags(recipe.id)

    return render_template('/recipe/view.jinja', recipes=recipes, user=user,
                           pagination=pagination, roommates=roommates,
                           tags=tags, sort=sort, limit=limit)
