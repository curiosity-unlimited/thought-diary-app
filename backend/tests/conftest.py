"""Pytest configuration and fixtures for the test suite.

This module provides shared fixtures for testing the Flask application,
including app instance, database, test client, and authentication helpers.
"""

import os
import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, token_blacklist
from app.extensions import db as _db
from app.models.user import User
from app.models.thought_diary import ThoughtDiary


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Set GITHUB_TOKEN for AI service tests
    os.environ['GITHUB_TOKEN'] = 'test-token-123'
    os.environ['GITHUB_MODEL_NAME'] = 'gpt-4o'
    yield
    # Clean up after all tests
    if 'GITHUB_TOKEN' in os.environ:
        del os.environ['GITHUB_TOKEN']
    if 'GITHUB_MODEL_NAME' in os.environ:
        del os.environ['GITHUB_MODEL_NAME']


@pytest.fixture(scope='function')
def app() -> Generator[Flask, None, None]:
    """Create and configure a Flask application instance for testing.
    
    Yields:
        Flask application configured for testing.
    """
    # Create app with testing configuration
    test_app = create_app('testing')
    
    # Establish an application context
    with test_app.app_context():
        # Create all database tables
        _db.create_all()
        
        yield test_app
        
        # Clean up: drop all tables and clear token blacklist
        _db.session.remove()
        _db.drop_all()
        token_blacklist.clear()


@pytest.fixture(scope='function')
def client(app: Flask) -> FlaskClient:
    """Create a test client for making HTTP requests.
    
    Args:
        app: Flask application instance from app fixture.
    
    Returns:
        Flask test client.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def db(app: Flask) -> Generator:
    """Provide database instance for tests.
    
    Args:
        app: Flask application instance from app fixture.
    
    Yields:
        SQLAlchemy database instance.
    """
    with app.app_context():
        yield _db


@pytest.fixture(scope='function')
def test_user(db) -> User:
    """Create a test user in the database.
    
    Args:
        db: Database instance from db fixture.
    
    Returns:
        User instance with test data.
    """
    user = User(email='testuser@example.com')
    user.set_password('TestPassword123!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def test_user2(db) -> User:
    """Create a second test user in the database.
    
    Args:
        db: Database instance from db fixture.
    
    Returns:
        User instance with test data.
    """
    user = User(email='testuser2@example.com')
    user.set_password('TestPassword123!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def auth_headers(client: FlaskClient, test_user: User) -> dict:
    """Generate JWT authentication headers for test user.
    
    Args:
        client: Flask test client from client fixture.
        test_user: Test user from test_user fixture.
    
    Returns:
        Dictionary with Authorization header containing JWT token.
    """
    # Login to get access token
    response = client.post(
        '/auth/login',
        json={
            'email': test_user.email,
            'password': 'TestPassword123!'
        }
    )
    
    data = response.get_json()
    access_token = data['access_token']
    
    return {
        'Authorization': f'Bearer {access_token}'
    }


@pytest.fixture(scope='function')
def test_diary(db, test_user: User) -> ThoughtDiary:
    """Create a test thought diary entry in the database.
    
    Args:
        db: Database instance from db fixture.
        test_user: Test user from test_user fixture.
    
    Returns:
        ThoughtDiary instance with test data.
    """
    diary = ThoughtDiary(
        user_id=test_user.id,
        content='I felt both excitement and anxiety today.',
        analyzed_content='I felt both <span class="positive">excitement</span> and <span class="negative">anxiety</span> today.',
        positive_count=1,
        negative_count=1
    )
    db.session.add(diary)
    db.session.commit()
    return diary


@pytest.fixture(scope='function')
def multiple_diaries(db, test_user: User) -> list:
    """Create multiple test thought diary entries in the database.
    
    Args:
        db: Database instance from db fixture.
        test_user: Test user from test_user fixture.
    
    Returns:
        List of ThoughtDiary instances.
    """
    diaries = [
        ThoughtDiary(
            user_id=test_user.id,
            content='I had a wonderful day filled with joy and happiness.',
            analyzed_content='I had a <span class="positive">wonderful</span> day filled with <span class="positive">joy</span> and <span class="positive">happiness</span>.',
            positive_count=3,
            negative_count=0
        ),
        ThoughtDiary(
            user_id=test_user.id,
            content='I felt terrible and sad about the situation.',
            analyzed_content='I felt <span class="negative">terrible</span> and <span class="negative">sad</span> about the situation.',
            positive_count=0,
            negative_count=2
        ),
        ThoughtDiary(
            user_id=test_user.id,
            content='Today was an ordinary day with no special events.',
            analyzed_content='Today was an ordinary day with no special events.',
            positive_count=0,
            negative_count=0
        ),
    ]
    
    for diary in diaries:
        db.session.add(diary)
    
    db.session.commit()
    return diaries
