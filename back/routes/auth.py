from flask import Blueprint, jsonify, request
import bcrypt as b
import dotenv

SALT_ROUNDS = int(dotenv.get_key(dotenv_path='../.env', key_to_get='SALT') or 10)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  print(data)

  try:
    # Generate salt with the specified rounds and hash the password
    salt = b.gensalt(rounds=SALT_ROUNDS)
    hashedPassword = b.hashpw(data['password'].encode('utf-8'), salt=salt)
    # connect to the database and save user
    # crear JWT y devolverlo
    return {'message': 'User created successfuly'}, 200 
  except Exception as e:
    return {'message': str(e)}, 400