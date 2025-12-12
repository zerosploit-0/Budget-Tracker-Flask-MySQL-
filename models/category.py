"""
Category Model - Angepasst an DB-Struktur

DB-Struktur:
- id INT
- user_id INT (NOT NULL - alle Kategorien sind user-spezifisch!)
- name VARCHAR(100)
- color CHAR(7) (z.B. '#FF6384')
- UNIQUE (user_id, name) - Jeder User kann eigene "Food" Kategorie haben
"""
from db_config import get_db_connection

class Category:
    """Category Model für Kategorienverwaltung"""
    
    def __init__(self, id=None, user_id=None, name=None, color=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.color = color
    
    @staticmethod
    def create(user_id, name, color='#999999'):
        """
        Erstellt neue Kategorie
        
        Args:
            user_id: User-ID (erforderlich!)
            name: Kategorie-Name
            color: Hex-Farbe (Standard: #999999)
            
        Returns:
            Category-ID bei Erfolg, None bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "INSERT INTO categories (user_id, name, color) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, name, color))
            conn.commit()
            
            category_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            return category_id
        except Exception as e:
            print(f"Error creating category: {e}")
            return None
    
    @staticmethod
    def get_all_by_user(user_id):
        """
        Holt alle Kategorien eines Users
        
        Returns:
            Liste von Category-Objekten
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM categories WHERE user_id = %s ORDER BY name"
            cursor.execute(query, (user_id,))
            categories_data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            categories = []
            for data in categories_data:
                categories.append(Category(
                    id=data['id'],
                    user_id=data['user_id'],
                    name=data['name'],
                    color=data['color']
                ))
            
            return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    @staticmethod
    def get_by_id(category_id, user_id):
        """
        Holt spezifische Kategorie (mit Sicherheitscheck!)
        
        Args:
            category_id: Kategorie-ID
            user_id: User-ID (Sicherheit!)
            
        Returns:
            Category-Objekt oder None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM categories WHERE id = %s AND user_id = %s"
            cursor.execute(query, (category_id, user_id))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if data:
                return Category(
                    id=data['id'],
                    user_id=data['user_id'],
                    name=data['name'],
                    color=data['color']
                )
            return None
        except Exception as e:
            print(f"Error getting category: {e}")
            return None
    
    @staticmethod
    def update(category_id, user_id, name=None, color=None):
        """
        Aktualisiert Kategorie
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            if name is not None:
                updates.append("name = %s")
                values.append(name)
            if color is not None:
                updates.append("color = %s")
                values.append(color)
            
            if not updates:
                return False
            
            values.extend([category_id, user_id])
            query = f"UPDATE categories SET {', '.join(updates)} WHERE id = %s AND user_id = %s"
            
            cursor.execute(query, tuple(values))
            conn.commit()
            
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return affected > 0
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
    
    @staticmethod
    def delete(category_id, user_id):
        """
        Löscht Kategorie
        
        WICHTIG: Transactions mit dieser Kategorie werden auf category_id=NULL gesetzt
        (wegen ON DELETE SET NULL in DB)
        
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM categories WHERE id = %s AND user_id = %s"
            cursor.execute(query, (category_id, user_id))
            conn.commit()
            
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return affected > 0
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
    
    @staticmethod
    def name_exists(user_id, name, exclude_id=None):
        """
        Prüft ob Kategorie-Name bereits existiert (für diesen User!)
        
        Args:
            user_id: User-ID
            name: Kategorie-Name
            exclude_id: Optional - bei Update, ignoriere diese ID
            
        Returns:
            True wenn existiert, False sonst
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if exclude_id:
                query = "SELECT COUNT(*) FROM categories WHERE user_id = %s AND name = %s AND id != %s"
                cursor.execute(query, (user_id, name, exclude_id))
            else:
                query = "SELECT COUNT(*) FROM categories WHERE user_id = %s AND name = %s"
                cursor.execute(query, (user_id, name))
            
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return count > 0
        except Exception as e:
            print(f"Error checking category name: {e}")
            return False
    
    @staticmethod
    def create_default_categories(user_id):
        """
        Erstellt Standard-Kategorien für neuen User
        
        Wird aufgerufen nach User-Registrierung
        
        Returns:
            Anzahl erstellter Kategorien
        """
        default_categories = [
            ('Lebensmittel', '#FF6384'),
            ('Transport', '#36A2EB'),
            ('Wohnung', '#FFCE56'),
            ('Unterhaltung', '#4BC0C0'),
            ('Einkaufen', '#9966FF'),
            ('Gesundheit', '#FF9F40'),
            ('Bildung', '#E7E9ED'),
            ('Gehalt', '#4BC0C0'),
            ('Sonstiges', '#95A5A6')
        ]
        
        count = 0
        for name, color in default_categories:
            if Category.create(user_id, name, color):
                count += 1
        
        return count