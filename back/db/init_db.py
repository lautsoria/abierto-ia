import mysql.connector
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)
# este archivo inicializa la base de datos junto con los datos dummy

# ahora leemos las querys del archivo 
script_dir = os.path.dirname(os.path.abspath(__file__))
sql_file = os.path.join(script_dir, 'init_maria.sql')

with open(sql_file) as f:
  sql = f.read()

db = mysql.connector.connect(
  # llenar estos datos con las variables del .env por seguridad
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD'),
  port=int(os.getenv('DB_PORT'))
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