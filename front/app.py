from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import jwt_required, JWTManager, verify_jwt_in_request, get_jwt, get_jwt_identity
from flask_cors import CORS
import os
from dotenv import load_dotenv
import qrcode

from static.icons import icons
from back_calls.calls import *


env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_NAME'] = 'access_token_cookie'

jwt = JWTManager(app)
CORS(app)

BACKEND_URL = 'http://localhost:5500'

# manejamos que hacer cuando el token no existe o es invalido
@jwt.unauthorized_loader
@jwt.expired_token_loader
@jwt.invalid_token_loader
def unauthorized_token(callback=None, error=None):
    next_url = request.url
    print(f"Unauthorized access to: {next_url}")
    return redirect(url_for('auth', next=next_url))


@app.route('/')
@jwt_required(locations=['cookies'], optional=True)
def home():
    data = get_jwt()
    user_data = data if data else None

    servicios = obtener_servicios_destacados()
    categorias = obtener_categorias()
    categorias_completas = []
    if categorias:
        for cat in categorias:
            nombre = cat["nombre"]
            cantidad = obtener_cantidad_categoria(nombre)
            categorias_completas.append({
                "nombre": nombre,
                "total_profesionales": cantidad,
                "icono": icons.get(nombre, "📁") 
            })

    return render_template('home.html', servicios=servicios, categorias=categorias_completas, data=user_data)


@app.route("/reservas")
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


@app.route('/confirmar-servicio/<string:id_reserva>', methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
def confirmar_servicio(id_reserva): 

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
            "servicio_id":servicio_id
        }

        response = requests.post(
            f"{BACKEND_URL}/resenas",
            json=payload
        )

        if response.status_code != 200:
            return "Error al enviar la reseña", 400

        return redirect(url_for('home'))
    
    # confirmar el servicio con el id de reserva
    response = requests.post(f"{BACKEND_URL}/reservas/confirmar-servicio/{id_reserva}")
    if response.status_code != 200:
        return "error desconocido", 404

    # si el usuario solo abrió la página (GET)
    return render_template("confirmado.html", reserva=id_reserva, data=data)
 

def generar_qr(id_reserva):
    base_url = os.getenv('PUBLIC_URL', 'http://localhost:5000')
    url = f"{base_url}/confirmar-servicio/{id_reserva}"
    qr = qrcode.make(url)
    qr.save(f"static/qr_reserva_{id_reserva}.png")
    return f"static/qr_reserva_{id_reserva}.png"

@app.route('/generar-qr')
def generarqr():
    id_reserva = request.args.get('id_reserva')
    if not id_reserva:  
        return "Falta id_reserva", 400
    
    response = requests.get(f"{BACKEND_URL}/reservas/{id_reserva}")
    if response.status_code != 200:  
        return "Reserva no encontrada", 404  
    
    data = response.json()
    qr_confirmacion = generar_qr(id_reserva)
    return render_template("qr.html", qr_path=qr_confirmacion)  


@app.route('/mi-perfil')
@jwt_required(locations=['cookies'])
def perfil():
    data = get_jwt()
    usuario_id = get_jwt_identity()

    response = requests.get(f"{BACKEND_URL}/usuarios/{usuario_id}")

    if response.status_code != 200:
        return "Usuario no encontrado", 404

    if data['rol'] == "proveedor":
        response = requests.get(f"{BACKEND_URL}/proveedores/{usuario_id}")
        
        if response.status_code != 200:
            return "Proveedor no encontrado", 404
        
        datos_user = response.json()
        
    
    return render_template(
        "editar_perfil.html",
        usuario=datos_user,
        data=data
    )


@app.route('/auth')
def auth():
  try:
    verify_jwt_in_request(locations=['cookies'])
    return redirect(url_for('home'))
  except:
    # Si el token es inválido o no existe, limpiar la cookie
    next = request.args.get('next', url_for('home'))
    resp = make_response(render_template('auth.html', next=next))
    resp.set_cookie('access_token_cookie', '', max_age=0)
    return resp


@app.route('/register', methods=['POST'])
def register():
    user = request.form.get("newUser")
    email = request.form.get("email")
    password = request.form.get("newPassword")
    repeatPassword = request.form.get("newPassword2")
    provider = request.form.get("isProveedor") == 'true'
    next_url = request.args.get('next', url_for('home'))

    if password != repeatPassword:
        flash('Las contraseñas no coinciden', 'error')
        return redirect(url_for('auth'))

    response = registrar_usuario(user, email, password, provider)
    
    if response and response.status_code == 200:
        if provider:
            # si el proveedor se registra
            # debera completar los datos de su perfil
            resp = make_response(redirect(url_for('registrar_servicio')))
        else:
            resp = make_response(redirect(next_url))
        
        # Copiar todas las cookies del backend al frontend
        for cookie_name, cookie_value in response.cookies.items():
            resp.set_cookie(
                cookie_name,
                cookie_value,
                httponly=True,
                samesite='Lax'
            )
        flash('Usuario creado con éxito', 'success')
        return resp
    else:
        flash('Error al registrar el usuario', 'error')
        return redirect(url_for('auth'))


