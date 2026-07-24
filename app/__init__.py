from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../app/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    from app.routes.reviews import reviews_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.admin import admin_bp
    from app.routes.users import users_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(users_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app