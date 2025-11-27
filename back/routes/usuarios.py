from flask import Blueprint, jsonify, request
from db.db import db_conn

usuarios_bp = Blueprint('usuarios', __name__)

# encontrar usuario por id
@usuarios_bp.route('/<string:id>')
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
    
# eliminar usuario por ID
@usuarios_bp.route('/<string:id>/eliminar', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        conn = db_conn()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM usuarios WHERE id = %s', (id,))
        usuario = cursor.fetchone()
        
        if usuario is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        
        cursor.execute('DELETE FROM proveedores WHERE usuario_id = %s', (id,))
        
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al eliminar el usuario'}), 500


@usuarios_bp.route('/todos', methods=['GET'])
def get_usuarios():
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT u.*, r.rol
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
    

@usuarios_bp.route('/<string:id>/mod', methods=['PUT'])
def mod_usuario(id):
    try:
        data = request.get_json()

        conn = db_conn()
        cursor = conn.cursor()

        # 1. Verificar si el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id,))
        user = cursor.fetchone()

        if user is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # 2. UPDATE correcto de la tabla usuarios
        update_query = """
            UPDATE usuarios
            SET nombre = %s,
                email = %s,
                rol = %s
            WHERE id = %s
        """

        cursor.execute(update_query, (
            data.get('nombre'),
            data.get('email'),
            data.get('rol'),
            id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Usuario modificado correctamente'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Error al modificar el usuario'}), 500


