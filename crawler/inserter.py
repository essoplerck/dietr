import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_staging", use_unicode=True, charset="utf8")



def insertrecipe(database, naam, url):
    mycursor = conn.cursor()
    print('insert')
    print(database)
    mycursor.execute("INSERT INTO "+database+"(name,url) VALUES(%s,%s)", (naam, url))
    conn.commit()
    mycursor.close()
    return mycursor.lastrowid


def insert(database, naam):
    mycursor = conn.cursor()
    print('insert')
    print(database)
    mycursor.execute("INSERT INTO  "+database+"(name) VALUES(%s) ", naam)
    conn.commit()
    mycursor.close()
    return mycursor.lastrowid


def relatietabel(database, tabel1, tabel2, id1, id2):
    mycursor = conn.cursor()
    #print(tabel1)
    mycursor.execute("SELECT * FROM  "+database+"  WHERE %s=%s AND %s=%s;", (tabel1, id1, tabel2, id2))
    id = mycursor.fetchall()
    print(database)
    print(tabel1)
    print(tabel2)
    if not id:
        #print(tabel2)
        query = "INSERT INTO "+str(database)+"("+str(tabel1)+","+str(tabel2)+") VALUES("+str(id1)+","+str(id2)+") "
        print(query)
        mycursor.execute(query)
        #print('nieuwe relatie')
    #else:
        #print('oude relatie')
    conn.commit()
    mycursor.close()
