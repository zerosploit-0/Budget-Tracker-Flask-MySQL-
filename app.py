"""
==============================================
app.py - Die neue, schlanke Hauptdatei!
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
    ✅ Kann mehrere Apps erstellen (Testing, Production)
    ✅ Kann verschiedene Configs übergeben
    ✅ Clean und professionell
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


"""
==============================================
VERGLEICH: VORHER vs NACHHER
==============================================

VORHER (Monolithische app.py - 500+ Zeilen):
────────────────────────────────────────────

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'xyz'

def get_db_connection():
    return mysql.connector.connect(...)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 20 Zeilen Validierung
        if not username:
            flash('Username fehlt')
            return redirect(url_for('register'))
        if len(username) < 3:
            flash('Username zu kurz')
            return redirect(url_for('register'))
        # ... usw
        
        # DB-Check
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
        if cursor.fetchone()[0] > 0:
            flash('Username existiert')
            return redirect(url_for('register'))
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Insert
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                      (username, email, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registriert!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # DB-Query
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login erfolgreich!')
            return redirect(url_for('dashboard'))
        else:
            flash('Ungültige Credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Hole Transactions
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC", (user_id,))
    transactions = cursor.fetchall()
    
    # Berechne Summen
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s AND type = 'income'", (user_id,))
    total_income = cursor.fetchone()['SUM(amount)'] or 0
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s AND type = 'expense'", (user_id,))
    total_expenses = cursor.fetchone()['SUM(amount)'] or 0
    
    balance = total_income - total_expenses
    
    # Kategorien
    cursor.execute("SELECT category, SUM(amount) as total FROM transactions WHERE user_id = %s AND type = 'expense' GROUP BY category", (user_id,))
    categories = {row['category']: row['total'] for row in cursor.fetchall()}
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', 
                          transactions=transactions,
                          total_income=total_income,
                          total_expenses=total_expenses,
                          balance=balance,
                          categories=categories)

@app.route('/transaction/add', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    amount = request.form['amount']
    transaction_type = request.form['type']
    category = request.form['category']
    description = request.form['description']
    date = request.form.get('date') or datetime.now().date()
    
    # Validierung
    try:
        amount = float(amount)
        if amount <= 0:
            flash('Betrag muss positiv sein')
            return redirect(url_for('dashboard'))
    except ValueError:
        flash('Ungültiger Betrag')
        return redirect(url_for('dashboard'))
    
    # DB Insert
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, amount, type, category, description, date) VALUES (%s, %s, %s, %s, %s, %s)",
                  (user_id, amount, transaction_type, category, description, date))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Transaktion hinzugefügt!')
    return redirect(url_for('dashboard'))

# ... 20+ weitere Routes für Edit, Delete, API, etc.

if __name__ == '__main__':
    app.run(debug=True)


NACHHER (Neue Struktur - nur 40 Zeilen!):
─────────────────────────────────────────

from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp
    from routes.api_routes import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


UNTERSCHIED:
✅ 500+ Zeilen → 40 Zeilen (92% weniger!)
✅ Alles organisiert in Models, Services, Routes
✅ Wiederverwendbar
✅ Testbar
✅ Wartbar
✅ Professionell


==============================================
DEPLOYMENT - Production vs Development
==============================================

DEVELOPMENT (während du entwickelst):
    python app.py
    → Flask's eingebauter Development Server
    → debug=True → Zeigt Fehler
    → Auto-Reload bei Code-Änderungen

PRODUCTION (Live-Server):
    gunicorn app:app
    → Gunicorn = Production WSGI Server
    → Viel schneller und stabiler
    → Kann mehrere Workers handhaben
    
    Installation:
        pip install gunicorn
    
    Verwendung:
        gunicorn app:app --workers 4 --bind 0.0.0.0:5000


==============================================
UMGEBUNGSVARIABLEN - Best Practice
==============================================

Secret Key NIEMALS im Code!

FALSCH:
    app.config['SECRET_KEY'] = 'mein-geheimer-schlüssel'

RICHTIG:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

Setzen:
    # Linux/Mac
    export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
    
    # Windows
    set SECRET_KEY=...

Oder .env Datei verwenden (mit python-dotenv):
    # .env
    SECRET_KEY=abc123xyz...
    
    # app.py
    from dotenv import load_dotenv
    load_dotenv()
"""