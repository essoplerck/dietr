from flask import request

from ..models.session import SessionModel

class SessionController:
    '''Controller for the authentication pages. This controller will contain
    actions for all routes.
    '''
    def __init__(self):
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
