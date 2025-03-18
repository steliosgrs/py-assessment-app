"""
Script to set up initial course data in the local filesystem.
This creates sample modules and exercises.
"""

import os
import json
import shutil
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import course loader to get directory paths
from shared.course_loader import (
    COURSE_DIR,
    MODULES_DIR,
    EXERCISES_DIR,
    ensure_course_directories,
)

# Sample module data
SAMPLE_MODULES = [
    {
        "id": "module1",
        "title": "Introduction to Python",
        "description": "Learn the basics of Python programming language.",
        "order": 1,
        "content": """
# Introduction to Python

Python is a high-level, interpreted, and general-purpose programming language. It is designed with an emphasis on code readability and simplicity.

## Getting Started

Before you begin, make sure you have Python installed on your system. You can download it from [python.org](https://python.org).

## Hello World

Let's start with a simple "Hello, World!" program:

```python
print("Hello, World!")
```

This program outputs the text "Hello, World!" to the console.

## Variables

Variables in Python are dynamically typed, which means you don't need to declare the type of variable.

```python
# Integer variable
age = 25

# String variable
name = "John"

# Float variable
height = 5.9

# Boolean variable
is_student = True

# Print variables
print(name)
print(age)
print(height)
print(is_student)
```

## Basic Data Types

Python has the following basic data types:

- **Numbers**: Integers, floating-point numbers, and complex numbers
- **Strings**: Sequences of characters
- **Booleans**: True or False values
- **Lists**: Ordered sequences of items
- **Tuples**: Ordered immutable sequences
- **Sets**: Unordered collections of unique items
- **Dictionaries**: Key-value pairs

## Control Flow

Python uses indentation to define code blocks.

### If-Else Statement

```python
age = 18

if age < 18:
    print("You are a minor.")
elif age == 18:
    print("You just became an adult!")
else:
    print("You are an adult.")
```

### For Loop

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

### While Loop

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

## Functions

Functions in Python are defined using the `def` keyword.

```python
def greet(name):
    return f"Hello, {name}!"

# Call the function
message = greet("Alice")
print(message)
```

## Try It Yourself

Now that you've learned the basics, try to write a function that calculates the factorial of a number.

Head over to the exercises section to practice what you've learned!
""",
    },
    {
        "id": "module2",
        "title": "Data Structures in Python",
        "description": "Learn about lists, tuples, dictionaries, and sets in Python.",
        "order": 2,
        "content": """
# Data Structures in Python

Python has several built-in data structures that are powerful and flexible.

## Lists

Lists are ordered collections that can hold items of different types. They are mutable, meaning you can change their content.

```python
# Creating a list
fruits = ["apple", "banana", "cherry"]

# Accessing elements
print(fruits[0])  # Output: apple

# Modifying elements
fruits[1] = "blueberry"
print(fruits)  # Output: ["apple", "blueberry", "cherry"]

# Adding elements
fruits.append("orange")
print(fruits)  # Output: ["apple", "blueberry", "cherry", "orange"]

# List length
print(len(fruits))  # Output: 4

# Slicing
print(fruits[1:3])  # Output: ["blueberry", "cherry"]
```

## Tuples

Tuples are similar to lists but are immutable, meaning they cannot be changed after creation.

```python
# Creating a tuple
coordinates = (10, 20)

# Accessing elements
print(coordinates[0])  # Output: 10

# Trying to modify a tuple will raise an error
# coordinates[0] = 15  # This will raise TypeError
```

## Dictionaries

Dictionaries store key-value pairs and allow you to retrieve values by their keys.

```python
# Creating a dictionary
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])  # Output: John

# Modifying values
person["age"] = 31
print(person)  # Output: {'name': 'John', 'age': 31, 'city': 'New York'}

# Adding new key-value pairs
person["email"] = "john@example.com"

# Getting all keys
print(list(person.keys()))  # Output: ['name', 'age', 'city', 'email']

# Getting all values
print(list(person.values()))  # Output: ['John', 31, 'New York', 'john@example.com']
```

## Sets

Sets are unordered collections of unique elements.

```python
# Creating a set
fruits = {"apple", "banana", "cherry"}

# Adding elements
fruits.add("orange")
print(fruits)

# Duplicates are not allowed
fruits.add("apple")  # This won't add a duplicate
print(fruits)

# Set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# Union
print(set1 | set2)  # Output: {1, 2, 3, 4, 5}

# Intersection
print(set1 & set2)  # Output: {3}

# Difference
print(set1 - set2)  # Output: {1, 2}
```

## List Comprehensions

List comprehensions provide a concise way to create lists.

```python
# Create a list of squares
squares = [x**2 for x in range(10)]
print(squares)  # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# List comprehension with a condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # Output: [0, 4, 16, 36, 64]
```

## Practice

Try to use these data structures to solve different problems. Head to the exercises section to practice your skills!
""",
    },
]

