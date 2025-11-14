from flask import Flask, render_template, request, redirect, flash, make_response
import os
import requests

app = Flask(__name__)

@app.before_request
def verify_token():
    public_routes = ['reg', 'error', 'static']
    if request.endpoint is None or request.endpoint in public_routes:
        return
    
    token = request.cookies.get('access_token')
    print(token)
    if not token:
        print('No existe token')
        return redirect('/')
    
    # validamos el token con el backend (NUNCA SE HACE EN EL FRONT)
    try:
        response = requests.get('http://localhost:5500/auth/validate', 
                              cookies={'access_token': token},
                              timeout=2)
        
        print(response)

        if response.status_code != 200:
            # si el token no es valido (expiro u otra cosa) lo borramos
            print('Token invalido')
            resp = make_response(redirect('/'))
            resp.set_cookie('access_token', '', expires=0)
            return resp
    except Exception as e:
        # ante cualquier error lo devolvemos al login para evitar problemas :)
        print(f'Error {e}')
        return redirect('/')

@app.route('/home')
def home():
    return render_template('base/base.html')

@app.route('/')
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

@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)