"""
Transaction Service - Business-Logik für Transaktionen
"""
from models.transaction import Transaction
from models.category import Category
from datetime import datetime

class TransactionService:
    """Service für Transaktions-Logik"""
    
    @staticmethod
    def add_transaction(user_id, amount, transaction_type, category_id, description, date=None):
        """
        Fügt eine neue Transaktion hinzu
        
        Args:
            user_id: Benutzer-ID
            amount: Betrag
            transaction_type: Typ (income/expense)
            category: Kategorie
            description: Beschreibung
            date: Datum (optional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validierung
        if not amount or not transaction_type or not category_id:
            return False, "Betrag, Typ und Kategorie sind erforderlich"
        
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Betrag muss größer als 0 sein"
        except ValueError:
            return False, "Ungültiger Betrag"
        
        if transaction_type not in ['income', 'expense']:
            return False, "Ungültiger Transaktionstyp"
        
        # Parse date if provided
        if date:
            try:
                if isinstance(date, str):
                    date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return False, "Ungültiges Datumsformat"
        
        # Kategorie-ID verarbeiten (leerer String -> None)
        if category_id == '':
            category_id = None
        else:
            try:
                category_id = int(category_id) if category_id is not None else None
            except (ValueError, TypeError):
                return False, "Ungültige Kategorie"

        # Erstelle Transaktion
        # Transaction.create signature: (user_id, amount, transaction_type, description, category_id=None, date=None)
        if Transaction.create(user_id, amount, transaction_type, description, category_id, date):
            return True, "Transaktion erfolgreich hinzugefügt!"
        else:
            return False, "Fehler beim Hinzufügen der Transaktion"
    
    @staticmethod
    def get_user_transactions(user_id):
        """
        Holt alle Transaktionen eines Benutzers
        
        Args:
            user_id: Benutzer-ID
            
        Returns:
            Liste von Transaction-Objekten
        """
        return Transaction.get_all_by_user(user_id)
    
    @staticmethod
    def get_transaction(transaction_id, user_id):
        """
        Holt eine spezifische Transaktion
        
        Args:
            transaction_id: Transaktions-ID
            user_id: Benutzer-ID
            
        Returns:
            Transaction-Objekt oder None
        """
        return Transaction.get_by_id(transaction_id, user_id)
    
    @staticmethod
    def update_transaction(transaction_id, user_id, **kwargs):
        """
        Aktualisiert eine Transaktion
        
        Args:
            transaction_id: Transaktions-ID
            user_id: Benutzer-ID
            **kwargs: Zu aktualisierende Felder
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validierung
        if 'amount' in kwargs:
            try:
                kwargs['amount'] = float(kwargs['amount'])
                if kwargs['amount'] <= 0:
                    return False, "Betrag muss größer als 0 sein"
            except ValueError:
                return False, "Ungültiger Betrag"
        
        if 'transaction_type' in kwargs and kwargs['transaction_type'] not in ['income', 'expense']:
            return False, "Ungültiger Transaktionstyp"
        
        # Parse date if provided
        if 'date' in kwargs and isinstance(kwargs['date'], str):
            try:
                kwargs['date'] = datetime.strptime(kwargs['date'], '%Y-%m-%d').date()
            except ValueError:
                return False, "Ungültiges Datumsformat"
        
        # Aktualisiere Transaktion
        if Transaction.update(transaction_id, user_id, **kwargs):
            return True, "Transaktion erfolgreich aktualisiert!"
        else:
            return False, "Fehler beim Aktualisieren der Transaktion"
    
    @staticmethod
    def delete_transaction(transaction_id, user_id):
        """
        Löscht eine Transaktion
        
        Args:
            transaction_id: Transaktions-ID
            user_id: Benutzer-ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if Transaction.delete(transaction_id, user_id):
            return True, "Transaktion erfolgreich gelöscht!"
        else:
            return False, "Fehler beim Löschen der Transaktion"
    
    @staticmethod
    def get_dashboard_data(user_id):
        """
        Holt alle Daten für das Dashboard
        
        Args:
            user_id: Benutzer-ID
            
        Returns:
            Dict mit Dashboard-Daten
        """
        transactions = Transaction.get_all_by_user(user_id)
        summary = Transaction.get_summary_by_user(user_id)

        # Kategorien für Chart (name -> {total, color})
        category_chart = Transaction.get_by_category(user_id)

        # Kategorien für Dropdown (Liste von Dicts mit id + name)
        category_objs = Category.get_all_by_user(user_id)
        categories_dropdown = [
            {'id': c.id, 'name': c.name, 'color': c.color}
            for c in category_objs
        ]

        # Format transactions for display to match template keys
        formatted_transactions = []
        for t in transactions:
            formatted_transactions.append({
                'id': t.id,
                'amount': float(t.amount),
                'type': t.transaction_type,
                'category_name': t.category_name or 'Ohne Kategorie',
                'category_color': t.category_color or '#999999',
                'description': t.description or '',
                'date': t.date.strftime('%Y-%m-%d') if t.date else ''
            })

        return {
            'transactions': formatted_transactions,
            'summary': summary,
            'categories': categories_dropdown,
            'category_chart': category_chart
        }
    
    @staticmethod
    def get_transactions_as_dict(user_id):
        """
        Holt Transaktionen als Dictionary (für API)
        
        Args:
            user_id: Benutzer-ID
            
        Returns:
            Liste von Dicts
        """
        transactions = Transaction.get_all_by_user(user_id)
        
        return [{
            'id': t.id,
            'amount': float(t.amount),
            'type': t.transaction_type,
            'category': t.category,
            'description': t.description,
            'date': t.date.strftime('%Y-%m-%d') if t.date else None
        } for t in transactions]