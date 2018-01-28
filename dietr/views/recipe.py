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

        return redirect(url_for('recipes.view', page=page, limit=limit))

    user = model.user
    start = limit * (page - 1)
    recipe_count = model.get_recipe_count(model.user_allergies)

    #Add pagination
    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recepten/page/{page}/show{limit}')

    recipes = model.get_recipe(model.user_allergies, start, limit)

    #Add information
    for recipe in recipes:

        # Add the source of the recipe
        recipe.source = recipe.get_source

        #Add the extra information
        recipe.extra_info = model.get_extra_info(recipe.id)

        #Add the image
        recipe.image = model.get_image(recipe.id)

        #Add all the ingredients contained in the recipe
        recipe.ingredients = model.get_ingredients(recipe.id)

        # Add all the allergens contained in the ingredients
        for ingredient in recipe.ingredients:
            allergens = model.get_allergies(ingredient.id)
            if allergens:
                recipe.allergies += allergens

    return render_template('/recipe/view.jinja', recipes=recipes, user=user,
                           pagination=pagination)
