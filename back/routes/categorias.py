from flask import Blueprint, jsonify, request
from db.db import db_conn

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/<string:categoria_nombre>')
def cantidad_por_categoria(categoria_nombre):
    """cantidad de profesionales de una categoria"""
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                c.id,
                c.nombre AS categoria,
                COUNT(DISTINCT s.proveedor_id) AS total_profesionales
            FROM categorias c
            LEFT JOIN servicios s ON s.categoria_id = c.id
            WHERE LOWER(c.nombre) = LOWER(%s)
            GROUP BY c.id, c.nombre
            LIMIT 1
            """

        cursor.execute(query, (categoria_nombre,))
        categoria = cursor.fetchone()

        cursor.close()
        conn.close()

        if not categoria:
            return jsonify({
                'categoria': categoria_nombre,
                'total_profesionales': 0
            }), 200

        return jsonify(categoria), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@categorias_bp.route('/')
def categorias():
    """categorias existentes"""
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, nombre
            FROM categorias
            ORDER BY nombre ASC
        """
        cursor.execute(query)
        categorias = cursor.fetchall()

        cursor.close()
        conn.close()

        if not categorias:
            categorias = []
            return jsonify(categorias), 200

        return jsonify(categorias), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500