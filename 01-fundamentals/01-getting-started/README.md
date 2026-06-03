# Module 01: Getting Started with Python

## 🎯 Learning Objectives
- Understand Python's philosophy and advantages
- Set up Python development environment
- Write your first Python program
- Understand Python's execution model
- Learn basic syntax and indentation rules

## 📖 Theory

### Why Python?

```
┌─────────────────────────────────────────────────────────────┐
│                    PYTHON ADVANTAGES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ Simple & Readable Syntax                                 │
│  ✓ Extensive Standard Library                               │
│  ✓ Cross-platform Compatibility                             │
│  ✓ Large Community & Ecosystem                              │
│  ✓ Versatile (Web, Data Science, AI, Automation)           │
│  ✓ Rapid Development                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Python vs Java: Key Differences

| Feature | Java | Python |
|---------|------|--------|
| **Typing** | Static, Strong | Dynamic, Strong |
| **Compilation** | Compiled to bytecode | Interpreted (with bytecode) |
| **Syntax** | Verbose, explicit | Concise, implicit |
| **Memory Management** | Automatic (GC) | Automatic (GC + Reference Counting) |
| **Indentation** | Optional (uses braces) | Mandatory (defines blocks) |
| **Performance** | Generally faster | Slower, but sufficient for most cases |
| **Use Cases** | Enterprise, Android, Large systems | Web, Data Science, Scripting, AI |

### Python Execution Flow

```
┌──────────────┐
│ Source Code  │
│  (.py file)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Python     │
│  Compiler    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Bytecode   │
│ (.pyc file)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Python     │
│   Virtual    │
│   Machine    │
│    (PVM)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Output     │
└──────────────┘
```

## 🛠️ Setup Instructions

### 1. Install Python

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3 --version
```

**Windows:**
```bash
# Download from python.org or use winget
winget install Python.Python.3.11

# Verify installation
python --version
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip

# Verify installation
python3 --version
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install --upgrade pip
```

### 3. IDE Setup

**VS Code Extensions:**
- Python (Microsoft)
- Pylance
- Python Indent
- autoDocstring

## 💻 Your First Python Program

### hello_world.py

```python
"""
My First Python Program
This is a docstring - used for documentation
"""

# This is a single-line comment

def main():
    """Main function - entry point of the program"""
    print("Hello, World!")
    print("Welcome to Python Programming!")
    
    # Variables (no type declaration needed!)
    name = "Java Developer"
    experience = 5
    is_learning_python = True
    
    # String formatting (f-strings - Python 3.6+)
    message = f"Hello {name}! You have {experience} years of experience."
    print(message)
    
    # Multiple ways to print
    print("Method 1:", name)
    print(f"Method 2: {name}")
    print("Method 3: " + name)

# Python's way of defining entry point
if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python hello_world.py
```

**Output:**
```
Hello, World!
Welcome to Python Programming!
Hello Java Developer! You have 5 years of experience.
Method 1: Java Developer
Method 2: Java Developer
Method 3: Java Developer
```

## 🔍 Understanding Python Syntax

### 1. Indentation (Critical!)

```python
# ✅ CORRECT - Consistent indentation
def greet(name):
    if name:
        print(f"Hello, {name}!")
        print("Welcome!")
    else:
        print("Hello, Guest!")

# ❌ WRONG - Inconsistent indentation
def greet_wrong(name):
    if name:
        print(f"Hello, {name}!")
      print("Welcome!")  # IndentationError!
```

### 2. No Semicolons or Braces

```python
# Java style
"""
public void processData() {
    int x = 10;
    if (x > 5) {
        System.out.println("Greater");
    }
}
"""

# Python style
def process_data():
    x = 10
    if x > 5:
        print("Greater")
```

### 3. Dynamic Typing

```python
# Variable can change type
x = 10          # int
print(type(x))  # <class 'int'>

x = "Hello"     # now it's a string
print(type(x))  # <class 'str'>

x = [1, 2, 3]   # now it's a list
print(type(x))  # <class 'list'>
```

## 🎓 Java to Python Translation

### Example 1: Simple Class

**Java:**
```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void introduce() {
        System.out.println("I'm " + name + ", " + age + " years old");
    }
}
```

**Python:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        print(f"I'm {self.name}, {self.age} years old")
```

### Example 2: List Operations

**Java:**
```java
List<String> fruits = new ArrayList<>();
fruits.add("apple");
fruits.add("banana");
fruits.add("orange");

for (String fruit : fruits) {
    System.out.println(fruit);
}
```

**Python:**
```python
fruits = []  # or fruits = list()
fruits.append("apple")
fruits.append("banana")
fruits.append("orange")

for fruit in fruits:
    print(fruit)

# Or even simpler
fruits = ["apple", "banana", "orange"]
```

## 🏋️ Exercises

### Exercise 1: Personal Info
Create a program that stores and displays your information.

```python
# TODO: Complete this
def display_info():
    # Store your name, age, profession, and years of experience
    # Print them in a formatted way
    pass

if __name__ == "__main__":
    display_info()
```

### Exercise 2: Simple Calculator
Create a basic calculator that adds two numbers.

```python
# TODO: Complete this
def calculator():
    # Get two numbers from user
    # Add them and display result
    pass

if __name__ == "__main__":
    calculator()
```

### Exercise 3: Java to Python Conversion
Convert this Java code to Python:

```java
public class Greeting {
    public static void main(String[] args) {
        String[] names = {"Alice", "Bob", "Charlie"};
        for (String name : names) {
            System.out.println("Hello, " + name + "!");
        }
    }
}
```

## 📝 Solutions

See `solutions.py` for complete solutions.

## 🎯 Key Takeaways

1. **Python is dynamically typed** - No need to declare variable types
2. **Indentation matters** - It defines code blocks (like braces in Java)
3. **No semicolons needed** - Line breaks define statement ends
4. **Everything is an object** - Even primitive types
5. **`if __name__ == "__main__"`** - Python's entry point pattern
6. **f-strings** - Modern way to format strings (Python 3.6+)

## 🔗 Next Module

[Module 02: Data Types & Variables →](../02-data-types/)

## 📚 Additional Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [PEP 8 - Style Guide](https://pep8.org/)
- [Python for Java Developers](https://realpython.com/python-vs-java/)