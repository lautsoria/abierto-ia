from flask import Blueprint, jsonify, request
from db.db import db_conn
import uuid

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
        
        reserva_id = str(uuid.uuid4())
        # crea la reserva
        query = """
            INSERT INTO reservas (id, usuario_id, servicio_id, fecha_servicio, hora_servicio, direccion, comentarios_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            reserva_id,
            data['usuario_id'],
            data['servicio_id'],
            data['fecha_servicio'],
            int(data['hora_servicio'].split(':')[0]),
            data['direccion'],
            data['comentarios_cliente']
        ))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Reserva creada exitosamente',
            'id': reserva_id
        }), 201
        
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


# reservas de un usuario/provee
@reservas_bp.route('', methods=['GET'])
def get_mis_reservas():
    try:
        usuario_id = request.args.get('usuario_id')
        rol = request.args.get('rol')
        print(usuario_id, rol)
        
        if not usuario_id:
            return jsonify({'error': 'usuario_id es requerido (temporal)'}), 400

        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        # segun rol del usuario
        cursor.execute("""
                       SELECT r.rol 
                       FROM roles r
                       JOIN usuarios u
                       ON u.rol_id = r.id
                       WHERE u.id = %s
                       """, (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if rol == 'cliente':
            print('Buscando reservas de cliente')
            # Si es cliente, mostrar sus reservas como cliente
            query = """
                SELECT 
                    r.*,
                    s.nombre as servicio_nombre,
                    s.precio as servicio_precio,
                    p.descripcion as proveedor_descripcion,
                    u.usuario as proveedor_nombre,
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
            
        elif rol == 'proveedor':
            print('Buscando reservas de proveedor')
            # Si es proveedor, mostrar reservas de sus servicios
            query = """
                    SELECT 
                        r.*,
                        s.nombre as servicio_nombre,
                        s.precio as servicio_precio,
                        u.usuario as cliente_nombre,
                        u.email as cliente_email,
                        c.nombre as categoria
                    FROM reservas r
                    INNER JOIN servicios s ON r.servicio_id = s.id
                    INNER JOIN proveedores p ON s.proveedor_id = p.id
                    INNER JOIN usuarios u ON r.usuario_id = u.id
                    INNER JOIN categorias c ON s.categoria_id = c.id
                    WHERE p.usuario_id = %s
                    ORDER BY r.fecha_reserva DESC
            """
            cursor.execute(query, (usuario_id,))

        
        reservas = cursor.fetchall()
        print(reservas)
        
        cursor.close()
        conn.close()
        
        return jsonify(reservas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ver todas las reservas,solo admins
@reservas_bp.route('/todas')
def get_all_reservas():
    try:
        usuario_id = request.json.values()
        
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT r.rol 
                       FROM roles r
                       JOIN roles_usuarios ru
                       ON r.id = ru.rol_id
                       JOIN usuarios u
                       ON ru.usuario_id = u.id
                       WHERE u.id = %s
                       """, (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
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
def get_reserva(id):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)  
        
        query = """
            SELECT 
                r.*,
                s.nombre AS servicio_nombre,
                s.descripcion AS servicio_descripcion,
                s.precio AS servicio_precio,
                uc.usuario AS cliente_usuario,
                uc.email AS cliente_email,
                up.usuario AS proveedor_usuario,
                p.telefono AS proveedor_telefono,
                p.ubicacion AS proveedor_ubicacion,
                c.nombre AS categoria
            FROM reservas r
            INNER JOIN servicios s ON r.servicio_id = s.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios uc ON r.usuario_id = uc.id
            INNER JOIN usuarios up ON p.usuario_id = up.id
            INNER JOIN categorias c ON s.categoria_id = c.id
            LEFT JOIN barrios_usuarios bu ON up.id = bu.usuario_id
            LEFT JOIN barrios b ON bu.barrio_id = b.id
            WHERE r.id = %s
            GROUP BY r.id
        """
        
        cursor.execute(query, (id,))
        reserva = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not reserva:
            return jsonify({'error': 'Reserva no encontrada'}), 404
        
        # Convert Decimal to float for JSON serialization
        if reserva.get('servicio_precio'):
            reserva['servicio_precio'] = float(reserva['servicio_precio'])
        
        # Format datetime fields
        if reserva.get('fecha_reserva'):
            reserva['fecha_reserva'] = reserva['fecha_reserva'].isoformat()
        if reserva.get('fecha_servicio'):
            reserva['fecha_servicio'] = reserva['fecha_servicio'].isoformat()
        
        return jsonify(reserva), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@reservas_bp.route('/confirmar-servicio/<string:id_reserva>/<string:token>', methods=['POST'])
def confirmar_servicio(id_reserva, token):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT * FROM reservas
                WHERE id = %s
                """
        cursor.execute(query, (id_reserva,))
        reserva = cursor.fetchone()

        if reserva is None:
            return jsonify({"error": "QR inválido o expirado"}), 400

        # actualizar estado
        update = """
                 UPDATE reservas SET estado = 'realizado'
                 WHERE id = %s
                 """
        cursor.execute(update, (id_reserva,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Servicio confirmado correctamente"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# @reservas_bp.route('/<string:id_reserva>/token')
# def get_reserva_token(id_reserva):
#     try:
#         if not id_reserva:
#             return jsonify({"error": "Falta id_reserva"}), 400

#         conn = db_conn()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT token_qr FROM reservas WHERE id = %s", (id_reserva,))
#         data = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if not data:
#             return jsonify({'error': 'Reserva no encontrada'}), 404

#         return jsonify({
#             "id_reserva": id_reserva,
#             "token_qr": data["token_qr"]
#         }), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
@reservas_bp.route('/<string:id>', methods=['PUT', 'GET'])
def reserva(id):
    if request.method == 'PUT':
        return update_reserva(id)

    if request.method == 'GET':
        return get_reserva(id)
    
    return jsonify({'error': 'Método no permitido'}), 405



@reservas_bp.route('/servicio/<string:id>')
def servicio_reservas(id):
    try:        
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                r.*
            FROM reservas r
            WHERE r.servicio_id = (%s) AND r.estado = 'pendiente' 
            ORDER BY r.fecha_reserva DESC
        """
        cursor.execute(query, (id,))
        
        reservas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        for reserva in reservas:
            reserva['fecha_reserva'] = reserva['fecha_reserva'].isoformat()
            reserva['fecha_servicio'] = reserva['fecha_servicio'].isoformat()
            reserva['hora_servicio'] = f"{int(reserva['hora_servicio']):02d}:00"

        return jsonify(reservas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
