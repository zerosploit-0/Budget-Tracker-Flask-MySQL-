"""
User Model - Angepasst an DB-Struktur

DB-Struktur:
- id INT
- username VARCHAR(190) UNIQUE
- password VARCHAR(255)  (gehashtes Passwort)
"""
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection

class User:
    """User Model für Benutzerverwaltung"""
    
    def __init__(self, id=None, username=None, password_hash=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    @staticmethod
    def create(username, password):
        """
        Erstellt neuen User
        
        Args:
            username: Benutzername
            password: Klartext-Passwort (wird gehasht)
            
        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            password_hash = generate_password_hash(password)
            
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password_hash))
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    @staticmethod
    def find_by_username(username):
        """
        Sucht User nach Username
        
        Returns:
            User-Objekt oder None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    password_hash=user_data['password']
                )
            return None
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
    
    @staticmethod
    def find_by_id(user_id):
        """
        Sucht User nach ID
        
        Returns:
            User-Objekt oder None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    password_hash=user_data['password']
                )
            return None
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None
    
    def verify_password(self, password):
        """
        Überprüft Passwort
        
        Args:
            password: Klartext-Passwort
            
        Returns:
            True wenn korrekt, sonst False
        """
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def username_exists(username):
        """
        Prüft ob Username bereits existiert
        
        Returns:
            True wenn existiert, sonst False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return count > 0
        except Exception as e:
            print(f"Error checking username: {e}")
            return False