#Het moet nog wel even wat netter afgewerkt worden, duplicates en nutteloos spul weghalen enzo, maar het werkt, dus het is goed
#
#-Rens en Glenn the Man
from flask import Flask, request
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql=MySQL()

#Dit is lokale server shit. Wordt aangepast naar online server shit wanneer dat een keer beschikbaar is
app.config["MYSQL_DATABASE_USER"]="renswnc266_dietr"
app.config["MYSQL_DATABASE_PASSWORD"]="qvuemzxu"
app.config["MYSQL_DATABASE_DB"]="renswnc266_dietr"
app.config["MYSQL_DATABASE_HOST"]="185.182.57.56"
mysql.init_app(app)

#Hashen moet ook nog een keer gebeuren
def pwdToHash(pw):
    return pw

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@app.route('/user/<ide>', methods=["POST", "GET"])
def user(ide):
    if request.method=="GET":
        html=""
        user=""
        pwd=""
        name=""
        email=""
        if (not isInt(ide)):
            html+="Sorry, deze gebruiker is niet gevonden!"
        else:
            query="select * from account where id="+ide+";"
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(query)
            numrows=cursor.rowcount
            conn.close()
            cursor.close()
            if (numrows>0):
                data=cursor.fetchone()
                name=data[1]
                user=data[2]
                pwd=data[3]
                email=data[4]
                html+="<strong>Hallo, "+name+"</strong><br>"
                html+="<form id='dataForm' method='POST' action='/user/"+ide+"'><table><tr><td>Username: </td><td><input name='uname' 'type='text' value='"+user+"' /></td></tr><tr><td>Current Password: </td><td><input name='curpwd' type='password' value='' /></td></tr><tr><td>New Password: </td><td><input name='newpwd' type='password' value='' /></td></tr><tr><td>Repeat new Password: </td><td><input name='rnewpwd' type='password' value='' /></td></tr><tr><td>E-mail address: </td><td><input name='email' type='text' value='"+email+"' /></td></tr><tr><td><input name='upTable' type='submit' value='Verander data' /></td></tr></table></form>"
            else:
                html+="Sorry, deze gebruiker is niet gevonden!"
    else:
        html=""
        user=""
        pwd=""
        name=""
        email=""
        if (not isInt(ide)):
            html+="Sorry, deze gebruiker is niet gevonden!"
        else:
            query="select * from account where id="+ide+";"
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(query)
            numrows=cursor.rowcount
            conn.close()
            cursor.close()
            if (numrows>0):
                data=cursor.fetchone()
                name=data[1]
                user=data[2]
                pwd=data[3]
                email=data[4]
                if pwd==pwdToHash(request.form["curpwd"]):
                    if len(request.form["newpwd"])>0:
                        if request.form["newpwd"]==request.form["rnewpwd"]:
                            query="update account set username=%s, password=%s, email=%s where id=%s;"
                            data=(request.form["uname"], pwdToHash(request.form["newpwd"]), request.form["email"], ide)
                            conn=mysql.connect()
                            cursor=conn.cursor()
                            cursor.execute(query, data)
                            conn.commit()
                            conn.close()
                            cursor.close()
                            html+="Gegevens succesvol aangepast!<br>"
                        else:
                            html+="Zorg ervoor dat het nieuwe wacthwoord twee keer correct is ingevuld!<br>"
                    else:
                        query="update account set username=%s, email=%s where id=%s;"
                        data= (request.form["uname"], request.form["email"], ide)
                        conn=mysql.connect()
                        cursor=conn.cursor()
                        cursor.execute(query, data)
                        conn.commit()
                        conn.close()
                        cursor.close()
                        html+="Gegevens succesvol aangepast!<br>"
                else:
                    html+="Het wachtwoord is niet correct ingevuld!<br>"
                html+="<strong>Hallo, "+name+"</strong><br>"
                html+="<form id='dataForm' method='POST' action='/user/"+ide+"'><table><tr><td>Username: </td><td><input name='uname' 'type='text' value='"+request.form["uname"]+"' /></td></tr><tr><td>Current Password: </td><td><input name='curpwd' type='password' value='' /></td></tr><tr><td>New Password: </td><td><input name='newpwd' type='password' value='' /></td></tr><tr><td>Repeat new Password: </td><td><input name='rnewpwd' type='password' value='' /></td></tr><tr><td>E-mail address: </td><td><input name='email' type='text' value='"+request.form["email"]+"' /></td></tr><tr><td><input name='upTable' type='submit' value='Verander data' /></td></tr></table></form>"


            else:
                html+="Sorry, deze gebruiker is niet gevonden!"

    return html
