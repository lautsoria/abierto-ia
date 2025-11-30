from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


from back_calls.servicios import *
from back_calls.categorias import obtener_categorias

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/')
@jwt_required(locations=['cookies'])
def admin_servicios():
    data = get_jwt()
    usuario_id = get_jwt_identity()
    
    if data['rol'] != 'admin':
        return "Acceso denegado", 401
    
    response = requests.get(f'{BACKEND_URL}/servicios/todos')
    
    if response.status_code != 200:
        return "Servicios no encontrados", 404
    
    servicios = response.json()

    return render_template('servicios.html',servicios=servicios, data=data)



@servicios_bp.route('/buscar')
def buscar_servicios():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("resultados_busqueda.html", servicios=[])

    response = requests.get(f"{BACKEND_URL}/servicios/buscar", params={"q": query})

    if response.status_code != 200:
        return render_template("resultados_busqueda.html", servicios=[])

    servicios = response.json()

    return render_template("resultados_busqueda.html", servicios=servicios, query=query)



@servicios_bp.route('/registrar_servicio', methods=['GET', 'POST'])
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
    

@servicios_bp.route('/mis_servicios', methods=['GET'])
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


def editar_servicio_view(id):
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

def editar_servicio(id):
    payload = {
        "id": id,
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "precio": request.form.get("precio"),
        "duracion": request.form.get("duracion"),
    }

    response = requests.patch(f"{BACKEND_URL}/servicios/mod", json=payload)

    if response.status_code not in (200, 204):
        return "Error al actualizar servicio", 400

    return redirect(url_for('servicios.admin_servicios'))

@servicios_bp.route('/editar_servicio', methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
def editar():

    if get_jwt()['rol'] != 'admin':
        return "Acceso denegado", 401

    data = request.form
    id = data.get("id")
    
    if request.method == 'POST':
        return editar_servicio(id)
    
    if request.method == 'GET':
      return editar_servicio_view(id)



@servicios_bp.route('/actualizar_servicio/<string:id>', methods=['POST'])
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
    
    return redirect(url_for('servicios.mis_servicios'))



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
    
    return redirect(url_for('servicios.mis_servicios'))

def eliminar_servicio(id):
    response = requests.delete(f"{BACKEND_URL}/servicios", json={"id": id})

    if response.status_code != 200:
        return "Error al eliminar el servicio", response.status_code
    
    return redirect(url_for('servicios.admin_servicios'))

@servicios_bp.route('/eliminar_servicio', methods=['POST', 'GET'])
@jwt_required(locations=['cookies'])
def eliminar():
    data = request.form
    id = data.get("id")
    
    if request.method == 'POST':
        return eliminar_servicio(id)
    
    if request.method == 'GET':
      return eliminar_servicio_view(id)



# vista tipo producto de un servicio 
@servicios_bp.route('/id/<string:id>')
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
    

