from time import sleep
from bs4 import BeautifulSoup
import pymysql
import requests
import checker

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_dietr", use_unicode=True, charset="utf8")


def receptenspider(begin, eind):
    i = begin
    while i <= eind:  # doorlopen van alle pagina's
        url = 'https://www.jumbo.com/recepten?PageNumber='+str(i)
        sourcecode = requests.get(url)
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        for section in soup.findAll('h3', {'data-jum-action': 'ellipsis'}):
            for link in section.findAll('a'):  # alleen de recepten url selecteren
                recepturl = link.get('href')
                recept = link.text
                lastrecipeid = checker.check('recipe', recept)
            productenspider(recepturl, lastrecipeid)
            sleep(5)
        i += 1
    conn.commit()
    conn.close()
    print("data inserted ")


def productenspider(url, lastrecipeid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for ingredienten in soup.findAll('input', {'type': 'checkbox'}):
        ingredient = ingredienten.get('data-jum-product-add')
        ingredient = ingredient.split('"')[3]  # de producten selecteren
        ingredienturl = 'https://www.jumbo.com/zoeken?SearchTerm=' + str(ingredient) + '&search=search='  # zoeken op de producten
        lastproductid = checker.check('ingredient', ingredient)  # controleer of het product al in de database staat
        checker.checkrelatie('recipe_ingredient_relation', 'recipe_id', 'ingredient_id', lastrecipeid, lastproductid)  # relatie toevoegen in de recipe ingredient relatietabel
        allergiespider(ingredienturl, lastproductid)
        sleep(1)  # sleep omdat anders de jumbo server de connectie verbreekt
        conn.commit()


def allergiespider(url, lastproductid):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for div in soup.findAll('div', {'class': 'jum-product-allergy-info jum-product-info-item'}):
        for li in div.findAll('li'):  # allergieen selecteren van producten
            allergie = li.text
            lastallergieid = checker.check('category', allergie)  # controleer of de allergie al in de database staat
            checker.checkrelatie('category_ingredient_relation', 'ingredient_id', 'category_id', lastproductid, lastallergieid)  # relatie toevoegen in de category ingredient relatietabel
    conn.close()


while True:  # de meeste errors zijn op te lossen door het programma opnieuw top te starten
    try:
        receptenspider(0, 340)
        break
    except Exception as e:
        print('Something went wrong: ' + repr(e) + 'starting over...')


