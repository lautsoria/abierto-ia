import requests
from flask import render_template, request, redirect, url_for, Blueprint
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

BACKEND_URL = 'http://localhost:5500/api'
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/mi-perfil')
@jwt_required(locations=['cookies'])
def perfil():
    data = get_jwt()
    usuario_id = get_jwt_identity()

    response = requests.get(f"{BACKEND_URL}/usuarios/{usuario_id}")

    if response.status_code != 200:
        return "Usuario no encontrado", 404

    if data['rol'] == "proveedor":
        response = requests.get(f"{BACKEND_URL}/proveedores/{usuario_id}")
        
        if response.status_code != 200:
            return "Proveedor no encontrado", 404
        
    datos_user = response.json()
        
    return render_template("editar_perfil.html", usuario=datos_user, data=data)



@usuarios_bp.route('/<id>/editar', methods=['POST'])
def editar_usuario(id):
    data = request.form
    payload = {
        "nombre": data.get("nombre"),
        "email": data.get("email"),
        "rol": data.get("rol"),
    }

    response = requests.put(f"{BACKEND_URL}/usuarios/{id}/mod", json=payload)

    if response.status_code != 200:
        return "Error al modificar usuario", 400

    return redirect(url_for('usuarios.admin_usuarios'))



@usuarios_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_usuario(id):
    response = requests.delete(f"{BACKEND_URL}/usuarios/{id}/eliminar")

    if response.status_code != 200:
        return "Usuario no encontrado", 404
    
    
    return redirect(url_for('usuarios.admin_usuarios'))



@usuarios_bp.route('/')
@jwt_required(locations=['cookies'])
def admin_usuarios():
    data = get_jwt()
    usuario_id = get_jwt_identity()
    
    # user_data = data if data else None

    if data['rol'] != 'admin':
        return "permiso denegado", 404
    
    # response_user = requests.get(f"{BACKEND_URL}/usuarios/{usuario_id}")

    # if response_user.status_code != 200:
    #     return "Usuario no encontrado", 404

    # datos_user = response_user.json()

    # if datos_user.get("rol") != "admin":
    #     
    
    response = requests.get(f'{BACKEND_URL}/usuarios/todos')
    
    if response.status_code != 200:
        return "Usuarios no encontrados", 404
    
    usuarios = response.json()

    return render_template('usuarios.html',usuarios=usuarios)


