"""Input validation and sanitization utilities.

This module provides functions for validating and sanitizing user input,
including email validation and text sanitization.
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email address format.

    Checks if the email follows a valid format with basic RFC 5322 compliance.
    Pattern validates:
    - Local part: alphanumeric, dots, hyphens, underscores
    - @ symbol
    - Domain: alphanumeric, dots, hyphens
    - TLD: 2+ characters

    Args:
        email: The email address to validate.

    Returns:
        True if email format is valid, False otherwise.

    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid-email")
        False
        >>> validate_email("user@domain")
        False
    """
    if not email:
        return False

    # Email regex pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(pattern, email))


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize string input by removing leading/trailing whitespace.

    Args:
        text: The string to sanitize.
        max_length: Optional maximum length to truncate to.

    Returns:
        The sanitized string.

    Example:
        >>> sanitize_string("  hello world  ")
        'hello world'
        >>> sanitize_string("  hello world  ", max_length=5)
        'hello'
    """
    if not text:
        return ""

    # Remove leading and trailing whitespace
    sanitized = text.strip()

    # Truncate if max_length is specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def normalize_email(email: str) -> str:
    """Normalize email address to lowercase.

    Args:
        email: The email address to normalize.

    Returns:
        The normalized email address in lowercase.

    Example:
        >>> normalize_email("User@Example.COM")
        'user@example.com'
    """
    if not email:
        return ""

    return email.strip().lower()
