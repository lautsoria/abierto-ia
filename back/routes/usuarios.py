from flask import Blueprint, jsonify, request
from db.db import db_conn

usuarios_bp = Blueprint('usuarios', __name__)

# encontrar usuario por id
def get_usuario(id):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT u.*, r.rol
            FROM usuarios u
            LEFT JOIN roles r ON u.rol_id = r.id
            WHERE u.id = %s
        """
        
        cursor.execute(query, (id,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify(usuario), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/<string:id>', methods=['GET'])
def usuario(id):
    if request.method == 'GET':
        return get_usuario(id)

    
# eliminar usuario por ID
@usuarios_bp.route('/eliminar', methods=['DELETE'])
def eliminar_usuario():
    data = request.json
    print(data)
    id = data['id']
    rol = data['rol']
    
    try:
        conn = db_conn()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM usuarios WHERE id = %s', (id,))
        usuario = cursor.fetchone()
        
        if usuario is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        
        if rol == 'proveedor':
            # hay que borrar las resenas que tienen sus servicios
            cursor.execute("""
                DELETE FROM resenas 
                WHERE servicio_id IN (
                    SELECT id FROM servicios WHERE proveedor_id = %s
                )
            """, (id,))

            # Las reservas de sus servicios
            cursor.execute("""
                DELETE FROM reservas 
                WHERE servicio_id IN (
                    SELECT id FROM servicios WHERE proveedor_id = %s
                )
            """, (id,))

            # Borramos los barrios asociados a sus servicios
            cursor.execute("""
                DELETE FROM barrios_servicios 
                WHERE servicio_id IN (
                    SELECT id FROM servicios WHERE proveedor_id = %s
                )
            """, (id,))

            # Borramos los servicios
            cursor.execute('DELETE FROM servicios WHERE proveedor_id = %s', (id,))

            # lo borramos de proveedores
            cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
            conn.commit()        
        
        if rol == 'cliente':
            # lo mismo pasa para los clientes
            # hay q borrar resenas y reservas
            cursor.execute('DELETE FROM resenas WHERE usuario_id = %s', (id,))
            
            cursor.execute('DELETE FROM reservas WHERE usuario_id = %s', (id,))
            conn.commit()

        # finalmente podemos borrar el usuario
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
        
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al eliminar el usuario'}), 500


@usuarios_bp.route('/todos', methods=['GET'])
def get_usuarios():
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT u.id,
                   u.usuario,
                   u.email,
                   u.fecha_registro,
                   r.rol
            FROM usuarios u
            LEFT JOIN roles r ON u.rol_id = r.id
        """
        
        cursor.execute(query)
        usuarios = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(usuarios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@usuarios_bp.route('/editar_perfil', methods=['PATCH'])
def editar_usuario():
    try:
        data = request.json

        conn = db_conn()
        cursor = conn.cursor()

        update_query = """
            UPDATE usuarios
            SET usuario = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
        """

        cursor.execute(update_query, (
            data['nombre'],
            data['email'],
            data['telefono'],
            data['id']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"status":"Usuario modificado"}, 204

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Error al modificar el usuario'}), 500
    
@usuarios_bp.route('/mod', methods=['PATCH'])
def mod_usuario():
    try:
        data = request.json
        print(data)

        conn = db_conn()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id
                       FROM roles
                       WHERE rol = %s
                       """,
                       (data['rol'],))

        rol_id = cursor.fetchone()[0]

        # 2. UPDATE correcto de la tabla usuarios
        update_query = """
            UPDATE usuarios
            SET usuario = %s,
                email = %s,
                rol_id = %s
            WHERE id = %s
            """

        cursor.execute(update_query, (
            data['nombre'],
            data['email'],
            rol_id,
            data['id']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Usuario modificado correctamente'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Error al modificar el usuario'}), 500


