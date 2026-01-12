"""Password utilities for secure password handling.

This module provides functions for password validation, hashing, and verification
using bcrypt for secure password storage.
"""

import re
from typing import Tuple
import bcrypt


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password against strict security requirements.

    Password must meet the following criteria:
    - Minimum 8 characters in length
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one digit (0-9)
    - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

    Args:
        password: The password string to validate.

    Returns:
        A tuple of (is_valid, error_message). If valid, error_message is empty.

    Example:
        >>> is_valid, error = validate_password("Weak123")
        >>> print(is_valid)
        False
        >>> print(error)
        Password must contain at least one special character
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
        return False, "Password must contain at least one special character"

    return True, ""


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: The plain text password to hash.

    Returns:
        The bcrypt hashed password as a string.

    Example:
        >>> hashed = hash_password("MySecurePass123!")
        >>> print(hashed.startswith("$2b$"))
        True
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash.

    Args:
        password: The plain text password to verify.
        password_hash: The bcrypt hash to verify against.

    Returns:
        True if the password matches the hash, False otherwise.

    Example:
        >>> hashed = hash_password("MySecurePass123!")
        >>> print(verify_password("MySecurePass123!", hashed))
        True
        >>> print(verify_password("WrongPassword", hashed))
        False
    """
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)
