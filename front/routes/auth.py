from flask import Flask, render_template, request, redirect, url_for, flash, make_response, Blueprint
from flask_jwt_extended import jwt_required, JWTManager, verify_jwt_in_request, get_jwt, get_jwt_identity
from flask_cors import CORS
import os
from dotenv import load_dotenv
import qrcode

from static.icons import icons
from back_calls.auth import *


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def auth():
  try:
    verify_jwt_in_request(locations=['cookies'])
    return redirect(url_for('home'))
  except:
    # Si el token es inválido o no existe, limpiar la cookie
    next = request.args.get('next', url_for('home'))
    resp = make_response(render_template('auth.html', next=next))
    resp.set_cookie('access_token_cookie', '', max_age=0)
    return resp



@auth_bp.route('/register', methods=['POST'])
def register():
    user = request.form.get("newUser")
    email = request.form.get("email")
    password = request.form.get("newPassword")
    repeatPassword = request.form.get("newPassword2")
    provider = request.form.get("isProveedor") == 'true'
    next_url = request.args.get('next', url_for('home'))

    if password != repeatPassword:
        flash('Las contraseñas no coinciden', 'error')
        return redirect(url_for('auth.auth'))

    response = registrar_usuario(user, email, password, provider)
    
    if response and response.status_code == 200:
        if provider:
            # si el proveedor se registra
            # debera completar los datos de su perfil
            resp = make_response(redirect(url_for('servicios.registrar_servicio')))
        else:
            resp = make_response(redirect(next_url))
        
        # Copiar todas las cookies del backend al frontend
        for cookie_name, cookie_value in response.cookies.items():
            resp.set_cookie(
                cookie_name,
                cookie_value,
                httponly=True,
                samesite='Lax'
            )
        flash('Usuario creado con éxito', 'success')
        return resp
    else:
        flash('Error al registrar el usuario', 'error')
        return redirect(url_for('auth.auth'))



@auth_bp.route('/login', methods=['POST'])
def login():
    credential = request.form.get("credential")
    password = request.form.get("password")
    next_url = request.args.get('next', url_for('home'))

    response = login_usuario(credential, password)
    
    if response and response.status_code == 200:
        # Obtener las cookies del backend y pasarlas al frontend
        print(next_url)      
        resp = make_response(redirect(next_url))
        
        # Copiar todas las cookies del backend al frontend
        for cookie_name, cookie_value in response.cookies.items():
            resp.set_cookie(
                cookie_name,
                cookie_value,
                httponly=True,
                samesite='Lax'
            )
        flash('Inicio de sesión exitoso', 'success')
        return resp
    else:
        flash('Credenciales inválidas', 'error')
        return redirect(url_for('auth.auth'))
    


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(locations=['cookies'])
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('access_token_cookie', '', max_age=0)
    flash('Sesión cerrada exitosamente', 'success')
    return resp 