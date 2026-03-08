from flask import Blueprint , request, jsonify, current_app
from ..models import User
from ..extensions import db, limiter
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['Post'])
@limiter.limit("5 per minute")
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # To check if the user already exists in the system

    user_exists = User.query.filter_by(username=username).first()

    if user_exists:
        return jsonify({"data":"username already exists"}), 400

    password_hash = generate_password_hash(password)

    user = User(username = username, password_hash = password_hash)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User successfully Registered. Please login"
    }), 201


@auth_bp.route('/login', methods=["Post"])
@limiter.limit("5 per minute")
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username = username).first()

    if not user:
        return jsonify({"data":f"No username with {username} found"}), 401 

    if check_password_hash(user.password_hash, password=password):
        payload = {
            'user_id': user.id,
            'type':'access',
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
        }
        access_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

        payload = {
            'user_id': user.id,
            'type':'refresh',
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)
        }
        refresh_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            "access_token":access_token,
            "refresh_token": refresh_token
        }), 200
    else:
        return jsonify({"data":f"Wrong Password"}), 401

@auth_bp.route('/refresh', methods=['POST'])
@limiter.limit("5 per 1 minute")
def refresh_token():
    token = request.headers.get('Authorization')

    if token:
        token = token.replace('Bearer ', '')

        try:

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            if data.get('type') == 'access':
                raise jwt.InvalidTokenError("Need Refresh token to provie new token")
            
            payload = {
                'user_id': data.get('user_id'),
                'type':'access',
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
            }
            access_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

            payload = {
                'user_id': data.get('user_id'),
                'type':'refresh',
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)
            }
            refresh_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({
                "access_token":access_token,
                "refresh_token": refresh_token
            }), 200


        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is Expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is Invalid!"}), 401 
        
    else:
        return jsonify({
            "message": "Please provide the token"
        }), 400