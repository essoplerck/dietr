from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")


def trade_spider(begin, eind, extra_info_id, url):
        mycursor = conn.cursor()
        tab = eind-begin
        i = begin

        while i <= tab:
            print(i)
            url = 'https://www.ah.nl/allerhande/recepten-zoeken/__/' + url + '?No=' + str(i*1000) + '&Nrpp=' + str((i+1)*1000)
            SourceCode = requests.get(url)
            PlainText = SourceCode.text
            soup = BeautifulSoup(PlainText, "html.parser")

            for figure in soup.findAll('figure', {'class': ''}):
                for link in figure.findAll('a'):
                    receptenurl = 'https://www.ah.nl' + link.get('href')
                    recepten = receptenurl.split('/')[-1]
                    print(recepten)
                    print(receptenurl)

                    mycursor.execute("SELECT * FROM recipe WHERE name=%s;", (recepten))
                    id = mycursor.fetchall()

                    if id:
                        for t in id:
                            line = ' '.join(str(x) for x in t)
                        lastrecipeid = line.split(' ')[0]
                        recipe_extra_info_relation(lastrecipeid, extra_info_id)
                    else:
                        print("Is er niet")
                print('')
            i += 1
        conn.commit()
        mycursor.close()
        conn.close()
        print('data inserted')


def recipe_extra_info_relation(lastrecipeid, extra_info_id):
    myCursor = conn.cursor()
    myCursor.execute("""INSERT INTO recipe_extra_info_relation(recipe_id,extra_info_id) VALUES(%s,%s) """, (lastrecipeid, extra_info_id))


def start():
    trade_spider(0, 10, 3, 'N-26vq')
    trade_spider(0, 10, 4, 'N-26vr')
    trade_spider(0, 10, 5, 'N-26vt')
    trade_spider(0, 10, 6, 'N-26y0')
    trade_spider(0, 10, 7, 'N-26xv')


