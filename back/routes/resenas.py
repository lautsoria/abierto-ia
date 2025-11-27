from flask import Blueprint, jsonify, request
from db.db import db_conn

resenas_bp = Blueprint('resenas', __name__)

@resenas_bp.route('/<string:id>', methods=['GET'])
def resenas_de_servicio(id):
    try:
      conn = db_conn()
      cursor = conn.cursor(dictionary=True)

      query = '''
              SELECT 
              u.usuario as usuario,
              r.puntuacion as puntuacion,
              r.comentarios_cliente as comentarios_cliente, 
              r.fecha as fecha
              FROM resenas r
              JOIN usuarios u
              ON r.usuario_id = u.id
              WHERE r.servicio_id = (%s)
              ORDER BY r.fecha DESC
              '''
      
      cursor.execute(query, (id,))
      resenas = cursor.fetchall()
      
      # Convert datetime to ISO string for JSON serialization
      for resena in resenas:
          if resena.get('fecha'):
              resena['fecha'] = resena['fecha'].isoformat()
      
      cursor.close()
      conn.close()

      if resenas is None or len(resenas) == 0:
        return jsonify([]), 200
      
      return jsonify(resenas), 200
    except Exception as e:
      print(f"Error in resenas_de_servicio: {e}")
      return jsonify({'error': str(e)}), 500