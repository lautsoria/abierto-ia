from flask import Blueprint, jsonify, request
import bcrypt as b
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# es mucho muy importante que definas salt
salt = os.getenv('SALT')
try:
  if salt is None:
    raise ValueError('SALT no esta definida')
  else:
    SALT_ROUNDS = int(salt)
    # bcrypt gensalt accepts a cost between 4 and 31 (practical range)
    if not (4 <= SALT_ROUNDS <= 31):
      raise ValueError('SALT debe tener un valor entre 4 y 31')
except Exception as e:
  raise ValueError('Valor invalido para salt', e)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()

  # Basic validation: require a password in request body
  if not data or 'password' not in data:
    return {'message': 'password is required'}, 400

  try:
    # Generate salt with the specified rounds and hash the password
    salt = b.gensalt(rounds=SALT_ROUNDS)
    hashedPassword = b.hashpw(data['password'].encode('utf-8'), salt=salt)
    # connect to the database and save user
    # crear JWT y devolverlo
    return {'message': 'User created successfully'}, 200
  except Exception as e:
    logger.exception('Error creating user')
    return {'message': str(e)}, 400