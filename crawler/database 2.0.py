import pymysql
import requests

from time import sleep
from bs4 import BeautifulSoup

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_dietr", use_unicode=True, charset="utf8")
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

                myCursor.execute("SELECT * FROM recipe WHERE name=%s;",(recepten))
                id=myCursor.fetchall()

            if id:
                for t in id:
                    line=' '.join(str(x) for x in t)
                lastrecipeid=line.split(' ')[0]
                #print('oud recept')

            else:
                myCursor.execute("""INSERT INTO recipe(name,url) VALUES(%s,%s) """, (recepten, receptenurl))
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
        #print('product ' + producten)
        productenurl = 'https://www.jumbo.com/zoeken?SearchTerm=' + str(producten) + '&search=search='

        myCursor.execute("SELECT * FROM ingredient WHERE name=%s;", producten)
        id=myCursor.fetchall()
        if id:
            for t in id:
                line = ' '.join(str(x) for x in t)
            lastproductid=line.split(' ')[0]
            print('oud product ' + producten)
        else:
            myCursor.execute("""INSERT INTO ingredient(name) VALUES(%s) """, producten)
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
            allergie=li.text
            myCursor.execute("SELECT * FROM category WHERE name=%s;", allergie)
            id=myCursor.fetchall()
            #print('allergie ' + allergie)
            if id:
                for t in id:
                    line = ' '.join(str(x) for x in t)
                lastallergieid=line.split(' ')[0]
                print('oud allergeen ' + allergie)
            else:
                myCursor.execute("""INSERT INTO category(name) VALUES(%s) """, allergie)
                lastallergieid = myCursor.lastrowid
                print('nieuw allergeen ' + allergie)
            product_allergie_relatietabel(lastproductid,lastallergieid)


def recept_product_relatietabel(lastrecipeid, lastproductid):
    myCursor.execute("SELECT * FROM recipe_ingredient_relation WHERE recipe_id=%s AND ingredient_id=%s;", (lastrecipeid, lastproductid))
    id=myCursor.fetchall()

    if not id:
        myCursor.execute("""INSERT INTO recipe_ingredient_relation(recipe_id,ingredient_id) VALUES(%s,%s) """, (lastrecipeid, lastproductid))
        #print('nieuwe relatie')
    #else:
        #print('oude relatie')

def product_allergie_relatietabel(lastproductid, lastallergieid):
    myCursor.execute("SELECT * FROM category_ingredient_relation WHERE ingredient_id=%s AND category_id=%s;", (lastproductid, lastallergieid))
    id=myCursor.fetchall()
    if not id:
        myCursor.execute("""INSERT INTO category_ingredient_relation(ingredient_id,category_id) VALUES(%s,%s) """, (lastproductid, lastallergieid))
        #print('nieuwe  relatie')
    #else:
        #print('oude  relatie')


receptenspider(340, 340, 5)
