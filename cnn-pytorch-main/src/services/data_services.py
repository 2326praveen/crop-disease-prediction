"""
Service implementations following SOLID principles.

This module contains concrete implementations of data interfaces.
"""

import sqlite3
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any

from src.interfaces.data_interfaces import (
    IUserRepository, 
    IPasswordHasher, 
    IDatabaseConnection
)


class SHA256PasswordHasher(IPasswordHasher):
    """
    SHA-256 password hasher implementation.
    
    SOLID Principles Applied:
    - SRP: Only responsible for password hashing
    - DIP: Implements IPasswordHasher interface
    - LSP: Can be substituted with any IPasswordHasher implementation
    """
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return self.hash_password(plain_password) == hashed_password


class SQLiteConnection(IDatabaseConnection):
    """
    SQLite database connection manager.
    
    SOLID Principles Applied:
    - SRP: Only manages database connections and queries
    - OCP: Can be extended without modification
    - DIP: Implements IDatabaseConnection interface
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish connection to SQLite database."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a SELECT query and return results."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    
    def execute_commit(self, query: str, params: tuple = ()) -> bool:
        """Execute an INSERT/UPDATE/DELETE query and commit."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception:
            return False


class UserRepository(IUserRepository):
    """
    User repository implementation using SQLite.
    
    SOLID Principles Applied:
    - SRP: Only handles user data operations
    - DIP: Depends on IDatabaseConnection and IPasswordHasher abstractions
    - OCP: Closed for modification, open for extension
    - ISP: Implements only user-related operations
    """
    
    def __init__(self, db_connection: IDatabaseConnection, password_hasher: IPasswordHasher):
        """
        Initialize repository with injected dependencies.
        
        DIP: Depends on abstractions (interfaces), not concrete implementations.
        """
        self.db = db_connection
        self.hasher = password_hasher
        self._init_table()
    
    def _init_table(self):
        """Create users table if it doesn't exist."""
        self.db.execute_commit('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def create_user(self, username: str, password: str, email: str = '') -> bool:
        """
        Create a new user with hashed password.
        
        SRP: Only creates user, delegates hashing to IPasswordHasher.
        """
        hashed_password = self.hasher.hash_password(password)
        return self.db.execute_commit(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, hashed_password, email)
        )
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by username."""
        result = self.db.execute_query(
            'SELECT id, username, password, email, created_at FROM users WHERE username = ?',
            (username,)
        )
        if result:
            row = result[0]
            return {
                'id': row[0],
                'username': row[1],
                'password': row[2],
                'email': row[3],
                'created_at': row[4]
            }
        return None
    
    def user_exists(self, username: str) -> bool:
        """Check if username exists."""
        return self.get_user_by_username(username) is not None
    
    def get_user_count(self) -> int:
        """Get total number of users."""
        result = self.db.execute_query('SELECT COUNT(*) FROM users')
        return result[0][0] if result else 0
