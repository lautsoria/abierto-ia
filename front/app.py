from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('base/base.html')

@app.route('/register')
def reg():
  return render_template('register.html')

@app.route('/formulario', methods=['GET', 'POST'])
def Formulario():
    if request.method == 'POST':
        nombre = request.form['fnombre']
        apellido = request.form['fapellido']
        celular = request.form['fcelular']
        direccion = request.form['fdirec']
        dni = request.form['fdni']
        # Acá podés procesar o guardar los datos
        return f"Datos recibidos: {nombre}, {apellido}, {celular}, {direccion}, {dni}"
    return render_template('formulario.html')

@app.route('/electricismo')
def electricismo():
  return render_template('electricismo.html')
@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)