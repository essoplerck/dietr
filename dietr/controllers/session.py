from flask import render_template, request

from ..models.session import SessionModel

class SessionController:
    def join(self):
        pass

    def login(self):
        if request.method == 'GET':
            username = request.form['username']
            password = request.form['password']

            pass

        pass

    def logout(self):
        pass

    def __init__(self):
        self.model = SessionModel()
