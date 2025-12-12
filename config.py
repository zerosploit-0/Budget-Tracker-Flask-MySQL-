"""
Zentrale Konfigurationsdatei für die Flask-Anwendung
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Database configuration
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'your_password'
    DB_NAME = 'budget_tracker'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

# Choose config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}