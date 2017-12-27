# Router

## Table

- [Routes](#routes)
- [Controllers](#controllers)
  - [Overview](#overview)
    - [Index](#index)
    - [About](#about)
    - [Contact](#contact)
  - [Allergies](#allergies)
    - [View](#view)
    - [Edit](#edit)
  - [Ingredient](#ingredient)
    - [View](#view)
    - [Add](#add)
    - [Edit](#edit)
    - [Delete](#delete)
  - [Pantry](#pantry)
    - [View](#view)
    - [Edit](#edit)
  - [Person](#person)
    - [View](#view)
    - [Add](#add)
    - [Edit](#edit)
    - [Delete](#delete)
  - [People](#people)
  - [Profile](#profile)
  - [Recipe](#recipe)
  - [Recipes](#recipes)
  - [Session](#session)
    - [login](#login)
    - [Logout](#logout)
    - [Join](#join)

## Routes

| URL                            | Controller | Action   | Identifier |
|:------------------------------ |:---------- |:-------- |:---------- |
| `/`                            | overview   | view     | none       |
| `/about`                       | overview   | about    | none       |
| `/contact`                     | overview   | contact  | none       |
| `/allergies`                   | allergies  | view     | none       |
| `/allergies/edit`              | allergies  | edit     | none       |
| `/ingredient/<int:id>`         | ingredient | view     | `id`       |
| `/ingredient/add`              | ingredient | add      | none       |
| `/ingredient/<int:id>/edit`    | ingredient | edit     | `id`       |
| `/ingredient/<int:id>/delete`  | ingredient | delete   | `id`       |
| `/pantry`                      | pantry     | overview | none       |
| `/pantry/add`                  | pantry     | add      | none       |
| `/pantry/<int:id>`             | pantry     | view     | `id`       |
| `/pantry/<int:id>/edit`        | pantry     | edit     | `id`       |
| `/pantry/<int:id>/delete`      | pantry     | delete   | `id`        |
| `/person/<string:name>`        | person     | view     | `name`     |
| `/person/add`                  | person     | view     | `name`     |
| `/person/<string:name>/edit`   | person     | view     | `name`     |
| `/person/<string:name>/delete` | person     | delete   | `name`     |
| `/people`                      | person     | overview | `name`     |
| `/profile`                     | profile    | view     | none       |
| `/profile/edit`                | profile    | edit     | none       |
| `/recipe/<int:id>`             | recipe     | view     | `id`       |
| `/recipes`                     | recipe     | overview | `1`        |
| `/recipes/page/<int:page>`     | recipe     | overview | `page`     |
| `/login`                       | session    | login    | none       |
| `/logout`                      | session    | logout   | none       |
| `/join`                        | session    | join     | none       |

## Controllers

### Overview

#### Index

URL scheme `/`

#### About

URL scheme `/about`

#### Contact

URL scheme `/contact`

### Allergies

#### View

URL scheme `/allergies`

Shows the allergies of the user.

#### Edit

URL scheme `/allergies/edit`

Allows the user to edit their allergies

### Ingredient

#### View

URL scheme `/ingredient/<int:id>`, `/ingredient/<int:id>/`

Will display information for a certain ingredient like certain allergies and
possible diets.

For signed in users it will display if they can consume the item.

#### Add

URL scheme `/ingredient/add`

**Maby don't do this, for testing only.** Add an ingredient.

#### Edit

URL scheme `/ingredient/<int:id>/edit`

**Maby don't do this, for testing only.** Edit an ingredient.

Edit ingredient in the user's pantry.

#### Delete

URL scheme `/ingredient/<int:id>/delete`

**Maby don't do this, for testing only.** Delete an ingredient.

### Pantry

#### View

URL scheme `/pantry`  
Alias `/ingredients`

Show the overview of the ingredient in the user's pantry.

#### Edit

URL scheme `/pantry/edit`  
Alias `/ingredients/edit`

### Person

#### View

URL scheme `/person/<string:name>`

Shows the allergies of a roommate

#### Add

URL scheme `/person/add`

Add a roommate.

#### Edit

URL scheme `/person/<string:name>/edit`

Edit the allergies of a person.

#### Delete

URL scheme `/person/<string:name>/delete`

Delete a roommate.

### People

URL scheme `/people`

Shows an overview of the user's roommates.

### Profile

URL scheme `/profile`

### Recipe

URL scheme `/recipe/<int:id>`

Will display information about a recipe like ingredients and allergies. **It
will not display the steps due to legal issues**. It will instead link to the
source. May be removed in the future.

### Recipes

URL scheme `/recipes` `/recipes/page/<int:page>`

Will show a list of recipes. If a user is logged in it will filter on known diets and _preferences_ of the user.

### Session

#### login

URL scheme `/login`

#### Logout

URL scheme `/logout`

#### Join

URL scheme `/join`

Allows a user to register with this service.

```py
class Router:
    # TODO create a dynamic router
    '''
    The router class is used to encapsulate the routing methods to prevent
    pollution of global namespace.
    '''
    @app.route('/')
    def index():
        pass

    @app.route('/about')
    def about():
        pass

    @app.route('/contact')
    def contact():
        pass

    @app.route('/allergies')
    def allergies():
        pass

    @app.route('/allergies/edit')
    def allergies_edit():
        pass

    @app.route('/ingredient/<int:id>')
    @app.route('/ingredient/<int:id>/<string:name>')
    def ingredient(id, name = None):
        controller  = IngredientController()
        action      = controller.view

        return action(id)

    @app.route('/ingredient/add')
    def ingredient_add():
        controller  = IngredientController()
        action      = controller.add

        return action()

    @app.route('/ingredient/<int:id>/edit')
    @app.route('/ingredient/<int:id>/<string:name>/edit')
    def ingredient_edit(id, name = None):
        controller  = IngredientController()
        action      = controller.edit

        return action(id)

    @app.route('/ingredient/<int:id>/delete')
    @app.route('/ingredient/<int:id>/<string:name>/delete')
    def ingredient_delete(id, name = None):
        controller  = IngredientController()
        action      = controller.delete

        return action(id)

    @app.route('/pantry')
    def pantry():
        pass

    @app.route('/pantry/edit')
    def pantry_edit():
        pass

    @app.route('/person/<string:name>')
    def person(name):
        pass

    @app.route('/person/add')
    def person_add():
        pass

    @app.route('/person/<string:name>/edit')
    def person_edit(name):s
        pass

    @app.route('/person/<string:name>/delete')
    def person_delete(name):
        pass

    @app.route('/people')
    def people():
        pass

    @app.route('/profile')
    def profile():
        pass

    @app.route('/recipe/<int:id>')
    @app.route('/recipe/<int:id>/<string:name>')
    def recipe(id, name = None):
        pass

    @app.route('/recipes', defaults = {
        'page': 1
    })
    @app.route('/recipes/page/<int:page>')
    def recipes(page):
        pass

    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        controller  = SessionController()
        action      = controller.login

        return action()

    @app.route('/logout', methods = ['GET', 'POST'])
    def logout():
        controller  = sx()
        action      = controller.logout

        return action()

    @app.route('/join', methods = ['GET', 'POST'])
    def join():
        controller  = SessionController()
        action      = controller.join

        return action()
```