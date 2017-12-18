from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time

def allergiespider(url):
    browser = webdriver.PhantomJS('./phantomjs.exe')
    browser.get(url)
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for p in soup.findAll('div', {'class' : 'section__content'}):
        for x in p.find_all(text=re.compile('Bevat:')):
            print(x)

allergiespider('http://www.ah.nl/producten/product/wi193444/calve-saus-fles-knoflook')
