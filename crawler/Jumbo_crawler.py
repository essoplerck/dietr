from time import sleep
from bs4 import BeautifulSoup
import pymysql
import requests
import inserter
import checker

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_staging", use_unicode=True, charset="utf8")



def receptenspider(i):
    page = 0
    while page <= i:
        url = 'https://www.jumbo.com/recepten?PageNumber='+str(page)
        #  print(url)
        sourcecode = requests.get(url)
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        for section in soup.findAll('h3', {'data-jum-action': 'ellipsis'}):
            for link in section.findAll('a'):
                recepturl = link.get('href')
                recept = link.text
                #  print('recept >'+recept+'<')
                lastrecipeid = checker.check('recipes', recept)
            productenspider(recepturl, lastrecipeid)
            sleep(5)
            print('')
        page += 1
    print("data inserted ")
    print(i)
    conn.commit()
    conn.close()



def productenspider(url, lastrecipeid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for ingredienten in soup.findAll('input', {'type': 'checkbox'}):
        ingredient = ingredienten.get('data-jum-product-add')
        ingredient = ingredient.split('"')[3]
        #  print('product ' + ingredient)
        ingredienturl = 'https://www.jumbo.com/zoeken?SearchTerm=' + str(ingredient) + '&search=search='
        lastproductid = checker.check('ingredients', ingredient)
        print(lastproductid)
        inserter.relatietabel('recipes_ingredients', 'recipe_id', 'ingredient_id', lastrecipeid, lastproductid)
        allergiespider(ingredienturl, lastproductid)
        sleep(1)



def allergiespider(url, lastproductid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for div in soup.findAll('div', {'class': 'jum-product-allergy-info jum-product-info-item'}):
        for li in div.findAll('li'):
            allergie = li.text
            lastallergieid = checker.allergycheck('allergies', allergie)
            inserter.relatietabel('allergies_ingredients', 'ingredient_id', 'allergy_id', lastproductid, lastallergieid)



def start(i):
    while True:
        try:
            receptenspider(i)
            break
        except Exception as e:
            print('Something went wrong: ' + repr(e) + 'starting over...')
            print(i)



