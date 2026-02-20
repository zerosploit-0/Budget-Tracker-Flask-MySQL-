"""
==============================================
app.py Die neue, schlanke Hauptdatei
==============================================

VORHER: 500-1000 Zeilen
- Alle Routes
- Alle DB-Queries
- Alle Validierungen
- Alles durcheinander

NACHHER: Nur noch 40 Zeilen!
- Nur App-Initialisierung
- Blueprint-Registrierung
- Start

Das ist APPLICATION FACTORY PATTERN!
"""

from flask import Flask
import os

def create_app():
    """
    Application Factory
    
    WARUM FUNKTION statt direkt app = Flask()?
    
    VORHER:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'xyz'
        # ... direkt im Modul
        
    Problem: Schwer zu testen, schwer zu konfigurieren
    
    NACHHER (Factory):
        def create_app():
            app = Flask(__name__)
            # ... konfiguriere
            return app
        
    Vorteile:
    Kann mehrere Apps erstellen (Testing, Production)
     Kann verschiedene Configs übergeben
     Clean und professionell
    """
    
    # ========================================
    # SCHRITT 1: App erstellen
    # ========================================
    app = Flask(__name__)
    
    # ========================================
    # SCHRITT 2: Konfiguration
    # ========================================
    
    # Secret Key für Sessions (WICHTIG!)
    # In Produktion: Verwende Umgebungsvariable!
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session-Konfiguration
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Sicherheit: JS kann nicht auf Cookie zugreifen
    app.config['SESSION_COOKIE_SECURE'] = False   # Set to True in production with HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 Stunde
    
    # Optional: Mehr Configs
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB Upload
    # app.config['JSON_SORT_KEYS'] = False  # JSON nicht sortieren
    
    # ========================================
    # SCHRITT 3: Blueprints registrieren
    # ========================================
    
    # Importiere Blueprints
    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp
    from routes.api_routes import api_bp
    
    # Registriere Blueprints
    # Ab jetzt sind alle Routes verfügbar!
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Optional: Custom Error-Handler
    @app.errorhandler(404)
    def not_found(error):
        """
        Custom 404 Page
        """
        return "Seite nicht gefunden", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """
        Custom 500 Page
        """
        return "Interner Serverfehler", 500
    
    # ========================================
    # SCHRITT 4: Return App
    # ========================================
    return app


# ========================================
# MAIN - Wenn direkt ausgeführt
# ========================================

if __name__ == '__main__':
    """
    Wird nur ausgeführt wenn du direkt `python app.py` ausführst
    Nicht wenn du importierst!
    
    VERWENDUNG:
        Development: python app.py
        Production:  gunicorn app:app
    """
    
    # Erstelle App
    app = create_app()
    
    # Starte Development Server
    app.run(
        debug=True,      # Zeigt Fehler im Browser
        host='0.0.0.0',  # Erreichbar von außen (nicht nur localhost)
        port=5000        # Port 5000
    )