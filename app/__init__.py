from flask import Flask
from .extensions import db, limiter, cors, migrate
from .routes.auth_routes import auth_bp
from .routes.todo_routes import todo_bp
from .utils import register_error_handlers
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    # The secret key that I am using is 18 characters but it needs 32 characters min to be unhackable as per maths calculation. HS256
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # 2. Initialize Extensions with the app
    db.init_app(app=app)
    limiter.init_app(app=app)
    cors.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # 3. Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)

    # 4. Register error handlers
    register_error_handlers(app)

    # with app.app_context():
    #     db.create_all()

    return app

