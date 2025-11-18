from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_cors import CORS
import os
import requests
import logging

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_NAME'] = 'access_token_cookie'

jwt = JWTManager(app)
CORS(app)

# manejamos que hacer cuando el token no existe
@jwt.unauthorized_loader
def unauthorized_callback(error):
    return redirect(url_for('home'))
# o cuando el token es invalido
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return redirect(url_for('home'))

icons = {
    # iconos hardcodeados
    "Electricista": "⚡",
    "Plomería": "💧",
    "Pintura": "📌",
    "Carpintería": "🔨",
    "Cerrajería": "🔑",
    "Limpieza": "✨",
    "Aire Acondicionado": "💨",
    "Jardinería": "🌿"
}

# @app.route("/reservas")
# def mis_reservas():
#     return render_template("reservas.html", reservas=RESERVAS_MOCK)

@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

BACKEND_URL = 'http://localhost:5500'

def obtener_cantidad_categoria(nombre):
    try:
        response = requests.get(f'{BACKEND_URL}/categorias/{nombre}')
        
        if response.status_code == 200:
            data = response.json()
            # la API retorna: { "categoria": "...", "total_profesionales": N }
            return data.get("total_profesionales", 0)
        return 0

    except Exception as e:
        print("Error al obtener cantidad categoria:", e)
        return 0

def obtener_servicios_destacados():
    """Obtiene servicios destacados desde el backend"""
    logging.info('Obteniendo servicios destacados')
    try:
        response = requests.get(  
            f'{BACKEND_URL}/servicios/top-rating',
            timeout=5
        )
        
        if response.status_code == 200:
            servicios = response.json()
            return servicios
        else:
            print(f" Error del backend: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:  
        print("Timeout: El backend tardó más de 5 segundos")
        return []
        
    except requests.exceptions.ConnectionError:  
        print(" Error: No se pudo conectar al backend en puerto 5500")
        print("¿Está corriendo el backend? Ejecuta: python backend/app.py")
        return []
        
    except requests.exceptions.RequestException as e:  
        print(f" Error al obtener servicios: {e}")
        return []

def obtener_proveedores(filtro_servicio=None):
    """Obtiene proveedores desde el backend"""
    try:
        url = f'{BACKEND_URL}/proveedores'
        if filtro_servicio:
            url += f'?servicio={filtro_servicio}'
        
        response = requests.get(url, timeout=5)  
        
        if response.status_code == 200:
            return response.json()
        return []
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener proveedores: {e}")
        return []

def obtener_proveedor_detalle(proveedor_id):
    """Obtiene detalles de un proveedor específico"""
    try:
        response = requests.get(  
            f'{BACKEND_URL}/proveedores/{proveedor_id}',
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener proveedor: {e}")
        return None

def obtener_categorias():
    try:
        response = requests.get(  
            f'{BACKEND_URL}/categorias',
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener categorias: {e}")
        return None


@app.route('/')
@jwt_required( optional=True, locations=['cookies'])
def home():
    data = get_jwt()    
    user_data = data if data else None

    servicios = obtener_servicios_destacados()
    categorias = obtener_categorias()
    categorias_completas = []
    if categorias:
        for cat in categorias:
            nombre = cat["nombre"]
            cantidad = obtener_cantidad_categoria(nombre)
            categorias_completas.append({
                "nombre": nombre,
                "total_profesionales": cantidad,
                "icono": icons.get(nombre, "📁") 
            })

    return render_template('home.html', servicios=servicios, categorias=categorias_completas, data=user_data)

@app.route('/auth')
def auth():
  try:
    verify_jwt_in_request(locations=['cookies'])

    return redirect(url_for('home'))
  except:
    return render_template('auth.html')

@app.route('/categoria/<nombre>')
@jwt_required(optional=True, locations=['cookies'])
def categoria(nombre):
    """Muestra servicios filtrados por categoría con opciones de filtrado"""
    data = get_jwt()    
    user_data = data if data else None

    # Obtener parámetros de filtro
    ubicacion_seleccionada = request.args.get('ubicacion', '')
    ordenar = request.args.get('ordenar', 'relevancia')

    try:
        # Construir URL con parámetros
        params = {}
        if ubicacion_seleccionada:
            params['ubicacion'] = ubicacion_seleccionada
        if ordenar != 'relevancia':
            params['ordenar'] = ordenar

        # Llamar al backend para obtener servicios
        response = requests.get(
            f'{BACKEND_URL}/servicios/categoria/{nombre}',
            params=params,
            timeout=3
        )

        if response.status_code == 200:
            servicios = response.json()
        else:
            servicios = []

        # Obtener ubicaciones únicas para el filtro
        ubicaciones_response = requests.get(
            f'{BACKEND_URL}/proveedores/ubicaciones',
            timeout=2
        )
        ubicaciones = ubicaciones_response.json() if ubicaciones_response.status_code == 200 else []

        # Contar total de servicios sin filtros
        total_response = requests.get(
            f'{BACKEND_URL}/servicios/categoria/{nombre}',
            timeout=2
        )
        total_servicios = len(total_response.json()) if total_response.status_code == 200 else 0

        return render_template(
            'categoria.html',
            categoria_nombre=nombre,
            servicios=servicios,
            total_servicios=total_servicios,
            ubicaciones=ubicaciones,
            ubicacion_seleccionada=ubicacion_seleccionada,
            ordenar=ordenar,
            data=user_data
        )

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener servicios: {e}")
        return render_template(
            'categoria.html',
            categoria_nombre=nombre,
            servicios=[],
            total_servicios=0,
            ubicaciones=[],
            ubicacion_seleccionada='',
            ordenar='relevancia',
            data=user_data
        )    


if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)