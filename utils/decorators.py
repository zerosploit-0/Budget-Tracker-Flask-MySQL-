from functools import wraps
from flask import session, redirect, url_for, flash, jsonify


def login_required(func):
    """Decorator for regular routes: redirects to login if not authenticated."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Bitte einloggen', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


def api_login_required(func):
    """Decorator for API routes: returns 401 JSON if not authenticated."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'error': 'Authentication required'}), 401
        return func(*args, **kwargs)
    return wrapper
