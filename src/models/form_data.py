"""Form data model for registration."""

import re
from email_validator import validate_email as validate_email_dns, EmailNotValidError
from pydantic import BaseModel, field_validator


class FormData(BaseModel):
    """Registration form data with validation."""

    full_name: str
    phone: str
    email: str | None = None
    business_type: str

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate full name - must be at least 2 characters."""
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number - must have at least 8 digits."""
        # Remove common formatting characters for digit count check
        digits_only = re.sub(r"[^\d]", "", v)
        if len(digits_only) < 8:
            raise ValueError("Phone must have at least 8 digits")

        # Validate phone pattern (digits, spaces, dashes, plus sign, at least 8 digits)
        phone_pattern = re.compile(r"^[\d\s\-\+\(\)]{8,}$")
        if not phone_pattern.match(v):
            raise ValueError("Invalid phone number format")

        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        """Validate email with DNS verification."""
        if v is None or v.strip() == "":
            return None

        v = v.strip()
        try:
            # Validate email format AND check DNS (domain exists and has mail servers)
            validate_email_dns(v, check_deliverability=True)
            return v
        except EmailNotValidError as e:
            # Raise ValueError with user-friendly message based on error type
            error_msg = str(e).lower()

            # Check for specific DNS-related errors
            if "domain name does not exist" in error_msg:
                raise ValueError("The email domain does not exist")
            elif "does not accept email" in error_msg or "no mx record" in error_msg:
                raise ValueError("The email domain does not accept emails")
            elif "not deliverable" in error_msg:
                raise ValueError("The email domain is not deliverable")
            elif "domain name" in error_msg and "invalid" in error_msg:
                raise ValueError("Invalid email domain")
            else:
                # Format errors or other validation errors
                raise ValueError("Invalid email address")
        except Exception:
            # Handle DNS lookup failures - fall back to basic format check
            # This handles network issues, timeouts, etc.
            email_pattern = re.compile(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            )
            if email_pattern.match(v):
                # Format is valid, but DNS check failed - accept it anyway
                return v
            raise ValueError("Invalid email format")

    @field_validator("business_type")
    @classmethod
    def validate_business_type(cls, v: str) -> str:
        """Validate business type - must be at least 2 characters."""
        if len(v.strip()) < 2:
            raise ValueError("Business type must be at least 2 characters")
        return v.strip()
