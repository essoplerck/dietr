import requests
from bs4 import BeautifulSoup

def receptenspider():
    url = 'https://www.jumbo.com/recepten'
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for section in soup.findAll('h3', {'data-jum-action': 'ellipsis'}):
        for link in section.findAll('a'):
            receptenurl = link.get('href')
            recepten = link.text
            print('recept '+recepten)
            productenspider(receptenurl)
            print('')

def productenspider(url):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for ingredienten in soup.findAll('input', {'type': 'checkbox'}):
        producten = ingredienten.get('data-jum-product-add')
        producten=producten.split('"')[3]
        print('product ' +producten)
        producten=producten.replace(' ', '-')
        allergiespider('https://www.jumbo.com/zoeken?SearchTerm=' + str(producten) + '&search=search=')

def allergiespider(url):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for div in soup.findAll('div', {'class': 'jum-product-allergy-info jum-product-info-item'}):
        for li in div.findAll('li'):
            allergie=li.text
            print(allergie)

receptenspider()
