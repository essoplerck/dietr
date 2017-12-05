from flask import render_template, request

from dietr.models.authentication import AuthenticationModel

class AuthenticationController:
    def join(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

    def __init__(self):
        self.model = AuthenticationModel()
