"""
Exercise testing utilities for running pytest on submitted code.
"""

import os
import sys
import tempfile
import subprocess
import importlib.util
from typing import Tuple, List, Dict, Any, Optional


def save_code_to_temp_file(code: str, filename: str = "exercise.py") -> str:
    """
    Save code to a temporary file.

    Args:
        code (str): Python code to save
        filename (str): Name for the file

    Returns:
        str: Path to the temporary file
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, filename)

    # Write code to the file
    with open(file_path, "w") as f:
        f.write(code)

    return file_path


def save_test_to_temp_file(test_code: str, filename: str = "test_exercise.py") -> str:
    """
    Save test code to a temporary file.

    Args:
        test_code (str): Test code to save
        filename (str): Name for the test file

    Returns:
        str: Path to the temporary file
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, filename)

    # Write test code to the file
    with open(file_path, "w") as f:
        f.write(test_code)

    return file_path


def run_pytest(test_file: str) -> Tuple[bool, List[str]]:
    """
    Run pytest on a test file.

    Args:
        test_file (str): Path to the test file

    Returns:
        Tuple[bool, List[str]]:
            - Success status (bool)
            - List of test result messages
    """
    try:
        # Run pytest using subprocess
        result = subprocess.run(
            ["pytest", test_file, "-v"], capture_output=True, text=True, check=False
        )

        # Parse the output
        output_lines = result.stdout.split("\n")
        error_lines = result.stderr.split("\n")

        # Filter out empty lines and add error lines if any
        messages = [line for line in output_lines if line.strip()]
        if any(error_lines):
            messages.extend([f"ERROR: {line}" for line in error_lines if line.strip()])

        # Check if all tests passed
        success = result.returncode == 0

        return success, messages
    except Exception as e:
        return False, [f"Error running pytest: {str(e)}"]


def test_exercise(
    exercise_content: bytes, test_content: bytes
) -> Tuple[bool, List[str]]:
    """
    Test a submitted exercise against provided tests.

    Args:
        exercise_content (bytes): Submitted Python file content
        test_content (bytes): Test file content

    Returns:
        Tuple[bool, List[str]]:
            - Success status (bool)
            - List of test result messages
    """
    # Convert bytes to string
    exercise_code = exercise_content.decode("utf-8")
    test_code = test_content.decode("utf-8")

    # Save to temporary files
    exercise_file = save_code_to_temp_file(exercise_code)
    test_file = save_test_to_temp_file(test_code)

    # Make sure the test can import the exercise file
    exercise_dir = os.path.dirname(exercise_file)
    test_dir = os.path.dirname(test_file)

    # Add the exercise directory to Python path if they're different
    if exercise_dir != test_dir:
        sys.path.append(exercise_dir)

    # Run tests
    success, messages = run_pytest(test_file)

    # Remove temporary files and directories
    try:
        os.remove(exercise_file)
        os.remove(test_file)
        os.rmdir(os.path.dirname(exercise_file))
        if exercise_dir != test_dir:
            os.rmdir(test_dir)
    except:
        pass

    return success, messages


def validate_exercise_inline(
    exercise_code: str, test_code: str
) -> Tuple[bool, List[str]]:
    """
    Validate an exercise by running the test code in-process.

    This is an alternative to running pytest as a subprocess, which
    may be faster but less isolated.

    Args:
        exercise_code (str): Python code to test
        test_code (str): Test code

    Returns:
        Tuple[bool, List[str]]:
            - Success status (bool)
            - List of test messages
    """
    try:
        # Create a temporary module for the exercise
        temp_module_name = f"exercise_{hash(exercise_code) % 10000}"
        spec = importlib.util.spec_from_loader(temp_module_name, loader=None)
        temp_module = importlib.util.module_from_spec(spec)
        sys.modules[temp_module_name] = temp_module

        # Execute the exercise code in the temporary module
        exec(exercise_code, temp_module.__dict__)

        # Prepare the test environment
        test_globals = {"exercise": temp_module, "pytest": __import__("pytest")}

        # Execute the test code
        test_results = []
        test_success = True

        try:
            exec(test_code, test_globals)
            test_results.append("All tests passed!")
        except Exception as e:
            test_success = False
            test_results.append(f"Test failed: {str(e)}")

        # Clean up
        del sys.modules[temp_module_name]

        return test_success, test_results
    except Exception as e:
        return False, [f"Error running tests: {str(e)}"]
