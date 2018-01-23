from flask import Blueprint, request, render_template, url_for, redirect

from dietr.models.recipe import RecipeModel
from dietr.pagination import Pagination

blueprint = Blueprint('recipe', __name__)

model = RecipeModel()


@blueprint.route('/recipes', defaults={
    'page': 1,
    'limit':  20
})
@blueprint.route('/recipes/page/<int:page>/show<int:limit>')
def view(page, limit):
    # Checks if the url doesn't ask for a non-excisting limit
    if limit not in [20, 40, 100]:
        limit = 20
        page = 1

        return redirect(url_for('recipes.view', page=page, limit=limit))

    start = model.lowest_id + (limit * (page - 1))

    recipe_count = model.highest_id - model.lowest_id

    print(model.lowest_id)
    print(recipe_count)

    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recepten/page/{page}/show/{limit}')

    recipes = model.create_list(limit, start)
    user = model.user

    return render_template('/recipes/recepten.html', recipes=recipes, pagination=pagination, user=user)
