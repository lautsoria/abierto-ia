# Esta es la aplicacion del back.

# aca definimos las rutas de la aplicacion, y las configuraciones del servidor

# - /auth
# - /proveedores
# - /clientes
# - /reservas
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp as auth
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# literalmente lo que vos quieras de 32 caracteres
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app) 

app.register_blueprint(auth, url_prefix="/auth")
# app.register_blueprint(proveedores, url_prefix="/proveedores")
# app.register_blueprint(clientes, url_prefix="/clientes")
# app.register_blueprint(reservas, url_prefix="/reservas")

if __name__ == "__main__":
    app.run(port=5500, debug=True)