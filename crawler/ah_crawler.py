import requests
from bs4 import BeautifulSoup

def receptenspider():
    url = 'http://localhost:8050/render.html?url={}&timeout=30&wait=10'.format('http://www.ah.nl/allerhande/recept/R-R1189762/hasselbackbietjes-met-tijm-en-geitenkaas')
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for header in soup.findAll('h1', {'itemprop' : 'name'}):
        #for link in section.findAll('a'):
            #receptenurl = link.get('href')
        recepten = header.text
        print('recept '+recepten)
        productenspider('http://www.ah.nl/producten/product/wi193444/calve-saus-fles-knoflook')
        print('')

def productenspider(url):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for ingredienten in soup.findAll('ul', {'class': 'list shopping ingredient-selector-list'}):
        producten = ingredienten.get('span', {'class' : 'js-label label'})
        producten=producten.split('"')[3]
        print('product ' +producten)
        producten=producten.replace(' ', '-')
        allergiespider('http://localhost:8050/render.html?url={}&timeout=30&wait=10'.format('http://www.ah.nl/producten/product/wi193444/calve-saus-fles-knoflook'))

def allergiespider(url):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for p in soup.findAll('p', text='Bevat:'):
        allergie=p.text
        print(allergie)

receptenspider()

#Start splash: sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
