import os
import pymysql
from sys import exit

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_production", use_unicode=True, charset="utf8")
myCursor = conn.cursor()


def relatietabel(counter):  # bij het recept de bijbehorende ingredienten id's zoeken

    i = counter*100+70
    max = (counter+1)*100
    while i <= max:
        myCursor.execute("SELECT * FROM recipes_ingredients WHERE recipe_id=%s", i)
        id = myCursor.fetchall()
        for t in id:
            line = ' '.join(str(x) for x in t)
            ingredientid = line.split(' ')[2]
            #  print('ingredientid ' + ingredientid)
            picture_title(ingredientid, i)
        i += 1
    conn.commit()
    conn.close()

def picture_title(ingredientid, i):
    myCursor.execute("SELECT ID from images ORDER BY id DESC LIMIT 1")
    row = myCursor.fetchall()
    foto = ' '
    if row:
        for t in row:
            line = ' '.join(str(x) for x in t)
            max = int(line.split(' ')[0])
    x = 0
    while x <= max:
        x += 1
        myCursor.execute("SELECT * FROM images WHERE id = %s", x)
        name = myCursor.fetchall()
        for t in name:
            line = ' '.join(str(x) for x in t)
            lowercase_title = line.split(' ')[1]
        myCursor.execute("SELECT * FROM ingredients WHERE name LIKE %s", ("%" + lowercase_title + "%",))  # zoeken van id's die lijken op de foto's
        id = myCursor.fetchall()
        for t in id:
            line = ' '.join(str(x) for x in t)
            fotoid = line.split(' ')[0]
            if ingredientid == fotoid:  # de ingredientenid's en fotoíd's vergelijken
                #print(lowercase_title)
                foto = lowercase_title
                #print('foto ' + picture)


    myCursor.execute("SELECT * FROM images WHERE name=%s", (foto))
    row = myCursor.fetchall()
    if row:
        for t in row:
            line = ' '.join(str(x) for x in t)
            image_id = int(line.split(' ')[0])
            print(foto)
            print(image_id)
            print(i)
            myCursor.execute("""UPDATE recipes SET image_id = %s WHERE id = %s """, (image_id, i))
            conn.commit()


def start(i):
    while True:
        try:
            relatietabel(i)
            break
        except Exception as e:
            print('Something went wrong: ' + repr(e) + 'starting over...')
            relatietabel(i)
