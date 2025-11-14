from flask import Blueprint, jsonify, request
import os
import logging
from flask_jwt_extended import create_access_token
import uuid
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
  user, email, password = request.json.values()
  
  try:
    # Generate salt with the specified rounds and hash the password
    # salt = b.gensalt(rounds=SALT_ROUNDS)
    # hashedPassword = b.hashpw(data['password'].encode('utf-8'), salt=salt)
    
    # connect to the database and save user
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT * 
                   FROM usuarios 
                   WHERE usuario = %s OR email = %s
                   ''', (user, email)
                  )
    existingUser = cursor.fetchone()
    if existingUser != None:
      # Por temas de seguirdad no informamos que el usuario existe
      return {'message': 'Error al crear el usuario'}, 400

    id = str(uuid.uuid4())
    cursor.execute('''INSERT INTO usuarios (id, usuario, email, contraseña) 
                  VALUES (%s, %s, %s, %s)''', (id, user, email, password))
    conn.commit()
    cursor.close()
    conn.close()

    access_token = create_access_token(
      identity=id
    )
  
    return jsonify(access_token=access_token), 200
  except Exception as e:
    logger.exception('Error creando usuario')
    return {'message': str(e)}, 400
  

@auth_bp.route('/login', methods=['POST'])
def login():
  credential, password = request.json.values()
  
  try:
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT id, contraseña 
                   FROM usuarios 
                   WHERE usuario = %s OR email = %s
                   ''', (credential, credential)
                  )
    userData = cursor.fetchone()
    cursor.close()
    conn.close()

    if userData is None:
      return {'message': 'Credenciales invalidas'}, 401

    if (password == userData[1]):

      access_token = create_access_token(
        identity=userData[0]
      )      

      return jsonify(access_token=access_token), 200
    else:
      return {'message': 'Credenciales invalidas'}, 401

  except Exception as e:
    logger.exception('Error logueando usuario')
    return {'message': str(e)}, 400