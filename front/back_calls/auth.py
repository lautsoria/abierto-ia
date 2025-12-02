import requests
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

BACKEND_URL = os.getenv('BACEKND_URL')

def registrar_usuario(user, email, password, provider):
    """Registra un nuevo usuario en el backend"""
    try:
        response = requests.post(
            f'{BACKEND_URL}/auth/register',
            json={
                'user': user,
                'email': email,
                'password': password,
                'provider': provider
            },
            timeout=5
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar usuario: {e}")
        return None

def login_usuario(credential, password):
    """Inicia sesión de un usuario en el backend"""
    try:
        response = requests.post(
            f'{BACKEND_URL}/auth/login',
            json={
                'credential': credential,
                'password': password
            },
            timeout=5
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al iniciar sesión: {e}")
        return None
