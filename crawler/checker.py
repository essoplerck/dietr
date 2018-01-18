import pymysql
import inserter

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_staging", use_unicode=True, charset="utf8")
mycursor = conn.cursor()


def checkrecipe(database, naam, url):
    #print(database)
    print(naam)
    mycursor.execute("SELECT * FROM "+database+" WHERE url=%s ;", url)
    id = mycursor.fetchall()
    #print(id)
    if not id == None:
        for t in id:
            line = ' '.join(str(x) for x in t)
        print('ken ik al')
        return line.split(' ')[0]
    else:
        inserter.insertrecipe(database, naam, url)


def check(database, naam):
    mycursor.execute("SELECT * FROM "+database+" WHERE name=%s;", naam)
    id = mycursor.fetchall()
    print(naam)
    if not id == None:
        for t in id:
            line = ' '.join(str(x) for x in t)
        print('ken ik al')
        return line.split(' ')[0]
    else:
        inserter.insert(database, naam)

def allergycheck(database, naam):
    mycursor.execute("SELECT * FROM "+database+" WHERE name LIKE %s;", naam)
    id = mycursor.fetchall()
    print(naam)
    if not id == None:
        for t in id:
            line = ' '.join(str(x) for x in t)
        print('ken ik al')
        return line.split(' ')[0]
    else:
        inserter.insert(database, naam)
