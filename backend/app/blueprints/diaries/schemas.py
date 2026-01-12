"""Marshmallow schemas for thought diary serialization and validation.

This module provides schemas for validating and serializing thought diary
data for API requests and responses.
"""

from marshmallow import Schema, fields, validate, ValidationError, validates


class DiaryCreateSchema(Schema):
    """Schema for creating a new thought diary entry.
    
    Attributes:
        content (str): The diary entry content (required, 1-10000 chars).
    """
    
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=10000),
        error_messages={
            'required': 'Content is required.',
            'invalid': 'Content must be a string.'
        }
    )
    
    @validates('content')
    def validate_content(self, value: str) -> None:
        """Validate that content is not empty or only whitespace.
        
        Args:
            value (str): The content to validate.
            
        Raises:
            ValidationError: If content is empty or only whitespace.
        """
        if not value.strip():
            raise ValidationError('Content cannot be empty or only whitespace.')


class DiaryUpdateSchema(Schema):
    """Schema for updating an existing thought diary entry.
    
    Attributes:
        content (str): The updated diary entry content (required, 1-10000 chars).
    """
    
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=10000),
        error_messages={
            'required': 'Content is required.',
            'invalid': 'Content must be a string.'
        }
    )
    
    @validates('content')
    def validate_content(self, value: str) -> None:
        """Validate that content is not empty or only whitespace.
        
        Args:
            value (str): The content to validate.
            
        Raises:
            ValidationError: If content is empty or only whitespace.
        """
        if not value.strip():
            raise ValidationError('Content cannot be empty or only whitespace.')


class DiarySchema(Schema):
    """Schema for serializing thought diary entries.
    
    Attributes:
        id (int): Diary entry ID.
        user_id (int): ID of the user who created the entry.
        content (str): Original plain text content.
        analyzed_content (str): HTML content with sentiment markers.
        positive_count (int): Number of positive sentiment markers.
        negative_count (int): Number of negative sentiment markers.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    """
    
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    analyzed_content = fields.Str(allow_none=True)
    positive_count = fields.Int(dump_only=True)
    negative_count = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')


class DiaryListSchema(Schema):
    """Schema for paginated list of thought diary entries.
    
    Attributes:
        items (list): List of diary entries.
        page (int): Current page number.
        per_page (int): Number of items per page.
        total (int): Total number of items.
        pages (int): Total number of pages.
    """
    
    items = fields.List(fields.Nested(DiarySchema), required=True)
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    total = fields.Int(required=True)
    pages = fields.Int(required=True)


class DiaryStatsSchema(Schema):
    """Schema for thought diary statistics.
    
    Attributes:
        total_entries (int): Total number of diary entries.
        positive_entries (int): Number of entries with more positive sentiment.
        negative_entries (int): Number of entries with more negative sentiment.
        neutral_entries (int): Number of entries with equal positive/negative sentiment.
    """
    
    total_entries = fields.Int(required=True)
    positive_entries = fields.Int(required=True)
    negative_entries = fields.Int(required=True)
    neutral_entries = fields.Int(required=True)
