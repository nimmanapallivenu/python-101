"""
Comprehensive OOP Demonstration
Shows all OOP concepts with practical examples
"""

from abc import ABC, abstractmethod


# ============================================================================
# 1. BASIC CLASS AND OBJECTS
# ============================================================================

class Person:
    """Basic class demonstrating instance variables and methods"""
    
    # Class variable (shared by all instances)
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        """Constructor"""
        self.name = name  # Instance variable
        self.age = age
    
    def introduce(self):
        """Instance method"""
        return f"Hi, I'm {self.name}, {self.age} years old"
    
    def birthday(self):
        """Modify instance state"""
        self.age += 1
        return f"Happy birthday! Now {self.age} years old"


# ============================================================================
# 2. INHERITANCE
# ============================================================================

class Employee(Person):
    """Demonstrates single inheritance"""
    
    def __init__(self, name, age, employee_id, salary):
        super().__init__(name, age)  # Call parent constructor
        self.employee_id = employee_id
        self.salary = salary
    
    def introduce(self):
        """Method overriding"""
        return f"Hi, I'm {self.name}, Employee ID: {self.employee_id}"
    
    def get_annual_salary(self):
        """New method specific to Employee"""
        return self.salary * 12


class Manager(Employee):
    """Multi-level inheritance"""
    
    def __init__(self, name, age, employee_id, salary, team_size):
        super().__init__(name, age, employee_id, salary)
        self.team_size = team_size
    
    def introduce(self):
        return f"{super().introduce()}, managing {self.team_size} people"


# ============================================================================
# 3. MULTIPLE INHERITANCE
# ============================================================================

class Flyable:
    def fly(self):
        return f"{self.name} is flying!"

class Swimmable:
    def swim(self):
        return f"{self.name} is swimming!"

class Duck(Person, Flyable, Swimmable):
    """Multiple inheritance example"""
    
    def __init__(self, name):
        super().__init__(name, 0)  # Ducks don't have age in years
    
    def introduce(self):
        return f"Quack! I'm {self.name} the duck"


# ============================================================================
# 4. MAGIC METHODS
# ============================================================================

class BankAccount:
    """Demonstrates magic methods"""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def __str__(self):
        """String representation for users"""
        return f"{self.owner}'s account: ${self.balance:.2f}"
    
    def __repr__(self):
        """String representation for developers"""
        return f"BankAccount('{self.owner}', {self.balance})"
    
    def __len__(self):
        """Return balance as integer"""
        return int(self.balance)
    
    def __eq__(self, other):
        """Equality comparison"""
        return self.balance == other.balance
    
    def __lt__(self, other):
        """Less than comparison"""
        return self.balance < other.balance
    
    def __add__(self, other):
        """Addition operator"""
        if isinstance(other, (int, float)):
            return BankAccount(self.owner, self.balance + other)
        return BankAccount(self.owner, self.balance + other.balance)
    
    def __iadd__(self, amount):
        """In-place addition (+=)"""
        self.balance += amount
        return self
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance


# ============================================================================
# 5. ABSTRACT CLASSES
# ============================================================================

class Shape(ABC):
    """Abstract base class"""
    
    def __init__(self, color):
        self.color = color
    
    @abstractmethod
    def area(self):
        """Must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Must be implemented by subclasses"""
        pass
    
    def describe(self):
        """Concrete method"""
        return f"A {self.color} shape"


class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius


# ============================================================================
# 6. COMPOSITION
# ============================================================================

class Engine:
    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.running = False
    
    def start(self):
        self.running = True
        return "Engine started"
    
    def stop(self):
        self.running = False
        return "Engine stopped"


class Car:
    """Composition: Car HAS-A Engine"""
    
    def __init__(self, make, model, horsepower, fuel_type):
        self.make = make
        self.model = model
        self.engine = Engine(horsepower, fuel_type)  # Composition
        self.speed = 0
    
    def start(self):
        return f"{self.make} {self.model}: {self.engine.start()}"
    
    def accelerate(self, amount):
        if self.engine.running:
            self.speed += amount
            return f"Speed: {self.speed} mph"
        return "Start the engine first!"
    
    def info(self):
        return f"{self.make} {self.model} - {self.engine.horsepower}HP {self.engine.fuel_type}"


# ============================================================================
# 7. PROPERTY DECORATORS
# ============================================================================

class Temperature:
    """Demonstrates property decorators"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """Getter for celsius"""
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
        """Set celsius from fahrenheit"""
        self._celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self):
        """Another computed property"""
        return self._celsius + 273.15


# ============================================================================
# 8. CLASS AND STATIC METHODS
# ============================================================================

class Date:
    """Demonstrates class and static methods"""
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string):
        """Alternative constructor (factory method)"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @staticmethod
    def is_leap_year(year):
        """Utility function"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"


# ============================================================================
# 9. DESIGN PATTERNS
# ============================================================================

class Singleton:
    """Singleton pattern"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
        return cls._instance


