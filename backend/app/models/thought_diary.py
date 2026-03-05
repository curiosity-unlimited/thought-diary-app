"""ThoughtDiary model for storing and analyzing user thought diary entries.

This module defines the ThoughtDiary model with AI sentiment analysis support,
including analyzed content and positive/negative sentiment counts.
"""

from datetime import datetime, timezone
from typing import Optional
from app.extensions import db


class ThoughtDiary(db.Model):
    """ThoughtDiary model for storing user thought diary entries.
    
    Attributes:
        id (int): Primary key for the thought diary entry.
        user_id (int): Foreign key reference to the user who created the entry.
        content (str): Original plain text content of the diary entry.
        analyzed_content (str): HTML content with sentiment analysis markers.
        positive_count (int): Count of positive sentiment markers in the entry.
        negative_count (int): Count of negative sentiment markers in the entry.
        created_at (datetime): Timestamp when the entry was created.
        updated_at (datetime): Timestamp when the entry was last updated.
        user (relationship): Many-to-one relationship with User.
    """
    
    __tablename__ = 'thought_diaries'
    
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False,
        index=True
    )
    content: str = db.Column(db.Text, nullable=False)
    analyzed_content: Optional[str] = db.Column(db.Text, nullable=True)
    positive_count: int = db.Column(db.Integer, default=0, nullable=False)
    negative_count: int = db.Column(db.Integer, default=0, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc),
        index=True  # Index for efficient sorting
    )
    updated_at: datetime = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    def __repr__(self) -> str:
        """Return a string representation of the ThoughtDiary object.
        
        Returns:
            str: String representation showing diary ID and user ID.
        """
        return f'<ThoughtDiary {self.id}: User {self.user_id}>'
    
    @staticmethod
    def validate_content(content: str) -> bool:
        """Validate diary content meets requirements.
        
        Args:
            content (str): Diary content to validate.
            
        Returns:
            bool: True if content is valid, False otherwise.
            
        Example:
            >>> ThoughtDiary.validate_content("Valid diary entry")
            True
            >>> ThoughtDiary.validate_content("")
            False
            >>> ThoughtDiary.validate_content("x" * 10001)
            False
        """
        if not content:
            return False
        
        # Content must not be empty after stripping whitespace
        if not content.strip():
            return False
        
        # Content should not exceed reasonable length (10000 characters)
        if len(content) > 10000:
            return False
        
        return True
    
    def get_sentiment(self) -> str:
        """Determine overall sentiment based on positive and negative counts.
        
        Returns:
            str: 'positive', 'negative', or 'neutral' based on sentiment counts.
            
        Example:
            >>> diary = ThoughtDiary(positive_count=5, negative_count=2)
            >>> diary.get_sentiment()
            'positive'
            >>> diary = ThoughtDiary(positive_count=2, negative_count=2)
            >>> diary.get_sentiment()
            'neutral'
        """
        if self.positive_count > self.negative_count:
            return 'positive'
        elif self.negative_count > self.positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def to_dict(self) -> dict:
        """Convert ThoughtDiary instance to dictionary representation.
        
        Returns:
            dict: Dictionary containing all diary fields including sentiment.
            
        Example:
            >>> diary = ThoughtDiary(content="Test", positive_count=1, negative_count=0)
            >>> diary.to_dict()
            {'id': 1, 'content': 'Test', 'sentiment': 'positive', ...}
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'analyzed_content': self.analyzed_content,
            'positive_count': self.positive_count,
            'negative_count': self.negative_count,
            'sentiment': self.get_sentiment(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
