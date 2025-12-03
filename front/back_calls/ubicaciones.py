import requests
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)
BACKEND_URL = os.getenv('BACKEND_URL')

def obtener_ubicaciones():
    """Obtiene todas las ubicaciones disponibles"""
    try:
        response = requests.get(
            f'{BACKEND_URL}/ubicacion',
            timeout=2
        )
        
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener ubicaciones: {e}")
        return []

