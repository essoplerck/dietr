from . import app
from .controllers.ingredient import IngredientController
from .controllers.session import SessionController

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
    def person_edit(name):
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
        controller  = SessionController()
        action      = controller.logout

        return action()

    @app.route('/join', methods = ['GET', 'POST'])
    def join():
        controller  = SessionController()
        action      = controller.join

        return action()