@app.route('/login', methods=['POST'])
def login():
    credential = request.form.get("credential")
    password = request.form.get("password")
    next_url = request.args.get('next', url_for('home'))

    response = login_usuario(credential, password)
    
    if response and response.status_code == 200:
        # Obtener las cookies del backend y pasarlas al frontend
        print(next_url)      
        resp = make_response(redirect(next_url))
        
        # Copiar todas las cookies del backend al frontend
        for cookie_name, cookie_value in response.cookies.items():
            resp.set_cookie(
                cookie_name,
                cookie_value,
                httponly=True,
                samesite='Lax'
            )
        flash('Inicio de sesión exitoso', 'success')
        return resp
    else:
        flash('Credenciales inválidas', 'error')
        return redirect(url_for('auth'))


@app.route('/categoria/<nombre>')
@jwt_required(optional=True, locations=['cookies'])
def categoria(nombre):
    """Muestra servicios filtrados por categoría con opciones de filtrado"""
    data = get_jwt()    
    user_data = data if data else None

    # Obtener parámetros de filtro
    ubicacion_seleccionada = request.args.get('ubicacion', '')

    # Obtener servicios filtrados
    servicios = obtener_servicios_por_categoria(nombre, ubicacion_seleccionada if ubicacion_seleccionada else None)
    
    # Obtener ubicaciones para el filtro
    ubicaciones = obtener_ubicaciones()
    
    # Obtener total de servicios sin filtros
    total_servicios = len(obtener_servicios_por_categoria(nombre))

    return render_template(
        'categoria.html',
        categoria_nombre=nombre,
        servicios=servicios,
        total_servicios=total_servicios,
        ubicaciones=ubicaciones,
        ubicacion_seleccionada=ubicacion_seleccionada,
        data=user_data
    )    


# vista tipo producto de un servicio 
@app.route('/servicio/id/<string:id>')
@jwt_required(locations=['cookies'], optional=True)
def servicio(id):
    data = get_jwt()    
    user_data = data if data else None
    
    url = request.url
    servicio = obtener_servicio_por_id(id)
    resenas = obtener_resenas_servicio(id)
    
    if servicio:
        return render_template('servicio.html', servicio=servicio, resenas=resenas, data=user_data, url=url)
    else:
        return redirect('error')
    

@app.route('/checkout/<string:id>')
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


@app.route('/reserva/<string:servicio>', methods=['POST'])
@jwt_required(locations=['cookies'])
def crear_reserva(servicio):
    data = get_jwt()
    user_data = data if data else None
    print(user_data)

    if user_data is None:
        return redirect(url_for('auth'))

    user_id = get_jwt_identity()
    servicio_id = servicio
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
        return redirect(f'/reserva/{reserva_id}')
    else:
        flash('Error al registrar la reserva', 'error')
        return redirect(url_for('checkout', id=servicio_id))
    

@app.route('/reserva/<string:reserva_id>')
@jwt_required(locations=['cookies'])
def detalle_reserva(reserva_id):
    data = get_jwt()
    user_data = data if data else None
    
    reserva = obtener_reserva_por_id(reserva_id)
    
    return render_template('reserva.html', reserva=reserva, data=user_data)


@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404


@app.route('/usuarios/<int:id>/eliminar', methods=['POST'])
def eliminar_usuario(id):
    response = requests.delete(f"{BACKEND_URL}/usuarios/{id}/eliminar")

    if response.status_code != 200:
        return "Usuario no encontrado", 404
    
    
    return redirect(url_for('ver_usuarios'))


@app.route('/usuarios')
@jwt_required(locations=['cookies'])
def ver_usuarios():
    data = get_jwt()
    usuario_id = get_jwt_identity()
    
    user_data = data if data else None

    if user_data is None:
        return redirect(url_for('auth'))
    
    response_user = requests.get(f"{BACKEND_URL}/usuarios/{usuario_id}")

    if response_user.status_code != 200:
        return "Usuario no encontrado", 404

    datos_user = response_user.json()

    if datos_user.get("rol") != "admin":
        return "permiso denegado", 404
    
    response = requests.get(f'{BACKEND_URL}/usuarios/todos')
    
    if response.status_code != 200:
        return "Usuarios no encontrados", 404
    
    usuarios = response.json()

    return render_template('usuarios.html',usuarios=usuarios)

@app.route('/todos_servicios')
@jwt_required(locations=['cookies'])
def servicios():
    data = get_jwt()
    usuario_id = get_jwt_identity()
    
    user_data = data if data else None

    if user_data is None:
        return redirect(url_for('auth'))
    
    response_user = requests.get(f"{BACKEND_URL}/usuarios/{usuario_id}")

    if response_user.status_code != 200:
        return "Usuario no encontrado", 404

    datos_user = response_user.json()

    if datos_user.get("rol") != "admin":
        return "permiso denegado", 404
    
    response = requests.get(f'{BACKEND_URL}/servicios/todos')
    
    if response.status_code != 200:
        return "Usuarios no encontrados", 404
    
    servicios = response.json()

    return render_template('servicios.html',servicios=servicios)

