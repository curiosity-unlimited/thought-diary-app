"""Unit tests for authentication endpoints.

This module tests:
- User registration with validation
- User login with JWT token generation
- Token refresh mechanism
- User logout with token invalidation
- Current user profile retrieval
- Rate limiting on auth endpoints
"""
from app.models.user import User


class TestRegisterEndpoint:
    """Test cases for POST /auth/register endpoint."""
    
    def test_register_success(self, client, app, db):
        """Test successful user registration."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'newuser@example.com',
                'password': 'SecurePass123!'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'email' in data
        assert data['email'] == 'newuser@example.com'
        assert 'password_hash' not in data
        assert 'id' in data
        
        # Verify user was created in database
        with app.app_context():
            user = db.session.query(User).filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.email == 'newuser@example.com'
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'invalid-email',
                'password': 'SecurePass123!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_missing_email(self, client):
        """Test registration without email field."""
        response = client.post(
            '/auth/register',
            json={
                'password': 'SecurePass123!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_missing_password(self, client):
        """Test registration without password field."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'test@example.com'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_weak_password(self, client):
        """Test registration with weak password (no uppercase)."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'weakpass123!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'password' in data['error'].lower()
    
    def test_register_short_password(self, client):
        """Test registration with password too short."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'Short1!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_password_no_number(self, client):
        """Test registration with password missing number."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'NoNumberPass!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_password_no_special_char(self, client):
        """Test registration with password missing special character."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'NoSpecial123'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with already existing email."""
        response = client.post(
            '/auth/register',
            json={
                'email': test_user.email,
                'password': 'AnotherPass123!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower() or 'already registered' in data['error'].lower()
    
    def test_register_empty_json(self, client):
        """Test registration with empty JSON body."""
        response = client.post('/auth/register', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestLoginEndpoint:
    """Test cases for POST /auth/login endpoint."""
    
    def test_login_success(self, client, test_user):
        """Test successful user login."""
        response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'TestPassword123!'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert isinstance(data['access_token'], str)
        assert isinstance(data['refresh_token'], str)
        assert len(data['access_token']) > 0
        assert len(data['refresh_token']) > 0
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'SomePassword123!'
            }
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'code' in data
        assert data['code'] == 'INVALID_CREDENTIALS'
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'WrongPassword123!'
            }
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'code' in data
        assert data['code'] == 'INVALID_CREDENTIALS'
    
    def test_login_missing_email(self, client):
        """Test login without email field."""
        response = client.post(
            '/auth/login',
            json={
                'password': 'SomePassword123!'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_login_missing_password(self, client):
        """Test login without password field."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'test@example.com'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_login_empty_credentials(self, client):
        """Test login with empty email and password."""
        response = client.post(
            '/auth/login',
            json={
                'email': '',
                'password': ''
            }
        )
        
        assert response.status_code in [400, 401]
        data = response.get_json()
        assert 'error' in data


class TestRefreshEndpoint:
    """Test cases for POST /auth/refresh endpoint."""
    
    def test_refresh_token_success(self, client, test_user):
        """Test successful token refresh."""
        # First login to get refresh token
        login_response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'TestPassword123!'
            }
        )
        
        refresh_token = login_response.get_json()['refresh_token']
        
        # Use refresh token to get new access token
        response = client.post(
            '/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert isinstance(data['access_token'], str)
        assert len(data['access_token']) > 0
    
    def test_refresh_without_token(self, client):
        """Test refresh without providing token."""
        response = client.post('/auth/refresh')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data or 'msg' in data
    
    def test_refresh_with_invalid_token(self, client):
        """Test refresh with invalid token."""
        response = client.post(
            '/auth/refresh',
            headers={'Authorization': 'Bearer invalid-token-here'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data or 'msg' in data
    
    def test_refresh_with_access_token_instead_of_refresh(self, client, test_user):
        """Test refresh using access token instead of refresh token."""
        # Login to get access token
        login_response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'TestPassword123!'
            }
        )
        
        access_token = login_response.get_json()['access_token']
        
        # Try to use access token for refresh
        response = client.post(
            '/auth/refresh',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        # Should fail because access token is not a refresh token
        assert response.status_code in [401, 422]


class TestLogoutEndpoint:
    """Test cases for POST /auth/logout endpoint."""
    
    def test_logout_success(self, client, auth_headers):
        """Test successful logout."""
        response = client.post('/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'logged out' in data['message'].lower() or 'success' in data['message'].lower()
    
    def test_logout_without_token(self, client):
        """Test logout without authentication token."""
        response = client.post('/auth/logout')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data or 'msg' in data
    
    def test_logout_with_invalid_token(self, client):
        """Test logout with invalid token."""
        response = client.post(
            '/auth/logout',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        
        assert response.status_code == 401
    
    def test_token_invalidated_after_logout(self, client, test_user):
        """Test that token is invalidated after logout."""
        # Login
        login_response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'TestPassword123!'
            }
        )
        
        access_token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Verify token works before logout
        response = client.get('/auth/me', headers=headers)
        assert response.status_code == 200
        
        # Logout
        logout_response = client.post('/auth/logout', headers=headers)
        assert logout_response.status_code == 200
        
        # Try to use the same token after logout
        response = client.get('/auth/me', headers=headers)
        assert response.status_code == 401


class TestMeEndpoint:
    """Test cases for GET /auth/me endpoint."""
    
    def test_get_current_user_success(self, client, auth_headers, test_user):
        """Test getting current user profile."""
        response = client.get('/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'email' in data
        assert data['email'] == test_user.email
        assert data['id'] == test_user.id
        assert 'password_hash' not in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_get_current_user_without_token(self, client):
        """Test getting current user without authentication."""
        response = client.get('/auth/me')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data or 'msg' in data
    
    def test_get_current_user_with_invalid_token(self, client):
        """Test getting current user with invalid token."""
        response = client.get(
            '/auth/me',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        
        assert response.status_code == 401


class TestRateLimiting:
    """Test cases for rate limiting on auth endpoints."""
    
    def test_register_rate_limit(self, client, app):
        """Test rate limiting on register endpoint (3 per hour)."""
        # Note: This test may be skipped in test environment if rate limiting is disabled
        if app.config.get('TESTING') and not app.config.get('RATELIMIT_ENABLED'):
            return  # Skip rate limiting test in test environment
        
        # Make 3 successful requests (should work)
        for i in range(3):
            response = client.post(
                '/auth/register',
                json={
                    'email': f'user{i}@example.com',
                    'password': 'SecurePass123!'
                }
            )
            assert response.status_code == 201
        
        # 4th request should be rate limited
        response = client.post(
            '/auth/register',
            json={
                'email': 'user4@example.com',
                'password': 'SecurePass123!'
            }
        )
        assert response.status_code == 429
    
    def test_login_rate_limit(self, client, app, test_user):
        """Test rate limiting on login endpoint (5 per 15 minutes)."""
        # Note: This test may be skipped in test environment if rate limiting is disabled
        if app.config.get('TESTING') and not app.config.get('RATELIMIT_ENABLED'):
            return  # Skip rate limiting test in test environment
        
        # Make 5 login attempts (should work)
        for i in range(5):
            response = client.post(
                '/auth/login',
                json={
                    'email': test_user.email,
                    'password': 'TestPassword123!'
                }
            )
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'TestPassword123!'
            }
        )
        assert response.status_code == 429


class TestErrorFormat:
    """Test cases for consistent error format across auth endpoints."""
    
    def test_error_format_structure(self, client):
        """Test that errors return consistent format with error and code fields."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'SomePass123!'
            }
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'code' in data
        assert isinstance(data['error'], str)
        assert isinstance(data['code'], str)
    
    def test_validation_error_format(self, client):
        """Test error format for validation errors."""
        response = client.post(
            '/auth/register',
            json={
                'email': 'invalid-email',
                'password': 'weak'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
