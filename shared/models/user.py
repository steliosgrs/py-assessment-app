from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    created_at: str
    hashed_password: str
    is_active: bool = True
    completed_modules: list[str] = []
    completed_exercises: list[str] = []

    @field_validator("email")
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v


class Exercise(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    module_id: str
    starter_code: str
    solution_code: str


# description " # List Operations Create a function called `process_list` that performs the following operations on a list: 1. Remove all duplicates from the list 2. Sort the list in ascending order 3. Return the sum of the first and last elements in the list ## Requirements: 1. The function should be named `process_list` 2. It should take one parameter: `numbers` (a list of integers) 3. It should return an integer (the sum of the first and last elements in the processed list) 4. If the list is empty, it should return 0 5. If the list has only one element after removing duplicates, that element should be considered both the first and last ## Example: ```python process_list([3, 1, 4, 1, 5, 9, 2, 6, 5]) # Should return 1 + 9 = 10 process_list([5, 5, 5, 5]) # Should return 5 + 5 = 10 (after removing duplicates there's only one 5) ``` ## Starter Code: ```python def process_list(numbers): # Your code here pass ``` Submit your solution and it will be automatically tested. "
# (string)
# difficulty "Medium"
# (string)
# moduleId "iywx5wDDnRGZYZbMCZQS"
# (string)
# order 1
# (number)
# starterCode "def process_list(numbers): # Your code here pass "
# (string)
# title "List Operations"
