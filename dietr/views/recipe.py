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
    #Checks if the url doesn't ask for a non-excisting limit
    if limit != 100 and limit != 40 and limit != 20:
        limit = 20
        page = 1

        return redirect('/recepten/')

    start = model.lowest_id + (limit * (page - 1))

    recipe_count = model.highest_id - model.lowest_id

    print(model.lowest_id)
    print(recipe_count)

    pagination = Pagination(page, limit, recipe_count)

    #Checks if the url doesn't ask for a non-excisting page and redirects to the last page
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recepten/page/{page}/show/{limit}')

    recipes = model.create_list(limit, start)
    user = model.user

    return render_template('/recipes/recepten.html', recipes=recipes, pagination=pagination, user=user)
