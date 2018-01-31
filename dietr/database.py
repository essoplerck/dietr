import pymysql as sql

from dietr.utils import singleton


@singleton
class Database:
    """Connects to the MySQL database and provides helper functions. Alls data
    is return in the form of dictionaries. This class is a singelton, there is
    only one instance.
    """
    def __init__(self):
        self.connection = None

    def close(self):
        """Close database connection."""
        self.connection.close()

    def connect(self, password):
        """Connecto to the database."""
        self.connection = sql.connect(database='renswnc266_production',
                                      host='185.182.57.56',
                                      user='renswnc266_dietr',
                                      password=password,
                                      cursorclass=sql.cursors.DictCursor)

    def commit(self, query, arugments=()):
        """Execute a query and commit."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            self.connection.commit()

    def fetch(self, query, arugments=()):
        """Fetch one row from the database."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            return cursor.fetchone()

    def fetch_all(self, query, arugments=()):
        """Fetch many rows from the database."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            return cursor.fetchall()


# Create an instance of the database class
database = Database()
