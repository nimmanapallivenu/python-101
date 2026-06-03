"""
Comprehensive Data Types Demonstration
This file demonstrates all Python data types with practical examples
"""

from decimal import Decimal
from typing import Union, Optional


def numeric_types_demo():
    """Demonstrate numeric types: int, float, complex"""
    print("=" * 60)
    print("NUMERIC TYPES DEMONSTRATION")
    print("=" * 60)
    
    # Integer
    print("\n1. INTEGER (int)")
    print("-" * 40)
    age = 30
    year = 2024
    big_num = 999_999_999_999_999_999_999
    
    print(f"Age: {age}, Type: {type(age)}")
    print(f"Year: {year}")
    print(f"Big number: {big_num}")
    
    # Different number systems
    binary = 0b1010
    octal = 0o12
    hexadecimal = 0xA
    print(f"\nBinary 0b1010 = {binary}")
    print(f"Octal 0o12 = {octal}")
    print(f"Hexadecimal 0xA = {hexadecimal}")
    
    # Float
    print("\n2. FLOAT (float)")
    print("-" * 40)
    price = 19.99
    pi = 3.14159
    scientific = 1.5e2
    
    print(f"Price: ${price}")
    print(f"Pi: {pi}")
    print(f"Scientific notation 1.5e2 = {scientific}")
    
    # Float precision
    print(f"\nFloat precision issue: 0.1 + 0.2 = {0.1 + 0.2}")
    print(f"Using Decimal: {Decimal('0.1') + Decimal('0.2')}")
    
    # Complex
    print("\n3. COMPLEX (complex)")
    print("-" * 40)
    z = 3 + 4j
    print(f"Complex number: {z}")
    print(f"Real part: {z.real}")
    print(f"Imaginary part: {z.imag}")
    print(f"Conjugate: {z.conjugate()}")
    
    # Mathematical operations
    print("\n4. MATHEMATICAL OPERATIONS")
    print("-" * 40)
    a, b = 10, 3
    print(f"a = {a}, b = {b}")
    print(f"Addition (a + b): {a + b}")
    print(f"Subtraction (a - b): {a - b}")
    print(f"Multiplication (a * b): {a * b}")
    print(f"Division (a / b): {a / b}")
    print(f"Floor Division (a // b): {a // b}")
    print(f"Modulus (a % b): {a % b}")
    print(f"Exponentiation (a ** b): {a ** b}")


def string_types_demo():
    """Demonstrate string operations"""
    print("\n" + "=" * 60)
    print("STRING TYPE DEMONSTRATION")
    print("=" * 60)
    
    # String creation
    print("\n1. STRING CREATION")
    print("-" * 40)
    single = 'Single quotes'
    double = "Double quotes"
    triple = """Triple quotes
    for multi-line
    strings"""
    raw = r"C:\Users\name\Documents"
    
    print(f"Single: {single}")
    print(f"Double: {double}")
    print(f"Triple: {triple}")
    print(f"Raw string: {raw}")
    
    # String operations
    print("\n2. STRING OPERATIONS")
    print("-" * 40)
    text = "Python Programming"
    
    print(f"Original: {text}")
    print(f"Length: {len(text)}")
    print(f"Upper: {text.upper()}")
    print(f"Lower: {text.lower()}")
    print(f"Title: {text.title()}")
    print(f"Replace: {text.replace('Python', 'Java')}")
    
    # String slicing
    print("\n3. STRING SLICING")
    print("-" * 40)
    print(f"First 6 chars: {text[:6]}")
    print(f"Last 11 chars: {text[7:]}")
    print(f"Every 2nd char: {text[::2]}")
    print(f"Reverse: {text[::-1]}")
    
    # String methods
    print("\n4. STRING METHODS")
    print("-" * 40)
    email = "  user@example.com  "
    print(f"Original: '{email}'")
    print(f"Strip: '{email.strip()}'")
    print(f"Split: {text.split()}")
    print(f"Join: {'-'.join(['Python', 'is', 'awesome'])}")
    print(f"Starts with 'Python': {text.startswith('Python')}")
    print(f"Ends with 'ing': {text.endswith('ing')}")
    print(f"Find 'gram': {text.find('gram')}")
    print(f"Count 'o': {text.count('o')}")
    
    # String formatting
    print("\n5. STRING FORMATTING")
    print("-" * 40)
    name = "Alice"
    age = 30
    salary = 75000.50
    
    # f-strings (recommended)
    print(f"f-string: {name} is {age} years old, salary: ${salary:,.2f}")
    
    # format() method
    print("format(): {} is {} years old".format(name, age))
    
    # % formatting (old style)
    print("% format: %s is %d years old" % (name, age))
    
    # Advanced formatting
    print(f"\nRight align: '{name:>10}'")
    print(f"Left align: '{name:<10}'")
    print(f"Center: '{name:^10}'")
    print(f"Number with separator: {salary:,.2f}")


