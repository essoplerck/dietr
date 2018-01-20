import os
import pymysql
from sys import exit

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_production", use_unicode=True, charset="utf8")
myCursor = conn.cursor()

link = os.listdir("C:\\Users\\Daan Renken\\Pictures\\Images")  # locatie foto's


def relatietabel():  # bij het recept de bijbehorende ingredienten id's zoeken
    myCursor.execute("SELECT ID from recipes ORDER BY id DESC LIMIT 1")
    row = myCursor.fetchall()
    if row:
        for t in row:
            line = ' '.join(str(x) for x in t)
            max = int(line.split(' ')[0])
    i = 1
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
    foto = ' '
    for picture in link:  # opsplitsen en parsen van de namen van de foto's
        title = picture[:-4]
        lowercase_title = str(title.lower())
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
    
relatietabel()
