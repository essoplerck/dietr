from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import requests
import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_test", passwd="qvuemzxu", db="renswnc266_test", use_unicode=True, charset="utf8")

def trade_spider(begin,eind):
        mycursor = conn.cursor()
        tab = eind-begin
        i = begin
        mycursor.execute("""INSERT INTO extra_info(name) VALUES(%s) """, 'Vegetarisch')
        extra_info_id=mycursor.lastrowid

        while i <= tab:
            print(i)
            url = 'https://www.ah.nl/allerhande/recepten-zoeken/__/N-26xv?No=' + str(i*1000) + '&Nrpp=' + str((i+1)*1000)
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


try:
    trade_spider(0, 4)
except Exception as e:
    print('Something went wrong: ' + repr(e) + 'starting over...')
    trade_spider(0, 4)

