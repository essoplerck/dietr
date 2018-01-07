import pymysql as sql

connection = sql.connect(host='185.182.57.56', user='renswnc266_dietr',
                         password='qvuemzxu', db='renswnc266_dietr',
                         cursorclass=sql.cursors.DictCursor)
