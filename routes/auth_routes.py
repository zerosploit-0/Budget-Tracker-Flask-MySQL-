"""
Authentication Routes - Login, Register, Logout
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registrierungsseite"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, message = AuthService.register_user(username, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login-Seite"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, user, message = AuthService.login_user(username, password)
        
        if success:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(message, 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Erfolgreich abgemeldet', 'success')
    return redirect(url_for('main.index'))