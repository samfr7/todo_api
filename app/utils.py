from functools import wraps
from flask import request, jsonify, current_app
from .models import User
import jwt


def token_required(f):
    # Need to learn why wraps
    # We need to use wrap as it copies the original functions data to this function makes it seem that this is the original function
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        token = token.split()[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            if data.get('type') == 'refresh':
                raise jwt.InvalidTokenError("Refresh tokens cannot be used to access data!!")
            user = User.query.filter_by(id=data.get('user_id')).first()

            if not user:
                jsonify({
                    "message":"User associated with this token no longer exists!"
                }), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is Expired!"}), 401
            # Here we need to try to do the refresh token logic. we can do this later though
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is Invalid!"}), 401
        
        return f(user, *args, **kwargs)
    return decorated


def register_error_handlers(current_app):

    @current_app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error":"ratelimit_exceeded",
            "message": f'Whoa there! You have exceeded your rate limit. {e.description}'
        }), 429

    @current_app.errorhandler(404)
    def data_not_found(e):
        return jsonify({
            "error":"Data not found",
            "message": f'Whoa there! The requested data is unavailable or deleted'
        }), 404

    @current_app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "error":"Method not allowed",
            "message": f'Whoa there! The requested method is unavailable currently'
        }), 405

    @current_app.errorhandler(500)
    def internal_server_error(e):
        # In production, you would also log the actual error to a file here!
        return jsonify({"error": "Internal server error", "message": "Something went wrong on our end."}), 500

    @current_app.errorhandler(400)
    def bad_request(e):
        # In production, you would also log the actual error to a file here!
        return jsonify({"error": "Bad Request", "message": "Bad Request"}), 400