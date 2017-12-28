from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/hello')
def hello():
    return 'Hello, world!\n'
