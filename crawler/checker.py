import pymysql
import inserter

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
mycursor = conn.cursor()


def checkrecipe(database, naam, url):
    #print(database)
    #print(naam)
    mycursor.execute("SELECT * FROM "+database+" WHERE name=%s ;", naam)
    id = mycursor.fetchall()
    #print(id)
    if id:
        for t in id:
            line = ' '.join(str(x) for x in t)
        return line.split(' ')[0]
    else:
        return inserter.insertrecipe(database, naam, url)


def check(database, naam):
    mycursor.execute("SELECT * FROM "+database+" WHERE name=%s;", naam)
    id = mycursor.fetchall()

    if id:
        for t in id:
            line = ' '.join(str(x) for x in t)
        return line.split(' ')[0]
    else:
        return inserter.insert(database, naam)
