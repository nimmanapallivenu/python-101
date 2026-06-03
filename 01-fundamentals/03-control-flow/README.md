# Module 03: Control Flow

## 🎯 Learning Objectives
- Master if-elif-else statements
- Understand Python's for and while loops
- Learn loop control statements (break, continue, pass)
- Work with range() and enumerate()
- Understand list comprehensions
- Master pattern matching (Python 3.10+)

## 📖 Control Flow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL FLOW STRUCTURES                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CONDITIONAL:                                                │
│    • if-elif-else                                           │
│    • Ternary operator                                       │
│    • match-case (Python 3.10+)                              │
│                                                              │
│  LOOPS:                                                      │
│    • for loop                                               │
│    • while loop                                             │
│    • Loop control: break, continue, pass                    │
│                                                              │
│  COMPREHENSIONS:                                             │
│    • List comprehension                                     │
│    • Dict comprehension                                     │
│    • Set comprehension                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ If-Elif-Else Statements

### Basic If Statement

```python
# Java:
# if (condition) {
#     // code
# }

# Python:
age = 18

if age >= 18:
    print("You are an adult")
    print("You can vote")  # Indentation defines the block!

# No braces needed!
```

### If-Else

```python
temperature = 25

if temperature > 30:
    print("It's hot!")
else:
    print("It's comfortable")
```

### If-Elif-Else

```python
score = 85

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(f"Your grade is: {grade}")
```

### Comparison with Java

```python
# Java:
"""
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else {
    grade = "F";
}
"""

# Python:
if score >= 90:
    grade = "A"
elif score >= 80:  # Note: elif, not "else if"
    grade = "B"
else:
    grade = "F"
```

### Nested If Statements

```python
age = 25
has_license = True

if age >= 18:
    if has_license:
        print("You can drive")
    else:
        print("You need a license")
else:
    print("You're too young to drive")
```

### Ternary Operator (Conditional Expression)

```python
# Java: String result = (age >= 18) ? "Adult" : "Minor";
# Python:
age = 20
result = "Adult" if age >= 18 else "Minor"
print(result)

# More examples
max_value = a if a > b else b
status = "Pass" if score >= 60 else "Fail"
message = "Even" if num % 2 == 0 else "Odd"
```

## 2️⃣ For Loops

### Basic For Loop

```python
# Java:
# for (int i = 0; i < 5; i++) {
#     System.out.println(i);
# }

# Python:
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)
```

### Iterating Over Collections

```python
# List
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

# String
for char in "Python":
    print(char)

# Dictionary
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Iterate over keys
for key in person:
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### Range Function

```python
# range(stop)
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop)
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Reverse
for i in range(10, 0, -1):
    print(i)  # 10, 9, 8, ..., 1
```

### Enumerate Function

```python
# Get both index and value
fruits = ["apple", "banana", "orange"]

# Java equivalent:
# for (int i = 0; i < fruits.length; i++) {
#     System.out.println(i + ": " + fruits[i]);
# }

# Python:
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Start from different index
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")  # 1: apple, 2: banana, 3: orange
```

### Zip Function

```python
# Iterate over multiple lists simultaneously
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["NYC", "LA", "Chicago"]

for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old and lives in {city}")
```

## 3️⃣ While Loops

### Basic While Loop

```python
# Java:
# while (condition) {
#     // code
# }

# Python:
count = 0
while count < 5:
    print(count)
    count += 1  # Note: No count++ in Python!
```

### While with Else

```python
# Unique to Python: else clause executes when loop completes normally
count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("Loop completed normally")
```

### Infinite Loop with Break

```python
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input.lower() == 'quit':
        break
    print(f"You entered: {user_input}")
```

## 4️⃣ Loop Control Statements

### Break Statement

```python
# Exit loop immediately
for i in range(10):
    if i == 5:
        break  # Exit loop when i is 5
    print(i)  # Prints 0, 1, 2, 3, 4

# Search example
numbers = [1, 3, 5, 7, 9, 2, 4, 6]
target = 7

for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} not found")  # else executes if break not called
```

### Continue Statement

```python
# Skip current iteration
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)  # Prints 1, 3, 5, 7, 9

# Filter example
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for num in numbers:
    if num % 3 != 0:
        continue
    print(f"{num} is divisible by 3")
```

### Pass Statement

```python
# Placeholder - does nothing
for i in range(5):
    if i == 2:
        pass  # TODO: implement later
    else:
        print(i)

# Useful for empty functions/classes during development
def future_function():
    pass  # Will implement later

class FutureClass:
    pass  # Will implement later
