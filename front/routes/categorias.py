from flask import render_template, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from back_calls.categorias import *
from back_calls.ubicaciones import *
from back_calls.servicios import obtener_servicios_por_categoria


categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/<string:nombre>')
@jwt_required(optional=True, locations=['cookies'])
def categoria(nombre):
    """Muestra servicios filtrados por categoría con opciones de filtrado"""
    data = get_jwt()    
    user_data = data if data else None

    # Obtener parámetros de filtro
    ubicacion_seleccionada = request.args.get('ubicacion', '')
    ordenar_seleccionado = request.args.get('ordenar', '')
    precio_min_seleccionado = request.args.get('precio_min', '')
    precio_max_seleccionado = request.args.get('precio_max', '')

    print(ubicacion_seleccionada, ordenar_seleccionado, precio_min_seleccionado, precio_max_seleccionado)

    # Obtener servicios filtrados
    servicios = obtener_servicios_por_categoria(
        nombre,
        ubicacion=ubicacion_seleccionada if ubicacion_seleccionada else None,
        ordenar=ordenar_seleccionado if ordenar_seleccionado else None,
        precio_min=precio_min_seleccionado if precio_min_seleccionado else None,
        precio_max=precio_max_seleccionado if precio_max_seleccionado else None,
    )
    
    ubicaciones = obtener_ubicaciones()
    
    # Obtener total de servicios sin filtros
    total_servicios = len(obtener_servicios_por_categoria(nombre))

    return render_template(
        'categoria.html',
        categoria_nombre=nombre,
        servicios=servicios,
        total_servicios=total_servicios,
        ubicaciones=ubicaciones,
        ubicacion_seleccionada=ubicacion_seleccionada,
        ordenar_seleccionado=ordenar_seleccionado,
        precio_min_seleccionado=precio_min_seleccionado,
        precio_max_seleccionado=precio_max_seleccionado,
        data=user_data
    )