from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.movie_routes import movie_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.main_routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    return app
