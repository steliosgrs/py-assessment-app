# String Reversal Challenge

## Objective

Write a function that takes a string as input and returns the reverse of that string.

## Requirements

1. Create a function named `reverse_string` that accepts a single string parameter.
2. The function should return the string with its characters in reverse order.
3. Your solution should work for any valid string input, including empty strings.
4. Handle special characters and spaces correctly.

## Examples

```python
reverse_string("hello") # should return "olleh"
reverse_string("Python") # should return "nohtyP"
reverse_string("12345") # should return "54321"
reverse_string("") # should return ""
reverse_string("a") # should return "a"
reverse_string("Hello, World!") # should return "!dlroW ,olleH"
```

## Tips

- Remember that strings in Python are immutable, but you can create a new string with characters in the reverse order.
- Think about how you can access characters in a string from the end to the beginning.
- Consider the different approaches: using slicing, loops, or built-in functions.

## Constraints

- Do not use any built-in functions specifically designed for reversing (such as `reversed()` or string slicing with a negative step).
- Your solution should have a time complexity of O(n) where n is the length of the string.