@app.route('/usuarios/<int:id>/eliminar', methods=['POST'])
def eliminar_servicio(id):
    response = requests.delete(f"{BACKEND_URL}/servicio/{id}/eliminar")

    if response.status_code != 200:
        return "Usuario no encontrado", 404
    
    
    return redirect(url_for('listar_usuarios'))

@app.route('/buscar')
def buscar_servicios():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("resultados_busqueda.html", servicios=[])

    response = requests.get(f"{BACKEND_URL}/servicios/buscar", params={"q": query})

    if response.status_code != 200:
        return render_template("resultados_busqueda.html", servicios=[])

    servicios = response.json()

    return render_template("resultados_busqueda.html", servicios=servicios, query=query)

@app.route('/registrar_servicio', methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
def registrar_servicio():
    if get_jwt()['rol'] == 'proveedor': 
        proveedor_id = get_jwt_identity()
        if request.method == 'POST':
            
            res = requests.post(f'{BACKEND_URL}/servicios', json={
                "proveedor_id": proveedor_id,
                "categoria_id": request.form.get('categoria_id'),
                "nombre": request.form.get('nombre'),
                "descripcion": request.form.get('descripcion'),
                "precio":  request.form.get('precio'),
                "hora_inicio": request.form.get('hora_inicio'),
                "hora_fin": request.form.get('hora_fin'),
                "duracion": request.form.get('duracion')
            })

            if res.status_code != 200:
                return {"message": "Error al cargar el servicio"}, 400
                
            return redirect(url_for('home'))
        
        if request.method == 'GET':
            data = get_jwt()
            categorias = obtener_categorias()
            return render_template('registrar_servicio.html', categorias=categorias, data=data)

    return render_template('404.html'), 401
    

@app.route('/mis_servicios', methods=['GET'])
@jwt_required(locations=['cookies'])
def mis_servicios():
    data = get_jwt()
    proveedor_id = get_jwt_identity()
    
    # Verificar que el usuario sea proveedor
    if data.get('rol') != 'proveedor':
        return render_template('404.html'), 401

    if request.method == 'GET':
        servicios = obtener_servicios_proveedor(proveedor_id)
        
        return render_template(
            'mis_servicios.html',
            servicios=servicios,
            data=data
        )


@app.route('/editar_servicio/<string:id>')
@jwt_required(locations=['cookies'])
def editar_servicio(id):
    data = get_jwt()
    proveedor_id = get_jwt_identity()
    
    if data.get('rol') != 'proveedor':
        return render_template('404.html'), 401
    
    servicio = obtener_servicio_por_id(id)
    
    if not servicio or servicio.get('proveedor_id') != proveedor_id:
        return render_template('404.html'), 404
    
    categorias = obtener_categorias()
    
    return render_template(
        'editar_servicio.html',
        servicio=servicio,
        categorias=categorias,
        data=data
    )


@app.route('/actualizar_servicio/<string:id>', methods=['POST'])
@jwt_required(locations=['cookies'])
def actualizar_servicio(id):
    data = get_jwt()
    proveedor_id = get_jwt_identity()
    
    if data.get('rol') != 'proveedor':
        return render_template('404.html'), 401
    
    # Verificar que el servicio pertenece al proveedor
    servicio = obtener_servicio_por_id(id)
    if not servicio or servicio.get('proveedor_id') != proveedor_id:
        return render_template('404.html'), 404
    
    res = requests.put(f'{BACKEND_URL}/servicios/{id}', json={
        "proveedor_id": proveedor_id,
        "categoria_id": request.form.get('categoria_id'),
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "precio": request.form.get('precio'),
        "hora_inicio": request.form.get('hora_inicio'),
        "hora_fin": request.form.get('hora_fin'),
        "duracion": request.form.get('duracion')
    })
    
    if res.status_code == 200:
        flash('Servicio actualizado exitosamente', 'success')
    else:
        flash('Error al actualizar el servicio', 'error')
    
    return redirect(url_for('mis_servicios'))


@app.route('/eliminar_servicio/<string:id>')
@jwt_required(locations=['cookies'])
def eliminar_servicio_view(id):
    data = get_jwt()
    proveedor_id = get_jwt_identity()
    
    if data.get('rol') != 'proveedor':
        return render_template('404.html'), 401
    
    # Verificar que el servicio pertenece al proveedor
    servicio = obtener_servicio_por_id(id)
    if not servicio or servicio.get('proveedor_id') != proveedor_id:
        return render_template('404.html'), 404
    
    res = requests.delete(f'{BACKEND_URL}/servicios/{id}')
    
    if res.status_code == 200:
        flash('Servicio eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el servicio', 'error')
    
    return redirect(url_for('mis_servicios'))

# TODO
@app.route('/cancelar_reserva/<string:id>', methods=['POST'])
@jwt_required(locations=['cookies'])
def cancelar_reserva(id):
    return

# TODO
@app.route('/logout')
@jwt_required(locations=['cookies'])
def logout():
    return 


if __name__ == '__main__':
    app.run("localhost", port=1234, debug=True)


