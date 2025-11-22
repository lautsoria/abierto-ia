# Esta es la aplicacion del back.

# aca definimos las rutas de la aplicacion, y las configuraciones del servidor

# - /auth
# - /proveedores
# - /clientes
# - /reservas

from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp as auth
from routes.provedores import proveedores_bp as proveedores
from routes.reservas import reservas_bp as reservas
from routes.servicios import servicios_bp as servicios
from routes.categorias import categoria_bp as categorias
from routes.servicios import servicios_bp as servicios
from routes.ubicacion import ubicacion_bp as ubicacion
from routes.resenas import resenas_bp as resenas

from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app, origins=["http://localhost:1234"], supports_credentials=True, methods=['POST', 'GET', 'UPDATE', 'DELETE'])

# configuracion de JWT en nuestra app
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_NAME'] = 'access_token_cookie'

jwt = JWTManager(app) 

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(proveedores, url_prefix='/proveedores')
app.register_blueprint(reservas, url_prefix="/reservas")
app.register_blueprint(servicios, url_prefix="/servicios")
app.register_blueprint(categorias, url_prefix="/categoria")
app.register_blueprint(ubicacion, url_prefix="/ubicacion")
app.register_blueprint(resenas, url_prefix="/resenas")
# app.register_blueprint(usuarios, url_prefix="/usuarios")

if __name__ == "__main__":
    app.run(port=5500, debug=True)
