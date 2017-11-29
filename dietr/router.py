from flask import Flask, request, render_template

app = Flask(__name__)

class Router:
    '''
    The router class is used to encapsulate the routing methods to prevent
    pollution of global namespace.
    '''
    @app.route('/')
    def index():
        return render_template('dashboard.html')
