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
    
    # Type checking
    print(f"\nType of name: {type(name)}")
    print(f"Type of experience: {type(experience)}")
    print(f"Type of is_learning_python: {type(is_learning_python)}")

# Python's way of defining entry point
if __name__ == "__main__":
    main()

# Made with Bob
