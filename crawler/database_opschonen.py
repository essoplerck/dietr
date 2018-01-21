import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_production", use_unicode=True, charset="utf8")
myCursor = conn.cursor()


def opschonen():
    myCursor.execute("SELECT ID from recipes_ingredients ORDER BY id DESC LIMIT 1")
    row = myCursor.fetchall()
    if row:
        for t in row:
            line = ' '.join(str(x) for x in t)
            max = int(line.split(' ')[0])
    i = 1
    while i <= max:
        myCursor.execute("SELECT * FROM recipes_ingredients WHERE recipe_id=%s;", (i))
        id = myCursor.fetchall()

        if id:
            for t in id:
                line = ' '.join(str(x) for x in t)
                lastrecipeid = line.split(' ')[0]
        else:
            myCursor.execute("DELETE FROM recipe WHERE id=%s;", (i))
            print(i)
        i += 1
    conn.commit()
    conn.close()
    print("updated")


def start():
    while True:
        try:
            opschonen()
            break
        except Exception as e:
            print('Something went wrong: ' + repr(e) + 'starting over...')
            opschonen()
