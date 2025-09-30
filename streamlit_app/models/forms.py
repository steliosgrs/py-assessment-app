from pydantic import BaseModel, EmailStr, field_validator


class RegistrationForm(BaseModel):
    """Pydantic model for registration form validation"""

    display_name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Display name must be at least 3 characters long")
        if len(v) > 20:
            raise ValueError("Display name must be less than 20 characters")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: EmailStr) -> EmailStr:
        email_str = str(v).lower()
        if not email_str.endswith("@ieee.org"):
            raise ValueError(
                "Only @ieee.org email addresses are allowed for registration"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 6 characters long")
        if len(v) > 32:
            raise ValueError("Password must be less than 32 characters")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_password_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v
