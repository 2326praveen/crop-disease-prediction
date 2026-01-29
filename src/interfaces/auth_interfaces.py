"""
Authentication interfaces following SOLID principles.

These interfaces demonstrate:
- Interface Segregation Principle: Separate interfaces for different auth concerns
- Dependency Inversion Principle: UI depends on these abstractions
"""

from abc import ABC, abstractmethod
from typing import Optional


class IAuthenticationService(ABC):
    """
    Interface for authentication operations.
    
    ISP: Focused only on authentication logic.
    DIP: UI components depend on this abstraction, not concrete implementation.
    SRP: Only handles authentication, not session management or UI.
    """
    
    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        """Authenticate user with credentials."""
        pass
    
    @abstractmethod
    def register(self, username: str, password: str, email: str = '') -> bool:
        """Register a new user."""
        pass
    
    @abstractmethod
    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials without logging in."""
        pass


class ISessionManager(ABC):
    """
    Interface for session management.
    
    ISP: Separate interface for session management, not mixed with authentication.
    DIP: Any session storage (memory, Redis, etc.) can be used.
    SRP: Only manages session state.
    """
    
    @abstractmethod
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        pass
    
    @abstractmethod
    def get_username(self) -> Optional[str]:
        """Get current logged in username."""
        pass
    
    @abstractmethod
    def create_session(self, username: str) -> None:
        """Create a new session for user."""
        pass
    
    @abstractmethod
    def destroy_session(self) -> None:
        """Destroy current session."""
        pass


class IPasswordValidator(ABC):
    """
    Interface for password validation rules.
    
    ISP: Separate interface for validation logic.
    OCP: New validation rules can be added without modifying existing code.
    SRP: Only validates passwords.
    """
    
    @abstractmethod
    def validate(self, password: str) -> tuple[bool, str]:
        """
        Validate password against rules.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        pass
