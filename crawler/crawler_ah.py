import requests
from bs4 import BeautifulSoup
import re

def allergiespider(url):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    soup = BeautifulSoup(plaintext, "html.parser")
    for p in soup.findAll('div', {'class' : 'section__content'}):
        for x in p.findAll(text=re.compile('Bevat:')):
            print(x)
allergiespider('http://localhost:8050/render.html?url={}&timeout=30&wait=10'.format('http://www.ah.nl/producten/product/wi193444/calve-saus-fles-knoflook'))
