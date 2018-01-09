import os
import pymysql
from sys import exit

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_dietr", use_unicode=True, charset="utf8")
myCursor = conn.cursor()

link = os.listdir("C:\\Users\\Daan Renken\\Pictures\\Images")  # locatie foto's
namen = 'Aardappel-appelhapje met kropsla, ei en ham'  # recept waar een foto bij gezocht moet worden


def database(namen):  # zoeken naar id van het recept

    myCursor.execute("SELECT * FROM recipe WHERE name=%s", namen)
    id = myCursor.fetchall()
    for t in id:
        line = ' '.join(str(x) for x in t)
        recipetid = line.split(' ')[0]
        relatietabel(recipetid)


def relatietabel(recipeid):  # bij het recept de bijbehorende ingredienten id's zoeken
    myCursor.execute("SELECT * FROM recipe_ingredient_relation WHERE recipe_id=%s", recipeid)
    id = myCursor.fetchall()
    for t in id:
        line = ' '.join(str(x) for x in t)
        ingredientid = line.split(' ')[2]
        picture_title(ingredientid)


def picture_title(ingredientid):
    for picture in link:  # opsplitsen en parsen van de namen van de foto's
        title = picture[:-4]
        lowercase_title = str(title.lower())
        myCursor.execute("SELECT * FROM ingredient WHERE name LIKE %s", ("%" + lowercase_title + "%",))  # zoeken van id's die lijken op de foto's
        id = myCursor.fetchall()
        for t in id:
            line = ' '.join(str(x) for x in t)
            fotoid = line.split(' ')[0]
            if ingredientid == fotoid:  # de ingredientenid's en fotoíd's vergelijken
                exit(0)
                return picture


database(namen)
