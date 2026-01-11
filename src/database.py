"""
SQLite database helper for user authentication.

REFACTORED following SOLID principles:
- SRP: Delegates responsibilities to specialized services
- DIP: Uses dependency injection with interfaces
- OCP: New features can be added without modifying this class
- ISP: Uses small, focused interfaces

This maintains backward compatibility with existing code.
"""

from src.services.data_services import (
    SQLiteConnection,
    SHA256PasswordHasher,
    UserRepository
)


class Database:
    """
    Database class refactored with SOLID principles.
    
    SOLID Principles Applied:
    - SRP (Single Responsibility): Delegates to specialized services:
      * SQLiteConnection: manages database connections
      * SHA256PasswordHasher: handles password hashing
      * UserRepository: manages user data operations
    
    - DIP (Dependency Inversion): Depends on interfaces through service layer
      rather than concrete implementations
    
    - OCP (Open/Closed): Closed for modification, open for extension.
      New features (like different databases) can be added by creating
      new implementations of the interfaces.
    
    - LSP (Liskov Substitution): Maintains original interface contract,
      can be replaced with any compatible implementation
    """
    
    def __init__(self, db_path='data/users.db'):
        """
        Initialize database with dependency injection.
        
        DIP: Injects concrete implementations of interfaces.
        SRP: Each dependency has a single, well-defined responsibility.
        """
        # Create dependencies (following DIP)
        self.db_connection = SQLiteConnection(db_path)
        self.password_hasher = SHA256PasswordHasher()
        self.user_repository = UserRepository(
            self.db_connection,
            self.password_hasher
        )
        
        # Backward compatibility: expose db_path
        self.db_path = db_path
    
    def init_db(self):
        """
        Create users table if it doesn't exist.
        
        Note: This is now handled automatically in UserRepository.
        Kept for backward compatibility.
        """
        # Already initialized in UserRepository constructor
        pass
    
    def hash_password(self, password):
        """
        Hash password using SHA-256.
        
        SRP: Delegates to password hasher service.
        """
        return self.password_hasher.hash_password(password)
    
    def create_user(self, username, password, email=''):
        """
        Create a new user.
        
        Args:
            username: Username for the account
            password: Plain text password (will be hashed)
            email: Optional email address
            
        Returns:
            True if user created successfully, False otherwise
        
        SOLID:
        - SRP: Delegates to user repository
        - DIP: Uses interface-based repository
        """
        return self.user_repository.create_user(username, password, email)
    
    def verify_user(self, username, password):
        """
        Verify user credentials.
        
        Args:
            username: Username to verify
            password: Password to verify
            
        Returns:
            True if credentials are valid, False otherwise
        
        SOLID:
        - SRP: Combines repository and hasher through well-defined interfaces
        """
        user = self.user_repository.get_user_by_username(username)
        if user is None:
            return False
        return self.password_hasher.verify_password(password, user['password'])
    
    def user_exists(self, username):
        """
        Check if username already exists.
        
        SRP: Delegates to repository.
        """
        return self.user_repository.user_exists(username)
    
    def get_user_count(self):
        """
        Get total number of users.
        
        SRP: Delegates to repository.
        """
        return self.user_repository.get_user_count()
