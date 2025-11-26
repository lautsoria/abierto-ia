from flask import Blueprint, jsonify, request
from db.db import db_conn
import uuid

servicios_bp = Blueprint('servicios', __name__)

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
            INNER JOIN usuarios u ON p.id = u.id
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
            INNER JOIN usuarios u ON p.id = u.id
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
                GROUP_CONCAT(DISTINCT b.nombre SEPARATOR ', ') as proveedor_ubicacion,
                (SELECT AVG(puntuacion) FROM resenas WHERE servicio_id = s.id) as rating,
                (SELECT COUNT(*) FROM resenas WHERE servicio_id = s.id) as reviews_count
            FROM servicios s
            INNER JOIN categorias c ON s.categoria_id = c.id
            INNER JOIN proveedores p ON s.proveedor_id = p.id
            INNER JOIN usuarios u ON p.id = u.id
            LEFT JOIN barrios_usuarios bu ON u.id = bu.usuario_id
            LEFT JOIN barrios b ON bu.barrio_id = b.id
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

        query += " GROUP BY s.id ORDER BY s.precio ASC"

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
                INNER JOIN usuarios u ON p.id = u.id
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


@servicios_bp.route('/buscar', methods=['GET'])
def buscar_servicios():
    q = request.args.get("q", "").strip()

    if not q:
        return jsonify([]), 200

    palabras = q.split()

    conditions = " OR ".join([
        "(s.nombre LIKE %s OR s.descripcion LIKE %s)"
        for _ in palabras
    ])

    params = []
    for palabra in palabras:
        like = f"%{palabra}%"
        params.extend([like, like])

    conn = db_conn()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT 
            s.id,
            s.nombre,
            s.descripcion,
            s.precio,

            c.nombre AS categoria_nombre,

            u.nombre AS proveedor_nombre,
            

            p.id AS proveedor_id

        FROM servicios s
        JOIN categorias c ON s.categoria_id = c.id
        JOIN proveedores p ON s.proveedor_id = p.id
        JOIN usuarios u ON p.id = u.id

        WHERE {conditions}
    """

    cursor.execute(query, params)
    servicios = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(servicios), 200

<<<<<<< HEAD
@servicios_bp.route('/', methods=['POST'])
def registrar_servicio():
    payload = request.json
    print(payload)
    (
    proveedor_id,
    categoria_id,
    nombre,
    descripcion,
    precio,
    hora_inicio,
    hora_fin,
    duracion
    ) = payload.values()

    try:
        conn = db_conn()
        cursor = conn.cursor()

        query = """
                INSERT INTO servicios (
                id,
                proveedor_id,
                categoria_id,
                nombre,
                descripcion,
                precio,
                hora_inicio,
                hora_fin,
                duracion 
                )
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(query, (
            str(uuid.uuid4()),
            proveedor_id,
            categoria_id,
            nombre,
            descripcion,
            precio,
            hora_inicio,
            hora_fin,
            duracion
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "ok"}, 200
    
    except Exception as e:
        return {"message": str(e)}, 400


@servicios_bp.route('/<string:id>', methods=['PUT'])
def actualizar_servicio(id):
    payload = request.json

    try:
        conn = db_conn()
        cursor = conn.cursor()

        query = """
                UPDATE servicios SET
                    categoria_id = %s,
                    nombre = %s,
                    descripcion = %s,
                    precio = %s,
                    hora_inicio = %s,
                    hora_fin = %s,
                    duracion = %s
                WHERE id = %s
                """
        cursor.execute(query, (
            payload.get('categoria_id'),
            payload.get('nombre'),
            payload.get('descripcion'),
            payload.get('precio'),
            payload.get('hora_inicio'),
            payload.get('hora_fin'),
            payload.get('duracion'),
            id
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Servicio actualizado"}, 200
    
    except Exception as e:
        return {"message": str(e)}, 400


@servicios_bp.route('/<string:id>', methods=['DELETE'])
def eliminar_servicio(id):
    try:
        conn = db_conn()
        cursor = conn.cursor()

        # Eliminar reseñas asociadas
        cursor.execute("DELETE FROM resenas WHERE servicio_id = %s", (id,))
        
        # Eliminar reservas asociadas
        cursor.execute("DELETE FROM reservas WHERE servicio_id = %s", (id,))
        
        # Eliminar el servicio
        cursor.execute("DELETE FROM servicios WHERE id = %s", (id,))
        
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Servicio eliminado"}, 200
    
    except Exception as e:
        return {"message": str(e)}, 400
    
@servicios_bp.route('/proveedor/<string:id>')
def servicios_proveedor(id):
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
            INNER JOIN usuarios u ON p.id = u.id
            LEFT JOIN barrios_usuarios bu ON u.id = bu.usuario_id
            LEFT JOIN barrios b ON bu.barrio_id = b.id
            WHERE p.id = %s
            GROUP BY s.id
            ORDER BY s.fecha_creacion DESC
        """
        cursor.execute(query, (id,))
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

@servicios_bp.route('/todos', methods=['GET'])
def todos_servicios ():
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT s.*, 
            FROM servicios s
        """
        
        cursor.execute(query)
        usuarios = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(usuarios), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@servicios_bp.route('/<string:id>/eliminar', methods=['DELETE'])
def eliminar_servicio(id):
    try:
        conn = db_conn()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM servicios WHERE id = %s', (id,))
        servicio = cursor.fetchone()
        
        if servicio is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Servicio no encontrado'}), 404
        
        
        cursor.execute('DELETE FROM servicio WHERE id = %s', (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Servicio eliminado correctamente'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al eliminar el servicio'}), 500

