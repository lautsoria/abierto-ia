import mysql.connector


with open("init_db.sql", "r", encoding="utf8") as f:
    sql = f.read()


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = conn.cursor()


for statement in sql.split(";"):
    stmt = statement.strip()
    if stmt:
        cursor.execute(stmt)

conn.commit()
cursor.close()
conn.close()
print("Base de datos inicializada correctamente ✅")