class AnimalFactory:
    """Factory pattern"""
    
    @staticmethod
    def create_animal(animal_type, name):
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        else:
            raise ValueError(f"Unknown animal: {animal_type}")


class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demo_basic_oop():
    print("=" * 60)
    print("1. BASIC OOP")
    print("=" * 60)
    
    person = Person("Alice", 30)
    print(person.introduce())
    print(person.birthday())
    print(f"Species: {Person.species}")


def demo_inheritance():
    print("\n" + "=" * 60)
    print("2. INHERITANCE")
    print("=" * 60)
    
    emp = Employee("Bob", 35, "E001", 5000)
    print(emp.introduce())
    print(f"Annual salary: ${emp.get_annual_salary()}")
    
    mgr = Manager("Charlie", 40, "M001", 8000, 5)
    print(mgr.introduce())


def demo_multiple_inheritance():
    print("\n" + "=" * 60)
    print("3. MULTIPLE INHERITANCE")
    print("=" * 60)
    
    duck = Duck("Donald")
    print(duck.introduce())
    print(duck.fly())
    print(duck.swim())


def demo_magic_methods():
    print("\n" + "=" * 60)
    print("4. MAGIC METHODS")
    print("=" * 60)
    
    acc1 = BankAccount("Alice", 1000)
    acc2 = BankAccount("Bob", 1500)
    
    print(str(acc1))  # __str__
    print(repr(acc1))  # __repr__
    print(f"Balance as int: {len(acc1)}")  # __len__
    print(f"acc1 == acc2: {acc1 == acc2}")  # __eq__
    print(f"acc1 < acc2: {acc1 < acc2}")  # __lt__
    
    acc1 += 500  # __iadd__
    print(f"After deposit: {acc1}")


def demo_abstract_classes():
    print("\n" + "=" * 60)
    print("5. ABSTRACT CLASSES")
    print("=" * 60)
    
    shapes = [
        Rectangle("red", 5, 10),
        Circle("blue", 7)
    ]
    
    for shape in shapes:
        print(f"{shape.describe()}")
        print(f"  Area: {shape.area():.2f}")
        print(f"  Perimeter: {shape.perimeter():.2f}")


def demo_composition():
    print("\n" + "=" * 60)
    print("6. COMPOSITION")
    print("=" * 60)
    
    car = Car("Toyota", "Camry", 200, "Gasoline")
    print(car.info())
    print(car.start())
    print(car.accelerate(30))
    print(car.accelerate(20))


def demo_properties():
    print("\n" + "=" * 60)
    print("7. PROPERTY DECORATORS")
    print("=" * 60)
    
    temp = Temperature(25)
    print(f"Celsius: {temp.celsius}°C")
    print(f"Fahrenheit: {temp.fahrenheit}°F")
    print(f"Kelvin: {temp.kelvin}K")
    
    temp.fahrenheit = 100
    print(f"\nAfter setting to 100°F:")
    print(f"Celsius: {temp.celsius:.2f}°C")


def demo_class_static_methods():
    print("\n" + "=" * 60)
    print("8. CLASS AND STATIC METHODS")
    print("=" * 60)
    
    # Regular constructor
    date1 = Date(2024, 1, 15)
    print(f"Date 1: {date1}")
    
    # Class method (alternative constructor)
    date2 = Date.from_string("2024-12-25")
    print(f"Date 2: {date2}")
    
    # Static method
    print(f"Is 2024 a leap year? {Date.is_leap_year(2024)}")


def demo_design_patterns():
    print("\n" + "=" * 60)
    print("9. DESIGN PATTERNS")
    print("=" * 60)
    
    # Singleton
    s1 = Singleton()
    s2 = Singleton()
    print(f"Singleton: s1 is s2? {s1 is s2}")
    
    # Factory
    factory = AnimalFactory()
    dog = factory.create_animal("dog", "Buddy")
    cat = factory.create_animal("cat", "Whiskers")
    print(dog.speak())
    print(cat.speak())


def main():
    """Run all demonstrations"""
    print("\n" + "🐍" * 30)
    print("PYTHON OOP - COMPREHENSIVE DEMO")
    print("🐍" * 30)
    
    demo_basic_oop()
    demo_inheritance()
    demo_multiple_inheritance()
    demo_magic_methods()
    demo_abstract_classes()
    demo_composition()
    demo_properties()
    demo_class_static_methods()
    demo_design_patterns()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
