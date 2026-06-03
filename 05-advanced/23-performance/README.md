# Module 23: Performance Optimization

## 🎯 Key Topics
- Profiling and benchmarking
- Memory optimization
- Algorithm optimization
- Caching strategies
- Parallel processing

## Quick Reference

### 1. Profiling
```python
import cProfile
import time

def slow_function():
    time.sleep(1)
    return sum(range(1000000))

# Profile code
cProfile.run('slow_function()')

# Using timeit
import timeit
timeit.timeit('sum(range(100))', number=10000)
```

### 2. List Comprehensions (Faster)
```python
# Slow
result = []
for i in range(1000):
    result.append(i * 2)

# Fast
result = [i * 2 for i in range(1000)]
```

### 3. Generators (Memory Efficient)
```python
# Memory intensive
def get_numbers():
    return [i for i in range(1000000)]

# Memory efficient
def get_numbers():
    return (i for i in range(1000000))
```

### 4. Use Built-ins
```python
# Slow
result = []
for item in items:
    if condition(item):
        result.append(item)

# Fast
result = list(filter(condition, items))
```

### 5. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 6. Multiprocessing
```python
from multiprocessing import Pool

def process_item(item):
    return item * 2

with Pool(4) as p:
    results = p.map(process_item, range(1000))
```

## 🔗 Next: [Module 24: Design Patterns →](../24-design-patterns/)