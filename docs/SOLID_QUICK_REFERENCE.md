# SOLID Principles Quick Reference

## File Structure After Refactoring

```
cnn-pytorch-main/
├── interfaces/              # Layer 1: Abstractions (ISP, DIP)
│   ├── __init__.py
│   ├── auth_interfaces.py   # IAuthenticationService, ISessionManager, IPasswordValidator
│   ├── data_interfaces.py   # IUserRepository, IPasswordHasher, IDatabaseConnection  
│   └── prediction_interfaces.py  # IModelLoader, IPredictionService, etc.
│
├── services/                # Layer 2: Implementations (SRP, OCP, DIP)
│   ├── __init__.py
│   ├── auth_services.py     # AuthenticationService, StreamlitSessionManager, PasswordValidator
│   ├── data_services.py     # UserRepository, SQLiteConnection, SHA256PasswordHasher
│   └── prediction_services.py  # PredictionService, PyTorchModelLoader, etc.
│
├── database.py              # Layer 3: Facade (maintains backward compatibility)
├── auth.py                  # Layer 3: Facade (maintains backward compatibility)
├── predictor.py             # Layer 3: Facade (maintains backward compatibility)
└── app.py                   # Layer 4: UI Components (SRP for each page)
```

## SOLID Principles in Action

### Single Responsibility Principle (SRP)
**One class = One responsibility**

✅ **Good Examples:**
- `SHA256PasswordHasher` - only hashes passwords
- `UserRepository` - only manages user data
- `HomePageComponent` - only renders home page

❌ **Bad Example (Before):**
- `Database` - managed connections, queries, hashing, AND user operations

### Open/Closed Principle (OCP)
**Open for extension, closed for modification**

✅ **How to Extend:**
```python
# Want Redis sessions instead of Streamlit sessions?
class RedisSessionManager(ISessionManager):
    def is_logged_in(self): ...
    def create_session(self, username): ...
    # No changes to Auth class needed!

auth = Auth()  # Internally can use Redis now
```

### Liskov Substitution Principle (LSP)
**Subtypes must be substitutable**

✅ **Example:**
```python
# Both implement IPasswordHasher
hasher1 = SHA256PasswordHasher()
hasher2 = BCryptPasswordHasher()  # Future

# Can use either without changing code
repo = UserRepository(db_conn, hasher1)  # Works
repo = UserRepository(db_conn, hasher2)  # Also works
```

### Interface Segregation Principle (ISP)
**Small, focused interfaces**

✅ **Good (After):**
```python
class IAuthenticationService(ABC):
    def login(self, username, password): pass
    def register(self, username, password): pass

class ISessionManager(ABC):
    def is_logged_in(self): pass
    def create_session(self, username): pass
```

❌ **Bad (Before):**
```python
class IAuthSystem(ABC):
    def login(...): pass
    def register(...): pass
    def is_logged_in(...): pass
    def create_session(...): pass
    def get_username(...): pass
    def render_ui(...): pass  # Too many responsibilities!
```

### Dependency Inversion Principle (DIP)
**Depend on abstractions, not concretions**

✅ **Good (After):**
```python
class UserRepository:
    def __init__(self, 
                 db_connection: IDatabaseConnection,  # Abstract
                 hasher: IPasswordHasher):            # Abstract
        self.db = db_connection
        self.hasher = hasher
```

❌ **Bad (Before):**
```python
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(...)  # Concrete dependency
```

## Common Patterns Used

### 1. Dependency Injection
```python
# Constructor injection
class Auth:
    def __init__(self, db_path='users.db'):
        # Create dependencies
        db_connection = SQLiteConnection(db_path)
        password_hasher = SHA256PasswordHasher()
        
        # Inject into services
        user_repository = UserRepository(db_connection, password_hasher)
        self.auth_service = AuthenticationService(user_repository, password_hasher)
```

### 2. Facade Pattern
```python
# database.py provides simple API
class Database:
    def __init__(self, db_path='users.db'):
        # Internally uses multiple services
        self.db_connection = SQLiteConnection(db_path)
        self.password_hasher = SHA256PasswordHasher()
        self.user_repository = UserRepository(...)
    
    def create_user(self, username, password):
        # Delegates to service
        return self.user_repository.create_user(username, password)
```

### 3. Component-Based UI
```python
# Each page is a component with single responsibility
class HomePageComponent:
    def render(self, username):
        self._render_intro()
        self._render_features()
        self._render_diseases()
```

## How to Add New Features

### Example 1: Add Email Verification

1. **Create interface** (`interfaces/auth_interfaces.py`):
```python
class IEmailVerificationService(ABC):
    @abstractmethod
    def send_verification_email(self, email: str) -> bool: pass
    
    @abstractmethod
    def verify_code(self, email: str, code: str) -> bool: pass
```

2. **Implement service** (`services/auth_services.py`):
```python
class EmailVerificationService(IEmailVerificationService):
    def send_verification_email(self, email):
        # Implementation
        pass
```

3. **Inject into Auth**:
```python
class Auth:
    def __init__(self):
        # ... existing code ...
        self.email_verifier = EmailVerificationService()
```

4. **Use in UI**:
```python
def _render_register_tab(self):
    # ... existing code ...
    if self.email_verifier.send_verification_email(email):
        st.success("Verification email sent!")
```

### Example 2: Add Database Logging

1. **Create interface** (`interfaces/data_interfaces.py`):
```python
class IDatabaseLogger(ABC):
    @abstractmethod
    def log_query(self, query: str, params: tuple): pass
```

2. **Implement service** (`services/data_services.py`):
```python
class DatabaseLogger(IDatabaseLogger):
    def log_query(self, query, params):
        # Log to file or monitoring service
        pass
```

3. **Inject into SQLiteConnection**:
```python
class SQLiteConnection:
    def __init__(self, db_path, logger: IDatabaseLogger = None):
        self.logger = logger
    
    def execute_query(self, query, params):
        if self.logger:
            self.logger.log_query(query, params)
        # Execute query
```

## Testing Made Easy

### Before (Hard to Test):
```python
# Tightly coupled - must use real database
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
    
    def verify_user(self, username, password):
        # Direct SQL query
        cursor = self.conn.cursor()
        cursor.execute(...)
```

### After (Easy to Test):
```python
# Mock the interface
class MockUserRepository(IUserRepository):
    def get_user_by_username(self, username):
        return {'username': 'test', 'password': 'hashed'}

# Test without database
def test_authentication():
    mock_repo = MockUserRepository()
    mock_hasher = MockPasswordHasher()
    auth_service = AuthenticationService(mock_repo, mock_hasher)
    
    result = auth_service.login('test', 'password')
    assert result == True
```

## Benefits Summary

| Principle | Before | After | Benefit |
|-----------|--------|-------|---------|
| **SRP** | Mixed responsibilities | Focused classes | Easy to understand & modify |
| **OCP** | Hard to extend | Interface-based | Add features without breaking code |
| **LSP** | Concrete dependencies | Abstract dependencies | Swap implementations easily |
| **ISP** | Large interfaces | Small interfaces | Use only what you need |
| **DIP** | High-level → Low-level | Both → Abstractions | Easy to test & maintain |

## Remember

✅ **DO:**
- Create small, focused classes
- Depend on interfaces
- Use dependency injection
- Write tests for each component
- Document which SOLID principle you're applying

❌ **DON'T:**
- Mix responsibilities in one class
- Create tight coupling
- Hard-code dependencies
- Create large, monolithic classes
- Skip interface documentation
