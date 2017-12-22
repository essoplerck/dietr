from flask import request

from .. import app
from ..models.session import SessionModel

model = SessionModel()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        pass

    pass

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    pass

@app.route('/join', methods = ['GET', 'POST'])
def join():
    pass
