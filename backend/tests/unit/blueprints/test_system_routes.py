"""Unit tests for system routes (health, version, docs).

This module contains pytest tests for system-level endpoints that provide
health checks, version information, and API documentation.
"""

import pytest
from datetime import datetime


class TestHealthEndpoint:
    """Tests for the /health endpoint."""
    
    def test_health_check_success(self, client):
        """Test health check returns healthy status.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        
        # Verify timestamp format (ISO 8601 with Z suffix)
        timestamp = data['timestamp']
        assert timestamp.endswith('Z')
        # Verify it's a valid ISO format datetime
        datetime.fromisoformat(timestamp.rstrip('Z'))
    
    def test_health_check_no_auth_required(self, client):
        """Test health check endpoint does not require authentication.
        
        Args:
            client: Flask test client fixture.
        """
        # No Authorization header
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'


class TestVersionEndpoint:
    """Tests for the /version endpoint."""
    
    def test_version_info_success(self, client):
        """Test version endpoint returns correct version info.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/version')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'version' in data
        assert 'api' in data
        assert data['version'] == '0.1.0'
        assert data['api'] == 'v1'
    
    def test_version_no_auth_required(self, client):
        """Test version endpoint does not require authentication.
        
        Args:
            client: Flask test client fixture.
        """
        # No Authorization header
        response = client.get('/version')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['version'] == '0.1.0'


class TestDocsEndpoint:
    """Tests for the /docs endpoint (Swagger UI)."""
    
    def test_docs_accessible(self, client):
        """Test that the API documentation endpoint is accessible.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/docs')
        
        # Should return HTML for Swagger UI or redirect to /docs/
        assert response.status_code in [200, 301, 302, 308]
        if response.status_code == 200:
            assert response.content_type.startswith('text/html')
    
    def test_apispec_json_accessible(self, client):
        """Test that the OpenAPI spec JSON is accessible.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/apispec.json')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'swagger' in data
        assert 'info' in data
        assert data['info']['title'] == 'Thought Diary API'
        assert data['info']['version'] == '0.1.0'
    
    def test_apispec_contains_endpoints(self, client):
        """Test that OpenAPI spec contains documented endpoints.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/apispec.json')
        data = response.get_json()
        
        # Check for key endpoints in the spec
        assert 'paths' in data
        paths = data['paths']
        
        # System endpoints
        assert '/health' in paths
        assert '/version' in paths
        
        # Auth endpoints
        assert '/auth/register' in paths
        assert '/auth/login' in paths
        assert '/auth/refresh' in paths
        assert '/auth/logout' in paths
        assert '/auth/me' in paths
        
        # Diary endpoints
        assert '/diaries' in paths
        assert '/diaries/{diary_id}' in paths
        assert '/diaries/stats' in paths
    
    def test_apispec_contains_security_definitions(self, client):
        """Test that OpenAPI spec includes security definitions.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/apispec.json')
        data = response.get_json()
        
        assert 'securityDefinitions' in data
        assert 'Bearer' in data['securityDefinitions']
        
        bearer_def = data['securityDefinitions']['Bearer']
        assert bearer_def['type'] == 'apiKey'
        assert bearer_def['name'] == 'Authorization'
        assert bearer_def['in'] == 'header'
    
    def test_apispec_contains_tags(self, client):
        """Test that OpenAPI spec includes endpoint tags.
        
        Args:
            client: Flask test client fixture.
        """
        response = client.get('/apispec.json')
        data = response.get_json()
        
        assert 'tags' in data
        tag_names = [tag['name'] for tag in data['tags']]
        
        assert 'System' in tag_names
        assert 'Authentication' in tag_names
        assert 'Thought Diaries' in tag_names
