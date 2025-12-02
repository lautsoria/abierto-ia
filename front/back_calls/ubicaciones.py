import requests

BACKEND_URL = 'https://abiertoia.pythonanywhere.com/api'

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

