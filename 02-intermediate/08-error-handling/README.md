# Module 08: Error Handling & Exceptions

## 🎯 Learning Objectives
- Understand Python exception hierarchy
- Handle exceptions with try-except-finally
- Create custom exceptions
- Use context managers for resource cleanup
- Implement logging for error tracking
- Apply best practices for error handling

## 📖 Exception Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                  PYTHON EXCEPTION HIERARCHY                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    BaseException                             │
│                         │                                    │
│         ┌───────────────┼───────────────┐                   │
│         │               │               │                   │
│    SystemExit    KeyboardInterrupt  Exception              │
│                                         │                   │
│         ┌───────────────────────────────┼─────────┐        │
│         │               │               │         │        │
│    ValueError    TypeError    IOError  Custom    ...       │
│         │                      │                           │
│    ├─ KeyError            ├─ FileNotFoundError            │
│    └─ IndexError          └─ PermissionError              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Basic Exception Handling

### Try-Except

```python
# Java:
"""
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
}
"""

# Python:
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
```

### Multiple Exceptions

```python
# Handle different exceptions
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result: {result}")
except ValueError:
    print("Invalid input! Please enter a number")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Catching Multiple Exception Types

```python
# Method 1: Separate handlers
try:
    # Some code
    pass
except (ValueError, TypeError) as e:
    print(f"Value or Type error: {e}")

# Method 2: Generic handler
try:
    # Some code
    pass
except Exception as e:
    print(f"Error: {e}")
```

## 2️⃣ Try-Except-Else-Finally

### Complete Structure

```python
try:
    # Code that might raise an exception
    file = open("data.txt", "r")
    data = file.read()
    number = int(data)
except FileNotFoundError:
    print("File not found")
except ValueError:
    print("Invalid data format")
else:
    # Executes if no exception occurred
    print(f"Successfully read number: {number}")
finally:
    # Always executes (cleanup code)
    if 'file' in locals():
        file.close()
    print("Cleanup completed")
```

### Else vs Finally

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    else:
        # Only runs if no exception
        print("Division successful")
        return result
    finally:
        # Always runs
        print("Division attempt completed")

print(divide(10, 2))   # Success case
print(divide(10, 0))   # Error case
```

## 3️⃣ Raising Exceptions

### Raise Statement

```python
def validate_age(age):
    """Validate age and raise exception if invalid"""
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")
```

### Re-raising Exceptions

```python
def process_data(data):
    try:
        # Process data
        result = int(data)
        return result
    except ValueError as e:
        print(f"Error processing data: {e}")
        raise  # Re-raise the same exception

try:
    process_data("invalid")
except ValueError:
    print("Caught re-raised exception")
```

### Raising from Another Exception

```python
def load_config(filename):
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Configuration file missing: {filename}") from e

try:
    load_config("config.txt")
except RuntimeError as e:
    print(f"Error: {e}")
    print(f"Original cause: {e.__cause__}")
```

## 4️⃣ Custom Exceptions

### Creating Custom Exceptions

```python
class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class DatabaseError(Exception):
    """Custom exception for database errors"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

class InsufficientFundsError(Exception):
    """Custom exception for banking operations"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        message = f"Insufficient funds: balance={balance}, required={amount}"
        super().__init__(message)

# Usage
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    new_balance = withdraw(100, 150)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"Balance: ${e.balance}, Attempted: ${e.amount}")
```

### Exception Hierarchy

```python
class ApplicationError(Exception):
    """Base exception for application"""
    pass

class DatabaseError(ApplicationError):
    """Database related errors"""
    pass

class NetworkError(ApplicationError):
    """Network related errors"""
    pass

class ConnectionError(NetworkError):
    """Connection specific errors"""
    pass

# Catch all application errors
try:
    raise ConnectionError("Failed to connect")
except ApplicationError as e:
    print(f"Application error: {e}")
```

## 5️⃣ Common Built-in Exceptions

### ValueError

```python
# Raised when operation receives wrong value type
try:
    number = int("abc")  # ValueError
except ValueError as e:
    print(f"ValueError: {e}")
```

### TypeError

```python
# Raised when operation applied to wrong type
try:
    result = "string" + 5  # TypeError
except TypeError as e:
    print(f"TypeError: {e}")
```

### KeyError

```python
# Raised when dictionary key doesn't exist
try:
    data = {"name": "Alice"}
    age = data["age"]  # KeyError
except KeyError as e:
    print(f"KeyError: {e}")
```

### IndexError

```python
# Raised when sequence index out of range
try:
    numbers = [1, 2, 3]
    value = numbers[10]  # IndexError
except IndexError as e:
    print(f"IndexError: {e}")
```

### FileNotFoundError

```python
# Raised when file doesn't exist
try:
    with open("nonexistent.txt") as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")
```

### AttributeError

```python
# Raised when attribute doesn't exist
try:
    text = "hello"
    text.nonexistent_method()  # AttributeError
except AttributeError as e:
    print(f"AttributeError: {e}")
```

## 6️⃣ Assertions

### Using Assertions

