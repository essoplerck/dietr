from flask_mysqldb import MySQL

from . import app

app.config['MYSQL_USER']     = 'renswnc266_dietr'
app.config['MYSQL_PASSWORD'] = 'qvuemzxu'
app.config['MYSQL_DB']       = 'renswnc266_dietr'
app.config['MYSQL_HOST']     = '185.182.57.56'

database = MySQL()
database.init_app(app)
