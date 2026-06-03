# Module 02: Data Types & Variables

## 🎯 Learning Objectives
- Master Python's built-in data types
- Understand type conversion and type checking
- Learn string manipulation techniques
- Work with numbers and mathematical operations
- Understand mutability vs immutability

## 📖 Python Data Types Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PYTHON DATA TYPES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TEXT TYPE:      str                                         │
│  NUMERIC TYPES:  int, float, complex                         │
│  SEQUENCE TYPES: list, tuple, range                          │
│  MAPPING TYPE:   dict                                        │
│  SET TYPES:      set, frozenset                              │
│  BOOLEAN TYPE:   bool                                        │
│  BINARY TYPES:   bytes, bytearray, memoryview               │
│  NONE TYPE:      NoneType                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Numeric Types

### Integer (int)

```python
# Java: int x = 10;
# Python: No size limit!

x = 10
y = -5
big_number = 999999999999999999999999999999  # No overflow!

# Binary, Octal, Hexadecimal
binary = 0b1010      # 10 in decimal
octal = 0o12         # 10 in decimal
hexadecimal = 0xA    # 10 in decimal

print(f"Binary {binary}, Octal {octal}, Hex {hexadecimal}")

# Underscore for readability (Python 3.6+)
million = 1_000_000
print(f"One million: {million}")
```

### Float (float)

```python
# Java: double price = 19.99;
# Python: Always 64-bit precision

price = 19.99
pi = 3.14159
scientific = 1.5e2  # 150.0

# Float precision issues (same as Java)
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")  # 0.30000000000000004

# Solution: Use decimal module for precision
from decimal import Decimal
precise = Decimal('0.1') + Decimal('0.2')
print(f"Precise: {precise}")  # 0.3
```

### Complex (complex)

```python
# Not available in Java by default
z = 3 + 4j
print(f"Real: {z.real}, Imaginary: {z.imag}")
print(f"Conjugate: {z.conjugate()}")
```

### Mathematical Operations

```python
# Basic operations
a, b = 10, 3

print(f"Addition: {a + b}")        # 13
print(f"Subtraction: {a - b}")     # 7
print(f"Multiplication: {a * b}")  # 30
print(f"Division: {a / b}")        # 3.333...
print(f"Floor Division: {a // b}") # 3 (like Java's int division)
print(f"Modulus: {a % b}")         # 1
print(f"Exponentiation: {a ** b}") # 1000 (10^3)

# Java equivalent: Math.pow(a, b)
# Python: a ** b or pow(a, b)
```

## 2️⃣ String Type (str)

### String Creation

```python
# Multiple ways to create strings
single = 'Hello'
double = "World"
triple_single = '''Multi
line
string'''
triple_double = """Another
multi-line
string"""

# Raw strings (ignore escape sequences)
path = r"C:\Users\name\Documents"  # No need to escape backslashes

# f-strings (formatted string literals)
name = "Python"
version = 3.11
message = f"{name} version {version}"
```

### String Operations

```python
text = "Python Programming"

# Length
print(f"Length: {len(text)}")  # 18

# Indexing (0-based, like Java)
print(f"First char: {text[0]}")   # P
print(f"Last char: {text[-1]}")   # g (negative indexing!)

# Slicing [start:end:step]
print(f"First 6: {text[0:6]}")    # Python
print(f"First 6: {text[:6]}")     # Python (same)
print(f"Last 11: {text[7:]}")     # Programming
print(f"Every 2nd: {text[::2]}")  # Pto rgamn
print(f"Reverse: {text[::-1]}")   # gnimmargorP nohtyP

# String methods (immutable - returns new string)
print(f"Upper: {text.upper()}")
print(f"Lower: {text.lower()}")
print(f"Replace: {text.replace('Python', 'Java')}")
print(f"Split: {text.split()}")   # ['Python', 'Programming']
print(f"Starts with: {text.startswith('Python')}")  # True
print(f"Ends with: {text.endswith('ing')}")         # True
```

### String Formatting

```python
name = "Alice"
age = 30
salary = 75000.50

# Method 1: f-strings (Python 3.6+, RECOMMENDED)
print(f"Name: {name}, Age: {age}, Salary: ${salary:,.2f}")

# Method 2: format() method
print("Name: {}, Age: {}, Salary: ${:,.2f}".format(name, age, salary))

# Method 3: % formatting (old style)
print("Name: %s, Age: %d, Salary: $%.2f" % (name, age, salary))

# Advanced f-string formatting
print(f"{name:>10}")      # Right align in 10 chars
print(f"{name:<10}")      # Left align
print(f"{name:^10}")      # Center align
print(f"{salary:,.2f}")   # Thousand separator with 2 decimals
```

