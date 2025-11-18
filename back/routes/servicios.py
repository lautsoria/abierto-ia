from flask import Blueprint, jsonify, request
from db.db import db_conn

servicios_bp = Blueprint('servicios', __name__)

#filtrar servicio por categoria
@servicios_bp.route('/<string:nombre>')
def servicios_por_categoria(nombre):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                s.*,
                c.nombre as categoria,
                p.id as proveedor_id,
                u.usuario as proveedor_nombre,
                p.ubicacion as proveedor_ubicacion,
                (SELECT AVG(puntuacion) FROM reseñas WHERE servicio_id = s.id) as rating,
                (SELECT COUNT(*) FROM reseñas WHERE servicio_id = s.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            WHERE LOWER(c.nombre) = LOWER(%s)
            ORDER BY s.id DESC
        """

        cursor.execute(query, (nombre,))
        servicios = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for servicio in servicios:
            if servicio.get('rating'):
                servicio['rating'] = float(servicio['rating'])

        cursor.close()
        conn.close()

        return jsonify(servicios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# buscar servicio con mejor rating, se le pone poner limite o default es 8
@servicios_bp.route('/top-rating')
def servicios_top_rating():
    try:
        limit = request.args.get('limit', default=8, type=int)

        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                s.*,
                c.nombre as categoria,
                p.id as proveedor_id,
                u.usuario as proveedor_nombre,
                p.ubicacion as proveedor_ubicacion,
                AVG(r.puntuacion) as rating,
                COUNT(r.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN reseñas r ON r.servicio_id = s.id
            GROUP BY s.id
            HAVING reviews_count > 0
            ORDER BY rating DESC, reviews_count DESC
            LIMIT %s
        """

        cursor.execute(query, (limit,))
        servicios = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for servicio in servicios:
            if servicio.get('rating'):
                servicio['rating'] = float(servicio['rating'])

        cursor.close()
        conn.close()

        return jsonify(servicios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# buscar servicio filtrado por precio
@servicios_bp.route('/precio')
def servicios_por_precio():
    try:
        precio_min = request.args.get('min', type=float)
        precio_max = request.args.get('max', type=float)

        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                s.*,
                c.nombre as categoria,
                p.id as proveedor_id,
                u.usuario as proveedor_nombre,
                p.ubicacion as proveedor_ubicacion,
                (SELECT AVG(puntuacion) FROM reseñas WHERE servicio_id = s.id) as rating,
                (SELECT COUNT(*) FROM reseñas WHERE servicio_id = s.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            WHERE 1=1
        """

        params = []

        # minimo
        if precio_min is not None:
            query += " AND s.precio >= %s"
            params.append(precio_min)

        # maximo
        if precio_max is not None:
            query += " AND s.precio <= %s"
            params.append(precio_max)

        query += " ORDER BY s.precio ASC"

        cursor.execute(query, params)
        servicios = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for servicio in servicios:
            if servicio.get('rating'):
                servicio['rating'] = float(servicio['rating'])
            if servicio.get('precio'):
                servicio['precio'] = float(servicio['precio'])

        cursor.close()
        conn.close()

        return jsonify(servicios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500