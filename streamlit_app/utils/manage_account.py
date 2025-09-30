import re

from pydantic import ValidationError

from models.forms import RegistrationForm
from utils.firebase import create_user

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def is_valid_email(email):
    """
    Validate email format.

    Args:
        email (str): Email to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return re.match(email_pattern, email) is not None


# TODO: to use
def is_valid_university_email(email: str, allowed_domains: list = None) -> bool:
    """
    Validate email format and ensure it's from allowed university domains

    Args:
        email (str): Email to validate
        allowed_domains (list): List of allowed domains (default: ['@ieee.org'])

    Returns:
        bool: True if valid, False otherwise
    """
    # Check domain
    if allowed_domains is None:
        allowed_domains = ["@ieee.org"]

    # Check username format
    username = email.split("@")[0]
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long")

    # Basic email format validation
    if not re.match(email_pattern, email):
        return False

    # Check if email ends with any of the allowed domains
    return any(email.endswith(domain) for domain in allowed_domains)


def register_user(display_name, email, password, confirm_password):
    """
    Register a new user with Firebase.

    Args:
        display_name (str): Display name for the user
        email (str): Email
        password (str): Password
        confirm_password (str): Password confirmation
    """
    try:
        form_data = RegistrationForm(
            display_name=display_name,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )
        return create_user(
            str(form_data.email), form_data.password, form_data.display_name
        )
    # except ValidationError as e:
    #     # Display validation errors
    #     st.error("Please correct the following errors:")
    #     for error in e.errors():
    #         field = error['loc'][0] if error['loc'] else 'form'
    #         message = error['msg']
    #         st.error(f"**{field.replace('_', ' ').title()}**: {message}")

    except ValidationError as e:
        return False, f"Validation error: {e.errors()[0]['msg']}", None
