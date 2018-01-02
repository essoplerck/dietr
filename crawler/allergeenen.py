import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
myCursor = conn.cursor()


def allergeen(allergeen):

    myCursor.execute("SELECT * FROM category WHERE name LIKE %s", ("%" + allergeen + "%",))
    id = myCursor.fetchall()
    for t in id:
        line = ' '.join(str(x) for x in t)
        idallergeen = line.split(' ')[0]
        category_ingredient_relation(idallergeen)


def category_ingredient_relation(idallergeen):
    myCursor.execute("SELECT * FROM category_ingredient_relation WHERE category_id=%s", idallergeen)
    id = myCursor.fetchall()

    for t in id:
        line = ' '.join(str(x) for x in t)
        idproduct=line.split(' ')[-1]
        recipe_ingredient_relation(idproduct)


def recipe_ingredient_relation(idproduct):
    myCursor.execute("SELECT * FROM recipe_ingredient_relation WHERE recipe_id=%s", idproduct)
    id = myCursor.fetchall()
    for t in id:
        line = ' '.join(str(x) for x in t)
        idrecept = line.split(' ')[-1]
        recept(idrecept)


def recept(idrecept):
    myCursor.execute("SELECT * FROM recipe WHERE id=%s", idrecept)
    id = myCursor.fetchall()
    for t in id:
        line = ' '.join(str(x) for x in t)
        naam = line.split(' ')[1: -1]
        naam = ' '.join(str(y) for y in naam)
        print(naam)


allergeen('')
