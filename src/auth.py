"""
Authentication module for Streamlit app.

REFACTORED following SOLID principles:
- SRP: Separates authentication, session management, and validation
- ISP: Uses small, focused interfaces
- DIP: Depends on abstractions, not concrete implementations
- OCP: Can extend with new auth methods without modification

Maintains backward compatibility with existing code.
"""

import streamlit as st
from src.services.auth_services import (
    AuthenticationService,
    StreamlitSessionManager,
    PasswordValidator
)
from src.services.data_services import (
    SQLiteConnection,
    SHA256PasswordHasher,
    UserRepository
)


class Auth:
    """
    Authentication class refactored with SOLID principles.
    
    SOLID Principles Applied:
    - SRP (Single Responsibility): Delegates to specialized services:
      * AuthenticationService: handles login/register logic
      * StreamlitSessionManager: manages session state
      * PasswordValidator: validates password rules
      * UserRepository: manages user data
    
    - ISP (Interface Segregation): Uses small, focused interfaces for
      each concern (IAuthenticationService, ISessionManager, etc.)
    
    - DIP (Dependency Inversion): All dependencies are injected and
      based on interfaces, not concrete implementations
    
    - OCP (Open/Closed): Can extend with new authentication methods
      (OAuth, LDAP, etc.) without modifying this class
    
    - LSP (Liskov Substitution): Each service can be substituted with
      any implementation of its interface
    """
    
    def __init__(self, db_path='data/users.db'):
        """
        Initialize authentication with dependency injection.
        
        DIP: All dependencies are injected and based on interfaces.
        """
        # Create data layer dependencies
        db_connection = SQLiteConnection(db_path)
        password_hasher = SHA256PasswordHasher()
        user_repository = UserRepository(db_connection, password_hasher)
        
        # Create service layer dependencies (following DIP)
        self.auth_service = AuthenticationService(user_repository, password_hasher)
        self.session_manager = StreamlitSessionManager()
        self.password_validator = PasswordValidator(min_length=4)
        
        # Store user repository for user count
        self.user_repository = user_repository
    
    def is_logged_in(self):
        """
        Check if user is logged in.
        
        SRP: Delegates to session manager.
        """
        return self.session_manager.is_logged_in()
    
    def get_username(self):
        """
        Get current logged in username.
        
        SRP: Delegates to session manager.
        """
        return self.session_manager.get_username()
    
    def login(self, username, password):
        """
        Attempt to log in user.
        
        Args:
            username: Username to login
            password: Password to verify
            
        Returns:
            True if login successful, False otherwise
        
        SOLID:
        - SRP: Separates authentication from session management
        - DIP: Uses interface-based services
        """
        # Authenticate (delegated to auth service)
        if self.auth_service.login(username, password):
            # Create session only after successful authentication
            self.session_manager.create_session(username)
            return True
        return False
    
    def logout(self):
        """
        Log out current user.
        
        SRP: Delegates to session manager.
        """
        self.session_manager.destroy_session()
    
    def register(self, username, password, email=''):
        """
        Register a new user.
        
        Args:
            username: Username for new account
            password: Password for new account
            email: Optional email address
            
        Returns:
            True if registration successful, False otherwise
        
        SOLID:
        - SRP: Delegates to authentication service
        - DIP: Uses interface-based service
        """
        return self.auth_service.register(username, password, email)
    
    def login_page(self):
        """
        Display login/registration page.
        
        SRP: Only handles UI rendering, delegates business logic to services.
        DIP: Uses services through interfaces.
        """
        st.title("🌾 Crop Disease Prediction System")
        st.markdown("### Welcome! Please login or register to continue")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            self._render_login_tab()
        
        with tab2:
            self._render_register_tab()
        
        # Show stats
        st.markdown("---")
        st.info(f"👥 Total registered users: {self.user_repository.get_user_count()}")
    
    def _render_login_tab(self):
        """
        Render login tab.
        
        SRP: Separate method for login UI rendering.
        OCP: Can extend UI without modifying main logic.
        """
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                elif self.login(username, password):
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    def _render_register_tab(self):
        """
        Render registration tab.
        
        SRP: Separate method for registration UI rendering.
        OCP: Can extend UI without modifying main logic.
        """
        st.subheader("Create New Account")
        with st.form("register_form"):
            new_username = st.text_input("Username", key="register_username")
            new_email = st.text_input("Email (optional)", key="register_email")
            new_password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            submit = st.form_submit_button("Register", use_container_width=True)
            
            if submit:
                # Validate inputs
                if not new_username or not new_password:
                    st.error("Username and password are required")
                    return
                
                # Use password validator service (SRP: separate validation logic)
                is_valid, error_msg = self.password_validator.validate(new_password)
                if not is_valid:
                    st.error(error_msg)
                    return
                
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                    return
                
                # Register user
                if self.register(new_username, new_password, new_email):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Username already exists")
