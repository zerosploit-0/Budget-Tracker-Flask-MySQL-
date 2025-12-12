"""
Transaction Model - Angepasst an DB-Struktur

DB-Struktur:
- id INT
- user_id INT
- amount DECIMAL(12,2)
- type ENUM('income','expense')
- description VARCHAR(255)
- date DATETIME (nicht nur DATE!)
- category_id INT (Foreign Key zu categories, kann NULL sein)
"""
from datetime import datetime
from db_config import get_db_connection

class Transaction:
    """Transaction Model für Transaktionsverwaltung"""
    
    def __init__(self, id=None, user_id=None, amount=None, transaction_type=None,
                 description=None, date=None, category_id=None, category_name=None, 
                 category_color=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.date = date
        self.category_id = category_id
        self.category_name = category_name  # Wird bei JOIN gefüllt
        self.category_color = category_color  # Wird bei JOIN gefüllt
    
    @staticmethod
    def create(user_id, amount, transaction_type, description, category_id=None, date=None):
        """
        Erstellt neue Transaktion
        
        Args:
            user_id: User-ID
            amount: Betrag (Decimal)
            transaction_type: 'income' oder 'expense'
            description: Beschreibung
            category_id: Kategorie-ID (optional, kann NULL sein)
            date: DATETIME (optional, Standard: jetzt)
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if date is None:
                date = datetime.now()
            
            query = """
                INSERT INTO transactions (user_id, amount, type, description, date, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, amount, transaction_type, description, date, category_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return False
    
    @staticmethod
    def get_all_by_user(user_id):
        """
        Holt alle Transaktionen eines Users MIT Kategorie-Info
        
        WICHTIG: Macht LEFT JOIN mit categories Tabelle!
        
        Returns:
            Liste von Transaction-Objekten (mit category_name, category_color)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    t.*,
                    c.name as category_name,
                    c.color as category_color
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = %s
                ORDER BY t.date DESC, t.id DESC
            """
            cursor.execute(query, (user_id,))
            transactions_data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            transactions = []
            for data in transactions_data:
                transactions.append(Transaction(
                    id=data['id'],
                    user_id=data['user_id'],
                    amount=data['amount'],
                    transaction_type=data['type'],
                    description=data.get('description'),
                    date=data['date'],
                    category_id=data.get('category_id'),
                    category_name=data.get('category_name'),
                    category_color=data.get('category_color')
                ))
            
            return transactions
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    @staticmethod
    def get_by_id(transaction_id, user_id):
        """
        Holt spezifische Transaktion (mit Sicherheitscheck!)
        
        Returns:
            Transaction-Objekt oder None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    t.*,
                    c.name as category_name,
                    c.color as category_color
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.id = %s AND t.user_id = %s
            """
            cursor.execute(query, (transaction_id, user_id))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if data:
                return Transaction(
                    id=data['id'],
                    user_id=data['user_id'],
                    amount=data['amount'],
                    transaction_type=data['type'],
                    description=data.get('description'),
                    date=data['date'],
                    category_id=data.get('category_id'),
                    category_name=data.get('category_name'),
                    category_color=data.get('category_color')
                )
            return None
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
    
    @staticmethod
    def update(transaction_id, user_id, amount=None, transaction_type=None,
               description=None, date=None, category_id=None):
        """
        Aktualisiert Transaktion
        
        WICHTIG: category_id kann auf None gesetzt werden!
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            if amount is not None:
                updates.append("amount = %s")
                values.append(amount)
            if transaction_type is not None:
                updates.append("type = %s")
                values.append(transaction_type)
            if description is not None:
                updates.append("description = %s")
                values.append(description)
            if date is not None:
                updates.append("date = %s")
                values.append(date)
            if category_id is not None or category_id == 0:  # Explizit None setzen erlauben
                updates.append("category_id = %s")
                values.append(category_id if category_id != 0 else None)
            
            if not updates:
                return False
            
            values.extend([transaction_id, user_id])
            query = f"UPDATE transactions SET {', '.join(updates)} WHERE id = %s AND user_id = %s"
            
            cursor.execute(query, tuple(values))
            conn.commit()
            
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return affected > 0
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
    
    @staticmethod
    def delete(transaction_id, user_id):
        """
        Löscht Transaktion
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
            cursor.execute(query, (transaction_id, user_id))
            conn.commit()
            
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return affected > 0
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
    
    @staticmethod
    def get_summary_by_user(user_id):
        """
        Erstellt Zusammenfassung: Einnahmen, Ausgaben, Saldo
        
        Returns:
            Dict mit total_income, total_expenses, balance
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as total_income,
                    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as total_expenses
                FROM transactions 
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            total_income = float(result['total_income']) if result else 0
            total_expenses = float(result['total_expenses']) if result else 0
            
            return {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'balance': total_income - total_expenses
            }
        except Exception as e:
            print(f"Error getting summary: {e}")
            return {'total_income': 0, 'total_expenses': 0, 'balance': 0}
    
    @staticmethod
    def get_by_category(user_id):
        """
        Gruppiert Ausgaben nach Kategorie (für Charts!)
        
        WICHTIG: Macht JOIN mit categories Tabelle
        
        Returns:
            Dict mit Kategorie-Name → Betrag
            Beispiel: {'Lebensmittel': 150.00, 'Transport': 50.00}
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    COALESCE(c.name, 'Ohne Kategorie') as category_name,
                    c.color as category_color,
                    SUM(t.amount) as total
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = %s AND t.type = 'expense'
                GROUP BY t.category_id, c.name, c.color
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Gibt Dict zurück mit Name, Color UND Total
            return {
                row['category_name']: {
                    'total': float(row['total']),
                    'color': row.get('category_color', '#999999')
                }
                for row in results
            }
        except Exception as e:
            print(f"Error getting category summary: {e}")
            return {}