def boolean_demo():
    """Demonstrate boolean operations"""
    print("\n" + "=" * 60)
    print("BOOLEAN TYPE DEMONSTRATION")
    print("=" * 60)
    
    # Boolean values
    print("\n1. BOOLEAN VALUES")
    print("-" * 40)
    is_active = True
    is_deleted = False
    
    print(f"is_active: {is_active}, Type: {type(is_active)}")
    print(f"is_deleted: {is_deleted}")
    
    # Boolean operations
    print("\n2. BOOLEAN OPERATIONS")
    print("-" * 40)
    print(f"True and False: {True and False}")
    print(f"True or False: {True or False}")
    print(f"not True: {not True}")
    print(f"not False: {not False}")
    
    # Comparison operators
    print("\n3. COMPARISON OPERATORS")
    print("-" * 40)
    x, y = 10, 20
    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}")
    print(f"x != y: {x != y}")
    print(f"x > y: {x > y}")
    print(f"x < y: {x < y}")
    print(f"x >= y: {x >= y}")
    print(f"x <= y: {x <= y}")
    
    # Truthy and Falsy
    print("\n4. TRUTHY AND FALSY VALUES")
    print("-" * 40)
    falsy_values = [False, None, 0, 0.0, '', [], {}, ()]
    
    print("Falsy values:")
    for val in falsy_values:
        print(f"  bool({repr(val):10s}) = {bool(val)}")
    
    print("\nTruthy values:")
    truthy_values = [True, 1, "text", [1], {"key": "value"}, (1,)]
    for val in truthy_values:
        print(f"  bool({repr(val):20s}) = {bool(val)}")


def none_type_demo():
    """Demonstrate None type"""
    print("\n" + "=" * 60)
    print("NONE TYPE DEMONSTRATION")
    print("=" * 60)
    
    value = None
    
    print(f"value = {value}")
    print(f"Type: {type(value)}")
    print(f"value is None: {value is None}")
    print(f"value == None: {value == None}")  # Works but 'is' is preferred
    
    # None vs other falsy values
    print("\nNone vs other falsy values:")
    print(f"None == False: {None == False}")
    print(f"None == 0: {None == 0}")
    print(f"None == '': {None == ''}")
    print(f"None == []: {None == []}")


def type_conversion_demo():
    """Demonstrate type conversion"""
    print("\n" + "=" * 60)
    print("TYPE CONVERSION DEMONSTRATION")
    print("=" * 60)
    
    # String to number
    print("\n1. STRING TO NUMBER")
    print("-" * 40)
    num_str = "123"
    float_str = "3.14"
    
    print(f"String '{num_str}' to int: {int(num_str)}")
    print(f"String '{float_str}' to float: {float(float_str)}")
    
    # Number to string
    print("\n2. NUMBER TO STRING")
    print("-" * 40)
    age = 25
    price = 19.99
    
    print(f"Int {age} to string: '{str(age)}'")
    print(f"Float {price} to string: '{str(price)}'")
    
    # To boolean
    print("\n3. TO BOOLEAN")
    print("-" * 40)
    values = [0, 1, "", "text", [], [1], None]
    for val in values:
        print(f"bool({repr(val):10s}) = {bool(val)}")
    
    # Error handling
    print("\n4. CONVERSION ERRORS")
    print("-" * 40)
    try:
        invalid = int("abc")
    except ValueError as e:
        print(f"Error converting 'abc' to int: {e}")
    
    try:
        invalid = float("not a number")
    except ValueError as e:
        print(f"Error converting 'not a number' to float: {e}")


def type_checking_demo():
    """Demonstrate type checking"""
    print("\n" + "=" * 60)
    print("TYPE CHECKING DEMONSTRATION")
    print("=" * 60)
    
    # Different types
    integer = 10
    floating = 3.14
    string = "Hello"
    boolean = True
    none_val = None
    list_val = [1, 2, 3]
    
    # Using type()
    print("\n1. USING type()")
    print("-" * 40)
    print(f"type(10): {type(integer)}")
    print(f"type(3.14): {type(floating)}")
    print(f"type('Hello'): {type(string)}")
    print(f"type(True): {type(boolean)}")
    print(f"type(None): {type(none_val)}")
    print(f"type([1,2,3]): {type(list_val)}")
    
    # Using isinstance()
    print("\n2. USING isinstance()")
    print("-" * 40)
    print(f"isinstance(10, int): {isinstance(integer, int)}")
    print(f"isinstance(3.14, float): {isinstance(floating, float)}")
    print(f"isinstance('Hello', str): {isinstance(string, str)}")
    print(f"isinstance(True, bool): {isinstance(boolean, bool)}")
    print(f"isinstance([1,2,3], list): {isinstance(list_val, list)}")
    
    # Multiple types
    print("\n3. CHECKING MULTIPLE TYPES")
    print("-" * 40)
    print(f"isinstance(10, (int, float)): {isinstance(integer, (int, float))}")
    print(f"isinstance(3.14, (int, float)): {isinstance(floating, (int, float))}")
    print(f"isinstance('Hello', (int, float)): {isinstance(string, (int, float))}")


def mutability_demo():
    """Demonstrate mutability vs immutability"""
    print("\n" + "=" * 60)
    print("MUTABILITY DEMONSTRATION")
    print("=" * 60)
    
    # Immutable: String
    print("\n1. IMMUTABLE: STRING")
    print("-" * 40)
    text = "Hello"
    print(f"Original: {text}, ID: {id(text)}")
    
    text = text + " World"
    print(f"After concatenation: {text}, ID: {id(text)}")
    print("Notice: ID changed - new object created!")
    
    # Mutable: List
    print("\n2. MUTABLE: LIST")
    print("-" * 40)
    numbers = [1, 2, 3]
    print(f"Original: {numbers}, ID: {id(numbers)}")
    
    numbers.append(4)
    print(f"After append: {numbers}, ID: {id(numbers)}")
    print("Notice: ID same - object modified in place!")


def main():
    """Run all demonstrations"""
    print("\n" + "🐍" * 30)
    print("PYTHON DATA TYPES - COMPREHENSIVE DEMO")
    print("🐍" * 30)
    
    numeric_types_demo()
    string_types_demo()
    boolean_demo()
    none_type_demo()
    type_conversion_demo()
    type_checking_demo()
    mutability_demo()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
