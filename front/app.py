from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
import os

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

@app.route('/home')
@jwt_required(locations=['cookies'])
def home():
    data = get_jwt_identity()
    print(f'User {data} logged with valid token')
    return render_template('base/base.html')

@app.route('/')
def reg():
  try:
    verify_jwt_in_request(locations=['cookies'])
    return redirect(url_for('home'))
  except:
    return render_template('register.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['fnombre']
        apellido = request.form['fapellido']
        celular = request.form['fcelular']
        direccion = request.form['fdirec']
        dni = request.form['fdni']
        # Acá podés procesar o guardar los datos
        return f"Datos recibidos: {nombre}, {apellido}, {celular}, {direccion}, {dni}"
    return render_template('formulario.html')

@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)