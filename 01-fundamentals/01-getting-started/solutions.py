"""
Solutions to Module 01 Exercises
"""

# Exercise 1: Personal Info
def display_info():
    """Display personal information in a formatted way"""
    name = "John Doe"
    age = 35
    profession = "Java Tech Lead"
    experience = 10
    
    print("=" * 50)
    print("PERSONAL INFORMATION")
    print("=" * 50)
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Profession: {profession}")
    print(f"Years of Experience: {experience}")
    print("=" * 50)
    
    # Alternative: Using dictionary
    info = {
        "Name": name,
        "Age": age,
        "Profession": profession,
        "Experience": f"{experience} years"
    }
    
    print("\nAlternative format:")
    for key, value in info.items():
        print(f"{key:20s}: {value}")


# Exercise 2: Simple Calculator
def calculator():
    """Simple calculator that adds two numbers"""
    print("Simple Calculator")
    print("-" * 30)
    
    # Method 1: Hardcoded values
    num1 = 10
    num2 = 20
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
    
    # Method 2: User input (commented out for automated testing)
    """
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = num1 + num2
        print(f"\nResult: {num1} + {num2} = {result}")
    except ValueError:
        print("Error: Please enter valid numbers!")
    """


# Exercise 3: Java to Python Conversion
def greeting():
    """
    Python version of the Java Greeting class
    
    Original Java code:
    public class Greeting {
        public static void main(String[] args) {
            String[] names = {"Alice", "Bob", "Charlie"};
            for (String name : names) {
                System.out.println("Hello, " + name + "!");
            }
        }
    }
    """
    names = ["Alice", "Bob", "Charlie"]
    
    # Method 1: Traditional loop
    print("Method 1: Traditional loop")
    for name in names:
        print(f"Hello, {name}!")
    
    # Method 2: List comprehension (more Pythonic)
    print("\nMethod 2: List comprehension")
    greetings = [f"Hello, {name}!" for name in names]
    for greeting in greetings:
        print(greeting)
    
    # Method 3: Using map and lambda
    print("\nMethod 3: Using map")
    greetings = list(map(lambda name: f"Hello, {name}!", names))
    print("\n".join(greetings))


# Bonus: Comparison of Java and Python patterns
def java_vs_python_examples():
    """Demonstrate common Java patterns in Python"""
    
    print("\n" + "=" * 60)
    print("JAVA VS PYTHON PATTERNS")
    print("=" * 60)
    
    # 1. Variable declaration
    print("\n1. Variable Declaration:")
    print("   Java:   String name = \"John\";")
    print("   Python: name = \"John\"")
    name = "John"
    print(f"   Result: {name}")
    
    # 2. Arrays/Lists
    print("\n2. Arrays/Lists:")
    print("   Java:   int[] numbers = {1, 2, 3, 4, 5};")
    print("   Python: numbers = [1, 2, 3, 4, 5]")
    numbers = [1, 2, 3, 4, 5]
    print(f"   Result: {numbers}")
    
    # 3. For loops
    print("\n3. For Loops:")
    print("   Java:   for (int i = 0; i < 5; i++) { ... }")
    print("   Python: for i in range(5): ...")
    print("   Output: ", end="")
    for i in range(5):
        print(i, end=" ")
    print()
    
    # 4. String concatenation
    print("\n4. String Concatenation:")
    print("   Java:   String msg = \"Hello \" + name + \"!\";")
    print("   Python: msg = f\"Hello {name}!\"")
    msg = f"Hello {name}!"
    print(f"   Result: {msg}")
    
    # 5. Null/None
    print("\n5. Null/None:")
    print("   Java:   String value = null;")
    print("   Python: value = None")
    value = None
    print(f"   Result: {value}")
    
    # 6. Boolean
    print("\n6. Boolean:")
    print("   Java:   boolean flag = true;")
    print("   Python: flag = True")
    flag = True
    print(f"   Result: {flag}")


def main():
    """Run all exercises"""
    print("EXERCISE SOLUTIONS\n")
    
    # Exercise 1
    print("\n" + "=" * 60)
    print("EXERCISE 1: Personal Info")
    print("=" * 60)
    display_info()
    
    # Exercise 2
    print("\n" + "=" * 60)
    print("EXERCISE 2: Simple Calculator")
    print("=" * 60)
    calculator()
    
    # Exercise 3
    print("\n" + "=" * 60)
    print("EXERCISE 3: Java to Python Conversion")
    print("=" * 60)
    greeting()
    
    # Bonus
    java_vs_python_examples()


if __name__ == "__main__":
    main()

# Made with Bob
