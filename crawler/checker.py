import pymysql
import inserter

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
mycursor = conn.cursor()


def checkrecipe(database, naam, url):
    mycursor.execute("SELECT * FROM "+database+" WHERE name=%s ;", naam)  # zoeken naar een variabele in een variabele database
    id = mycursor.fetchall()
    if id:
        for t in id:
            line = ' '.join(str(x) for x in t)
        return line.split(' ')[0]  # als er een id wordt gevonden stuur deze terug
    else:
        return inserter.insertrecipe(database, naam, url)  # als er geen id wordt gevonden voeg deze dan toe aan de database


def check(database, naam):
    mycursor.execute("SELECT * FROM "+database+" WHERE name=%s;", naam)  # zoeken naar een variabele in een variabele database
    id = mycursor.fetchall()

    if id:
        for t in id:
            line = ' '.join(str(x) for x in t)
        return line.split(' ')[0]  # als er een id wordt gevonden stuur deze terug
    else:
        return inserter.insert(database, naam)  # als er geen id wordt gevonden voeg deze dan toe aan de database


def checkrelatie(database, tabel1, tabel2, id1, id2):
    mycursor.conn.cursor()
    mycursor.execute("SELECT * FROM  "+database+"  WHERE %s=%s AND %s=%s;", (tabel1, id1, tabel2, id2))
    id = mycursor.fetchall()
    if not id:  # controleer of de relatie als bestaat zo niet voeg deze toe
        inserter.relatietabel(database, tabel1, tabel2, id1, id2)
    mycursor.close()
