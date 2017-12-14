from flask import Flask, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql=MySQL()

app.config["MYSQL_DATABASE_USER"]="renswnc266_dietr"
app.config["MYSQL_DATABASE_PASSWORD"]="qvuemzxu"
app.config["MYSQL_DATABASE_DB"]="renswnc266_dietr"
app.config["MYSQL_DATABASE_HOST"]="185.182.57.56"
mysql.init_app(app)

@app.route('/login', methods=["POST", "GET"])
def login():
    html=""
    if request.method=="GET":
        html+="<form id='loginForm' method='POST' action='/login'><table><tr><td>E-mailaddress: </td><td><input name='email' type='text' value='' /></td></tr><tr><td>Password: </td><td><input name='pwd' type='password' value='' /></td></tr><tr><td><input name='log' type='submit' value='Log in' /></td><td><input name='log' type='submit' value='Wachtwoord vergeten?'</tr></table></form>"
    else:
        if request.form["log"]=="Log in":
            email=request.form["email"]
            pwd=request.form["pwd"]
            conn=mysql.connect()
            cursor=conn.cursor()
            query="select * from account where email=%s and password=%s"
            data=(email, pwd)
            if cursor.execute(query, data)>0:
                userdata=cursor.fetchone()
                html+="Login succesvol! Welkom, "+userdata[1]+"."
            else:
                html+="Login gefaald."
        elif request.form["log"]=="Wachtwoord vergeten?":
            html+="Vul je e-mailadres en gebruikersnaam in:<br><form id='pwdForm' method='POST' action='/login'><table><tr><td>E-mailaddress: </td><td><input name='email' type='text' value='' /></td></tr><tr><td>Username: </td><td><input name='uname' type='text' value='' /></td></tr><tr><td><input name='log' type='submit' value='Geef wachtwoord' /></td></tr></table></form>"
        elif request.form["log"]=="Geef wachtwoord":
            email=request.form["email"]
            uname=request.form["uname"]
            conn=mysql.connect()
            cursor=conn.cursor()
            query="select * from account where email=%s and username=%s"
            data=(email, uname)
            if cursor.execute(query, data)>0:
                userdata=cursor.fetchone()
                html+="Het wachtwoord van "+uname+" is: "+userdata[3]+"<br>"
            else:
                html+="Sorry, deze gebruiker is niet gevonden!<br>"
            html+="<form id='goBack' method='GET' action='/login'><input name='log' type='submit' value='Ga terug' /></form>"
    return html
