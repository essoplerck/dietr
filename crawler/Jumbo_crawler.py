from time import sleep
from bs4 import BeautifulSoup
import pymysql
import requests
import inserter
import checker

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_dietr", use_unicode=True, charset="utf8")



def receptenspider(begin, eind):
    i = begin
    while i <= eind:
        url = 'https://www.jumbo.com/recepten?PageNumber='+str(i)
        sourcecode = requests.get(url)
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        for section in soup.findAll('h3', {'data-jum-action': 'ellipsis'}):

            for link in section.findAll('a'):
                recepturl = link.get('href')
                recept = link.text
                #  print('recept >'+recept+'<')
                lastrecipeid = checker.check('recipe', recept)
            productenspider(recepturl, lastrecipeid)
            sleep(5)
            #  print('')
        i += 1
        #  print(i)
    conn.commit()
    conn.close()
    print("data inserted ")



def productenspider(url, lastrecipeid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for ingredienten in soup.findAll('input', {'type': 'checkbox'}):
        ingredient = ingredienten.get('data-jum-product-add')
        ingredient = ingredient.split('"')[3]
        #  print('product ' + producten)
        ingredienturl = 'https://www.jumbo.com/zoeken?SearchTerm=' + str(ingredient) + '&search=search='
        lastproductid = checker.check('ingredient', ingredient)
        inserter.relatietabel('recipe_ingredient_relation', 'recipe_id', 'ingredient_id', lastrecipeid, lastproductid)
        allergiespider(ingredienturl, lastproductid)
        sleep(1)
        conn.commit()


def allergiespider(url, lastproductid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for div in soup.findAll('div', {'class': 'jum-product-allergy-info jum-product-info-item'}):
        for li in div.findAll('li'):
            allergie = li.text
            lastallergieid = checker.check('category', allergie)
            inserter.relatietabel('category_ingredient_relation', 'ingredient_id', 'category_id', lastproductid, lastallergieid)
    conn.close()


while True:
    try:
        receptenspider(0, 340)
        break
    except Exception as e:
        print('Something went wrong: ' + repr(e) + 'starting over...')


