import pymysql
import requests

from time import sleep
from bs4 import BeautifulSoup

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_production", use_unicode=True, charset="utf8")
myCursor = conn.cursor()


def receptenspider(begin, eind, wait):
    i = begin
    while i <= eind:
        url = 'https://www.jumbo.com/recepten?PageNumber='+str(i)
        sourcecode = requests.get(url)
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        for section in soup.findAll('h3', {'data-jum-action': 'ellipsis'}):
            for link in section.findAll('a'):
                receptenurl = link.get('href')
                recepten = link.text
                print('recept >'+recepten+'<')

                myCursor.execute("SELECT * FROM recipes WHERE url=%s;",(receptenurl))
                id=myCursor.fetchall()

            if id:
                for t in id:
                    line=' '.join(str(x) for x in t)
                lastrecipeid=line.split(' ')[0]
                #print('oud recept')

            else:
                myCursor.execute("""INSERT INTO recipes(name,url) VALUES(%s,%s) """, (recepten, receptenurl))
                lastrecipeid = myCursor.lastrowid
                #print('nieuw recept')
            productenspider(receptenurl, lastrecipeid)
            sleep(wait)
            #print('')
        i += 1
        print(i)

    conn.commit()
    conn.close()
    print(" > data inserted ")


def productenspider(url, lastrecipeid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for ingredienten in soup.findAll('input', {'type': 'checkbox'}):
        producten = ingredienten.get('data-jum-product-add')
        producten = producten.split('"')[3]
        #  print('product ' + producten)
        productenurl = 'https://www.jumbo.com/zoeken?SearchTerm=' + str(producten) + '&search=search='
        myCursor.execute("SELECT * FROM ingredients WHERE name=%s;", producten)
        id=myCursor.fetchall()
        if id:
            for t in id:
                line = ' '.join(str(x) for x in t)
            lastproductid = line.split(' ')[0]
            print('oud product ' + producten)
        else:
            myCursor.execute("""INSERT INTO ingredients(name) VALUES(%s) """, producten)
            lastproductid = myCursor.lastrowid
            print('nieuw product ' + producten)
        recept_product_relatietabel(lastrecipeid, lastproductid)
        allergiespider(productenurl, lastproductid)
        sleep(1)
        conn.commit()


def allergiespider(url, lastproductid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for div in soup.findAll('div', {'class': 'jum-product-allergy-info jum-product-info-item'}):
        for li in div.findAll('li'):
            allergie = li.text
            allergie = allergie.split()[-1]
            myCursor.execute("SELECT * FROM allergies WHERE name like %s;", allergie)
            id=myCursor.fetchall()
            if id:
                for t in id:
                    line = ' '.join(str(x) for x in t)
                lastallergieid = line.split(' ')[0]
                print(lastallergieid)
                print('oud allergeen ' + allergie)
                product_allergie_relatietabel(lastproductid, lastallergieid)
            else:
                myCursor.execute("""INSERT INTO temp_allergies(name) VALUES(%s) """, allergie)
                lastallergieid = myCursor.lastrowid
                product_allergie_temp_relatietabel(lastproductid, lastallergieid)
                print('nieuw allergeen ' + allergie)


def recept_product_relatietabel(lastrecipeid, lastproductid):
    myCursor.execute("SELECT * FROM recipes_ingredients WHERE recipe_id=%s AND ingredient_id=%s;", (lastrecipeid, lastproductid))
    id = myCursor.fetchall()

    if not id:
        myCursor.execute("""INSERT INTO recipes_ingredients(recipe_id,ingredient_id) VALUES(%s,%s) """, (lastrecipeid, lastproductid))


def product_allergie_relatietabel(lastproductid, lastallergieid):
    myCursor.execute("SELECT * FROM allergies_ingredients WHERE ingredient_id=%s AND allergy_id=%s;", (lastproductid, lastallergieid))
    id = myCursor.fetchall()
    if not id:
        myCursor.execute("""INSERT INTO allergies_ingredients(ingredient_id,allergy_id) VALUES(%s,%s) """, (lastproductid, lastallergieid))


def product_allergie_temp_relatietabel(lastproductid, lastallergieid):
    myCursor.execute("SELECT * FROM temp_allergies_ingredients WHERE ingredient_id=%s AND allergy_id=%s;", (lastproductid, lastallergieid))
    id = myCursor.fetchall()
    if not id:
        myCursor.execute("""INSERT INTO temp_allergies_ingredients(ingredient_id,allergy_id) VALUES(%s,%s) """, (lastproductid, lastallergieid))


def start(i):
    while True:
        try:
            receptenspider(0, i, 5)
            break
        except Exception as e:
            print('Something went wrong: ' + repr(e) + 'starting over...')
            receptenspider(0, i, 5)

