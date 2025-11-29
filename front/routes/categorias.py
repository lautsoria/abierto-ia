from flask import Flask, render_template, request, redirect, url_for, flash, make_response, Blueprint
from flask_jwt_extended import jwt_required, JWTManager, verify_jwt_in_request, get_jwt, get_jwt_identity
from flask_cors import CORS
import os
from dotenv import load_dotenv
import qrcode

from static.icons import icons
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

    # Obtener servicios filtrados
    servicios = obtener_servicios_por_categoria(nombre, ubicacion_seleccionada if ubicacion_seleccionada else None)
    
    # Obtener ubicaciones para el filtro
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
        data=user_data
    )