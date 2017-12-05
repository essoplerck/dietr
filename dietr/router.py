from flask import Flask, request, render_template

from dietr.controllers.ingredient import IngredientController
from dietr.controllers.authentication import AuthenticationController

app = Flask(__name__)
app.config.from_object('config')

class Router:
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

    @app.route('/login')
    def login():
        controller  = AuthenticationController()
        action      = controller.login

        return action()

    @app.route('/logout', methods = ['GET', 'POST'])
    def logout():
        controller  = AuthenticationController()
        action      = controller.logout

        return action()

    @app.route('/join')
    def join():
        controller  = AuthenticationController()
        action      = controller.join

        return action()
