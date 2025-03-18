def reverse_string(input_string):
    """
    Reverses a given string.

    Args:
        input_string (str): The string to be reversed

    Returns:
        str: The reversed string
    """
    result = ""
    for char in input_string:
        result = char + result
    return result
