"""
Authentication service implementations following SOLID principles.
"""

import streamlit as st
from typing import Optional

from src.interfaces.auth_interfaces import (
    IAuthenticationService,
    ISessionManager,
    IPasswordValidator
)
from src.interfaces.data_interfaces import IUserRepository, IPasswordHasher


class PasswordValidator(IPasswordValidator):
    """
    Password validation implementation.
    
    SOLID Principles Applied:
    - SRP: Only validates passwords
    - OCP: Can be extended with additional validators without modification
    """
    
    def __init__(self, min_length: int = 4):
        self.min_length = min_length
    
    def validate(self, password: str) -> tuple[bool, str]:
        """
        Validate password against rules.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        if len(password) < self.min_length:
            return False, f"Password must be at least {self.min_length} characters long"
        return True, ""


class StreamlitSessionManager(ISessionManager):
    """
    Session manager using Streamlit's session state.
    
    SOLID Principles Applied:
    - SRP: Only manages session state
    - DIP: Implements ISessionManager interface
    - LSP: Can be replaced with Redis or other session stores
    """
    
    def __init__(self):
        # Initialize session state if not exists
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'username' not in st.session_state:
            st.session_state.username = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return st.session_state.get('logged_in', False)
    
    def get_username(self) -> Optional[str]:
        """Get current logged in username."""
        return st.session_state.get('username')
    
    def create_session(self, username: str) -> None:
        """Create a new session for user."""
        st.session_state.logged_in = True
        st.session_state.username = username
    
    def destroy_session(self) -> None:
        """Destroy current session."""
        st.session_state.logged_in = False
        st.session_state.username = None


class AuthenticationService(IAuthenticationService):
    """
    Authentication service implementation.
    
    SOLID Principles Applied:
    - SRP: Only handles authentication logic
    - DIP: Depends on IUserRepository and IPasswordHasher abstractions
    - OCP: Closed for modification, open for extension
    """
    
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        """
        Initialize with injected dependencies.
        
        DIP: Depends on abstractions, not concrete implementations.
        """
        self.user_repo = user_repository
        self.hasher = password_hasher
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user with credentials.
        
        SRP: Only validates credentials, doesn't manage session.
        """
        return self.validate_credentials(username, password)
    
    def register(self, username: str, password: str, email: str = '') -> bool:
        """
        Register a new user.
        
        SRP: Delegates user creation to repository.
        """
        if self.user_repo.user_exists(username):
            return False
        return self.user_repo.create_user(username, password, email)
    
    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials without creating session."""
        user = self.user_repo.get_user_by_username(username)
        if user is None:
            return False
        return self.hasher.verify_password(password, user['password'])
