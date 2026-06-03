"""
Comprehensive Control Flow Demonstration
Includes if-elif-else, loops, comprehensions, and pattern matching
"""


def if_statements_demo():
    """Demonstrate if-elif-else statements"""
    print("=" * 60)
    print("IF-ELIF-ELSE DEMONSTRATION")
    print("=" * 60)
    
    # Basic if
    print("\n1. BASIC IF STATEMENT")
    print("-" * 40)
    age = 18
    if age >= 18:
        print(f"Age {age}: You are an adult")
    
    # If-else
    print("\n2. IF-ELSE STATEMENT")
    print("-" * 40)
    temperature = 25
    if temperature > 30:
        print(f"Temperature {temperature}°C: It's hot!")
    else:
        print(f"Temperature {temperature}°C: It's comfortable")
    
    # If-elif-else
    print("\n3. IF-ELIF-ELSE STATEMENT")
    print("-" * 40)
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
    print(f"Score {score}: Grade {grade}")
    
    # Nested if
    print("\n4. NESTED IF STATEMENTS")
    print("-" * 40)
    age = 25
    has_license = True
    
    if age >= 18:
        if has_license:
            print("✓ You can drive")
        else:
            print("✗ You need a license")
    else:
        print("✗ You're too young to drive")
    
    # Ternary operator
    print("\n5. TERNARY OPERATOR")
    print("-" * 40)
    age = 20
    status = "Adult" if age >= 18 else "Minor"
    print(f"Age {age}: {status}")
    
    # Multiple conditions
    print("\n6. MULTIPLE CONDITIONS")
    print("-" * 40)
    username = "admin"
    password = "secret123"
    
    if username == "admin" and password == "secret123":
        print("✓ Login successful")
    else:
        print("✗ Invalid credentials")


def for_loops_demo():
    """Demonstrate for loops"""
    print("\n" + "=" * 60)
    print("FOR LOOPS DEMONSTRATION")
    print("=" * 60)
    
    # Basic for loop with range
    print("\n1. BASIC FOR LOOP")
    print("-" * 40)
    print("Numbers 0-4:")
    for i in range(5):
        print(i, end=" ")
    print()
    
    # Range with start and stop
    print("\n2. RANGE WITH START AND STOP")
    print("-" * 40)
    print("Numbers 2-6:")
    for i in range(2, 7):
        print(i, end=" ")
    print()
    
    # Range with step
    print("\n3. RANGE WITH STEP")
    print("-" * 40)
    print("Even numbers 0-10:")
    for i in range(0, 11, 2):
        print(i, end=" ")
    print()
    
    # Reverse range
    print("\n4. REVERSE RANGE")
    print("-" * 40)
    print("Countdown from 5:")
    for i in range(5, 0, -1):
        print(i, end=" ")
    print()
    
    # Iterate over list
    print("\n5. ITERATE OVER LIST")
    print("-" * 40)
    fruits = ["apple", "banana", "orange", "grape"]
    for fruit in fruits:
        print(f"  • {fruit}")
    
    # Enumerate
    print("\n6. ENUMERATE (INDEX + VALUE)")
    print("-" * 40)
    for index, fruit in enumerate(fruits, start=1):
        print(f"  {index}. {fruit}")
    
    # Zip multiple lists
    print("\n7. ZIP MULTIPLE LISTS")
    print("-" * 40)
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    cities = ["NYC", "LA", "Chicago"]
    
    for name, age, city in zip(names, ages, cities):
        print(f"  {name}, {age} years old, lives in {city}")
    
    # Dictionary iteration
    print("\n8. DICTIONARY ITERATION")
    print("-" * 40)
    person = {"name": "Alice", "age": 30, "city": "NYC"}
    
    print("Keys:")
    for key in person:
        print(f"  {key}")
    
    print("\nValues:")
    for value in person.values():
        print(f"  {value}")
    
    print("\nKey-Value pairs:")
    for key, value in person.items():
        print(f"  {key}: {value}")


