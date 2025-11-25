import mysql.connector
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)


def db_conn():
  return mysql.connector.connect(
    # llenar estos datos con las variables del .env por seguridad
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    # database=os.getenv('DB_DATABASE'),
    database='ids',
    port=int(os.getenv('DB_PORT'))
  )