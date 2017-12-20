from flask import request

from .. import app
from ..models.session import SessionModel

class SessionController:
    '''Controller for the authentication pages. This controller will contain
    actions for all routes.
    '''
    def __init__(self):
        # Get the model for the ingredient pages
        self.model = SessionModel()

    def join(self):
        pass

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            pass

        pass

    def logout(self):
        pass

controller = SessionController()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return controller.login()

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    return controller.logout()

@app.route('/join', methods = ['GET', 'POST'])
def join():
    return controller.join()
