import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")



def insertrecipe(database, naam, url):
    mycursor = conn.cursor()
    #print('insert')
    mycursor.execute("INSERT INTO "+database+"(name,url) VALUES(%s,%s)", (naam, url))
    mycursor.close()
    return mycursor.lastrowid


def insert(database, naam):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO  "+database+"(name) VALUES(%s) ", naam)
    mycursor.close()
    return mycursor.lastrowid


def relatietabel(database, tabel1, tabel2, id1, id2):
    mycursor = conn.cursor()
    #print(tabel1)

    mycursor.execute("SELECT * FROM  "+database+"  WHERE %s=%s AND %s=%s;", (tabel1, id1, tabel2, id2))
    id = mycursor.fetchall()

    if not id:
        #print(tabel2)
        mycursor.execute("INSERT INTO "+database+"("+tabel1+","+tabel2+") VALUES(%s,%s) ", (id1, id2))
        #print('nieuwe relatie')
    #else:
        #print('oude relatie')
    mycursor.close()
