"""Category Service - Business-Logik für Kategorien (korrekte Version)

Dieses Modul benutzt die Methoden aus `models.category`.
"""
from models.category import Category


class CategoryService:
    @staticmethod
    def add_category(name, user_id, icon=None, color='#999999'):
        if not name:
            return False, "Kategorie-Name ist erforderlich"

        if len(name) < 2:
            return False, "Kategorie-Name muss mindestens 2 Zeichen lang sein"

        if len(name) > 100:
            return False, "Kategorie-Name darf maximal 100 Zeichen lang sein"

        # Prüfe ob Name schon existiert (Model erwartet (user_id, name, ...))
        if Category.name_exists(user_id, name):
            return False, "Eine Kategorie mit diesem Namen existiert bereits"

        category_id = Category.create(user_id, name, color)
        if category_id:
            return True, "Kategorie erfolgreich erstellt!"
        return False, "Fehler beim Erstellen der Kategorie"

    @staticmethod
    def get_categories_for_user(user_id):
        return Category.get_all_by_user(user_id)

    @staticmethod
    def get_categories_as_dict(user_id):
        cats = Category.get_all_by_user(user_id)
        return [
            {
                'id': c.id,
                'name': c.name,
                'color': c.color,
                'is_standard': c.user_id is None,
                'can_edit': (c.user_id == user_id)
            }
            for c in cats
        ]

    @staticmethod
    def update_category(category_id, user_id, name=None, icon=None, color=None):
        category = Category.get_by_id(category_id, user_id)
        if not category:
            return False, "Kategorie nicht gefunden"

        if category.user_id is None:
            return False, "Standard-Kategorien können nicht bearbeitet werden"

        if category.user_id != user_id:
            return False, "Keine Berechtigung"

        if name:
            if len(name) < 2:
                return False, "Name muss mindestens 2 Zeichen lang sein"
            if len(name) > 100:
                return False, "Name darf maximal 100 Zeichen lang sein"
            if Category.name_exists(user_id, name, exclude_id=category_id):
                return False, "Eine Kategorie mit diesem Namen existiert bereits"

        success = Category.update(category_id, user_id, name=name, color=color)
        if success:
            return True, "Kategorie erfolgreich aktualisiert!"
        return False, "Fehler beim Aktualisieren der Kategorie"

    @staticmethod
    def delete_category(category_id, user_id):
        category = Category.get_by_id(category_id, user_id)
        if not category:
            return False, "Kategorie nicht gefunden"

        if category.user_id is None:
            return False, "Standard-Kategorien können nicht gelöscht werden"

        if category.user_id != user_id:
            return False, "Keine Berechtigung"

        if Category.delete(category_id, user_id):
            return True, "Kategorie erfolgreich gelöscht!"
        return False, "Fehler beim Löschen der Kategorie"

    @staticmethod
    def get_category_stats(user_id):
        cats = Category.get_all_by_user(user_id)
        standard_count = sum(1 for c in cats if c.user_id is None)
        custom_count = len(cats) - standard_count
        return {
            'total': len(cats),
            'standard': standard_count,
            'custom': custom_count
        }
"""Deprecated duplicate module.

This file is a case-variant duplicate of
`services/category_service.py`. Use the lowercase module
`services.category_service` instead. Keeping this small
placeholder avoids accidental heavy imports on Windows.
"""

from services.category_service import CategoryService  # re-export

__all__ = ['CategoryService']


# ============================================================
# BEISPIEL-VERWENDUNG
# ============================================================

"""
DASHBOARD - Kategorien-Dropdown:

    @main_bp.route('/dashboard')
    @login_required
    def dashboard():
        user_id = session['user_id']
        
        # Hole Kategorien für Dropdown
        categories = CategoryService.get_categories_as_dict(user_id)
        
        return render_template('dashboard.html', 
                              categories=categories)


HTML (dashboard.html):

    <select name="category">
        {% for cat in categories %}
            <option value="{{ cat.name }}">
                {% if cat.icon %}{{ cat.icon }}{% endif %}
                {{ cat.name }}
                {% if cat.is_standard %}(Standard){% endif %}
            </option>
        {% endfor %}
    </select>


KATEGORIEN VERWALTEN - Route:

    @main_bp.route('/categories')
    @login_required
    def manage_categories():
        user_id = session['user_id']
        
        categories = CategoryService.get_categories_as_dict(user_id)
        stats = CategoryService.get_category_stats(user_id)
        
        return render_template('categories.html',
                              categories=categories,
                              stats=stats)
    
    @main_bp.route('/category/add', methods=['POST'])
    @login_required
    def add_category():
        user_id = session['user_id']
        
        name = request.form.get('name')
        icon = request.form.get('icon')
        color = request.form.get('color')
        
        success, message = CategoryService.add_category(name, user_id, icon, color)
        flash(message, 'success' if success else 'error')
        
        return redirect(url_for('main.manage_categories'))


API - Kategorien:

    @api_bp.route('/categories', methods=['GET'])
    @api_login_required
    def api_get_categories():
        user_id = session['user_id']
        
        categories = CategoryService.get_categories_as_dict(user_id)
        
        return jsonify(categories), 200
    
    @api_bp.route('/categories', methods=['POST'])
    @api_login_required
    def api_add_category():
        user_id = session['user_id']
        data = request.get_json()
        
        name = data.get('name')
        icon = data.get('icon')
        color = data.get('color')
        
        success, message = CategoryService.add_category(name, user_id, icon, color)
        
        if success:
            return jsonify({'message': message}), 201
        else:
            return jsonify({'error': message}), 400
"""