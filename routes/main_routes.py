"""
Main Routes - Index, Dashboard, Transaktionsverwaltung
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from utils.decorators import login_required
from services.transaction_service import TransactionService
from services.category_service import CategoryService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing Page"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard mit Transaktionsübersicht"""
    user_id = session.get('user_id')
    dashboard_data = TransactionService.get_dashboard_data(user_id)

    return render_template('dashboard.html', 
                          transactions=dashboard_data['transactions'],
                          summary=dashboard_data['summary'],
                          categories=dashboard_data['categories'],
                          category_chart=dashboard_data.get('category_chart', {}))


@main_bp.route('/categories')
@login_required
def manage_categories():
    user_id = session.get('user_id')

    categories = CategoryService.get_categories_as_dict(user_id)
    stats = CategoryService.get_category_stats(user_id)

    return render_template('categories.html', categories=categories, stats=stats)


@main_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    user_id = session.get('user_id')

    name = request.form.get('name')
    color = request.form.get('color')

    # CategoryService expects (name, user_id, icon=None, color=None)
    success, message = CategoryService.add_category(name, user_id, None, color)
    flash(message, 'success' if success else 'error')

    return redirect(url_for('main.manage_categories'))


@main_bp.route('/category/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    user_id = session.get('user_id')

    success, message = CategoryService.delete_category(category_id, user_id)
    flash(message, 'success' if success else 'error')

    return redirect(url_for('main.manage_categories'))

@main_bp.route('/transaction/add', methods=['POST'])
@login_required
def add_transaction():
    """Neue Transaktion hinzufügen"""
    user_id = session.get('user_id')
    
    amount = request.form.get('amount')
    transaction_type = request.form.get('type')
    category_id = request.form.get('category_id')
    description = request.form.get('description')
    date = request.form.get('date')

    success, message = TransactionService.add_transaction(
        user_id, amount, transaction_type, category_id, description, date
    )
    
    flash(message, 'success' if success else 'error')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/transaction/edit/<int:transaction_id>', methods=['POST'])
@login_required
def edit_transaction(transaction_id):
    """Transaktion bearbeiten"""
    user_id = session.get('user_id')
    
    update_data = {}
    if request.form.get('amount'):
        update_data['amount'] = request.form.get('amount')
    if request.form.get('type'):
        update_data['transaction_type'] = request.form.get('type')
    if request.form.get('category_id'):
        update_data['category_id'] = request.form.get('category_id')
    if request.form.get('description'):
        update_data['description'] = request.form.get('description')
    if request.form.get('date'):
        update_data['date'] = request.form.get('date')
    
    success, message = TransactionService.update_transaction(
        transaction_id, user_id, **update_data
    )
    
    flash(message, 'success' if success else 'error')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/transaction/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Transaktion löschen"""
    user_id = session.get('user_id')
    
    success, message = TransactionService.delete_transaction(transaction_id, user_id)
    
    flash(message, 'success' if success else 'error')
    return redirect(url_for('main.dashboard'))