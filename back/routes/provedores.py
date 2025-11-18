"""GET /proveedores

    Descripción: Devuelve una lista de todos los proveedores.
    Filtros (Query Params): Se puede filtrar por servicio. Ej: ?servicio=plomeria
    Autorización: Pública.

GET /proveedores/<id>

    Descripción: Devuelve los detalles de un proveedor específico por su ID.
    Autorización: Pública.

POST /proveedores

    Descripción: Crea un nuevo proveedor en el sistema.
    Autorización: Debe presentar un certificado valido.

PUT /proveedores/<id>

    Descripción: Actualiza la información de un proveedor.
    Autorización: Solo proveedores."""

from flask import Blueprint, jsonify, request
from db.db import db_conn

proveedores_bp = Blueprint('proveedores', __name__)

# listar provee
@proveedores_bp.route('/')
def get_proveedores():
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener filtro de servicio si existe
        servicio = request.args.get('servicio')
        
        if servicio:
            # filtro categoria
            query = """
                SELECT DISTINCT p.*, u.usuario as nombre_usuario, u.email
                FROM proveedores p
                INNER JOIN usuarios u ON p.usuario_id = u.id
                INNER JOIN servicios s ON s.proveedor_id = p.id
                INNER JOIN categorias c ON s.categoria_id = c.id
                WHERE LOWER(c.nombre) = LOWER(%s)
            """
            cursor.execute(query, (servicio,))
        else:
            # devuelve todos (no filtro)
            query = """
                SELECT p.*, u.usuario as nombre_usuario, u.email
                FROM proveedores p
                INNER JOIN usuarios u ON p.usuario_id = u.id
            """
            cursor.execute(query)
        
        proveedores = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(proveedores), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# provedor por id
@proveedores_bp.route('/<int:id>')
def get_proveedor(id):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        # datos del provedor
        query = """
            SELECT p.*, u.usuario as nombre_usuario, u.email
            FROM proveedores p
            INNER JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.id = %s
        """
        cursor.execute(query, (id,))
        proveedor = cursor.fetchone()
        
        if not proveedor:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Proveedor no encontrado'}), 404
        
        # servicios del provedor
        query_servicios = """
            SELECT s.*, c.nombre as categoria
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            WHERE s.proveedor_id = %s
        """
        cursor.execute(query_servicios, (id,))
        servicios = cursor.fetchall()
        
        proveedor['servicios'] = servicios
        
        cursor.close()
        conn.close()
        
        return jsonify(proveedor), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# actualizar info de un provedor
@proveedores_bp.route('/<int:id>', methods=['PUT'])
def update_proveedor(id):
    try:
        data = request.get_json()
        
        # TODO: Validar que el usuario sea proveedor
        # Por ahora, comentamos esta validación
        # if not es_proveedor(request):
        #     return jsonify({'error': 'No autorizado'}), 403
        
        conn = db_conn()
        cursor = conn.cursor()
        
        # si es provedor existente
        cursor.execute("SELECT id FROM proveedores WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Proveedor no encontrado'}), 404
        
        # actualizar campo por campo
        campos_permitidos = ['descripcion', 'ubicacion', 'telefono']
        campos_actualizar = []
        valores = []
        
        for campo in campos_permitidos:
            if campo in data:
                campos_actualizar.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos_actualizar:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        valores.append(id)
        query = f"UPDATE proveedores SET {', '.join(campos_actualizar)} WHERE id = %s"
        
        cursor.execute(query, valores)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Proveedor actualizado exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500