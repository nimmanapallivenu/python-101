# Module 06: Advanced Object-Oriented Programming

## 🎯 Learning Objectives
- Master Python classes and objects
- Understand inheritance and polymorphism
- Learn about magic methods (dunder methods)
- Implement abstract classes and interfaces
- Use composition and aggregation
- Apply SOLID principles in Python

## 📖 OOP Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    OOP CONCEPTS IN PYTHON                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Class                              │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │         Attributes (Data)                      │  │  │
│  │  │  • Instance variables                          │  │  │
│  │  │  • Class variables                             │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │         Methods (Behavior)                     │  │  │
│  │  │  • Instance methods                            │  │  │
│  │  │  • Class methods                               │  │  │
│  │  │  • Static methods                              │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│                    ┌─────────┐                              │
│                    │ Objects │                              │
│                    │(Instances)                             │
│                    └─────────┘                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Classes and Objects

### Basic Class Definition

```python
# Java:
"""
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void introduce() {
        System.out.println("I'm " + name);
    }
}
"""

# Python:
class Person:
    """A class representing a person"""
    
    def __init__(self, name, age):
        """Constructor (initializer)"""
        self.name = name
        self.age = age
    
    def introduce(self):
        """Instance method"""
        print(f"I'm {self.name}, {self.age} years old")

# Create objects
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

person1.introduce()  # I'm Alice, 30 years old
person2.introduce()  # I'm Bob, 25 years old
```

### Instance vs Class Variables

```python
class Employee:
    # Class variable (shared by all instances)
    company = "TechCorp"
    employee_count = 0
    
    def __init__(self, name, salary):
        # Instance variables (unique to each instance)
        self.name = name
        self.salary = salary
        Employee.employee_count += 1
    
    def display_info(self):
        print(f"{self.name} works at {Employee.company}")

# Usage
emp1 = Employee("Alice", 75000)
emp2 = Employee("Bob", 80000)

print(f"Total employees: {Employee.employee_count}")  # 2
print(f"Company: {Employee.company}")  # TechCorp
```

### Instance, Class, and Static Methods

```python
class MathOperations:
    pi = 3.14159
    
    def __init__(self, value):
        self.value = value
    
    # Instance method (needs self)
    def square(self):
        """Operates on instance data"""
        return self.value ** 2
    
    # Class method (needs cls)
    @classmethod
    def circle_area(cls, radius):
        """Operates on class data"""
        return cls.pi * radius ** 2
    
    # Static method (needs neither)
    @staticmethod
    def add(a, b):
        """Utility function, doesn't need class or instance"""
        return a + b

# Usage
obj = MathOperations(5)
print(obj.square())  # 25 (instance method)
print(MathOperations.circle_area(10))  # 314.159 (class method)
print(MathOperations.add(3, 4))  # 7 (static method)
```

## 2️⃣ Inheritance

### Single Inheritance

```python
# Base class (Parent)
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass  # Abstract method
    
    def info(self):
        print(f"I am {self.name}")

# Derived class (Child)
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # Call parent constructor
        self.breed = breed
    
    def speak(self):
        return "Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Usage
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers")

print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
dog.info()  # I am Buddy
print(dog.fetch())  # Buddy is fetching!
```

### Multiple Inheritance

```python
class Flyable:
    def fly(self):
        return "Flying high!"

class Swimmable:
    def swim(self):
        return "Swimming fast!"

class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return "Quack!"

# Usage
duck = Duck("Donald")
print(duck.speak())  # Quack!
print(duck.fly())    # Flying high!
print(duck.swim())   # Swimming fast!
```

### Method Resolution Order (MRO)

```python
class A:
    def method(self):
        print("A method")

class B(A):
    def method(self):
        print("B method")

class C(A):
    def method(self):
        print("C method")

class D(B, C):
    pass

# Check MRO
print(D.mro())
# [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]

d = D()
d.method()  # B method (follows MRO)
```

## 3️⃣ Polymorphism

### Method Overriding

```python
class Shape:
    def area(self):
        pass
    
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Polymorphism in action
shapes = [
    Rectangle(5, 10),
    Circle(7),
    Rectangle(3, 4)
]

for shape in shapes:
    print(f"Area: {shape.area():.2f}")
```

### Duck Typing

```python
# "If it walks like a duck and quacks like a duck, it's a duck"

class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Car:
    def honk(self):
        return "Beep!"

def make_sound(animal):
    """Works with any object that has a speak() method"""
    return animal.speak()

# Works!
print(make_sound(Dog()))  # Woof!
print(make_sound(Cat()))  # Meow!

# Fails - Car doesn't have speak()
# print(make_sound(Car()))  # AttributeError
```

## 4️⃣ Magic Methods (Dunder Methods)

