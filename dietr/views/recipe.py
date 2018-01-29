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
        limit = 20
        page = 1

        return redirect(url_for('recipe.view', page=page, limit=limit))

    user_id = session['user']
    user = model.user.get_user(user_id)
    start = limit * (page - 1)
    sort = Order(1)

    #Get the user's information
    user.allergies = model.user.get_allergies(user.id)
    user.preferences = model.user.get_preferences(user.id)
    user.roommates = model.roommate.get_roommates(user.id)
    all_allergies = [allergy.id for allergy in user.allergies]

    checked_roommates = []
    course = []
    diet = []
    if request.method == 'POST':
        if request.form.get('sort'):
            sort = Order(request.form.get('sort'))
            print(sort)
        if user.roommates:
            for roommate in user.roommates:
                if request.form.get('roommate_' + str(roommate.id)):
                    #roommate.preferences = model.roommate.get_preferences(roommate.id)
                    checked_roommates.append(roommate.id)
                    roommate.allergies = model.roommate.get_allergies(roommate.id)
                    all_allergies += [allergy.id for allergy in roommate.allergies]

        if request.form.get('course_3'):
            course.append(3)
        if request.form.get('course_4'):
            course.append(4)
        if request.form.get('course_5'):
            course.append(5)
        if request.form.get('diet_6'):
            diet.append(6)
        if request.form.get('diet_7'):
            diet.append(7)

    all_allergies = tuple(all_allergies) if all_allergies else None
    course = tuple(course) if course else None
    diet = tuple(diet) if diet else None

    recipe_count = model.recipe.get_recipe_count(all_allergies, course, diet)

    # Add pagination
    pagination = Pagination(page, limit, recipe_count)

    # Check if page exits
    if page > pagination.pages:
        page = pagination.pages

        return redirect(f'/recipes/page/{page}/show{limit}')


    recipes = model.recipe.get_recipes(start, limit, all_allergies, course, diet, sort)

    # Add information to the recipes
    for recipe in recipes:

        recipe.source = recipe.get_source
        recipe.extra_info = model.recipe.get_extra_info(recipe.id)
        recipe.ingredients = model.recipe.get_ingredients(recipe.id)
        recipe.allergies = model.recipe.get_allergies(recipe.id)

    return render_template('/recipe/view.jinja', recipes=recipes, user=user,
                           pagination=pagination, checked_roommates=checked_roommates, course=course, diet=diet, sort=sort)
