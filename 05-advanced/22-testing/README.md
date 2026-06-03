# Module 22: Testing & Test-Driven Development

## 🎯 Learning Objectives
- Master pytest framework
- Implement Test-Driven Development (TDD)
- Write unit, integration, and end-to-end tests
- Use mocking and fixtures
- Measure code coverage
- Implement CI/CD testing

## 📖 Testing Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING PYRAMID                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                      ▲                                       │
│                     ╱ ╲                                      │
│                    ╱   ╲  E2E Tests (Few)                   │
│                   ╱─────╲                                    │
│                  ╱       ╲                                   │
│                 ╱         ╲ Integration Tests (Some)        │
│                ╱───────────╲                                 │
│               ╱             ╲                                │
│              ╱               ╲ Unit Tests (Many)            │
│             ╱─────────────────╲                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Pytest Basics

### Simple Test

```python
# test_calculator.py
def add(a, b):
    return a + b

def test_add():
    """Test addition function"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

# Run: pytest test_calculator.py
```

### Test Class

```python
# test_math_operations.py
class TestMathOperations:
    """Group related tests"""
    
    def test_addition(self):
        assert 2 + 2 == 4
    
    def test_subtraction(self):
        assert 5 - 3 == 2
    
    def test_multiplication(self):
        assert 3 * 4 == 12
    
    def test_division(self):
        assert 10 / 2 == 5
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

## 2️⃣ Fixtures

### Basic Fixture

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide test data"""
    return {"name": "John", "age": 30}

def test_user_data(sample_data):
    """Use fixture in test"""
    assert sample_data["name"] == "John"
    assert sample_data["age"] == 30
```

### Setup and Teardown

```python
import pytest

@pytest.fixture
def database_connection():
    """Setup and teardown database"""
    # Setup
    conn = create_connection()
    yield conn
    # Teardown
    conn.close()

def test_database_query(database_connection):
    result = database_connection.execute("SELECT * FROM users")
    assert len(result) > 0
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default, runs for each test
def function_fixture():
    return "function"

@pytest.fixture(scope="class")  # Runs once per test class
def class_fixture():
    return "class"

@pytest.fixture(scope="module")  # Runs once per module
def module_fixture():
    return "module"

@pytest.fixture(scope="session")  # Runs once per test session
def session_fixture():
    return "session"
```

## 3️⃣ Mocking

### Using unittest.mock

```python
from unittest.mock import Mock, patch
import requests

def get_user_data(user_id):
    """Fetch user data from API"""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

def test_get_user_data():
    """Test with mocked API call"""
    with patch('requests.get') as mock_get:
        # Configure mock
        mock_get.return_value.json.return_value = {
            "id": 1,
            "name": "John Doe"
        }
        
        # Test
        result = get_user_data(1)
        
        # Assertions
        assert result["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### pytest-mock

```python
def test_with_pytest_mock(mocker):
    """Using pytest-mock plugin"""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"id": 1, "name": "John"}
    
    result = get_user_data(1)
    assert result["name"] == "John"
```

## 4️⃣ Test-Driven Development (TDD)

### TDD Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                      TDD CYCLE                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. RED: Write failing test                                 │
│     ↓                                                        │
│  2. GREEN: Write minimal code to pass                       │
│     ↓                                                        │
│  3. REFACTOR: Improve code quality                          │
│     ↓                                                        │
│  4. REPEAT                                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### TDD Example

```python
# Step 1: Write test first (RED)
def test_calculate_total():
    cart = ShoppingCart()
    cart.add_item("Apple", 1.00, 3)
    cart.add_item("Banana", 0.50, 2)
    assert cart.calculate_total() == 4.00

# Step 2: Write minimal code (GREEN)
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, name, price, quantity):
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    
    def calculate_total(self):
        return sum(item['price'] * item['quantity'] for item in self.items)

# Step 3: Refactor if needed
```

## 5️⃣ Testing Flask Applications

### Flask Test Client

```python
import pytest
from flask import Flask

