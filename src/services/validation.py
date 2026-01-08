"""Validation service for form fields."""

import re
from email_validator import validate_email as validate_email_dns, EmailNotValidError
from pydantic import ValidationError

from src.models.form_data import FormData


class FormValidator:
    """Validates form input data directly without creating full models."""

    @staticmethod
    def validate_name(name: str) -> tuple[bool, str]:
        """Validate name field - must be at least 2 characters.

        Args:
            name: Name to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        return True, ""

    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """Validate phone field - must have at least 8 digits.

        Args:
            phone: Phone number to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone:
            return False, "Phone number is required"

        # Remove common formatting characters for digit count check
        digits_only = re.sub(r"[^\d]", "", phone)
        if len(digits_only) < 8:
            return False, "Phone must have at least 8 digits"

        # Validate phone pattern (digits, spaces, dashes, plus sign, parentheses)
        phone_pattern = re.compile(r"^[\d\s\-\+\(\)]{8,}$")
        if not phone_pattern.match(phone):
            return False, "Invalid phone number format"

        return True, ""

    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """Validate email field with DNS verification.

        Args:
            email: Email to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Email is optional - empty is valid
        if not email or email.strip() == "":
            return True, ""

        email = email.strip()

        try:
            # Validate email format AND check DNS (domain exists and has mail servers)
            validate_email_dns(email, check_deliverability=True)
            return True, ""
        except EmailNotValidError as e:
            # Return user-friendly error message based on error type
            error_msg = str(e).lower()

            # Check for specific DNS-related errors
            if "domain name does not exist" in error_msg:
                return False, "The email domain does not exist"
            elif "does not accept email" in error_msg or "no mx record" in error_msg:
                return False, "The email domain does not accept emails"
            elif "not deliverable" in error_msg:
                return False, "The email domain is not deliverable"
            elif "domain name" in error_msg and "invalid" in error_msg:
                return False, "Invalid email domain"
            else:
                # Format errors or other validation errors
                return False, "Invalid email address"
        except Exception as e:
            # Handle DNS lookup failures (network issues, timeouts, etc.)
            # Fall back to basic format check
            print(f"DNS validation error (falling back to format check): {e}")
            # Basic format check as fallback
            email_pattern = re.compile(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            )
            if email_pattern.match(email):
                return True, ""  # Format is valid, but DNS check failed
            return False, "Invalid email format"

    @staticmethod
    def validate_business_type(business_type: str) -> tuple[bool, str]:
        """Validate business type - must be at least 2 characters.

        Args:
            business_type: Business type to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not business_type or len(business_type.strip()) < 2:
            return False, "Business type must be at least 2 characters"
        return True, ""

    @staticmethod
    def validate_form_data(
        full_name: str, phone: str, email: str | None, business_type: str
    ) -> tuple[bool, FormData | None, str]:
        """Validate complete form data using Pydantic model.

        Args:
            full_name: User's full name
            phone: User's phone number
            email: User's email (optional)
            business_type: User's business type

        Returns:
            Tuple of (is_valid, FormData object or None, error_message)
        """
        try:
            form_data = FormData(
                full_name=full_name,
                phone=phone,
                email=email,
                business_type=business_type,
            )
            return True, form_data, ""
        except ValidationError as e:
            # Get first error message
            error_msg = e.errors()[0]["msg"] if e.errors() else "Validation failed"
            return False, None, error_msg
