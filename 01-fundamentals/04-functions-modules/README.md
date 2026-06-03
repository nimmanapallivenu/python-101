# Module 04: Functions & Modules

## 🎯 Learning Objectives
- Master function definition and calling
- Understand parameters and return values
- Work with *args and **kwargs
- Create and import modules
- Understand scope and namespaces
- Use lambda functions and closures

## 📖 Functions Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FUNCTION ANATOMY                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  def function_name(parameters):                             │
│      """Docstring"""                                        │
│      # Function body                                        │
│      return result                                          │
│                                                              │
│  ┌──────────────┐                                           │
│  │   Input      │                                           │
│  │ (Parameters) │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │   Process    │                                           │
│  │  (Function   │                                           │
│  │    Body)     │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │   Output     │                                           │
│  │  (Return)    │                                           │
│  └──────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Basic Functions

### Simple Function

```python
# Java:
"""
public int add(int a, int b) {
    return a + b;
}
"""

# Python:
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

# Call function
result = add(5, 3)
print(result)  # 8
```

### Function with No Return

```python
def greet(name):
    """Print greeting message."""
    print(f"Hello, {name}!")

greet("Alice")  # Hello, Alice!
```

### Multiple Return Values

```python
def get_user_info():
    """Return multiple values as tuple."""
    name = "John"
    age = 30
    city = "NYC"
    return name, age, city

# Unpack return values
name, age, city = get_user_info()
print(f"{name}, {age}, {city}")
```

## 2️⃣ Function Parameters

### Default Parameters

```python
def greet(name, greeting="Hello"):
    """Greet with default greeting."""
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Bob", "Hi"))          # Hi, Bob!
print(greet("Charlie", greeting="Hey"))  # Hey, Charlie!
```

### Keyword Arguments

```python
def create_user(name, age, city, email):
    """Create user with named parameters."""
    return {
        "name": name,
        "age": age,
        "city": city,
        "email": email
    }

# Call with keyword arguments (order doesn't matter)
user = create_user(
    email="john@example.com",
    name="John",
    city="NYC",
    age=30
)
```

### *args (Variable Positional Arguments)

```python
def sum_all(*numbers):
    """Sum any number of arguments."""
    return sum(numbers)

print(sum_all(1, 2, 3))           # 6
print(sum_all(1, 2, 3, 4, 5))     # 15
print(sum_all(10, 20))            # 30

# Real-world example
def log_message(level, *messages):
    """Log multiple messages."""
    print(f"[{level}]", " ".join(messages))

log_message("INFO", "User", "logged", "in")
# [INFO] User logged in
```

### **kwargs (Variable Keyword Arguments)

```python
def create_profile(**details):
    """Create profile with any number of key-value pairs."""
    for key, value in details.items():
        print(f"{key}: {value}")

create_profile(name="Alice", age=30, city="NYC", job="Engineer")
# name: Alice
# age: 30
# city: NYC
# job: Engineer

# Real-world example
def build_query(table, **conditions):
    """Build SQL WHERE clause."""
    where_parts = [f"{key}='{value}'" for key, value in conditions.items()]
    return f"SELECT * FROM {table} WHERE {' AND '.join(where_parts)}"

query = build_query("users", age=30, city="NYC", active=True)
print(query)
# SELECT * FROM users WHERE age='30' AND city='NYC' AND active='True'
```

### Combining All Parameter Types

```python
def complex_function(required, *args, default="value", **kwargs):
    """Function with all parameter types."""
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Default: {default}")
    print(f"Kwargs: {kwargs}")

complex_function(
    "must_have",
    "extra1", "extra2",
    default="custom",
    key1="value1",
    key2="value2"
)
```

## 3️⃣ Lambda Functions

### Basic Lambda

```python
# Regular function
def square(x):
    return x ** 2

# Lambda (anonymous function)
square = lambda x: x ** 2

print(square(5))  # 25

# Common use with map, filter, sorted
numbers = [1, 2, 3, 4, 5]

# Map
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# Filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# Sorted
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]
sorted_users = sorted(users, key=lambda u: u["age"])
print([u["name"] for u in sorted_users])  # ['Bob', 'Alice', 'Charlie']
```

## 4️⃣ Scope and Namespaces

### Variable Scope

```python
# Global scope
global_var = "I'm global"

def outer_function():
    # Enclosing scope
    outer_var = "I'm in outer"
    
    def inner_function():
        # Local scope
        local_var = "I'm local"
        print(global_var)  # Can access global
        print(outer_var)   # Can access enclosing
        print(local_var)   # Can access local
    
    inner_function()

outer_function()
```

### Global and Nonlocal Keywords

```python
counter = 0

def increment():
    global counter  # Modify global variable
    counter += 1

increment()
print(counter)  # 1

def outer():
    count = 0
    
    def inner():
        nonlocal count  # Modify enclosing variable
        count += 1
        return count
    
    return inner

counter_func = outer()
print(counter_func())  # 1
print(counter_func())  # 2
```

## 5️⃣ Closures

### Basic Closure

