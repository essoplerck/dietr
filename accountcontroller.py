from flask import render_template
from . import AccountModel

class AccountController:
    #The account controller. Links the model with the view.
    acc=""
    def __init__(self):
        acc=AccountModel()

    def add_account(name, username, password, email):
        key=""
        for val in range(7):
            key=key+chr(65+random.randint(0,25))

        acc.add_account(name, username, password, email, key)

        return render_template("registered.html", mail=email)

    def login(email, password):
        data=acc.get_account(email, password)
        if len(data)>0:
            return render_template("user.html", account=data)
        return render_template("login.html")

    def get_password(email, username):
        data=acc.get_password(email, username)
        if len(data)>0:
            return render_template("showpassword.html" account=data)
        return render_template("404.html")

    def view_account(ide):
        data=acc.get_account(ide)
        return render_template("user.html", account=data)

    def edit_account(name, username, password, email, ide):
        data=acc.update_account(username, password, email, ide)
        return render_template("user.html", account=data)

    def edit_account(name, username, email, ide):
        data=acc.update_account(name, username, email, ide)
        return render_template("user.html", account=data)
