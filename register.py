from flask import Flask, request
from flaskext.mysql import MySQL
#from flask_mail import Mail, Message
import random
app = Flask(__name__)
mysql=MySQL()

#Dit is lokale server shit. Wordt aangepast naar online server shit wanneer dat een keer beschikbaar is
app.config["MYSQL_DATABASE_USER"]="renswnc266_dietr"
app.config["MYSQL_DATABASE_PASSWORD"]="qvuemzxu"
app.config["MYSQL_DATABASE_DB"]="renswnc266_dietr"
app.config["MYSQL_DATABASE_HOST"]="185.182.57.56"
#app.config["MAIL_SERVER"]="mail.axc.nl"
#app.config["MAIL_PORT"]=465
mysql.init_app(app)

def exec_query(query, values):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    cursor.close()

@app.route('/register', methods=["POST", "GET"])
def register():
    html=""
    if request.method=="GET":
        html+="<form id='dataForm' method='POST' action='/register'><table><tr><td>Name: </td><td><input name='name' type='text' value='' /></td></tr><tr><td>Username: </td><td><input name='uname' type='text' value='' /></td></tr><tr><td>Password: </td><td><input name='pwd' type='password' value='' /></td></tr><tr><td>Confirm password: </td><td><input name='rpwd' type='password' value='' /></td></tr><tr><td>E-mailaddress: </td><td><input name='email' type='text' value='' /></td></tr><tr><td><input name='reg' type='submit' value='Registreer' /></td></tr></table></form>"
    else:
        name=request.form["name"]
        uname=request.form["uname"]
        pwd=request.form["pwd"]
        rpwd=request.form["rpwd"]
        email=request.form["email"]
        if pwd==rpwd or len(pwd)<8:
            key=""
            for val in range(7):
                key=key+chr(65+random.randint(0,25))
            data=(name, uname, pwd, email, key)
            query="insert into account (name, username, password, email, confirm_key) values (%s, %s, %s, %s, %s);"
            exec_query(query, data)
#            email=Mail()
#            email.init_app(app)
#            msg=Message("Hallo!", sender="rs.wolters68@gmail.com", recipients=[email])
#            msg.body="Bedankt voor registreren. Je bevestigingskey is: "+key+" -DietR"
#            email.send(msg)
            html+="Account succesvol aangemaakt! Check je mail voor je key!"
        else:
            html+="Je wachtwoorden zijn niet correct. Probeer opnieuw.<br>"
            html+="<form id='dataForm' method='POST' action='/register'><table><tr><td>Name: </td><td><input name='name' type='text' value='' /></td></tr><tr><td>Username: </td><td><input name='uname' type='text' value='' /></td></tr><tr><td>Password: </td><td><input name='pwd' type='password' value='' /></td></tr><tr><td>Confirm password: </td><td><input name='rpwd' type='password' value='' /></td></tr><tr><td>E-mailaddress: </td><td><input name='email' type='text' value='' /></td></tr><tr><td><input name='reg' type='submit' value='Registreer' /></td></tr></table></form>"

    return html
