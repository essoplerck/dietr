import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_dietr", use_unicode=True, charset="utf8")


def insertrecipe(database, naam, url):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO "+database+"(name,url) VALUES(%s,%s)", (naam, url))
    mycursor.close()
    return mycursor.lastrowid  # retrun id voor de relatietabel


def insert(database, naam):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO  "+database+"(name) VALUES(%s) ", naam)
    mycursor.close()
    return mycursor.lastrowid  # retrun id voor de relatietabel


def relatietabel(database, tabel1, tabel2, id1, id2):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO "+database+"("+tabel1+","+tabel2+") VALUES(%s,%s) ", (id1, id2))
    mycursor.close()
