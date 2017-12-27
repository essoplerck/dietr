import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
myCursor = conn.cursor()


def allergeen(max):

    i=1
    while i<150:
        myCursor.execute("SELECT * FROM recipe_ingredient_relation WHERE recipe_id=%s;", (i))
        id = myCursor.fetchall()

        if id:
            for t in id:
                line = ' '.join(str(x) for x in t)
                lastrecipeid = line.split(' ')[0]
        else:
            myCursor.execute("""DELETE From recipe WHERE id Like '%s' """ %id)
            #myCursor.execute("""DELETE FROM recipe WHERE id LIKE %s""", (id))
            print(i)
        i+=1
    conn.commit()
    conn.close()
    print("updated")

allergeen(19317)