```

## 5️⃣ List Comprehensions

### Basic List Comprehension

```python
# Java:
"""
List<Integer> squares = new ArrayList<>();
for (int i = 0; i < 10; i++) {
    squares.add(i * i);
}
"""

# Python - Traditional way:
squares = []
for i in range(10):
    squares.append(i * i)

# Python - List comprehension (Pythonic way):
squares = [i * i for i in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### List Comprehension with Condition

```python
# Get even numbers
evens = [i for i in range(20) if i % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Get squares of odd numbers
odd_squares = [i * i for i in range(10) if i % 2 != 0]
print(odd_squares)  # [1, 9, 25, 49, 81]

# Filter and transform
words = ["hello", "world", "python", "programming"]
long_words = [word.upper() for word in words if len(word) > 5]
print(long_words)  # ['PYTHON', 'PROGRAMMING']
```

### Nested List Comprehension

```python
# Create 2D matrix
matrix = [[i * j for j in range(3)] for i in range(3)]
print(matrix)  # [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# Flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Dictionary Comprehension

```python
# Create dictionary
squares_dict = {i: i * i for i in range(5)}
print(squares_dict)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Filter dictionary
prices = {"apple": 0.5, "banana": 0.3, "orange": 0.8, "grape": 1.2}
expensive = {k: v for k, v in prices.items() if v > 0.5}
print(expensive)  # {'orange': 0.8, 'grape': 1.2}
```

### Set Comprehension

```python
# Create set (unique values)
unique_squares = {i * i for i in range(-5, 6)}
print(unique_squares)  # {0, 1, 4, 9, 16, 25}
```

## 6️⃣ Match-Case (Python 3.10+)

### Basic Match Statement

```python
# Similar to Java's switch statement, but more powerful

def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:  # Default case (like 'default' in Java)
            return "Unknown Status"

print(http_status(200))  # OK
print(http_status(999))  # Unknown Status
```

### Pattern Matching with Multiple Values

```python
def describe_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (0, y):
            return f"On Y-axis at {y}"
        case (x, 0):
            return f"On X-axis at {x}"
        case (x, y):
            return f"Point at ({x}, {y})"

print(describe_point((0, 0)))    # Origin
print(describe_point((0, 5)))    # On Y-axis at 5
print(describe_point((3, 0)))    # On X-axis at 3
print(describe_point((3, 4)))    # Point at (3, 4)
```

### Pattern Matching with Guards

```python
def categorize_number(num):
    match num:
        case n if n < 0:
            return "Negative"
        case 0:
            return "Zero"
        case n if n > 0 and n < 10:
            return "Small positive"
        case n if n >= 10:
            return "Large positive"

print(categorize_number(-5))   # Negative
print(categorize_number(0))    # Zero
print(categorize_number(5))    # Small positive
print(categorize_number(15))   # Large positive
```

## 🎨 Control Flow Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    DECISION FLOW                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────┐                              │
│                    │  Start  │                              │
│                    └────┬────┘                              │
│                         │                                    │
│                    ┌────▼────┐                              │
│                    │Condition│                              │
│                    └─┬─────┬─┘                              │
│                      │     │                                 │
│                 True │     │ False                           │
│                      │     │                                 │
│                 ┌────▼─┐ ┌─▼────┐                          │
│                 │Action│ │Action│                          │
│                 │  A   │ │  B   │                          │
│                 └────┬─┘ └─┬────┘                          │
│                      │     │                                 │
│                      └──┬──┘                                 │
│                         │                                    │
│                    ┌────▼────┐                              │
│                    │   End   │                              │
│                    └─────────┘                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 💻 Complete Examples

See `control_flow_demo.py` for comprehensive demonstrations.

## 🏋️ Exercises

1. **Grade Calculator**: Calculate letter grade from numeric score
2. **FizzBuzz**: Classic programming challenge
3. **Prime Numbers**: Find all prime numbers up to N
4. **Pattern Printing**: Print various patterns using loops
5. **List Processing**: Use comprehensions for data transformation

See `exercises.py` and `solutions.py`.

## 🎯 Key Takeaways

1. **Indentation is crucial** - Defines code blocks
2. **No braces or semicolons** - Clean, readable syntax
3. **for-else and while-else** - Unique Python feature
4. **List comprehensions** - Concise and Pythonic
5. **enumerate() and zip()** - Powerful iteration tools
6. **match-case** - Modern pattern matching (3.10+)
7. **Ternary operator** - One-line conditionals

## 🔗 Next Module

[Module 04: Functions & Modules →](../04-functions-modules/)

## 📚 Additional Resources

- [Python Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
- [List Comprehensions](https://realpython.com/list-comprehension-python/)
- [Pattern Matching](https://peps.python.org/pep-0636/)