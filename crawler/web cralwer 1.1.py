import requests
from bs4 import BeautifulSoup


def trade_spider(page):

        url = 'https://www.ah.nl/allerhande/recepten/R-L1383828531946/hoofdgerechten?Nrpp='+ str(page)
        SourceCode = requests.get(url)
        PlainText = SourceCode.text
        soup = BeautifulSoup(PlainText)

        for figure in soup.findAll('figure', {'class': ''}):
            for link in figure.findAll('a'):
                href = 'https://www.ah.nl' + link.get('href')
                print(href)
                GetProducten(href)
                print('')


def GetProducten(ItemUrl):
    sourcecode=requests.get(ItemUrl)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext)
    for link in soup.findAll('a', {'class': 'js-ingredient ingredient-selector js-ingredient-is-selected'}):
        ingredienten = link.get('data-search-term')
        print(ingredienten)
        GetArtikelen('https://www.google.nl/search?source=hp&ei=1scjWuC3I8fKkwXEy6qIAQ&q=' + str(ingredienten) + 'ah allergie informatie' + '&oq=ol&gs_l=psy-ab.3.0.35i39k1l2j0i67k1l2j0i131k1j0i67k1j0j0i67k1l2j0.2462.2735.0.5018.3.2.0.0.0.0.62.112.2.2.0....0...1c.1.64.psy-ab..1.2.111.0...0.SpRlw3_ntA8')

def GetArtikelen(ingredientenUrl):
    sourcecode=requests.get(ingredientenUrl)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext)

    for href in soup.findAll('class'):
            artikelen = href.get('st')
            print(artikelen)


trade_spider(1)


