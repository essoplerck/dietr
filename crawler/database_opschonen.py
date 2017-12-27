import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
myCursor = conn.cursor()


def allergeen(allergeen):

    myCursor.execute("""INSERT INTO category(name) VALUES(%s) """, allergeen)
    allergeenid = myCursor.lastrowid
    myCursor.execute("SELECT * FROM category WHERE name LIKE %s", ("%" + allergeen + "%",))
    id = myCursor.fetchall()
    for t in id:
        line = ' '.join(str(x) for x in t)
        idallergeen = line.split(' ')[0]
        print(idallergeen)
        category_ingredient_relation(idallergeen,allergeenid)
    conn.commit()
    conn.close()
    print("updated")



def category_ingredient_relation(idallergeen,allergeenid):
    myCursor.execute("UPDATE category_ingredient_relation SET category_id=%s WHERE category_id=%s",(allergeenid,idallergeen))






allergeen('Zout')