# Sample exercise data
SAMPLE_EXERCISES = [
    {
        "id": "exercise1",
        "title": "Factorial Calculator",
        "description": """
# Factorial Calculator

Write a function named `factorial` that takes an integer `n` as input and returns the factorial of `n`.

The factorial of a number is the product of all positive integers less than or equal to the number. For example, the factorial of 5 (denoted as 5!) is calculated as:

5! = 5 × 4 × 3 × 2 × 1 = 120

## Requirements:

1. The function should be named `factorial`
2. It should take one parameter: `n` (an integer)
3. It should return the factorial of `n`
4. If `n` is 0, it should return 1 (as 0! = 1 by definition)
5. If `n` is negative, it should return None or raise an error

## Example:

```python
factorial(5)  # Should return 120
factorial(0)  # Should return 1
```
""",
        "moduleId": "module1",
        "difficulty": "Easy",
        "order": 1,
        "starterCode": """def factorial(n):
    # Your code here
    pass
""",
        "testCode": """
import pytest
from exercise import factorial

def test_factorial_zero():
    assert factorial(0) == 1, "Factorial of 0 should be 1"
    
def test_factorial_one():
    assert factorial(1) == 1, "Factorial of 1 should be 1"
    
def test_factorial_five():
    assert factorial(5) == 120, "Factorial of 5 should be 120"
    
def test_factorial_ten():
    assert factorial(10) == 3628800, "Factorial of 10 should be 3628800"
    
def test_factorial_negative():
    assert factorial(-1) is None, "Factorial of negative numbers should return None"
""",
    },
    {
        "id": "exercise2",
        "title": "List Operations",
        "description": """
# List Operations

Create a function called `process_list` that performs the following operations on a list:

1. Remove all duplicates from the list
2. Sort the list in ascending order
3. Return the sum of the first and last elements in the list

## Requirements:

1. The function should be named `process_list`
2. It should take one parameter: `numbers` (a list of integers)
3. It should return an integer (the sum of the first and last elements in the processed list)
4. If the list is empty, it should return 0
5. If the list has only one element after removing duplicates, that element should be considered both the first and last

## Example:

```python
process_list([3, 1, 4, 1, 5, 9, 2, 6, 5])  # Should return 1 + 9 = 10
process_list([5, 5, 5, 5])  # Should return 5 + 5 = 10 (after removing duplicates there's only one 5)
```
""",
        "moduleId": "module2",
        "difficulty": "Medium",
        "order": 1,
        "starterCode": """def process_list(numbers):
    # Your code here
    pass
""",
        "testCode": """
import pytest
from exercise import process_list

def test_process_list_normal():
    assert process_list([3, 1, 4, 1, 5, 9, 2, 6, 5]) == 10, "Should return 1 + 9 = 10"
    
def test_process_list_single_value():
    assert process_list([5, 5, 5, 5]) == 10, "Should return 5 + 5 = 10 (as there's only one 5 after removing duplicates)"
    
def test_process_list_empty():
    assert process_list([]) == 0, "Should return 0 for an empty list"
    
def test_process_list_negative():
    assert process_list([-3, -1, -4, -1, -5]) == -8, "Should return -5 + (-3) = -8"
    
def test_process_list_mixed():
    assert process_list([10, -5, 10, 15, 20, -5]) == 15, "Should return -5 + 20 = 15"
""",
    },
]


def setup_modules():
    """Set up sample modules in the filesystem"""
    print("Setting up modules...")

    for module in SAMPLE_MODULES:
        module_id = module["id"]
        module_dir = MODULES_DIR / module_id

        # Create module directory
        module_dir.mkdir(exist_ok=True)

        # Create metadata.json
        metadata = {
            "title": module["title"],
            "description": module["description"],
            "order": module["order"],
        }

        with open(module_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # Create content.md
        with open(module_dir / "content.md", "w", encoding="utf-8") as f:
            f.write(module["content"])

        print(f"Created module: {module['title']} in {module_dir}")


def setup_exercises():
    """Set up sample exercises in the filesystem"""
    print("Setting up exercises...")

    for exercise in SAMPLE_EXERCISES:
        exercise_id = exercise["id"]
        exercise_dir = EXERCISES_DIR / exercise_id

        # Create exercise directory
        exercise_dir.mkdir(exist_ok=True)

        # Create metadata.json
        metadata = {
            "title": exercise["title"],
            "moduleId": exercise["moduleId"],
            "difficulty": exercise["difficulty"],
            "order": exercise["order"],
        }

        with open(exercise_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # Create description.md
        with open(exercise_dir / "description.md", "w", encoding="utf-8") as f:
            f.write(exercise["description"])

        # Create starter_code.py
        with open(exercise_dir / "starter_code.py", "w", encoding="utf-8") as f:
            f.write(exercise["starterCode"])

        # Create test.py
        with open(exercise_dir / "test.py", "w", encoding="utf-8") as f:
            f.write(exercise["testCode"])

        print(f"Created exercise: {exercise['title']} in {exercise_dir}")


def main():
    # Ensure course directories exist
    ensure_course_directories()

    # Set up modules
    setup_modules()

    # Set up exercises
    setup_exercises()

    print("\nSetup completed successfully!")
    print(
        f"Created {len(SAMPLE_MODULES)} modules and {len(SAMPLE_EXERCISES)} exercises."
    )
    print("You can now run the Streamlit app and test with this sample data.")


if __name__ == "__main__":
    main()
