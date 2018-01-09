from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import pymysql
import checker

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")


def ah_crawler(begin, eind):
    i = begin
    while i <= eind:  # het doorlopen van de pagina's
        mycursor = conn.cursor()
        url = 'https://www.ah.nl/allerhande/recepten-zoeken?No=' + str(i*1000) + '&Nrpp=' + str((i+1)*1000)  # elke pagina heeft 1000 recepten de eerste variabele is het begin en de tweede het laaste recept op de pagina
        sourcecode = requests.get(url)
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        for figure in soup.findAll('figure', {'class': ''}):
            for link in figure.findAll('a'):
                recepturl = 'https://www.ah.nl' + link.get('href')  # selecteer alle urls op de pagina
                recept = recepturl.split('/')[-1]
                lastrecipeid = checker.checkrecipe('recipe', recept, recepturl)  # controleer of het recept al in de database staat
                get_ingredienten(recepturl, lastrecipeid)
            i += 1
    conn.commit()
    mycursor.close()
    conn.close()
    print('data inserted')


def get_ingredienten(itemurl, lastrecipeid):
    sourcecode = requests.get(itemurl)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for link in soup.findAll('a', {'class': 'js-ingredient ingredient-selector js-ingredient-is-selected'}):
        ingredient = link.get('data-search-term')  # selecteer alle ingredienten
        lastproductid = checker.check('ingredient', ingredient)  # controleer of het ingredient al in de database staat
        checker.checkrelatie('recipe_ingredient_relation', 'recipe_id', 'ingredient_id', lastrecipeid, lastproductid)  # controleer of de relatie al in de database staat
        getproducten(ingredient, lastproductid)
        conn.commit()


def getproducten(ingredient, lastproductid):
    browser = webdriver.PhantomJS()  # omdat de pagina javascript bevat gebruik de headless browser PhantomJS
    browser.get('https://www.ah.nl/zoeken?rq='+str(ingredient)+'&searchType=global')  # zoek op naar het ingredient
    time.sleep(4)  # 4 seconden is nodig om de browser de tijd te geven om de javascript code uit te voeren
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class': 'lane row product-lane search-lane'}):
        p = p.a
        href = p.get('href')  # selecteer het ingredient
        allergiespider('https://www.ah.nl' + str(href), lastproductid)


def allergiespider(url, lastproductid):
    browser = webdriver.PhantomJS()  # omdat de pagina javascript bevat gebruik de headless browser PhantomJS
    browser.get(url)
    time.sleep(4)  # 4 seconden is nodig om de browser de tijd te geven om de javascript code uit te voeren
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class': 'section__content'}):
        for x in p.find_all(text=re.compile('Bevat:')):
            words = x.split(' ', 1)[1]
            words = words.split()
            for word in words:  # selecteer de allergie
                allergie = word[:-1]
                lastallergieid = checker.check('category', allergie)  # cntroleer of de allergie al in de database staat
                checker.checkrelatie('category_ingredient_relation', 'ingredient_id', 'category_id', lastproductid, lastallergieid)  # controleer of de relatie al in de database staat


while True:  # de meeste errors zijn op te lossen door het programma opnieuw top te starten
    try:
        ah_crawler(0, 17)
        break
    except Exception as e:
        print('Something went wrong: ' + repr(e) + 'starting over...')
