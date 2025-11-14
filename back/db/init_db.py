import mysql.connector
import os

# este archivo inicializa la base de datos junto con los datos dummy

# ahora leemos las querys del archivo 
script_dir = os.path.dirname(os.path.abspath(__file__))
sql_file = os.path.join(script_dir, 'init_db.sql')

with open(sql_file) as f:
  sql = f.read()

db = mysql.connector.connect(
  # llenar estos datos con las variables del .env por seguridad
  host='localhost',
  user='root',
  password='0074'
)

cursor = db.cursor()

for query in sql.split(';'):
  if query.strip():
    print(query)
    # ejecutamos la query
    cursor.execute(query)
    # guardamos los cambios en nuestra base de datos
    db.commit()

cursor.close()
db.close()



