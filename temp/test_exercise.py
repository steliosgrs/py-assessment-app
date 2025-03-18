import pytest
import sys
import os
import inspect

# Add the directory containing the exercise code to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the student's function
from exercise import reverse_string


def test_reverse_empty_string():
    """Test that an empty string returns an empty string."""
    assert reverse_string("") == "", "Empty string should return empty string"


def test_reverse_single_character():
    """Test that a single character returns itself."""
    assert reverse_string("a") == "a", "Single character should return itself"
    assert reverse_string("X") == "X", "Single character should return itself"


def test_reverse_simple_word():
    """Test reversing a simple word."""
    assert reverse_string("hello") == "olleh", "Should reverse 'hello' to 'olleh'"
    assert reverse_string("Python") == "nohtyP", "Should reverse 'Python' to 'nohtyP'"


def test_reverse_with_spaces():
    """Test reversing a string with spaces."""
    assert (
        reverse_string("hello world") == "dlrow olleh"
    ), "Should handle spaces correctly"


def test_reverse_with_special_characters():
    """Test reversing a string with special characters."""
    assert (
        reverse_string("Hello, World!") == "!dlroW ,olleH"
    ), "Should handle special characters correctly"
    assert (
        reverse_string("12345!@#$%") == "%$#@!54321"
    ), "Should handle numbers and special characters correctly"


def test_reverse_palindrome():
    """Test reversing a palindrome."""
    assert (
        reverse_string("racecar") == "racecar"
    ), "Palindrome should remain unchanged when reversed"
    assert (
        reverse_string("madam") == "madam"
    ), "Palindrome should remain unchanged when reversed"


def test_implementation_approach():
    """Test that the implementation doesn't use built-in reversing functions."""
    # Get the source code of the student's function
    source = inspect.getsource(reverse_string)

    # Check for usage of built-in reversing methods
    disallowed = ["[::-1]", "reversed(", ".reverse()"]
    for method in disallowed:
        assert method not in source, f"Solution should not use {method}"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
