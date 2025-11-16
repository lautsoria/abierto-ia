from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt
import os
import requests
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_NAME'] = 'access_token_cookie'

jwt = JWTManager(app)

# manejamos que hacer cuando el token no existe
@jwt.unauthorized_loader
def unauthorized_callback(error):
    return redirect(url_for('reg'))
# o cuando el token es invalido
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return redirect(url_for('reg'))

@app.route('/auth')
def auth():
  try:
    verify_jwt_in_request(locations=['cookies'])

    return redirect(url_for('home'))
  except:
    return render_template('auth.html')





@app.route('/base')
@jwt_required(locations=['cookies'])
def base():
    data = get_jwt_identity()
    role = get_jwt()
    provider = role['provider']
    print(data)
    print(f'User {data} logged with valid token. Is provider? ${provider}')
    return render_template('base/base.html', data={'userId':data, 'provider':provider})

ICONOS_CATEGORIAS = {
    "iconos hardcodeados"
    "Electricista": "⚡",
    "Plomería": "💧",
    "Pintura": "📌",
    "Carpintería": "🔨",
    "Cerrajería": "🔑",
    "Limpieza": "✨",
    "Aire Acondicionado": "💨",
    "Jardinería": "🌿"
}

RESERVAS_MOCK = [
    {
        'id': 1,
        'usuario_id': 1,
        'servicio_id': 1,
        'fecha_reserva': '2025-11-10 14:30:00',
        'fecha_servicio': '2025-11-20 10:00:00',
        'estado': 'pendiente',
        'comentarios_cliente': 'Necesito ayuda urgente con una cañería rota',
        'servicio_nombre': 'Reparación de cañerías',
        'servicio_precio': 5000.00,
        'proveedor_nombre': 'Juan Pérez',
        'proveedor_descripcion': 'Plomero con 15 años de experiencia',
        'categoria': 'Plomería'
    },
    {
        'id': 2,
        'usuario_id': 1,
        'servicio_id': 2,
        'fecha_reserva': '2025-11-08 09:15:00',
        'fecha_servicio': '2025-11-15 14:00:00',
        'estado': 'realizado',
        'comentarios_cliente': 'Instalación de lámpara en el living',
        'servicio_nombre': 'Instalación eléctrica',
        'servicio_precio': 3500.00,
        'proveedor_nombre': 'María López',
        'proveedor_descripcion': 'Electricista matriculada',
        'categoria': 'Electricidad'
    },
    {
        'id': 3,
        'usuario_id': 1,
        'servicio_id': 3,
        'fecha_reserva': '2025-11-05 16:45:00',
        'fecha_servicio': '2025-11-10 09:00:00',
        'estado': 'cancelado',
        'comentarios_cliente': 'Corte de césped y limpieza de jardín',
        'servicio_nombre': 'Mantenimiento de jardín',
        'servicio_precio': 4200.00,
        'proveedor_nombre': 'Carlos Gómez',
        'proveedor_descripcion': 'Jardinero profesional',
        'categoria': 'Jardinería'
    },
    {
        'id': 4,
        'usuario_id': 1,
        'servicio_id': 4,
        'fecha_reserva': '2025-11-12 11:20:00',
        'fecha_servicio': '2025-11-25 16:30:00',
        'estado': 'pendiente',
        'comentarios_cliente': 'Revisión de instalación de gas',
        'servicio_nombre': 'Inspección de gas',
        'servicio_precio': 6500.00,
        'proveedor_nombre': 'Roberto Díaz',
        'proveedor_descripcion': 'Gasista matriculado',
        'categoria': 'Gasista'
    }
]

@app.route("/reservas")
def mis_reservas():
    return render_template("reservas.html", reservas=RESERVAS_MOCK)

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
    try:
        response = requests.get(  
            f'{BACKEND_URL}/servicios/top-rating',
            timeout=5
        )
        
        if response.status_code == 200:
            servicios = response.json()
            print(f" Servicios obtenidos: {len(servicios)}")
            return servicios
        else:
            print(f" Error del backend: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:  
        print("Timeout: El backend tardó más de 5 segundos")
        return []
        
    except requests.exceptions.ConnectionError:  
        print(" Error: No se pudo conectar al backend en puerto 5500")
        print("   ¿Está corriendo el backend? Ejecuta: python backend/app.py")
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
            f'{BACKEND_URL}/categorias/buscar_existentes',
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener categorias: {e}")
        return None



@app.route('/')
def home():
    """Página principal con servicios destacados"""
    data = None
    
    
    try:
        verify_jwt_in_request(locations=['cookies'], optional=True)
        data = get_jwt()
    except:
        pass
    
    
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
                "icono": ICONOS_CATEGORIAS.get(nombre, "📁") 
            })

    
    
    
    return render_template('home.html', servicios=servicios,categorias=categorias_completas, data=data)


if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)