```python
def make_multiplier(factor):
    """Create a multiplier function."""
    def multiplier(number):
        return number * factor
    return multiplier

# Create specific multipliers
times_2 = make_multiplier(2)
times_3 = make_multiplier(3)

print(times_2(5))  # 10
print(times_3(5))  # 15

# Real-world example: Logger factory
def create_logger(prefix):
    """Create logger with specific prefix."""
    def log(message):
        print(f"[{prefix}] {message}")
    return log

info_logger = create_logger("INFO")
error_logger = create_logger("ERROR")

info_logger("Application started")   # [INFO] Application started
error_logger("Connection failed")    # [ERROR] Connection failed
```

## 6️⃣ Decorators

### Basic Decorator

```python
def timing_decorator(func):
    """Measure function execution time."""
    import time
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    
    return wrapper

@timing_decorator
def slow_function():
    """Function that takes time."""
    import time
    time.sleep(1)
    return "Done"

result = slow_function()
# slow_function took 1.0012 seconds
```

### Decorator with Arguments

```python
def repeat(times):
    """Decorator that repeats function execution."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

## 7️⃣ Modules

### Creating a Module

```python
# mymath.py
"""Custom math module."""

PI = 3.14159

def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

class Calculator:
    """Simple calculator class."""
    
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self.result
```

### Importing Modules

```python
# Method 1: Import entire module
import mymath
result = mymath.add(5, 3)
print(mymath.PI)

# Method 2: Import specific items
from mymath import add, PI
result = add(5, 3)
print(PI)

# Method 3: Import with alias
import mymath as mm
result = mm.add(5, 3)

# Method 4: Import all (not recommended)
from mymath import *
result = add(5, 3)
```

### Module Structure

```
myproject/
├── main.py
├── utils/
│   ├── __init__.py
│   ├── math_utils.py
│   └── string_utils.py
└── models/
    ├── __init__.py
    └── user.py
```

```python
# utils/__init__.py
"""Utils package."""
from .math_utils import add, multiply
from .string_utils import capitalize

__all__ = ['add', 'multiply', 'capitalize']

# main.py
from utils import add, multiply
from models.user import User

result = add(5, 3)
user = User("Alice")
```

## 8️⃣ Built-in Functions

### Common Built-in Functions

```python
# map() - Apply function to all items
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# filter() - Filter items based on condition
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# reduce() - Reduce to single value
from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# zip() - Combine iterables
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
combined = list(zip(names, ages))
print(combined)  # [('Alice', 25), ('Bob', 30), ('Charlie', 35)]

# enumerate() - Get index and value
for index, name in enumerate(names):
    print(f"{index}: {name}")

# any() and all()
numbers = [2, 4, 6, 8]
print(all(x % 2 == 0 for x in numbers))  # True
print(any(x > 5 for x in numbers))       # True
```

## 9️⃣ Real-World Examples

### Example 1: Data Processing Pipeline

```python
def read_data(filename):
    """Read data from file."""
    with open(filename) as f:
        return [line.strip() for line in f]

def clean_data(data):
    """Remove empty lines and comments."""
    return [line for line in data if line and not line.startswith('#')]

def transform_data(data):
    """Transform data to uppercase."""
    return [line.upper() for line in data]

def save_data(data, filename):
    """Save data to file."""
    with open(filename, 'w') as f:
        f.write('\n'.join(data))

# Pipeline
def process_file(input_file, output_file):
    """Complete data processing pipeline."""
    data = read_data(input_file)
    data = clean_data(data)
    data = transform_data(data)
    save_data(data, output_file)

process_file('input.txt', 'output.txt')
```

### Example 2: API Request Handler

```python
import requests
from functools import wraps
import time

def retry(max_attempts=3, delay=1):
    """Retry decorator for API calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_user_data(user_id):
    """Fetch user data from API."""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()

# Usage
try:
    user = fetch_user_data(123)
    print(user)
except Exception as e:
    print(f"Failed to fetch user: {e}")
```

### Example 3: Configuration Manager

```python
class ConfigManager:
    """Manage application configuration."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
        return cls._instance
    
    def set(self, key, value):
        """Set configuration value."""
        self.config[key] = value
    
    def get(self, key, default=None):
        """Get configuration value."""
        return self.config.get(key, default)

# Usage
config = ConfigManager()
config.set('database_url', 'postgresql://localhost/mydb')
config.set('debug', True)

# Anywhere in the application
config2 = ConfigManager()  # Same instance
print(config2.get('database_url'))
```

## 🎯 Key Takeaways

1. **Functions are first-class** - Can be passed as arguments
2. ***args and **kwargs** - Flexible parameters
3. **Lambda functions** - Anonymous functions for simple operations
4. **Closures** - Functions that remember enclosing scope
5. **Decorators** - Modify function behavior
6. **Modules** - Organize code into reusable components
7. **Built-in functions** - Powerful tools (map, filter, reduce)

## 🔗 Next Module

[Module 05: OOP Basics →](../05-oop-basics/) (See Module 06 for comprehensive OOP)

## 📚 Additional Resources

- [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Modules](https://docs.python.org/3/tutorial/modules.html)
- [Decorators Guide](https://realpython.com/primer-on-python-decorators/)