from flask import Flask, request, render_template

from dietr.controllers.ingredient import IngredientController
from dietr.controllers.session import SessionController

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
        controller  = SessionController()
        action      = controller.login

        return action()

    @app.route('/logout', methods = ['GET', 'POST'])
    def logout():
        controller  = SessionController()
        action      = controller.logout

        return action()

    @app.route('/join')
    def join():
        controller  = SessionController()
        action      = controller.join

        return action()
