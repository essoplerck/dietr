from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")

def trade_spider(begin,eind):
        mycursor = conn.cursor()
        tab = eind-begin
        i = begin
        while i <= tab:
            print(i)
            url = 'https://www.ah.nl/allerhande/recepten-zoeken?No=' + str(i*1000) + '&Nrpp=' + str((i+1)*1000)
            SourceCode = requests.get(url)
            PlainText = SourceCode.text
            soup = BeautifulSoup(PlainText, "html.parser")

            for figure in soup.findAll('figure', {'class': ''}):
                for link in figure.findAll('a'):
                    receptenurl = 'https://www.ah.nl' + link.get('href')
                    recepten = receptenurl.split('/')[-1]
                    #print(recepten)
                    print(receptenurl)

                    mycursor.execute("SELECT * FROM recipe WHERE name=%s;", (recepten))
                    id = mycursor.fetchall()

                    if id:
                        for t in id:
                            line = ' '.join(str(x) for x in t)
                        lastrecipeid = line.split(' ')[0]
                    else:
                         mycursor.execute("""INSERT INTO recipe(name,url) VALUES(%s,%s) """, (recepten, receptenurl))
                         lastrecipeid = mycursor.lastrowid
                         get_ingredienten(receptenurl, lastrecipeid)
                #print('')
            i += 1
        conn.commit()
        mycursor.close()
        conn.close()
        print('data inserted')


def get_ingredienten(itemurl, lastrecipeid):
    myCursor = conn.cursor()
    sourcecode=requests.get(itemurl)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for link in soup.findAll('a', {'class': 'js-ingredient ingredient-selector js-ingredient-is-selected'}):
        ingredienten = link.get('data-search-term')
        #print(ingredienten)

        myCursor.execute("SELECT * FROM ingredient WHERE name=%s;", ingredienten)
        id = myCursor.fetchall()

        if id:
            for t in id:
                line = ' '.join(str(x) for x in t)
            lastproductid = line.split(' ')[0]
        else:
                myCursor.execute("""INSERT INTO ingredient(name) VALUES(%s) """, ingredienten)
                lastproductid = myCursor.lastrowid
                Getproducten(ingredienten,lastproductid)
        recept_product_relatietabel(lastrecipeid, lastproductid)
    conn.commit()
    myCursor.close()


def Getproducten(ingredienten,lastproductid):
    browser = webdriver.PhantomJS()
    browser.get('https://www.ah.nl/zoeken?rq='+str(ingredienten)+'&searchType=global')
    time.sleep(4)
    soup=BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class': 'lane row product-lane search-lane'}):
        p = p.a
        href=p.get('href')
        #print('https://www.ah.nl'+ str(href))
        allergiespider('https://www.ah.nl'+ str(href),lastproductid)


def allergiespider(url, lastproductid):
    myCursor = conn.cursor()
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(4)
    soup=BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class': 'section__content'}):
        for x in p.find_all(text=re.compile('Bevat:')):
            words =x.split(' ', 1)[1]
            words = words.split()
            for word in words:
                allergie = word[:-1]
                print(allergie)
                myCursor.execute("SELECT * FROM category WHERE name=%s;", allergie)
                id = myCursor.fetchall()

                if id:
                    for t in id:
                        line = ' '.join(str(x) for x in t)
                    lastallergieid = line.split(' ')[0]
                else:
                    myCursor.execute("""INSERT INTO category(name) VALUES(%s) """, allergie)
                    lastallergieid = myCursor.lastrowid
                product_allergie_relatietabel(lastproductid,lastallergieid)
    myCursor.close()


def recept_product_relatietabel(lastrecipeid, lastproductid):
    myCursor = conn.cursor()
    myCursor.execute("SELECT * FROM recipe_ingredient_relation WHERE recipe_id=%s AND ingredient_id=%s;", (lastrecipeid, lastproductid))
    id = myCursor.fetchall()

    if not id:
        myCursor.execute("""INSERT INTO recipe_ingredient_relation(recipe_id,ingredient_id) VALUES(%s,%s) """, (lastrecipeid, lastproductid))

        #print('nieuwe relatie')
    #else:
        #print('oude relatie')

        #print('nieuwe relatie')
    #else:
        #print('oude relatie')
    myCursor.close()


def product_allergie_relatietabel(lastproductid, lastallergieid):
    myCursor = conn.cursor()
    myCursor.execute("SELECT * FROM category_ingredient_relation WHERE ingredient_id=%s AND category_id=%s;", (lastproductid, lastallergieid))
    id = myCursor.fetchall()
    if not id:
        myCursor.execute("""INSERT INTO category_ingredient_relation(ingredient_id,category_id) VALUES(%s,%s) """, (lastproductid, lastallergieid))

        #print('nieuwe  relatie')
    #else:
        #print('oude  relatie')


try:
    trade_spider(0, 17)
except Exception as e:
    print('Something went wrong: ' + repr(e) + 'starting over...')
    trade_spider(0, 17)
