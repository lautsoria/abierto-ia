from flask import Flask
from flask_cors import CORS
from routes.provedores import proveedores_bp
# from routes.auth import auth_bp
# from routes.clientes import clientes_bp
# from routes.reservas import reservas_bp

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
# Registrar los blueprints cuando los crees
# app.register_blueprint(auth_bp, url_prefix='/auth')

# app.register_blueprint(clientes_bp, url_prefix='/clientes')
# app.register_blueprint(reservas_bp, url_prefix='/reservas')

@app.route('/')
def home():
    return {'message': 'API Abierto IA funcionando ✅'}

if __name__ == '__main__':
    app.run(port=5000, debug=True)






