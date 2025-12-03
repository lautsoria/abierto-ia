from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
import os

from back_calls.reservas import *
from back_calls.servicios import obtener_servicio_por_id


reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route("/")
@jwt_required(locations=['cookies'])
def mis_reservas():
    user_data = get_jwt()
    usuario_id = get_jwt_identity()
    rol = user_data['rol']

    if rol == "admin":
        response = requests.get(f"{BACKEND_URL}/reservas/todas")  
    else:    
        response = requests.get(f"{BACKEND_URL}/reservas", params={"usuario_id":usuario_id, "rol":rol})

    if response.status_code != 200:
        return "Usuario no encontrado", 404

    reservas = response.json()

    return render_template("reservas.html", reservas=reservas, data=user_data, rol=rol), 201



@reservas_bp.route('/realizada/<string:id_reserva>', methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
def realizada(id_reserva):

    # verificar que el usuario autenticado sea el dueño de la reserva
    data = get_jwt()
    usuario_id = get_jwt_identity()

    response_reserva = requests.get(f"{BACKEND_URL}/reservas/{id_reserva}")
    if response_reserva.status_code != 200:
        return "Reserva no encontrada", 404

    datos_reserva = response_reserva.json()
    usuario_reserva = datos_reserva.get("usuario_id")

    if usuario_id != usuario_reserva:
        return "usuario incorrecto", 401

    # si es post
    if request.method == "POST":
        estrellas = int(request.form.get("puntuacion"))
        descripcion = request.form.get("resena")

        servicio_id = datos_reserva.get("servicio_id")

        payload = {
            "estrellas": estrellas,
            "descripcion": descripcion,
            "usuario_id":usuario_id,
            "servicio_id":servicio_id,
            "reserva_id":id_reserva
        }

        response = requests.post(
            f"{BACKEND_URL}/resenas",
            json=payload
        )

        if response.status_code != 200:
            if response.status_code == 409:
                flash('Ya has dejado una reseña para este servicio', 'warning')
                return redirect(url_for('reservas.mis_reservas'))
            flash('Error al enviar la reseña', 'error')
            return redirect(url_for('reservas.mis_reservas'))

        flash('Reseña enviada exitosamente', 'success')
        return redirect(url_for('home'))
    
    # confirmar el servicio con el id de reserva
    response = requests.post(f"{BACKEND_URL}/reservas/confirmar-servicio/{id_reserva}")
    if response.status_code != 200:
        return "error desconocido", 404

    # si el usuario solo abrió la página (GET)
    return render_template("confirmado.html", reserva=id_reserva, data=data)



def generar_qr(id_reserva):
    base_url = os.getenv('PUBLIC_URL', 'http://localhost:5000')
    url = f"{base_url}/reservas/realizada/{id_reserva}"
    qr = qrcode.make(url)
    qr_route = f"static/images/qr_reservas/qr_reserva_{id_reserva}.png"
    qr.save(qr_route)
    return f"images/qr_reservas/qr_reserva_{id_reserva}.png"

@reservas_bp.route('/generar-qr')
@jwt_required(locations=['cookies'])
def qr():
    data = get_jwt()

    if data['rol'] != 'proveedor':
        return render_template('404.html'), 401

    id_reserva = request.args.get('id_reserva')
    if not id_reserva:  
        return "Falta id_reserva", 400
    
    response = requests.get(f"{BACKEND_URL}/reservas/{id_reserva}")
    if response.status_code != 200:  
        return "Reserva no encontrada", 404  
    
    qr_confirmacion = generar_qr(id_reserva)
    return render_template("qr.html", qr_path=qr_confirmacion, data=data) 



@reservas_bp.route('/checkout/<string:id>')
@jwt_required(locations=['cookies'])
def checkout(id):
  try:
    data = get_jwt()    
    user_data = data if data else None
    
    # if user_data is None:
    #     return render_template('auth.html'), 401
    
    servicio = obtener_servicio_por_id(id, horarios=True)
    print(servicio)
    reservas = no_disponibles(id)

    if servicio:
        return render_template('checkout.html', servicio=servicio, reservas=reservas, data=user_data)
    else:
        return render_template('404.html'), 404
  except Exception as e:
    print(e)
    return render_template('404.html'), 404



@reservas_bp.route('/reserva/<string:id_servicio>', methods=['POST'])
@jwt_required(locations=['cookies'])
def crear_reserva(id_servicio):
    data = get_jwt()
    user_data = data if data else None
    print(user_data)

    if user_data is None:
        return redirect(url_for('auth.auth'))

    user_id = get_jwt_identity()
    servicio_id = id_servicio
    fecha = request.form.get('fecha')
    horario = request.form.get('hora')
    direccion = request.form.get('direccion')
    notas = request.form.get('notas_direccion', '')
    mensaje = request.form.get('mensaje', '')
    comentarios = f"{notas} {mensaje}".strip()

    response = reservar(user_id, servicio_id, fecha, horario, direccion, comentarios)
    
    if response and response.status_code == 201:
        reserva_data = response.json()
        reserva_id = reserva_data.get('id')
        flash('Reserva confirmada exitosamente', 'success')
        return redirect(url_for('reservas.reserva', id=reserva_id))
    else:
        flash('Error al registrar la reserva', 'error')
        return redirect(url_for('reservas.checkout', id=servicio_id))

    

@reservas_bp.route('/reserva/<string:id>')
@jwt_required(locations=['cookies'])
def reserva(id):
    data = get_jwt()
    user_data = data if data else None
    
    reserva = obtener_reserva_por_id(id)
    
    return render_template('reserva.html', reserva=reserva, data=user_data)



@reservas_bp.route('/cancelar_reserva/<string:id>', methods=['POST'])
@jwt_required(locations=['cookies'])
def cancelar(id):
    data = get_jwt()
    user_id = get_jwt_identity()

    if data['rol'] == 'proveedor':
        cancelar = cancelar_reserva(id)
    
    if data['rol'] == 'cliente':
        cancelar = cancelar_reserva(id, user_id)

    return mis_reservas()