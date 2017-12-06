from flask import Flask

from dietr import app
from dietr.controllers.ingredient import IngredientController
from dietr.controllers.session import SessionController

class Router:
    # TODO create a dynamic router
    '''
    The router class is used to encapsulate the routing methods to prevent
    pollution of global namespace.
    '''
    @app.route('/')
    def index():
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

    @app.route('/ingredients/overview')
    def ingredient_overview():
        controller  = IngredientController()
        action      = controller.overview

        return action()

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
