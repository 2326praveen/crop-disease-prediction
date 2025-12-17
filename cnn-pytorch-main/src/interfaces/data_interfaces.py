"""
Data layer interfaces following SOLID principles.

These interfaces demonstrate:
- Interface Segregation Principle: Separate interfaces for different responsibilities
- Dependency Inversion Principle: High-level modules depend on these abstractions
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class IUserRepository(ABC):
    """
    Interface for user data operations.
    
    ISP: This interface is focused only on user CRUD operations.
    DIP: Authentication and other modules depend on this abstraction, not concrete implementation.
    """
    
    @abstractmethod
    def create_user(self, username: str, password: str, email: str = '') -> bool:
        """Create a new user."""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by username."""
        pass
    
    @abstractmethod
    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        pass
    
    @abstractmethod
    def get_user_count(self) -> int:
        """Get total number of users."""
        pass


class IPasswordHasher(ABC):
    """
    Interface for password hashing operations.
    
    ISP: Separate interface for password hashing, not mixed with database operations.
    DIP: Any password hashing algorithm can be used by implementing this interface.
    SRP: Single responsibility - only password hashing.
    """
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a plain text password."""
        pass
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        pass


class IDatabaseConnection(ABC):
    """
    Interface for database connection operations.
    
    ISP: Focused only on connection management.
    OCP: New database types can be added by implementing this interface.
    """
    
    @abstractmethod
    def connect(self):
        """Establish database connection."""
        pass
    
    @abstractmethod
    def close(self):
        """Close database connection."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a database query."""
        pass
    
    @abstractmethod
    def execute_commit(self, query: str, params: tuple = ()) -> bool:
        """Execute a query and commit changes."""
        pass
