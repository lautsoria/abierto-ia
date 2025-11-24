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


