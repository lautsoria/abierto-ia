from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import jwt_required, JWTManager, verify_jwt_in_request, get_jwt
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv

from static.icons import icons
from back_calls.calls import *

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
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

# @app.route("/reservas")
# def mis_reservas():
#     return render_template("reservas.html", reservas=RESERVAS_MOCK)

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
  
@app.route('/register', methods=['POST'])
def register():
    user = request.form.get("newUser")
    email = request.form.get("email")
    password = request.form.get("newPassword")
    repeatPassword = request.form.get("newPassword2")
    provider = request.form.get("isProveedor") == 'true'

    if password != repeatPassword:
        flash('Las contraseñas no coinciden', 'error')
        return redirect(url_for('auth'))

    response = registrar_usuario(user, email, password, provider)
    
    if response and response.status_code == 200:
        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('auth'))
    else:
        flash('Error al registrar el usuario', 'error')
        return redirect(url_for('auth'))

@app.route('/login', methods=['POST'])
def login():
    credential = request.form.get("credential")
    password = request.form.get("password")

    response = login_usuario(credential, password)
    
    if response and response.status_code == 200:
        # Obtener las cookies del backend y pasarlas al frontend
        resp = make_response(redirect(url_for('home')))
        
        # Copiar todas las cookies del backend al frontend
        for cookie_name, cookie_value in response.cookies.items():
            resp.set_cookie(
                cookie_name,
                cookie_value,
                httponly=True,
                samesite='Lax'
            )
        flash('Inicio de sesión exitoso', 'success')
        return resp
    else:
        flash('Credenciales inválidas', 'error')
        return redirect(url_for('auth'))

@app.route('/categoria/<nombre>')
@jwt_required(optional=True, locations=['cookies'])
def categoria(nombre):
    """Muestra servicios filtrados por categoría con opciones de filtrado"""
    data = get_jwt()    
    user_data = data if data else None

    # Obtener parámetros de filtro
    ubicacion_seleccionada = request.args.get('ubicacion', '')

    # Obtener servicios filtrados
    servicios = obtener_servicios_por_categoria(nombre, ubicacion_seleccionada if ubicacion_seleccionada else None)
    
    # Obtener ubicaciones para el filtro
    ubicaciones = obtener_ubicaciones()
    
    # Obtener total de servicios sin filtros
    total_servicios = len(obtener_servicios_por_categoria(nombre))

    return render_template(
        'categoria.html',
        categoria_nombre=nombre,
        servicios=servicios,
        total_servicios=total_servicios,
        ubicaciones=ubicaciones,
        ubicacion_seleccionada=ubicacion_seleccionada,
        data=user_data
    )    

@app.route('/servicio/id/<string:id>')
@jwt_required(locations=['cookies'], optional=True)
def servicio(id):
    data = get_jwt()    
    user_data = data if data else None
    
    servicio = obtener_servicio_por_id(id)
    
    if servicio:
        return render_template('servicio.html', servicio=servicio, data=user_data)
    else:
        return redirect('error')
    
@app.route('/checkout/<string:id>')
@jwt_required(locations=['cookies'], optional=True)
def checkout(id):
  try:

    data = get_jwt()    
    user_data = data if data else None
    
    if user_data is None:
        return render_template('auth.html')
    
    servicio = obtener_servicio_por_id(id)

    if servicio:
        return render_template('checkout.html', servicio=servicio, data=user_data)
    else:
        return render_template('404.html'), 404
  except Exception as e:
    print(e)
    return render_template('404.html'), 404
      

    
@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)