def while_loops_demo():
    """Demonstrate while loops"""
    print("\n" + "=" * 60)
    print("WHILE LOOPS DEMONSTRATION")
    print("=" * 60)
    
    # Basic while loop
    print("\n1. BASIC WHILE LOOP")
    print("-" * 40)
    count = 0
    while count < 5:
        print(f"Count: {count}")
        count += 1
    
    # While with else
    print("\n2. WHILE WITH ELSE")
    print("-" * 40)
    count = 0
    while count < 3:
        print(f"Iteration {count}")
        count += 1
    else:
        print("Loop completed normally")
    
    # Countdown
    print("\n3. COUNTDOWN")
    print("-" * 40)
    countdown = 5
    while countdown > 0:
        print(f"{countdown}...", end=" ")
        countdown -= 1
    print("Blast off! 🚀")


def loop_control_demo():
    """Demonstrate break, continue, pass"""
    print("\n" + "=" * 60)
    print("LOOP CONTROL DEMONSTRATION")
    print("=" * 60)
    
    # Break
    print("\n1. BREAK STATEMENT")
    print("-" * 40)
    print("Find first number divisible by 7:")
    for i in range(1, 20):
        if i % 7 == 0:
            print(f"Found: {i}")
            break
    
    # Continue
    print("\n2. CONTINUE STATEMENT")
    print("-" * 40)
    print("Print odd numbers only:")
    for i in range(10):
        if i % 2 == 0:
            continue
        print(i, end=" ")
    print()
    
    # Pass
    print("\n3. PASS STATEMENT")
    print("-" * 40)
    print("Processing numbers (skip 5):")
    for i in range(8):
        if i == 5:
            pass  # Placeholder - do nothing
        else:
            print(i, end=" ")
    print()
    
    # For-else with break
    print("\n4. FOR-ELSE WITH BREAK")
    print("-" * 40)
    numbers = [1, 3, 5, 7, 9]
    target = 7
    
    for num in numbers:
        if num == target:
            print(f"✓ Found {target}!")
            break
    else:
        print(f"✗ {target} not found")


def list_comprehensions_demo():
    """Demonstrate list comprehensions"""
    print("\n" + "=" * 60)
    print("LIST COMPREHENSIONS DEMONSTRATION")
    print("=" * 60)
    
    # Basic list comprehension
    print("\n1. BASIC LIST COMPREHENSION")
    print("-" * 40)
    squares = [i * i for i in range(10)]
    print(f"Squares: {squares}")
    
    # With condition
    print("\n2. WITH CONDITION")
    print("-" * 40)
    evens = [i for i in range(20) if i % 2 == 0]
    print(f"Even numbers: {evens}")
    
    # Transform and filter
    print("\n3. TRANSFORM AND FILTER")
    print("-" * 40)
    words = ["hello", "world", "python", "programming"]
    long_words = [word.upper() for word in words if len(word) > 5]
    print(f"Long words (uppercase): {long_words}")
    
    # Nested comprehension
    print("\n4. NESTED COMPREHENSION")
    print("-" * 40)
    matrix = [[i * j for j in range(3)] for i in range(3)]
    print("Multiplication table (3x3):")
    for row in matrix:
        print(f"  {row}")
    
    # Flatten 2D list
    print("\n5. FLATTEN 2D LIST")
    print("-" * 40)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [num for row in matrix for num in row]
    print(f"Original: {matrix}")
    print(f"Flattened: {flat}")
    
    # Dictionary comprehension
    print("\n6. DICTIONARY COMPREHENSION")
    print("-" * 40)
    squares_dict = {i: i * i for i in range(6)}
    print(f"Squares dict: {squares_dict}")
    
    # Set comprehension
    print("\n7. SET COMPREHENSION")
    print("-" * 40)
    unique_squares = {i * i for i in range(-5, 6)}
    print(f"Unique squares: {unique_squares}")


