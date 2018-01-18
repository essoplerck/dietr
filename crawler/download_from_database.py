import pymysql

conn = pymysql.connect(host="185.182.57.56", user="renswnc266_dietr", passwd="qvuemzxu", db="renswnc266_staging", use_unicode=True, charset="utf8")
myCursor = conn.cursor()
f = open('file2.txt','w')

def ingredient(idrecept):
    i = 1
    while i <= idrecept:
        myCursor.execute("SELECT * FROM allergies WHERE id=%s", i)
        id = myCursor.fetchall()
        for t in id:
            line = ' '.join(str(x) for x in t)
            naam = line.split(' ')[1]
            print(naam)
            try:
                f.write(naam+"\n")
            except:
                print('deze lukte helaas niet')
        i=i+1
    f.close()





ingredient(800)
