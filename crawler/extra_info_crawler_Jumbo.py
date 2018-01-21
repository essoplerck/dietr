from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")
myCursor= conn.cursor()


def trade_spider(begin, eind, extra_info_id, url):

    i = begin
    while i <= eind:
        url = 'https://www.jumbo.com/recepten/soort-gerecht/' + url + '/?PageNumber='+str(i)
        sourcecode = requests.get(url)
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        for section in soup.findAll('h3', {'data-jum-action': 'ellipsis'}):

            for link in section.findAll('a'):
                receptenurl = link.get('href')
                recepten = link.text
                print('recept >'+recepten+'<')

                myCursor.execute("SELECT * FROM recipe WHERE name=%s;",(recepten))
                id=myCursor.fetchall()

            if id:
                for t in id:
                    line=' '.join(str(x) for x in t)
                lastrecipeid = line.split(' ')[0]
                recipe_extra_info_relation(lastrecipeid, extra_info_id)
            else:
                print("Is er niet")

        print('')
        i += 1


    conn.commit()
    conn.close()
    print(" > data inserted ")


def recipe_extra_info_relation(lastrecipeid, extra_info_id):
    myCursor = conn.cursor()
    myCursor.execute("""INSERT INTO recipe_extra_info_relation(recipe_id,extra_info_id) VALUES(%s,%s) """, (lastrecipeid, extra_info_id))


def start():
    trade_spider(0, 300, 3, 'hoofdgerecht')
    trade_spider(0, 300, 4, 'voorgerecht')
    trade_spider(0, 300, 5, 'nagerecht-~-dessert')
    trade_spider(0, 300, 7, 'vegetarisch')