def pattern_matching_demo():
    """Demonstrate match-case (Python 3.10+)"""
    print("\n" + "=" * 60)
    print("PATTERN MATCHING DEMONSTRATION (Python 3.10+)")
    print("=" * 60)
    
    def http_status(status):
        match status:
            case 200:
                return "OK"
            case 404:
                return "Not Found"
            case 500:
                return "Internal Server Error"
            case _:
                return "Unknown Status"
    
    print("\n1. BASIC MATCH-CASE")
    print("-" * 40)
    statuses = [200, 404, 500, 999]
    for status in statuses:
        print(f"Status {status}: {http_status(status)}")
    
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
    
    print("\n2. PATTERN MATCHING WITH TUPLES")
    print("-" * 40)
    points = [(0, 0), (0, 5), (3, 0), (3, 4)]
    for point in points:
        print(f"{point}: {describe_point(point)}")


def fizzbuzz():
    """Classic FizzBuzz challenge"""
    print("\n" + "=" * 60)
    print("FIZZBUZZ CHALLENGE")
    print("=" * 60)
    print("\nRules:")
    print("  • Divisible by 3: Fizz")
    print("  • Divisible by 5: Buzz")
    print("  • Divisible by both: FizzBuzz")
    print("  • Otherwise: the number")
    print("\nOutput:")
    print("-" * 40)
    
    for i in range(1, 31):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz", end=" ")
        elif i % 3 == 0:
            print("Fizz", end=" ")
        elif i % 5 == 0:
            print("Buzz", end=" ")
        else:
            print(i, end=" ")
        
        if i % 10 == 0:  # New line every 10 numbers
            print()
    print()
    
    # Pythonic version using list comprehension
    print("\nPythonic version (list comprehension):")
    print("-" * 40)
    result = [
        "FizzBuzz" if i % 15 == 0 else
        "Fizz" if i % 3 == 0 else
        "Buzz" if i % 5 == 0 else
        str(i)
        for i in range(1, 31)
    ]
    print(" ".join(result[:10]))
    print(" ".join(result[10:20]))
    print(" ".join(result[20:30]))


def practical_examples():
    """Practical real-world examples"""
    print("\n" + "=" * 60)
    print("PRACTICAL EXAMPLES")
    print("=" * 60)
    
    # Example 1: Grade calculator
    print("\n1. GRADE CALCULATOR")
    print("-" * 40)
    scores = [95, 87, 76, 64, 52]
    
    for score in scores:
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
        print(f"Score {score:3d} → Grade {grade}")
    
    # Example 2: Find prime numbers
    print("\n2. PRIME NUMBERS (1-50)")
    print("-" * 40)
    primes = []
    for num in range(2, 51):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    print(f"Primes: {primes}")
    
    # Example 3: Data filtering
    print("\n3. DATA FILTERING")
    print("-" * 40)
    employees = [
        {"name": "Alice", "age": 30, "salary": 75000},
        {"name": "Bob", "age": 25, "salary": 60000},
        {"name": "Charlie", "age": 35, "salary": 90000},
        {"name": "Diana", "age": 28, "salary": 70000},
    ]
    
    # Filter high earners
    high_earners = [emp for emp in employees if emp["salary"] > 70000]
    print("High earners (>$70k):")
    for emp in high_earners:
        print(f"  {emp['name']}: ${emp['salary']:,}")
    
    # Example 4: Pattern printing
    print("\n4. PATTERN PRINTING")
    print("-" * 40)
    print("Triangle pattern:")
    for i in range(1, 6):
        print("* " * i)
    
    print("\nPyramid pattern:")
    for i in range(1, 6):
        print(" " * (5 - i) + "* " * i)


def main():
    """Run all demonstrations"""
    print("\n" + "🐍" * 30)
    print("PYTHON CONTROL FLOW - COMPREHENSIVE DEMO")
    print("🐍" * 30)
    
    if_statements_demo()
    for_loops_demo()
    while_loops_demo()
    loop_control_demo()
    list_comprehensions_demo()
    
    # Pattern matching requires Python 3.10+
    import sys
    if sys.version_info >= (3, 10):
        pattern_matching_demo()
    else:
        print("\n⚠️  Pattern matching requires Python 3.10+")
    
    fizzbuzz()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
