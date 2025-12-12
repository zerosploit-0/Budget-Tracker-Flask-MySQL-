"""
Authentication Service - Business-Logik für Authentifizierung
Angepasst an deine DB (ohne email)
"""
from models.user import User
from models.category import Category

class AuthService:
    """Authentication Service - Alle Auth-Logik"""
    
    @staticmethod
    def register_user(username, password):
        """
        Registriert neuen User
        
        Args:
            username: Benutzername
            password: Passwort
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validierung
        if not username or not password:
            return False, "Username und Passwort erforderlich"
        
        if len(username) < 3:
            return False, "Username muss mindestens 3 Zeichen lang sein"
        
        if len(password) < 6:
            return False, "Passwort muss mindestens 6 Zeichen lang sein"
        
        # Prüfe Existenz
        if User.username_exists(username):
            return False, "Username bereits vergeben"
        
        # Erstelle User
        if User.create(username, password):
            # Erstelle Standard-Kategorien für neuen User
            user = User.find_by_username(username)
            if user:
                Category.create_default_categories(user.id)
            
            return True, "Registrierung erfolgreich!"
        else:
            return False, "Fehler bei der Registrierung"
    
    @staticmethod
    def login_user(username, password):
        """
        Meldet User an
        
        Returns:
            tuple: (success: bool, user: User|None, message: str)
        """
        if not username or not password:
            return False, None, "Bitte alle Felder ausfüllen"
        
        user = User.find_by_username(username)
        
        if not user:
            return False, None, "Ungültiger Username oder Passwort"
        
        if not user.verify_password(password):
            return False, None, "Ungültiger Username oder Passwort"
        
        return True, user, "Login erfolgreich!"
    
    @staticmethod
    def get_user_by_id(user_id):
        """Holt User anhand ID"""
        return User.find_by_id(user_id)