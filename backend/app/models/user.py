"""User model for authentication and user management.

This module defines the User model with secure password handling using bcrypt,
email validation, and relationships to thought diary entries.
"""

from datetime import datetime, timezone
from typing import Optional
import re
import bcrypt
from app.extensions import db


class User(db.Model):
    """User model for authentication and profile management.
    
    Attributes:
        id (int): Primary key for the user.
        email (str): Unique email address for the user (indexed).
        password_hash (str): Bcrypt hashed password.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
        thought_diaries (relationship): One-to-many relationship with ThoughtDiary.
    """
    
    __tablename__ = 'users'
    
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(255), nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Relationship to ThoughtDiary (one-to-many)
    thought_diaries = db.relationship(
        'ThoughtDiary',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self) -> str:
        """Return a string representation of the User object.
        
        Returns:
            str: String representation showing user ID and email.
        """
        return f'<User {self.id}: {self.email}>'
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format using regex pattern.
        
        Args:
            email (str): Email address to validate.
            
        Returns:
            bool: True if email format is valid, False otherwise.
            
        Example:
            >>> User.validate_email("user@example.com")
            True
            >>> User.validate_email("invalid-email")
            False
        """
        if not email:
            return False
        
        # RFC 5322 simplified email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def set_password(self, password: str) -> None:
        """Hash password using bcrypt and store in password_hash field.
        
        Args:
            password (str): Plain text password to hash.
            
        Example:
            >>> user = User(email="test@example.com")
            >>> user.set_password("SecurePass123!")
            >>> user.password_hash  # Returns bcrypt hash string
        """
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, salt)
        self.password_hash = hashed.decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password against stored hash using bcrypt.
        
        Args:
            password (str): Plain text password to verify.
            
        Returns:
            bool: True if password matches hash, False otherwise.
            
        Example:
            >>> user.set_password("SecurePass123!")
            >>> user.check_password("SecurePass123!")
            True
            >>> user.check_password("WrongPassword")
            False
        """
        if not self.password_hash:
            return False
        
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
