import pymysql as sql

connection = sql.connect(host='185.182.57.56', user='renswnc266_dietr',
                         password='qvuemzxu', db='renswnc266_dietr',
                         cursorclass=sql.cursors.DictCursor)


def commit(query, arugments=()):
    with connection.cursor() as cursor:
        cursor.execute(query, arugments)

    connection.commit()


def fetch(query, arugments=()):
    with connection.cursor() as cursor:
        cursor.execute(query, arugments)

    return cursor.fetchone()


def fetch_all(query, arugments=()):
    with connection.cursor() as cursor:
        cursor.execute(query, arugments)

    return cursor.fetchall()
