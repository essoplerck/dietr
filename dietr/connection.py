import pymysql as sql

connection = sql.connect(host='185.182.57.56', user='renswnc266_dietr',
                         password='69f5854300d331e7', db='renswnc266_dietr',
                         cursorclass=sql.cursors.DictCursor)


class Database:
    def __init__(self):
        self.connection = sql.connect(db='renswnc266_development',
                                      host='185.182.57.56',
                                      user='renswnc266_dietr',
                                      password='69f5854300d331e7')

    def commit(self, query, arugments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            self.connection.commit()

    def fetch(self, query, arugments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            return cursor.fetchone()

    def fetch_all(self, query, arugments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            return cursor.fetchall()