@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    
    @app.route('/api/users/<int:user_id>')
    def get_user(user_id):
        return {"id": user_id, "name": "John Doe"}
    
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_get_user(client):
    """Test API endpoint"""
    response = client.get('/api/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == "John Doe"
```

## 6️⃣ Database Testing

### Using Test Database

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def test_db():
    """Create test database"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(test_db):
    """Test user creation"""
    user = User(name="John", email="john@example.com")
    test_db.add(user)
    test_db.commit()
    
    retrieved = test_db.query(User).filter_by(email="john@example.com").first()
    assert retrieved.name == "John"
```

## 7️⃣ Code Coverage

### Measuring Coverage

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=myapp tests/

# Generate HTML report
pytest --cov=myapp --cov-report=html tests/

# View report
open htmlcov/index.html
```

### Coverage Configuration

```ini
# .coveragerc
[run]
source = myapp
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

## 8️⃣ Integration Testing

### API Integration Test

```python
import pytest
import requests

@pytest.fixture(scope="module")
def api_base_url():
    return "http://localhost:5000/api"

def test_user_workflow(api_base_url):
    """Test complete user workflow"""
    # Create user
    response = requests.post(f"{api_base_url}/users", json={
        "name": "John Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 201
    user_id = response.json()['id']
    
    # Get user
    response = requests.get(f"{api_base_url}/users/{user_id}")
    assert response.status_code == 200
    assert response.json()['name'] == "John Doe"
    
    # Update user
    response = requests.put(f"{api_base_url}/users/{user_id}", json={
        "name": "Jane Doe"
    })
    assert response.status_code == 200
    
    # Delete user
    response = requests.delete(f"{api_base_url}/users/{user_id}")
    assert response.status_code == 200
```

## 9️⃣ Best Practices

### Test Organization

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
├── e2e/
│   └── test_workflows.py
├── conftest.py  # Shared fixtures
└── pytest.ini   # Configuration
```

### Naming Conventions

```python
# ✓ Good test names
def test_user_creation_with_valid_data():
    pass

def test_user_creation_fails_with_invalid_email():
    pass

def test_calculate_total_returns_zero_for_empty_cart():
    pass

# ✗ Bad test names
def test1():
    pass

def test_user():
    pass
```

### AAA Pattern

```python
def test_shopping_cart_total():
    # Arrange
    cart = ShoppingCart()
    cart.add_item("Apple", 1.00, 3)
    cart.add_item("Banana", 0.50, 2)
    
    # Act
    total = cart.calculate_total()
    
    # Assert
    assert total == 4.00
```

## 🔟 Complete Example

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, name, price, quantity):
        if price < 0 or quantity < 0:
            raise ValueError("Price and quantity must be positive")
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    
    def remove_item(self, name):
        self.items = [item for item in self.items if item['name'] != name]
    
    def calculate_total(self):
        return sum(item['price'] * item['quantity'] for item in self.items)
    
    def apply_discount(self, percentage):
        if not 0 <= percentage <= 100:
            raise ValueError("Discount must be between 0 and 100")
        total = self.calculate_total()
        return total * (1 - percentage / 100)

# test_shopping_cart.py
import pytest

class TestShoppingCart:
    @pytest.fixture
    def cart(self):
        return ShoppingCart()
    
    def test_add_item(self, cart):
        cart.add_item("Apple", 1.00, 3)
        assert len(cart.items) == 1
        assert cart.items[0]['name'] == "Apple"
    
    def test_add_item_with_negative_price_raises_error(self, cart):
        with pytest.raises(ValueError):
            cart.add_item("Apple", -1.00, 3)
    
    def test_remove_item(self, cart):
        cart.add_item("Apple", 1.00, 3)
        cart.add_item("Banana", 0.50, 2)
        cart.remove_item("Apple")
        assert len(cart.items) == 1
        assert cart.items[0]['name'] == "Banana"
    
    def test_calculate_total(self, cart):
        cart.add_item("Apple", 1.00, 3)
        cart.add_item("Banana", 0.50, 2)
        assert cart.calculate_total() == 4.00
    
    @pytest.mark.parametrize("discount,expected", [
        (0, 4.00),
        (10, 3.60),
        (50, 2.00),
        (100, 0.00),
    ])
    def test_apply_discount(self, cart, discount, expected):
        cart.add_item("Apple", 1.00, 3)
        cart.add_item("Banana", 0.50, 2)
        assert cart.apply_discount(discount) == expected
    
    def test_apply_invalid_discount_raises_error(self, cart):
        with pytest.raises(ValueError):
            cart.apply_discount(150)
```

## 🎯 Key Takeaways

1. **Write tests first** - TDD approach
2. **Use fixtures** - Reusable test data
3. **Mock external dependencies** - Isolate tests
4. **Measure coverage** - Aim for >80%
5. **Follow AAA pattern** - Arrange, Act, Assert
6. **Name tests clearly** - Describe what's being tested
7. **Test edge cases** - Not just happy path
8. **Keep tests fast** - Quick feedback loop

## 🔗 Next Module

[Module 23: Performance Optimization →](../23-performance/)

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://testdriven.io/)
- [Python Testing Best Practices](https://realpython.com/python-testing/)