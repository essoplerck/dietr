from flask import Blueprint, request, render_template, url_for, redirect

from dietr.models.recipe import RecipeModel
from dietr.pagination import Pagination
from dietr.utils import login_required

blueprint = Blueprint('recipe', __name__)

model = RecipeModel()


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

        return redirect(url_for('recipe.view', page=page, limit=limit))

    user = model.user
    start = limit * (page - 1)

    roommates_allergies = []
    if request.method == 'POST' and user.roommates:
        for roommate in user.roommates:
            if request.form.get(roommate.id):
                for allergy in roommate.allergies:
                    roommate.allergies += allergy.id

    recipe_count = model.get_recipe_count(model.user_allergies(roommates_allergies))

    #Add pagination
    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recepten/page/{page}/show{limit}')


    recipes = model.get_recipe(model.user_allergies(roommates_allergies), start, limit)

    #Add information
    for recipe in recipes:

        recipe.source = recipe.get_source
        recipe.extra_info = model.get_extra_info(recipe.id)
        recipe.image = model.get_image(recipe.id)
        recipe.ingredients = model.get_ingredients(recipe.id)
        recipe.allergies = model.get_allergies(recipe.id)

    return render_template('/recipe/view.jinja', recipes=recipes, user=user,
                           pagination=pagination)