### Common Magic Methods

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        """String representation for users"""
        return f"{self.title} by {self.author}"
    
    def __repr__(self):
        """String representation for developers"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def __len__(self):
        """Length of the book"""
        return self.pages
    
    def __eq__(self, other):
        """Equality comparison"""
        return self.title == other.title and self.author == other.author
    
    def __lt__(self, other):
        """Less than comparison"""
        return self.pages < other.pages
    
    def __add__(self, other):
        """Addition operator"""
        return self.pages + other.pages

# Usage
book1 = Book("Python Basics", "John Doe", 300)
book2 = Book("Advanced Python", "Jane Smith", 450)

print(str(book1))  # Python Basics by John Doe
print(repr(book1))  # Book('Python Basics', 'John Doe', 300)
print(len(book1))  # 300
print(book1 == book2)  # False
print(book1 < book2)  # True (300 < 450)
print(book1 + book2)  # 750
```

### Container Magic Methods

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def __len__(self):
        """Number of items"""
        return len(self.items)
    
    def __getitem__(self, index):
        """Get item by index"""
        return self.items[index]
    
    def __setitem__(self, index, value):
        """Set item by index"""
        self.items[index] = value
    
    def __delitem__(self, index):
        """Delete item by index"""
        del self.items[index]
    
    def __contains__(self, item):
        """Check if item exists"""
        return item in self.items
    
    def __iter__(self):
        """Make iterable"""
        return iter(self.items)
    
    def add(self, item):
        self.items.append(item)

# Usage
cart = ShoppingCart()
cart.add("Apple")
cart.add("Banana")
cart.add("Orange")

print(len(cart))  # 3
print(cart[0])  # Apple
print("Banana" in cart)  # True

for item in cart:
    print(item)
```

## 5️⃣ Abstract Classes and Interfaces

### Using ABC (Abstract Base Class)

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract base class for payment processors"""
    
    @abstractmethod
    def process_payment(self, amount):
        """Must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id):
        """Must be implemented by subclasses"""
        pass
    
    def log_transaction(self, message):
        """Concrete method (optional to override)"""
        print(f"LOG: {message}")

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        self.log_transaction(f"Processing ${amount} via Credit Card")
        return f"Charged ${amount} to credit card"
    
    def refund(self, transaction_id):
        self.log_transaction(f"Refunding transaction {transaction_id}")
        return f"Refunded transaction {transaction_id}"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        self.log_transaction(f"Processing ${amount} via PayPal")
        return f"Charged ${amount} via PayPal"
    
    def refund(self, transaction_id):
        return f"PayPal refund for {transaction_id}"

# Usage
# payment = PaymentProcessor()  # Error: Can't instantiate abstract class

cc_processor = CreditCardProcessor()
print(cc_processor.process_payment(100))

paypal_processor = PayPalProcessor()
print(paypal_processor.process_payment(50))
```

## 6️⃣ Composition vs Inheritance

### Composition (Has-A Relationship)

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        return "Engine started"
    
    def stop(self):
        return "Engine stopped"

class Wheel:
    def __init__(self, size):
        self.size = size

class Car:
    """Car HAS-A Engine and HAS-A Wheels"""
    def __init__(self, make, model, horsepower):
        self.make = make
        self.model = model
        self.engine = Engine(horsepower)  # Composition
        self.wheels = [Wheel(17) for _ in range(4)]
    
    def start(self):
        return f"{self.make} {self.model}: {self.engine.start()}"
    
    def info(self):
        return f"{self.make} {self.model} with {self.engine.horsepower}HP"

# Usage
car = Car("Toyota", "Camry", 200)
print(car.start())  # Toyota Camry: Engine started
print(car.info())  # Toyota Camry with 200HP
```

## 7️⃣ Property Decorators

### Getters and Setters

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """Getter"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Setter with validation"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Computed property"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9

# Usage
temp = Temperature(25)
print(temp.celsius)  # 25
print(temp.fahrenheit)  # 77.0

temp.celsius = 30
print(temp.fahrenheit)  # 86.0

temp.fahrenheit = 100
print(temp.celsius)  # 37.77...

# temp.celsius = -300  # ValueError!
```

## 8️⃣ Design Patterns

### Singleton Pattern

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected to DB"
        return cls._instance

# Usage
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  # True (same instance)
```

### Factory Pattern

```python
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# Usage
factory = AnimalFactory()
dog = factory.create_animal("dog")
cat = factory.create_animal("cat")

print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
```

## 💻 Complete Example

See `oop_demo.py` for comprehensive demonstrations.

## 🎯 Key Takeaways

1. **Classes define blueprints** - Objects are instances
2. **self is explicit** - Unlike Java's implicit this
3. **No access modifiers** - Use _ for "private" by convention
4. **Multiple inheritance** - Supported with MRO
5. **Duck typing** - Focus on behavior, not type
6. **Magic methods** - Customize object behavior
7. **ABC for interfaces** - Use abstract base classes
8. **Composition over inheritance** - Prefer has-a over is-a

## 🔗 Next Module

[Module 07: File Handling & I/O →](../07-file-handling/)

## 📚 Additional Resources

- [Python OOP Tutorial](https://realpython.com/python3-object-oriented-programming/)
- [Magic Methods Guide](https://rszalski.github.io/magicmethods/)
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)