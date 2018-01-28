from flask import Blueprint, request, render_template, url_for, redirect, \
                  session

from dietr.models import model
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
    # Checks if the url doesn't ask for a non-excisting limit
    if limit not in [20, 40, 100]:
        limit = 20
        page = 1

        return redirect(url_for('recipes.view', page=page, limit=limit))

    user_id = session['user']
    user = model.user.get_user(user_id)

    user.allergies = model.user.get_allergies(user.id)
    user.preferences = model.user.get_preferences(user.id)
    user.roommates = model.roommate.get_roommates(user.id)

    if user.roommates:
        for roommate in user.roommates:
            roommate.allergies = model.roommate.get_allergies(roommate.id)
            roommate.preferences = model.roommate.get_preferences(roommate.id)

    start = limit * (page - 1)

    allergies = tuple([allergy.id for allergy in user.allergies])

    recipe_count = model.recipe.get_recipe_count(allergies)

    # Add pagination
    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recepten/page/{page}/show{limit}')

    recipes = model.recipe.get_recipes(allergies, start, limit)

    # Add information
    for recipe in recipes:
        # Add the source of the recipe
        recipe.source = recipe.get_source

        # Add the extra information
        recipe.extra_info = model.recipe.get_extra_info(recipe.id)

        # Add the image
        recipe.image = model.recipe.get_image(recipe.id)

        # Add all the ingredients contained in the recipe
        recipe.ingredients = model.recipe.get_ingredients(recipe.id)

        # Add all the allergens contained in the ingredients
        for ingredient in recipe.ingredients:
            print(ingredient.id)
            allergens = model.ingredient.get_allergens(ingredient.id)

            if allergens:
                recipe.allergies += allergens

    return render_template('/recipe/view.jinja', recipes=recipes, user=user,
                           pagination=pagination)
