from flask import Blueprint, request
import logging
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies
)
import uuid
from flask import make_response
# from dotenv import load_dotenv
# import bcrypt as b

from db.db import db_conn

logger = logging.getLogger(__name__)

# es mucho muy importante que definas salt
# env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# load_dotenv(dotenv_path=env_path)
# salt = os.getenv('SALT')
# try:
#   if salt is None:
#     logger.warning('SALT no esta definida')
#   else:
#     SALT_ROUNDS = int(salt)
#     # bcrypt gensalt accepts a cost between 4 and 31 (practical range)
#     if not (4 <= SALT_ROUNDS <= 31):
#       logger.warning('SALT debe tener un valor entre 4 y 31')
# except Exception as e:
#   raise ValueError('Valor invalido para salt', e)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
  user, email, password, provider = request.json.values()
  rol = 'cliente' if not provider else 'proveedor'
  print(rol)

  try:
    # Generate salt with the specified rounds and hash the password
    # salt = b.gensalt(rounds=SALT_ROUNDS)
    # hashedPassword = b.hashpw(data['password'].encode('utf-8'), salt=salt)
    
    # connect to the database and save user
    conn = db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
      SELECT * FROM usuarios WHERE usuario = %s OR email = %s
      ''', (user, email))
    
    existingUser = cursor.fetchone()
    if existingUser:
      # Por temas de seguirdad no informamos que el usuario existe
      return {'message': 'Error al crear el usuario'}, 400

    cursor.execute('SELECT id FROM roles WHERE rol = (%s)', (rol,))
    rol_id = cursor.fetchone()['id']

    id = str(uuid.uuid4())
    cursor.execute('''
      INSERT INTO usuarios (id, usuario, email, contrasena, rol_id)
      VALUES (%s, %s, %s, %s, %s)''', (id, user, email, password, rol_id))
    
    if provider:
      providerId = str(uuid.uuid4())
      cursor.execute('''
        INSERT INTO proveedores (id, usuario_id) 
        VALUES (%s, %s)''', (providerId, id))
    conn.commit()
    cursor.close()
    conn.close()

    access_token = create_access_token( 
      identity=id,
      additional_claims={'rol':rol, 'user':user}
    )

    # debemos settear las cookies desde el back para poder acceder desde aca y desde el front
    # de otra manera se quedaran pegadas al dominio del front
    res = make_response({'message': 'Login exitoso'}, 200)
    set_access_cookies(res, access_token)
    return res
    
  except Exception as e:
    logger.exception('Error creando usuario')
    return {'message': str(e)}, 400
  

@auth_bp.route('/login', methods=['POST'])
def login():
  credential, password = request.json.values()  
  try:
    conn = db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
      SELECT u.id, u.usuario, u.contrasena, r.rol
      FROM usuarios u
      JOIN roles r
      ON r.id = u.rol_id
      WHERE usuario = %s OR email = %s
      ''', (credential, credential)
    )
    userData = cursor.fetchone()
    print(userData)

    # primero chequeamos que el usuario exista
    if userData is None:
      cursor.close()
      conn.close()      
      return {'message': 'Credenciales invalidas'}, 401

    # y que la clave sea valida
    if (password != userData['contrasena']):
      cursor.close()
      conn.close()  
      return {'message': 'Credenciales invalidas'}, 401
    
    cursor.close()
    conn.close()             
    
    access_token = create_access_token( 
      identity=userData['id'],
      additional_claims={'rol':userData['rol'], 'user':userData['usuario']}
    )

    # debemos settear las cookies desde el back para poder acceder desde aca y desde el front
    # de otra manera se quedaran pegadas al dominio del front
    res = make_response({'message': 'Login exitoso'}, 200)
    set_access_cookies(res, access_token)
    return res

  except Exception as e:
    logger.exception('Error logueando usuario')
    return {'message': str(e)}, 400