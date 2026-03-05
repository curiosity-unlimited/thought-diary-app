"""System endpoints for health checks, version info, and API documentation.

This module provides system-level endpoints that don't require authentication
and are useful for monitoring, debugging, and API exploration.
"""

from datetime import datetime, UTC
from flask import jsonify
from flasgger import swag_from

from . import system_bp


@system_bp.route('/health', methods=['GET'])
@swag_from({
    'tags': ['System'],
    'summary': 'Health check endpoint',
    'description': 'Returns the health status of the API',
    'responses': {
        200: {
            'description': 'API is healthy',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'example': 'healthy'
                    },
                    'timestamp': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2026-01-13T10:30:00.000Z'
                    }
                }
            }
        }
    }
})
def health_check() -> tuple:
    """Health check endpoint.
    
    Returns:
        tuple: JSON response with health status and HTTP status code.
        
    Example:
        >>> GET /health
        {
            "status": "healthy",
            "timestamp": "2026-01-13T10:30:00.000Z"
        }
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }), 200


@system_bp.route('/version', methods=['GET'])
@swag_from({
    'tags': ['System'],
    'summary': 'API version information',
    'description': 'Returns the current version of the API',
    'responses': {
        200: {
            'description': 'Version information',
            'schema': {
                'type': 'object',
                'properties': {
                    'version': {
                        'type': 'string',
                        'example': '0.1.0'
                    },
                    'api': {
                        'type': 'string',
                        'example': 'v1'
                    }
                }
            }
        }
    }
})
def version_info() -> tuple:
    """API version information endpoint.
    
    Returns:
        tuple: JSON response with version info and HTTP status code.
        
    Example:
        >>> GET /version
        {
            "version": "0.1.0",
            "api": "v1"
        }
    """
    return jsonify({
        'version': '0.1.0',
        'api': 'v1'
    }), 200
