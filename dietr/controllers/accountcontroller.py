from flask import render_template
from ..models.accountmodel import AccountModel

class AccountController:
    #The account controller. Links the model with the view.
    acc=""
    def __init__(self):
        acc=AccountModel()
        pass

    def add_account(name, username, password, confirm_password, email):
        data=[0, 0, 0, 0, 0]
        if len(name.split(" "))==0:
            data[0]=1
            data[1]=1
        elif name[0]==" ":
            data=[0]=1
        elif name[len(name)-1]==" ":
            data[1]=1

        if len(password)<8 or len(password)>20:
            data[2]=1
        else:
            lets=0
            nums=0
            chars=0
            for char in password:
                if char.isdigit():
                    nums+=1
                elif char.isalpha():
                    lets+=1
                else:
                    chars+=1
            if lets==0 or nums==0 or chars==0:
                data[2]=1
        if not (password==confirm_password):
            data[3]=1

        if len(email.split(" "))==0 or len(email.split("@"))!=2 or len(email.split("."))<2:
            data[4]=1

        noerrors=1
        for error in data:
            if error==1:
                noerrors=0

        if noerrors==1:
            key=""
            for val in range(7):
                key=key+chr(65+random.randint(0,25))

            acc.add_account(name, username, password, email, key)

            return render_template("Account_activeren.html", mail=email)

        return render_template("Registreren.html", errors=data)

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
        account={"name": data[1], "username": data[2], "email": data[4]}
        persons=acc.get+persons(ide)
        return render_template("user.html", account=account, persons=persons)

    def edit_account(name, username, password, email, ide):
        data=acc.update_account(username, password, email, ide)
        persons=acc.get+persons(ide)
        return render_template("user.html", account=data, persons=persons)

    def edit_account(name, username, email, ide):
        data=acc.update_account(name, username, email, ide)
        persons=acc.get+persons(ide)
        return render_template("user.html", account=data, persons=persons)
