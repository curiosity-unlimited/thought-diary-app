"""Application configuration module.

This module defines configuration classes for different environments
(Development, Testing, Production). Each configuration class inherits
from a base Config class and provides environment-specific settings.
"""

import os
from datetime import timedelta
from typing import Optional


class Config:
    """Base configuration class with common settings for all environments.
    
    Attributes:
        SECRET_KEY: Secret key for Flask session management and security.
        JWT_SECRET_KEY: Secret key for JWT token generation and verification.
        SQLALCHEMY_TRACK_MODIFICATIONS: Disable SQLAlchemy event system to save resources.
        JWT_ACCESS_TOKEN_EXPIRES: Access token expiration time (15 minutes).
        JWT_REFRESH_TOKEN_EXPIRES: Refresh token expiration time (7 days).
        CORS_ORIGINS: Allowed origins for CORS requests.
        GITHUB_TOKEN: GitHub API token for model inference.
        GITHUB_MODEL_NAME: GitHub model name for sentiment analysis.
        GITHUB_API_URL: GitHub Models API endpoint.
    """
    
    # Flask settings
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # JWT settings
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=7)
    
    # CORS settings
    CORS_ORIGINS: str = os.environ.get('CORS_ORIGINS', 'http://localhost:5173')
    
    # GitHub Models API settings
    GITHUB_TOKEN: Optional[str] = os.environ.get('GITHUB_TOKEN')
    GITHUB_MODEL_NAME: str = os.environ.get('GITHUB_MODEL_NAME', 'gpt-4o')
    GITHUB_API_URL: str = 'https://models.inference.ai.azure.com/chat/completions'
    
    # Rate limiting settings
    RATELIMIT_STORAGE_URL: Optional[str] = os.environ.get('REDIS_URL')
    RATELIMIT_STRATEGY: str = 'fixed-window'


class DevelopmentConfig(Config):
    """Development environment configuration.
    
    Enables debug mode and uses SQLite database for local development.
    CORS is relaxed for development ease.
    
    Attributes:
        DEBUG: Enable debug mode for detailed error messages.
        SQLALCHEMY_DATABASE_URI: SQLite database path for development.
    """
    
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL',
        'sqlite:///dev.db'
    )


class TestingConfig(Config):
    """Testing environment configuration.
    
    Uses in-memory SQLite database for faster test execution.
    Disables rate limiting for testing.
    
    Attributes:
        TESTING: Enable testing mode.
        SQLALCHEMY_DATABASE_URI: In-memory SQLite database.
        RATELIMIT_ENABLED: Disable rate limiting for tests.
    """
    
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    RATELIMIT_ENABLED: bool = False
    # Use shorter token expiration for faster testing
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(seconds=30)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(minutes=1)


class ProductionConfig(Config):
    """Production environment configuration.
    
    Uses PostgreSQL database and enforces stricter security settings.
    Requires Redis for rate limiting persistence.
    
    Attributes:
        DEBUG: Disable debug mode in production.
        SQLALCHEMY_DATABASE_URI: PostgreSQL database connection string.
        RATELIMIT_STORAGE_URL: Redis URL for rate limiting (required).
    """
    
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL',
        'postgresql://localhost/thought_diary_prod'
    )
    # Override base config to make Redis required for production
    RATELIMIT_STORAGE_URL: str = os.environ.get(
        'REDIS_URL',
        'redis://localhost:6379/0'
    )


# Configuration dictionary for easy access by environment name
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: Optional[str] = None) -> type[Config]:
    """Get configuration class based on environment name.
    
    Args:
        env: Environment name ('development', 'testing', 'production').
             If None, uses FLASK_ENV environment variable or 'default'.
    
    Returns:
        Configuration class for the specified environment.
    
    Examples:
        >>> config_class = get_config('development')
        >>> app.config.from_object(config_class)
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, DevelopmentConfig)
