from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import pymysql
import inserter
import checker

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")


def ah_crawler(i):

    mycursor = conn.cursor()
    #  print(i)
    url = 'https://www.ah.nl/allerhande/recepten-zoeken?No=' + str(i*1000) + '&Nrpp=' + str((i+1)*1000)
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for figure in soup.findAll('figure', {'class': ''}):
        for link in figure.findAll('a'):
            recepturl = 'https://www.ah.nl' + link.get('href')
            recept = recepturl.split('/')[-1]
            #  print(recept)
            #  print(recepturl)
            lastrecipeid = checker.checkrecipe('recipe', recept, recepturl)
            get_ingredienten(recepturl, lastrecipeid)
        #  print('')
    conn.commit()
    mycursor.close()
    conn.close()
    print('data inserted')


def get_ingredienten(itemurl, lastrecipeid):
    sourcecode = requests.get(itemurl)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for link in soup.findAll('a', {'class': 'js-ingredient ingredient-selector js-ingredient-is-selected'}):
        ingredient = link.get('data-search-term')
        #   print(ingredient)
        lastproductid = checker.check('ingredient', ingredient)
        inserter.relatietabel('recipe_ingredient_relation', 'recipe_id', 'ingredient_id', lastrecipeid, lastproductid)
        getproducten(ingredient, lastproductid)
        conn.commit()


def getproducten(ingredient, lastproductid):
    browser = webdriver.PhantomJS()
    browser.get('https://www.ah.nl/zoeken?rq='+str(ingredient)+'&searchType=global')
    time.sleep(4)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class': 'lane row product-lane search-lane'}):
        p = p.a
        href = p.get('href')
        #  print('https://www.ah.nl'+ str(href))
        allergiespider('https://www.ah.nl' + str(href), lastproductid)


def allergiespider(url, lastproductid):
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(4)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class': 'section__content'}):
        for x in p.find_all(text=re.compile('Bevat:')):
            words = x.split(' ', 1)[1]
            words = words.split()
            for word in words:
                allergie = word[:-1]
                #  print(allergie)
                lastallergieid = checker.check('category', allergie)
                inserter.relatietabel('category_ingredient_relation', 'ingredient_id', 'category_id', lastproductid, lastallergieid)


def start(i):
    while True:
        try:
            ah_crawler(i)
            break
        except Exception as e:
            print('Something went wrong: ' + repr(e) + 'starting over...')
