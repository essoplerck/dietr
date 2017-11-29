# Router

## Table of Contents

## Routes

| URL                       | Controller  | Action  | Identifier          |
|:--------------------------|:------------|:--------|:--------------------|
| `/`                       | overview    | view    | none                |
| `/about`                  |
| `/contact`                |
| `/diet/<string:name>`     | diet        | view    | `<string:name>`     |
| `/diets`                  | diets       | view    | none                |
| `/ingredient/<int:id>`    | ingredient  | view    | `<int:id>`          |
| `/ingredients`            | ingredients | view    | none                |
| `/recipe/<int:id>`        | recipe      | view    | `<int:id>`          |
| `/recipes`                | recipes     | view    | none                |
| `/user/<string:username>` | user        | view    | `<string:username>` |
| `/users`                  | users       | view    | `1`                 |
| `/users/page/<int:page>`  | users       | view    | `<int:page>`        |
| `/login`                  | sessions    | login   | none                |
| `/logout`                 | sessions    | logout  | none                |
| `/register`               | sessions    | regiser | none                |

## Controllers

### Overview

URL scheme `/`

## About

URL scheme `/about`

## Contact

URL scheme `/contact`

### Diet

URL scheme `/diet/<string:name>`

### Diets

URL scheme `/diets`

### Ingredient

URL scheme `/ingredient/<int:id>`

Will display information for a certain ingredient like certain allergies and possible diets.

For signed in users it will display if they can consume the item.

### Ingredients

URL scheme `/ingredients`  
Alias `/pantry`

Shows a list of popular ingredients.

### Recipe

URL scheme `/recipe/<int:id>`

Will display information about a recipe like ingredients and avalible diets. **It will not display the steps due to legal issues**. It will instead link to the source.

## Recipes

URL scheme `/recipes`

Will show a list of recipes. If a user is logged in it will filter on known diets and _preferences_ of the user.

## User

URL scheme `/user/<string:username>/`

## Users

URL scheme `/users`, `/users/page/<int:page>`

```py
class Router:
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

    @app.route('/diet/<string:name>')
    def diet(name):
        pass

    @app.route('/diets')
    def diets():
        pass

    @app.route('/ingredient/<int:id>')
    def ingredient(id, name = None):
        pass

    @app.route('/ingredients')
    def ingredients():
        pass

    @app.route('/recipe/<int:id>')
    def recipe(id, name = None):
        pass

    @app.route('/recipes')
    def recipes():
        pass

    @app.route('/profile')
    def profile():
        pass

    @app.route('/user/<string:username>')
    def user(username):
        pass

    @app.route('/users', defaults = {
        'page': 1
    })
    @app.route('/users/page/<int:page>')
    def users(page):
        pass
```
