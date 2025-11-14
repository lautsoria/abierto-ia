import mysql.connector

def db_conn():
  return mysql.connector.connect(
    # llenar estos datos con las variables del .env por seguridad
    host='localhost',
    user='root',
    password='0074',
    database='IDS'
  )