```python
def calculate_average(numbers):
    """Calculate average with assertion"""
    assert len(numbers) > 0, "List cannot be empty"
    assert all(isinstance(n, (int, float)) for n in numbers), "All items must be numbers"
    
    return sum(numbers) / len(numbers)

# Usage
try:
    avg = calculate_average([])
except AssertionError as e:
    print(f"Assertion failed: {e}")

# Assertions can be disabled with -O flag
# python -O script.py
```

### When to Use Assertions

```python
# ✓ Good: Internal consistency checks
def set_age(age):
    assert age >= 0, "Age must be non-negative"
    self.age = age

# ✗ Bad: User input validation (use exceptions instead)
def process_user_input(data):
    # Don't use assert for user input
    if not data:
        raise ValueError("Data cannot be empty")
```

## 7️⃣ Logging

### Basic Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

# Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
```

### Logging with Exceptions

```python
import logging

logger = logging.getLogger(__name__)

def divide(a, b):
    try:
        result = a / b
        logger.info(f"Division successful: {a}/{b} = {result}")
        return result
    except ZeroDivisionError:
        logger.error(f"Division by zero: {a}/{b}", exc_info=True)
        return None
    except Exception as e:
        logger.exception(f"Unexpected error in division: {e}")
        raise

# Usage
divide(10, 2)
divide(10, 0)
```

### Custom Logger

```python
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Usage
logger = setup_logger('my_app', 'app.log')
logger.info("Application started")
logger.error("An error occurred")
```

## 8️⃣ Best Practices

### 1. Be Specific with Exceptions

```python
# ✗ Bad: Too broad
try:
    result = process_data()
except Exception:
    print("Something went wrong")

# ✓ Good: Specific exceptions
try:
    result = process_data()
except ValueError as e:
    print(f"Invalid data: {e}")
except IOError as e:
    print(f"I/O error: {e}")
except Exception as e:
    logger.exception("Unexpected error")
    raise
```

### 2. Don't Silence Exceptions

```python
# ✗ Bad: Silent failure
try:
    risky_operation()
except:
    pass  # Never do this!

# ✓ Good: Log and handle
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    # Take appropriate action
```

### 3. Use Context Managers

```python
# ✗ Bad: Manual cleanup
file = open("data.txt")
try:
    data = file.read()
finally:
    file.close()

# ✓ Good: Context manager
with open("data.txt") as file:
    data = file.read()
```

### 4. Fail Fast

```python
# ✓ Good: Validate early
def process_user(user_id, email):
    if not user_id:
        raise ValueError("user_id is required")
    if not email or "@" not in email:
        raise ValueError("Valid email is required")
    
    # Process user
    return process(user_id, email)
```

## 9️⃣ Practical Examples

### Example 1: Robust File Reader

```python
import logging

logger = logging.getLogger(__name__)

def read_file_safely(filename, default=None):
    """Read file with comprehensive error handling"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info(f"Successfully read {filename}")
            return content
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        return default
    except PermissionError:
        logger.error(f"Permission denied: {filename}")
        return default
    except UnicodeDecodeError:
        logger.error(f"Encoding error in {filename}")
        return default
    except Exception as e:
        logger.exception(f"Unexpected error reading {filename}")
        raise

# Usage
content = read_file_safely("data.txt", default="")
```

### Example 2: Retry Decorator

```python
import time
import logging
from functools import wraps

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Decorator to retry function on exception"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    logging.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, delay=2, exceptions=(ConnectionError,))
def fetch_data(url):
    # Simulated API call
    import random
    if random.random() < 0.7:
        raise ConnectionError("Connection failed")
    return "Data fetched successfully"

try:
    result = fetch_data("https://api.example.com")
    print(result)
except ConnectionError:
    print("Failed after all retries")
```

### Example 3: Validation Framework

```python
class ValidationError(Exception):
    """Custom validation exception"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class Validator:
    """Data validation framework"""
    
    @staticmethod
    def validate_email(email):
        if not email or "@" not in email:
            raise ValidationError("email", "Invalid email format")
    
    @staticmethod
    def validate_age(age):
        if not isinstance(age, int):
            raise ValidationError("age", "Age must be an integer")
        if age < 0 or age > 150:
            raise ValidationError("age", "Age must be between 0 and 150")
    
    @staticmethod
    def validate_user(data):
        """Validate user data"""
        errors = []
        
        try:
            Validator.validate_email(data.get("email"))
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_age(data.get("age"))
        except ValidationError as e:
            errors.append(str(e))
        
        if errors:
            raise ValidationError("user", "; ".join(errors))

# Usage
try:
    user_data = {"email": "invalid", "age": -5}
    Validator.validate_user(user_data)
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## 💻 Complete Example

See `error_handling_demo.py` for comprehensive demonstrations.

## 🎯 Key Takeaways

1. **Be specific** - Catch specific exceptions, not generic Exception
2. **Don't silence** - Always log or handle exceptions
3. **Use finally** - For cleanup code that must run
4. **Custom exceptions** - Create meaningful exception hierarchies
5. **Log exceptions** - Use logging module for tracking
6. **Fail fast** - Validate early and raise exceptions
7. **Context managers** - For automatic resource cleanup
8. **Document exceptions** - In docstrings

## 🔗 Next Module

[Module 09: Data Structures →](../09-data-structures/)

## 📚 Additional Resources

- [Python Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Exception Handling Best Practices](https://realpython.com/python-exceptions/)