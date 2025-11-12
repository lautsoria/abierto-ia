# Esta es la aplicacion del back.

# aca definimos las rutas de la aplicacion, y las configuraciones del servidor

# - /auth
# - /proveedores
# - /clientes
# - /reservas
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp as auth

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix="/auth")
# app.register_blueprint(proveedores, url_prefix="/proveedores")
# app.register_blueprint(clientes, url_prefix="/clientes")
# app.register_blueprint(reservas, url_prefix="/reservas")

if __name__ == "__main__":
    app.run(port=5000, debug=True)