## 3️⃣ Boolean Type (bool)

```python
# Java: boolean flag = true;
# Python: True/False (capitalized!)

is_active = True
is_deleted = False

# Boolean operations
print(f"AND: {True and False}")   # False
print(f"OR: {True or False}")     # True
print(f"NOT: {not True}")         # False

# Comparison operators
x, y = 10, 20
print(f"Equal: {x == y}")         # False
print(f"Not equal: {x != y}")     # True
print(f"Greater: {x > y}")        # False
print(f"Less or equal: {x <= y}") # True

# Truthy and Falsy values
# Falsy: False, None, 0, 0.0, '', [], {}, ()
# Everything else is Truthy

if []:
    print("Empty list is truthy")
else:
    print("Empty list is falsy")  # This prints

if [1, 2, 3]:
    print("Non-empty list is truthy")  # This prints
```

## 4️⃣ None Type

```python
# Java: null
# Python: None

value = None

if value is None:  # Use 'is' for None comparison
    print("Value is None")

# None is not the same as False, 0, or empty string
print(f"None == False: {None == False}")  # False
print(f"None is False: {None is False}")  # False
```

## 5️⃣ Type Conversion

```python
# Implicit conversion (automatic)
x = 10      # int
y = 3.14    # float
result = x + y  # result is float (10 + 3.14 = 13.14)

# Explicit conversion (casting)
# int()
num_str = "123"
num_int = int(num_str)
print(f"String to int: {num_int}, type: {type(num_int)}")

# float()
num_float = float("3.14")
print(f"String to float: {num_float}")

# str()
age = 25
age_str = str(age)
print(f"Int to string: '{age_str}', type: {type(age_str)}")

# bool()
print(f"bool(1): {bool(1)}")      # True
print(f"bool(0): {bool(0)}")      # False
print(f"bool(''): {bool('')}")    # False
print(f"bool('hi'): {bool('hi')}")  # True

# Error handling in conversion
try:
    invalid = int("abc")
except ValueError as e:
    print(f"Conversion error: {e}")
```

## 6️⃣ Type Checking

```python
x = 10
y = "Hello"
z = [1, 2, 3]

# type() function
print(f"Type of x: {type(x)}")  # <class 'int'>
print(f"Type of y: {type(y)}")  # <class 'str'>
print(f"Type of z: {type(z)}")  # <class 'list'>

# isinstance() function (preferred for type checking)
print(f"Is x an int? {isinstance(x, int)}")        # True
print(f"Is y a str? {isinstance(y, str)}")         # True
print(f"Is z a list? {isinstance(z, list)}")       # True

# Multiple types
print(f"Is x int or float? {isinstance(x, (int, float))}")  # True
```

## 🎨 Mutability vs Immutability

```
┌─────────────────────────────────────────────────────────────┐
│                    MUTABILITY CONCEPT                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  IMMUTABLE (Cannot be changed after creation):              │
│    • int, float, complex, bool                              │
│    • str, tuple, frozenset                                  │
│                                                              │
│  MUTABLE (Can be changed after creation):                   │
│    • list, dict, set                                        │
│    • Custom objects (by default)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

```python
# Immutable example (string)
text = "Hello"
print(f"Original: {text}, ID: {id(text)}")

text = text + " World"  # Creates NEW string
print(f"Modified: {text}, ID: {id(text)}")  # Different ID!

# Mutable example (list)
numbers = [1, 2, 3]
print(f"Original: {numbers}, ID: {id(numbers)}")

numbers.append(4)  # Modifies SAME list
print(f"Modified: {numbers}, ID: {id(numbers)}")  # Same ID!
```

## 💻 Complete Example

See `data_types_demo.py` for a comprehensive demonstration.

## 🏋️ Exercises

1. **Number Operations**: Create a program that performs all mathematical operations
2. **String Manipulation**: Parse and format user information
3. **Type Conversion**: Build a calculator that handles string inputs
4. **Boolean Logic**: Implement a simple authentication system

See `exercises.py` for exercise templates and `solutions.py` for answers.

## 🎯 Key Takeaways

1. **Dynamic typing** - Variables can change types
2. **No primitive types** - Everything is an object
3. **Immutable strings** - String operations create new strings
4. **Truthy/Falsy** - Many values evaluate to True/False
5. **None vs null** - Use `is None` for comparison
6. **f-strings** - Modern, readable string formatting
7. **Type hints** - Optional but recommended for clarity

## 🔗 Next Module

[Module 03: Control Flow →](../03-control-flow/)

## 📚 Additional Resources

- [Python Data Types Documentation](https://docs.python.org/3/library/stdtypes.html)
- [String Formatting Guide](https://realpython.com/python-f-strings/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)