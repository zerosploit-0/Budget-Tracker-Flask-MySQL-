"""
API Routes - RESTful API Endpunkte
"""
from flask import Blueprint, request, session, jsonify
from services.auth_service import AuthService
from services.transaction_service import TransactionService
from utils.decorators import api_login_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Authentication Endpoints

@api_bp.route('/register', methods=['POST'])
def api_register():
    """API: Benutzer registrieren"""
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    success, message = AuthService.register_user(username, email, password)
    
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 400

@api_bp.route('/login', methods=['POST'])
def api_login():
    """API: Benutzer anmelden"""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    success, user, message = AuthService.login_user(username, password)
    
    if success:
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({
            'message': message,
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200
    else:
        return jsonify({'error': message}), 401

@api_bp.route('/logout', methods=['POST'])
@api_login_required
def api_logout():
    """API: Benutzer abmelden"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

# Transaction Endpoints

@api_bp.route('/transactions', methods=['GET'])
@api_login_required
def api_get_transactions():
    """API: Alle Transaktionen abrufen"""
    user_id = session.get('user_id')
    
    transactions = TransactionService.get_transactions_as_dict(user_id)
    
    return jsonify(transactions), 200

@api_bp.route('/transactions', methods=['POST'])
@api_login_required
def api_add_transaction():
    """API: Neue Transaktion hinzufügen"""
    user_id = session.get('user_id')
    data = request.get_json()
    
    amount = data.get('amount')
    transaction_type = data.get('type')
    category = data.get('category')
    description = data.get('description')
    date = data.get('date')
    
    success, message = TransactionService.add_transaction(
        user_id, amount, transaction_type, category, description, date
    )
    
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 400

@api_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@api_login_required
def api_get_transaction(transaction_id):
    """API: Spezifische Transaktion abrufen"""
    user_id = session.get('user_id')
    
    transaction = TransactionService.get_transaction(transaction_id, user_id)
    
    if transaction:
        return jsonify({
            'id': transaction.id,
            'amount': float(transaction.amount),
            'type': transaction.transaction_type,
            'category': transaction.category,
            'description': transaction.description,
            'date': transaction.date.strftime('%Y-%m-%d') if transaction.date else None
        }), 200
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@api_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
@api_login_required
def api_update_transaction(transaction_id):
    """API: Transaktion aktualisieren"""
    user_id = session.get('user_id')
    data = request.get_json()
    
    update_data = {}
    if 'amount' in data:
        update_data['amount'] = data['amount']
    if 'type' in data:
        update_data['transaction_type'] = data['type']
    if 'category' in data:
        update_data['category'] = data['category']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'date' in data:
        update_data['date'] = data['date']
    
    success, message = TransactionService.update_transaction(
        transaction_id, user_id, **update_data
    )
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@api_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@api_login_required
def api_delete_transaction(transaction_id):
    """API: Transaktion löschen"""
    user_id = session.get('user_id')
    
    success, message = TransactionService.delete_transaction(transaction_id, user_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@api_bp.route('/dashboard', methods=['GET'])
@api_login_required
def api_get_dashboard():
    """API: Dashboard-Daten abrufen"""
    user_id = session.get('user_id')
    
    dashboard_data = TransactionService.get_dashboard_data(user_id)
    
    return jsonify(dashboard_data), 200