import pymysql
import inserter

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
mycursor = conn.cursor()


def checkrecipe(database, naam, url):
    mycursor.execute("SELECT * FROM %s WHERE name=%s;", (database,naam))
    id = mycursor.fetchall()

    if id:
        for t in id:
            line = ' '.join(str(x) for x in t)
        return line.split(' ')[0]
    else:
        inserter.insertrecipe(database, naam, url)
        return mycursor.lastrowid

def check(database, naam):
    mycursor.execute("SELECT * FROM %s WHERE name=%s;", (database,naam))
    id = mycursor.fetchall()

    if id:
        for t in id:
            line = ' '.join(str(x) for x in t)
        return line.split(' ')[0]
    else:
        inserter.insert(database, naam)
        return mycursor.lastrowid
