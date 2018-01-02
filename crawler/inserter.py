import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
mycursor = conn.cursor()


def insertrecipe(database, naam, url):
    mycursor.execute("""INSERT INTO %s(name,url) VALUES(%s,%s) """, (database, naam, url))


def insert(database, naam):
    mycursor.execute("""INSERT INTO %s(name) VALUES(%s) """, (database, naam))


def relatietabel(naam, tabel1, tabel2, id1, id2):

    mycursor.execute("SELECT * FROM %s WHERE %s=%s AND %s=%s;", (id1, id2))
    id = mycursor.fetchall()
    if not id:
        mycursor.execute("""INSERT INTO %s(%s,%s) VALUES(%s,%s) """, (naam, tabel1, tabel2, id1, id2))
