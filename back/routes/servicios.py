from flask import Blueprint, jsonify, request
from db.db import db_conn

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/buscar', methods=['GET'])
def buscar_servicios():
    """
    Buscador principal. 
    Ejemplo: /servicios/buscar?q=plomero&min=1000&max=5000&ubicacion=Centro&sort=precio_asc
    """
    try:
        # 1. Obtener parámetros
        q = request.args.get('q', '').strip()
        precio_min = request.args.get('min', type=float)
        precio_max = request.args.get('max', type=float)
        ubicacion = request.args.get('ubicacion', '')
        ordenar = request.args.get('sort', 'relevancia') # relevancia, precio_asc, precio_desc

        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        # 2. Query Base
        query = """
            SELECT 
                s.id,
                s.nombre,
                s.descripcion,
                s.precio,
                c.nombre as categoria_nombre,
                p.id as proveedor_id,
                u.usuario as proveedor_nombre,
                GROUP_CONCAT(DISTINCT b.nombre SEPARATOR ', ') as ubicacion,
                (SELECT AVG(puntuacion) FROM resenas WHERE servicio_id = s.id) as calificacion_promedio,
                (SELECT COUNT(*) FROM resenas WHERE servicio_id = s.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN barrios_usuarios bu ON u.id = bu.usuario_id
            LEFT JOIN barrios b ON bu.barrio_id = b.id
            WHERE 1=1
        """
        
        params = []

        # 3. Aplicar Filtros
        
        # Filtro de Texto (Busca en nombre del servicio, descripción o nombre de categoría)
        if q:
            query += " AND (s.nombre LIKE %s OR s.descripcion LIKE %s OR c.nombre LIKE %s)"
            search_term = f"%{q}%"
            params.extend([search_term, search_term, search_term])

        # Filtro de Precio Mínimo
        if precio_min is not None:
            query += " AND s.precio >= %s"
            params.append(precio_min)

        # Filtro de Precio Máximo
        if precio_max is not None:
            query += " AND s.precio <= %s"
            params.append(precio_max)

        # Filtro de Ubicación
        if ubicacion:
            query += " AND b.nombre = %s"
            params.append(ubicacion)
        
        # Agrupar por ID de servicio
        query += " GROUP BY s.id"

        # 4. Ordenamiento
        if ordenar == 'precio_asc':
            query += " ORDER BY s.precio ASC"
        elif ordenar == 'precio_desc':
            query += " ORDER BY s.precio DESC"
        else:
            # Default: Relevancia (Mejor rating y más reviews)
            query += " ORDER BY calificacion_promedio DESC, reviews_count DESC"

        cursor.execute(query, params)
        servicios = cursor.fetchall()
        
        # Convertir Decimales a float
        for servicio in servicios:
            if servicio.get('calificacion_promedio'):
                servicio['calificacion_promedio'] = float(servicio['calificacion_promedio'])
            if servicio.get('precio'):
                servicio['precio'] = float(servicio['precio'])

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
                GROUP_CONCAT(DISTINCT b.nombre SEPARATOR ', ') as proveedor_ubicacion,
                AVG(r.puntuacion) as rating,
                COUNT(r.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN barrios_usuarios bu ON u.id = bu.usuario_id
            LEFT JOIN barrios b ON bu.barrio_id = b.id
            LEFT JOIN resenas r ON r.servicio_id = s.id
            GROUP BY s.id
            HAVING reviews_count > 0
            ORDER BY rating DESC, reviews_count DESC
            LIMIT %s
        """

        cursor.execute(query, (limit,))
        servicios = cursor.fetchall()
        
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
    

# busca servicio por id
@servicios_bp.route('/id/<string:id>', methods=['GET'])
def servicio(id):
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT 
                    s.*,
                    c.nombre as categoria_nombre,
                    p.id as proveedor_id,
                    u.usuario as proveedor_nombre,
                    GROUP_CONCAT(DISTINCT b.nombre SEPARATOR ', ') as ubicacion,
                    (SELECT AVG(puntuacion) FROM resenas WHERE servicio_id = s.id) as calificacion_promedio,
                    (SELECT COUNT(*) FROM resenas WHERE servicio_id = s.id) as reviews_count
                FROM servicios s
                INNER JOIN categorias c ON s.categoria_id = c.id
                INNER JOIN proveedores p ON s.proveedor_id = p.id
                INNER JOIN usuarios u ON p.usuario_id = u.id
                LEFT JOIN barrios_usuarios bu ON u.id = bu.usuario_id
                LEFT JOIN barrios b ON bu.barrio_id = b.id
                WHERE s.id = %s
                GROUP BY s.id
                """
        cursor.execute(query, (id,))
        servicio = cursor.fetchone()

        cursor.close()
        conn.close()

        if servicio is None:
            servicio = []

        return jsonify(servicio), 200
    except Exception as e:
        return jsonify({'error': e}), 400
    
    
#servicios por categoria
@servicios_bp.route('/<string:nombre>')
def servicios_por_categoria(nombre):
    ubicacion = request.args.get('ubicacion', '')
    
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                s.id,
                s.nombre,
                s.descripcion,
                s.precio,
                c.nombre as categoria_nombre,
                p.id as proveedor_id,
                u.usuario as proveedor_nombre,
                GROUP_CONCAT(DISTINCT b.nombre SEPARATOR ', ') as ubicacion,
                (SELECT AVG(puntuacion) FROM resenas WHERE servicio_id = s.id) as calificacion_promedio,
                (SELECT COUNT(*) FROM resenas WHERE servicio_id = s.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN barrios_usuarios bu ON u.id = bu.usuario_id
            LEFT JOIN barrios b ON bu.barrio_id = b.id
            WHERE LOWER(c.nombre) = LOWER(%s)
        """
        
        params = [nombre]
        
        # Agregar filtro de ubicación
        if ubicacion:
            query += " AND b.nombre = %s"
            params.append(ubicacion)
        
        query += " GROUP BY s.id"

        # Agregar ordenamiento
        # if ordenar == 'precio_asc':
        #     query += " ORDER BY s.precio ASC"
        # elif ordenar == 'precio_desc':
        #     query += " ORDER BY s.precio DESC"
        # elif ordenar == 'rating':
        #     query += " ORDER BY calificacion_promedio DESC"
        # else:  # relevancia o default
        query += " ORDER BY calificacion_promedio DESC, s.precio ASC"

        cursor.execute(query, params)
        servicios = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for servicio in servicios:
            if servicio.get('calificacion_promedio'):
                servicio['calificacion_promedio'] = float(servicio['calificacion_promedio'])
            if servicio.get('precio'):
                servicio['precio'] = float(servicio['precio'])

        cursor.close()
        conn.close()

        return jsonify(servicios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
