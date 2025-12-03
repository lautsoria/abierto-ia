from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, JWTManager, get_jwt
from flask_cors import CORS
import os
from dotenv import load_dotenv

from static.icons import icons
from back_calls.servicios import obtener_servicios_destacados
from back_calls.categorias import obtener_categorias, obtener_cantidad_categoria


from routes.auth import auth_bp as auth
from routes.reservas import reservas_bp as reservas
from routes.usuarios import usuarios_bp as usuarios
from routes.servicios import servicios_bp as servicios
from routes.categorias import categorias_bp as categorias


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

# manejamos que hacer cuando el token no existe o es invalido
@jwt.unauthorized_loader
@jwt.expired_token_loader
@jwt.invalid_token_loader
def unauthorized_token(callback=None, error=None):
    next_url = request.url
    print(f"Unauthorized access to: {next_url}")
    return redirect(url_for('auth.auth', next=next_url))

@app.route('/')
@jwt_required(locations=['cookies'], optional=True)
def home():
    data = get_jwt()
    user_data = data if data else None

    servicios = obtener_servicios_destacados()
    print(servicios)
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

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(reservas, url_prefix="/reservas")
app.register_blueprint(servicios, url_prefix="/servicios")
app.register_blueprint(categorias, url_prefix="/categorias")
app.register_blueprint(usuarios, url_prefix="/usuarios")


@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port=1234, debug=True)


