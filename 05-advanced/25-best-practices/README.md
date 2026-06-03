# Module 25: Python Best Practices

## 🎯 Code Quality Guidelines

### 1. PEP 8 Style Guide
```python
# Good
def calculate_total(items):
    """Calculate total price of items."""
    return sum(item.price for item in items)

# Bad
def calculateTotal(Items):
    return sum([item.price for item in Items])
```

### 2. Type Hints
```python
from typing import List, Dict, Optional

def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    """Process list of users and return status."""
    if not users:
        return None
    return "processed"
```

### 3. Docstrings
```python
def fetch_user_data(user_id: int) -> Dict:
    """
    Fetch user data from database.
    
    Args:
        user_id: The unique identifier for the user
        
    Returns:
        Dictionary containing user data
        
    Raises:
        ValueError: If user_id is invalid
        DatabaseError: If database connection fails
    """
    pass
```

### 4. Error Handling
```python
# Good
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
finally:
    cleanup()

# Bad
try:
    result = risky_operation()
except:
    pass
```

### 5. Context Managers
```python
# Good
with open('file.txt') as f:
    data = f.read()

# Bad
f = open('file.txt')
data = f.read()
f.close()
```

### 6. List Comprehensions
```python
# Good
squares = [x**2 for x in range(10)]

# Bad
squares = []
for x in range(10):
    squares.append(x**2)
```

### 7. Use Built-in Functions
```python
# Good
total = sum(numbers)
maximum = max(numbers)

# Bad
total = 0
for num in numbers:
    total += num
```

### 8. Avoid Mutable Default Arguments
```python
# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad
def add_item(item, items=[]):
    items.append(item)
    return items
```

### 9. Use Enums
```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# Usage
order_status = Status.PENDING
```

### 10. Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.error("An error occurred", exc_info=True)
```

## 🎯 Project Structure
```
myproject/
├── src/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

## 🔗 Resources
- [PEP 8](https://pep8.org/)
- [Python Guide](https://docs.python-guide.org/)
- [Real Python](https://realpython.com/)

## 🎉 Congratulations!
You've completed all Python modules. You're now ready to build production-grade Python applications!