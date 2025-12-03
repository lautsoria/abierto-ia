import requests
from flask import render_template, request, redirect, url_for, Blueprint
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)
BACKEND_URL = os.getenv('BACKEND_URL')

usuarios_bp = Blueprint('usuarios', __name__)


def mostrar_perfil(data, usuario_id):
    response = requests.get(f"{BACKEND_URL}/usuarios/{usuario_id}")

    if response.status_code != 200:
        return "Usuario no encontrado", 404
        
    datos_user = response.json()
        
    return render_template("editar_perfil.html", usuario=datos_user, data=data)


def editar_perfil(id):
    
    data = request.form
    payload = {
        "nombre": data.get("nombre"),
        "email": data.get("email"),
        "telefono": data.get("telefono"),
    }

    response = requests.patch(f"{BACKEND_URL}/usuarios/{id}", json=payload)

    if response.status_code != 204:
        return "Error al modificar usuario", 400

    return redirect(url_for('usuarios.perfil'))



@usuarios_bp.route('/mi-perfil', methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
def perfil():
    data = get_jwt()
    usuario_id = data['sub']

    if request.method == 'GET':
        return mostrar_perfil(data, usuario_id)
    
    if request.method == 'POST':
        return editar_perfil(usuario_id)



@usuarios_bp.route('/editar', methods=['POST'])
@jwt_required(locations=['cookies'])
def editar_usuario():
    id = get_jwt_identity()
    data = request.form
    payload = {
        "id": data.get("id"),
        "nombre": data.get("nombre"),
        "email": data.get("email"),
        "rol": data.get("rol"),
    }

    response = requests.patch(f"{BACKEND_URL}/usuarios/mod", json=payload)

    if response.status_code != 200:
        return "Error al modificar usuario", 400

    return redirect(url_for('usuarios.admin_usuarios'))



@usuarios_bp.route('/eliminar', methods=['POST'])
@jwt_required(locations=['cookies'])
def eliminar_usuario():
    
    data = request.form
    id = data.get("id")
    rol = data.get("rol")

    
    payload = {
        "id": id,
        "rol": rol
    }

    response = requests.delete(f"{BACKEND_URL}/usuarios/eliminar", json=payload)

    if response.status_code != 200:
        return "Usuario no encontrado", 404
    
    
    return redirect(url_for('usuarios.admin_usuarios'))



@usuarios_bp.route('/')
@jwt_required(locations=['cookies'])
def admin_usuarios():
    data = get_jwt()
    usuario_id = get_jwt_identity()

    if data['rol'] != 'admin':
        return "permiso denegado", 404     
    
    response = requests.get(f'{BACKEND_URL}/usuarios/todos')
    
    if response.status_code != 200:
        return "Usuarios no encontrados", 404
    
    usuarios = response.json()

    return render_template('usuarios.html', usuarios=usuarios, data=data)


