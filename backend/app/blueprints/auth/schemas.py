"""Marshmallow schemas for authentication and user serialization.

This module defines schemas for request validation and response serialization
in the authentication system.
"""

from marshmallow import Schema, fields, validates, ValidationError, post_load
from app.utils.validators import validate_email as check_email, normalize_email
from app.utils.password import validate_password


class RegisterSchema(Schema):
    """Schema for user registration request validation.

    Validates email format and password strength requirements.
    """

    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required",
            "invalid": "Invalid email format",
        },
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required"},
    )

    @validates("email")
    def validate_email_format(self, value: str, **kwargs) -> None:
        """Validate email address format.

        Args:
            value: The email address to validate.
            **kwargs: Additional keyword arguments from Marshmallow.

        Raises:
            ValidationError: If email format is invalid.
        """
        if not check_email(value):
            raise ValidationError("Invalid email format")

    @validates("password")
    def validate_password_strength(self, value: str, **kwargs) -> None:
        """Validate password against security requirements.

        Args:
            value: The password to validate.
            **kwargs: Additional keyword arguments from Marshmallow.

        Raises:
            ValidationError: If password doesn't meet requirements.
        """
        is_valid, error_message = validate_password(value)
        if not is_valid:
            raise ValidationError(error_message)

    @post_load
    def normalize_data(self, data, **kwargs):
        """Normalize email to lowercase after validation.

        Args:
            data: Validated data dictionary.
            **kwargs: Additional keyword arguments from Marshmallow.

        Returns:
            Data with normalized email.
        """
        if "email" in data:
            data["email"] = normalize_email(data["email"])
        return data


class LoginSchema(Schema):
    """Schema for user login request validation."""

    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required",
            "invalid": "Invalid email format",
        },
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required"},
    )


class UserSchema(Schema):
    """Schema for user data serialization.

    Excludes password_hash for security. Used for response serialization.
    """

    id = fields.Int(dump_only=True)
    email = fields.Email()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TokenSchema(Schema):
    """Schema for JWT token response serialization."""

    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    token_type = fields.Str(dump_default="Bearer")


class MessageSchema(Schema):
    """Schema for simple message responses."""

    message = fields.Str(required=True)


class ErrorSchema(Schema):
    """Schema for error responses with consistent format."""

    error = fields.Str(required=True)
    code = fields.Str(required=True)
