from flask import Blueprint, jsonify
from db.db import db_conn

ubicacion_bp = Blueprint('ubicacion', __name__)

@ubicacion_bp.route('', methods=['GET'])
def ubicaciones():
    try:
      conn = db_conn()
      cursor = conn.cursor(dictionary=True)

      query = '''
              SELECT id, nombre
              FROM barrios              
              '''
      cursor.execute(query)
      barrios = cursor.fetchall()
      cursor.close()
      conn.close()

      # if (ubicaciones == None):
      #   barrios = []
      # else:
      #   barrios = [barrio[0] for barrio in ubicaciones]
      
      return jsonify(barrios), 200
    except Exception as e:
      return jsonify(e), 405
      
