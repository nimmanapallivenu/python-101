# Module 24: Design Patterns in Python

## 🎯 Common Design Patterns

### 1. Singleton
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. Factory
```python
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
```

### 3. Observer
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, data):
        for observer in self._observers:
            observer.update(data)
```

### 4. Strategy
```python
class PaymentStrategy:
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ${amount} with credit card")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ${amount} with PayPal")
```

### 5. Decorator Pattern
```python
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time: {end - start}s")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
```

### 6. Builder
```python
class UserBuilder:
    def __init__(self):
        self.user = User()
    
    def set_name(self, name):
        self.user.name = name
        return self
    
    def set_email(self, email):
        self.user.email = email
        return self
    
    def build(self):
        return self.user

# Usage
user = UserBuilder().set_name("John").set_email("john@example.com").build()
```

## 🔗 Next: [Module 25: Best Practices →](../25-best-practices/)