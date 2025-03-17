"""
Utility module for loading course content from local files.
This reduces database operations to stay within Firebase free tier limits.
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
COURSE_DIR = PROJECT_ROOT / "course"
MODULES_DIR = COURSE_DIR / "modules"
EXERCISES_DIR = COURSE_DIR / "exercises"


def get_all_modules() -> List[Dict[str, Any]]:
    """
    Get all available modules from the filesystem.

    Returns:
        List[Dict[str, Any]]: List of module metadata dictionaries
    """
    modules = []

    # Check if modules directory exists
    if not MODULES_DIR.exists():
        print(f"Warning: Modules directory not found at {MODULES_DIR}")
        return modules

    # Iterate through module directories
    for module_dir in sorted(MODULES_DIR.iterdir()):
        if not module_dir.is_dir():
            continue

        # Get module ID from directory name
        module_id = module_dir.name

        # Load metadata
        metadata_file = module_dir / "metadata.json"
        if not metadata_file.exists():
            print(f"Warning: Metadata file not found for module {module_id}")
            continue

        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            # Add module ID to metadata
            metadata["id"] = module_id

            # Add to modules list
            modules.append(metadata)
        except Exception as e:
            print(f"Error loading module {module_id}: {str(e)}")

    # Sort modules by order field
    modules.sort(key=lambda m: m.get("order", 999))

    return modules


def get_module_by_id(module_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific module's data by ID.

    Args:
        module_id (str): ID of the module to get

    Returns:
        Optional[Dict[str, Any]]: Module data if found, None otherwise
    """
    module_dir = MODULES_DIR / module_id

    # Check if module directory exists
    if not module_dir.exists() or not module_dir.is_dir():
        print(f"Module directory not found: {module_dir}")
        return None

    # Load metadata
    metadata_file = module_dir / "metadata.json"
    if not metadata_file.exists():
        print(f"Metadata file not found for module {module_id}")
        return None

    try:
        # Load metadata
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Add module ID
        metadata["id"] = module_id

        # Load content
        content_file = module_dir / "content.md"
        if content_file.exists():
            with open(content_file, "r", encoding="utf-8") as f:
                metadata["content"] = f.read()
        else:
            metadata["content"] = "Content not available."
            print(f"Content file not found for module {module_id}")

        return metadata
    except Exception as e:
        print(f"Error loading module {module_id}: {str(e)}")
        return None


def get_exercises_by_module(module_id: str) -> List[Dict[str, Any]]:
    """
    Get all exercises for a specific module.

    Args:
        module_id (str): Module ID

    Returns:
        List[Dict[str, Any]]: List of exercise metadata dictionaries
    """
    exercises = []

    # Check if exercises directory exists
    if not EXERCISES_DIR.exists():
        print(f"Warning: Exercises directory not found at {EXERCISES_DIR}")
        return exercises

    # Iterate through exercise directories
    for exercise_dir in sorted(EXERCISES_DIR.iterdir()):
        if not exercise_dir.is_dir():
            continue

        # Get exercise ID from directory name
        exercise_id = exercise_dir.name

        # Load metadata
        metadata_file = exercise_dir / "metadata.json"
        if not metadata_file.exists():
            print(f"Warning: Metadata file not found for exercise {exercise_id}")
            continue

        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            # Check if this exercise belongs to the requested module
            if metadata.get("moduleId") != module_id:
                continue

            # Add exercise ID to metadata
            metadata["id"] = exercise_id

            # Add to exercises list
            exercises.append(metadata)
        except Exception as e:
            print(f"Error loading exercise {exercise_id}: {str(e)}")

    # Sort exercises by order field
    exercises.sort(key=lambda e: e.get("order", 999))

    return exercises


def get_exercise_by_id(exercise_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific exercise's data by ID.

    Args:
        exercise_id (str): ID of the exercise to get

    Returns:
        Optional[Dict[str, Any]]: Exercise data if found, None otherwise
    """
    exercise_dir = EXERCISES_DIR / exercise_id

    # Check if exercise directory exists
    if not exercise_dir.exists() or not exercise_dir.is_dir():
        print(f"Exercise directory not found: {exercise_dir}")
        return None

    # Load metadata
    metadata_file = exercise_dir / "metadata.json"
    if not metadata_file.exists():
        print(f"Metadata file not found for exercise {exercise_id}")
        return None

    try:
        # Load metadata
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Add exercise ID
        metadata["id"] = exercise_id

        # Load description
        description_file = exercise_dir / "description.md"
        if description_file.exists():
            with open(description_file, "r", encoding="utf-8") as f:
                metadata["description"] = f.read()
        else:
            metadata["description"] = "Description not available."
            print(f"Description file not found for exercise {exercise_id}")

        # Load starter code
        starter_code_file = exercise_dir / "starter_code.py"
        if starter_code_file.exists():
            with open(starter_code_file, "r", encoding="utf-8") as f:
                metadata["starterCode"] = f.read()
        else:
            metadata["starterCode"] = "# Your code here"
            print(f"Starter code file not found for exercise {exercise_id}")

        return metadata
    except Exception as e:
        print(f"Error loading exercise {exercise_id}: {str(e)}")
        return None


def get_test_file_for_exercise(exercise_id: str) -> tuple:
    """
    Get the test file for a specific exercise.

    Args:
        exercise_id (str): Exercise ID

    Returns:
        tuple: (success, message, test_content)
    """
    exercise_dir = EXERCISES_DIR / exercise_id
    test_file = exercise_dir / "test.py"

    if not test_file.exists():
        return False, f"Test file not found for exercise {exercise_id}", None

    try:
        with open(test_file, "rb") as f:
            test_content = f.read()
        return True, "Test file loaded successfully", test_content
    except Exception as e:
        return False, f"Error loading test file: {str(e)}", None


def mark_module_completed(user_id: str, module_id: str) -> bool:
    """
    Mark a module as completed for a user in Firebase.
    This still uses Firebase to track user progress.

    Args:
        user_id (str): User ID
        module_id (str): Module ID

    Returns:
        bool: Success status
    """
    # Import Firebase functions here to avoid circular imports
    from shared.firebase import mark_module_completed as firebase_mark_module_completed

    return firebase_mark_module_completed(user_id, module_id)


def mark_exercise_completed(user_id: str, exercise_id: str) -> bool:
    """
    Mark an exercise as completed for a user in Firebase.
    This still uses Firebase to track user progress.

    Args:
        user_id (str): User ID
        exercise_id (str): Exercise ID

    Returns:
        bool: Success status
    """
    # Import Firebase functions here to avoid circular imports
    from shared.firebase import (
        mark_exercise_completed as firebase_mark_exercise_completed,
    )

    return firebase_mark_exercise_completed(user_id, exercise_id)


def ensure_course_directories():
    """
    Ensure that all necessary course directories exist.
    Create them if they don't.
    """
    # Create main directories
    COURSE_DIR.mkdir(exist_ok=True)
    MODULES_DIR.mkdir(exist_ok=True)
    EXERCISES_DIR.mkdir(exist_ok=True)

    print(f"Course directories created at {COURSE_DIR}")
