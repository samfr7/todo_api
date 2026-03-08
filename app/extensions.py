from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, current_app
import jwt



db = SQLAlchemy()

def get_user_id_or_ip():
    """
    This function acts as the nametag reader for the Limiter.
    It does not need the database or the models!
    """
    token = request.headers.get('Authorization')
    
    if token:
        token = token.replace('Bearer ', '')
        try:
            # We use current_app.config to safely get the secret key!
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Return the user ID as the rate limit bucket!
            return str(data.get('user_id'))
        except Exception:
            # If the token is expired or fake, just ignore it and fall back to IP
            pass
            
    # If there is no token (like on the /login or /register routes), track by IP
    return get_remote_address()


limiter = Limiter(
    key_func=get_user_id_or_ip,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="moving-window"
)
