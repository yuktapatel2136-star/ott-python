from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # 
    from app.models.auth_model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # 

    from .routes.auth_route import main
    from app.routes.category_route import category_bp
    from app.routes.admin_route import admin_bp

    app.register_blueprint(main)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)

    return app
