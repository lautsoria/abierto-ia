from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

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

RESERVAS_MOCK = [
    {
        'id': 1,
        'usuario_id': 1,
        'servicio_id': 1,
        'fecha_reserva': '2025-11-10 14:30:00',
        'fecha_servicio': '2025-11-20 10:00:00',
        'estado': 'pendiente',
        'comentarios_cliente': 'Necesito ayuda urgente con una cañería rota',
        'servicio_nombre': 'Reparación de cañerías',
        'servicio_precio': 5000.00,
        'proveedor_nombre': 'Juan Pérez',
        'proveedor_descripcion': 'Plomero con 15 años de experiencia',
        'categoria': 'Plomería'
    },
    {
        'id': 2,
        'usuario_id': 1,
        'servicio_id': 2,
        'fecha_reserva': '2025-11-08 09:15:00',
        'fecha_servicio': '2025-11-15 14:00:00',
        'estado': 'realizado',
        'comentarios_cliente': 'Instalación de lámpara en el living',
        'servicio_nombre': 'Instalación eléctrica',
        'servicio_precio': 3500.00,
        'proveedor_nombre': 'María López',
        'proveedor_descripcion': 'Electricista matriculada',
        'categoria': 'Electricidad'
    },
    {
        'id': 3,
        'usuario_id': 1,
        'servicio_id': 3,
        'fecha_reserva': '2025-11-05 16:45:00',
        'fecha_servicio': '2025-11-10 09:00:00',
        'estado': 'cancelado',
        'comentarios_cliente': 'Corte de césped y limpieza de jardín',
        'servicio_nombre': 'Mantenimiento de jardín',
        'servicio_precio': 4200.00,
        'proveedor_nombre': 'Carlos Gómez',
        'proveedor_descripcion': 'Jardinero profesional',
        'categoria': 'Jardinería'
    },
    {
        'id': 4,
        'usuario_id': 1,
        'servicio_id': 4,
        'fecha_reserva': '2025-11-12 11:20:00',
        'fecha_servicio': '2025-11-25 16:30:00',
        'estado': 'pendiente',
        'comentarios_cliente': 'Revisión de instalación de gas',
        'servicio_nombre': 'Inspección de gas',
        'servicio_precio': 6500.00,
        'proveedor_nombre': 'Roberto Díaz',
        'proveedor_descripcion': 'Gasista matriculado',
        'categoria': 'Gasista'
    }
]


@app.route("/reservas")
def mis_reservas():
    return render_template("eservas.html", reservas=RESERVAS_MOCK)

@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)