from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)


API_BASE ="http//localhost:500"


@app.route('/')
def home():
  return render_template('base/base.html')

@app.route('/register')
def reg():
  return render_template('register.html')

@app.route('/loguin', methods=['GET', 'POST'])
def Loguin():
    if request.method == 'POST':
        nombre = request.form['fnombre']         
        contraseña = request.form['fcontraseña'] 

        
        if nombre == "admin" and contraseña == "1234":
            return "Inicio de sesión exitoso"
        else:
            return "Nombre o contraseña incorrectos"

    
    return render_template('formulario.html')


@app.route('/formulario', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['fnewUsername']
        email = request.form['femail']
        contraseña = request.form['fnewpassword']
        direccion = request.form.get('fnewDirección')
        edad = request.form.get('fnewEdad')
        servicios = request.form.get('fnewServicios')
        empresa = request.form.get('fnewEmpresa')

        
        return f"Usuario {nombre} registrado con éxito (Email: {email})"

    return render_template('formulario.html')

@app.route("/mis-reservas")


@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404
if __name__ == '__main__':
    app.run("localhost", port= 5001, debug=True)