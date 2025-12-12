"""Routes Package"""
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.api_routes import api_bp

__all__ = ['auth_bp', 'main_bp', 'api_bp']