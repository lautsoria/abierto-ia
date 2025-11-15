from flask import Blueprint, jsonify, request
from db.db import db_conn
from datetime import datetime

reservas_bp = Blueprint('reservas', __name__)

# crear reserva
@reservas_bp.route('/', methods=['POST'])
def create_reserva():
    try:
        data = request.get_json()
        
        # datos
        required_fields = ['servicio_id', 'fecha_servicio']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # TODO: Obtener usuario_id del token JWT(parte de fran)
        # Por ahora, lo tomamos del body (temporal)
        if 'usuario_id' not in data:
            return jsonify({'error': 'usuario_id es requerido (temporal)'}), 400
        
        conn = db_conn()
        cursor = conn.cursor()
        
        # si servicio existente
        cursor.execute("SELECT id FROM servicios WHERE id = %s", (data['servicio_id'],))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Servicio no encontrado'}), 404
        
        # crea la reserva
        query = """
            INSERT INTO reservas (usuario_id, servicio_id, fecha_servicio, comentarios_cliente)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['usuario_id'],
            data['servicio_id'],
            data['fecha_servicio'],
            data.get('comentarios_cliente', '')
        ))
        
        conn.commit()
        reserva_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Reserva creada exitosamente',
            'id': reserva_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# reservas de un usuario/provee
@reservas_bp.route('/mis-reservas')
def get_mis_reservas():
    try:
        # TODO: Obtener usuario_id del token JWT
        # Por ahora, lo tomamos de query params (temporal)
        usuario_id = request.args.get('usuario_id')
        
        if not usuario_id:
            return jsonify({'error': 'usuario_id es requerido (temporal)'}), 400
        
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        # segun rol del usuario
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if usuario['rol'] == 'cliente':
            # Si es cliente, mostrar sus reservas como cliente
            query = """
                SELECT 
                    r.*,
                    s.nombre as servicio_nombre,
                    s.precio as servicio_precio,
                    p.descripcion as proveedor_descripcion,
                    u.nombre as proveedor_nombre,
                    c.nombre as categoria
                FROM reservas r
                INNER JOIN servicios s ON r.servicio_id = s.id
                INNER JOIN proveedores p ON s.proveedor_id = p.id
                INNER JOIN usuarios u ON p.usuario_id = u.id
                INNER JOIN categorias c ON s.categoria_id = c.id
                WHERE r.usuario_id = %s
                ORDER BY r.fecha_reserva DESC
            """
            cursor.execute(query, (usuario_id,))
            
        elif usuario['rol'] == 'proveedor':
            # Si es proveedor, mostrar reservas de sus servicios
            query = """
                SELECT 
                    r.*,
                    s.nombre as servicio_nombre,
                    s.precio as servicio_precio,
                    uc.nombre as cliente_nombre,
                    uc.email as cliente_email,
                    c.nombre as categoria
                FROM reservas r
                INNER JOIN servicios s ON r.servicio_id = s.id
                INNER JOIN proveedores p ON s.proveedor_id = p.id
                INNER JOIN usuarios uc ON r.usuario_id = uc.id
                INNER JOIN categorias c ON s.categoria_id = c.id
                WHERE p.usuario_id = %s
                ORDER BY r.fecha_reserva DESC
            """
            cursor.execute(query, (usuario_id,))
        else:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Rol no válido'}), 400
        
        reservas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(reservas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ver todas las reservas,solo admins
@reservas_bp.route('/')
def get_all_reservas():
    try:
        # TODO: Validar que el usuario sea admin desde el token JWT
        # Por ahora, comentamos esta validación
        # if not es_admin(request):
        #     return jsonify({'error': 'No autorizado'}), 403
        
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                r.*,
                s.nombre as servicio_nombre,
                s.precio as servicio_precio,
                uc.nombre as cliente_nombre,
                uc.email as cliente_email,
                up.nombre as proveedor_nombre,
                c.nombre as categoria
            FROM reservas r
            INNER JOIN servicios s ON r.servicio_id = s.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios uc ON r.usuario_id = uc.id
            INNER JOIN usuarios up ON p.usuario_id = up.id
            INNER JOIN categorias c ON s.categoria_id = c.id
            ORDER BY r.fecha_reserva DESC
        """
        cursor.execute(query)
        
        reservas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(reservas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# mod estado reserva
@reservas_bp.route('/<int:id>', methods=['PUT'])
def update_reserva(id):
    try:
        data = request.get_json()
        
        # TODO: Validar que el usuario sea admin o proveedor de la reserva
        # Por ahora, comentamos esta validación
        # if not es_admin_o_proveedor(request, id):
        #     return jsonify({'error': 'No autorizado'}), 403
        
        conn = db_conn()
        cursor = conn.cursor()
        
        # si la reserva existe
        cursor.execute("SELECT id FROM reservas WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Reserva no encontrada'}), 404
        
        # query campo por campo
        campos_permitidos = ['estado', 'comentarios_cliente', 'fecha_servicio']
        campos_actualizar = []
        valores = []
        
        for campo in campos_permitidos:
            if campo in data:
                campos_actualizar.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos_actualizar:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        # Validar estado si se está actualizando
        if 'estado' in data:
            estados_validos = ['pendiente', 'realizado', 'cancelado']
            if data['estado'] not in estados_validos:
                cursor.close()
                conn.close()
                return jsonify({'error': f'Estado debe ser uno de: {", ".join(estados_validos)}'}), 400
        
        valores.append(id)
        query = f"UPDATE reservas SET {', '.join(campos_actualizar)} WHERE id = %s"
        
        cursor.execute(query, valores)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Reserva actualizada exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# reserva especifica
@reservas_bp.route('/<int:id>')
def get_reserva(id):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                r.*,
                s.nombre as servicio_nombre,
                s.descripcion as servicio_descripcion,
                s.precio as servicio_precio,
                uc.nombre as cliente_nombre,
                uc.email as cliente_email,
                up.nombre as proveedor_nombre,
                p.telefono as proveedor_telefono,
                p.ubicacion as proveedor_ubicacion,
                c.nombre as categoria
            FROM reservas r
            INNER JOIN servicios s ON r.servicio_id = s.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios uc ON r.usuario_id = uc.id
            INNER JOIN usuarios up ON p.usuario_id = up.id
            INNER JOIN categorias c ON s.categoria_id = c.id
            WHERE r.id = %s
        """
        cursor.execute(query, (id,))
        
        reserva = cursor.fetchone()
        
        if not reserva:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Reserva no encontrada'}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify(reserva), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500