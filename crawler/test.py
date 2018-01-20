import os
import pymysql
from sys import exit

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_production", use_unicode=True, charset="utf8")
myCursor = conn.cursor()

link = os.listdir("C:\\Users\\Daan Renken\\Pictures\\Images")  # locatie foto's

def picture_title():
    foto = 'Zout.png'
    for picture in link:  # opsplitsen en parsen van de namen van de foto's
        title = picture[:-4]
        lowercase_title = str(title.lower())
        myCursor.execute("SELECT * FROM ingredients WHERE name LIKE %s", ("%" + lowercase_title + "%",))  # zoeken van id's die lijken op de foto's
        id = myCursor.fetchall()
        print(title)
        myCursor.execute("""INSERT INTO images(name) VALUES(%s) """, (title))
    conn.commit()
    conn.close
picture_title()

