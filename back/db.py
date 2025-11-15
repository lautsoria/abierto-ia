import mysql.connector

def get_connection(database="abierto_ia"):
    """
    Obtiene una conexión a MySQL.
    
    Args:
        database: Nombre de la base de datos. Si es None, no se especifica base de datos.
    """
    config = {
        "host": "localhost",
        "user": "root",
        "password": ""
    }
    
    if database:
        config["database"] = database
    
    return mysql.connector.connect(**config)