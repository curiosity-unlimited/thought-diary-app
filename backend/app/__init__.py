"""Flask application factory module.

This module implements the application factory pattern for creating
Flask application instances with different configurations.
"""

from typing import Optional
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from config import get_config
from app.extensions import db, migrate, ma, jwt, limiter, cors
# Import models to register them with SQLAlchemy
from app.models import User, ThoughtDiary


# Token blacklist for logout functionality
# In production, use Redis for distributed systems
token_blacklist = set()


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure a Flask application instance.
    
    This function implements the application factory pattern, allowing
    the creation of multiple app instances with different configurations
    (e.g., for testing, development, production).
    
    Args:
        config_name: Configuration name ('development', 'testing', 'production').
                    If None, uses FLASK_ENV environment variable.
    
    Returns:
        Configured Flask application instance.
    
    Examples:
        >>> app = create_app('testing')
        >>> app = create_app('production')
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS with origins from config
    cors_origins = app.config.get('CORS_ORIGINS', '').split(',')
    cors.init_app(app, origins=cors_origins, supports_credentials=True)
    
    # Configure rate limiter with storage from config
    limiter.init_app(app)
    if app.config.get('RATELIMIT_STORAGE_URL'):
        app.config['RATELIMIT_STORAGE_URI'] = app.config['RATELIMIT_STORAGE_URL']
    
    # Configure JWT callbacks
    configure_jwt_callbacks(app)
    
    # Register blueprints
    from app.blueprints.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def configure_jwt_callbacks(app: Flask) -> None:
    """Configure JWT-Extended callbacks for token validation.
    
    Args:
        app: Flask application instance.
    """
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        """Check if a token has been revoked (is in blacklist).
        
        Args:
            jwt_header: JWT header data.
            jwt_payload: JWT payload containing token data.
        
        Returns:
            True if token is revoked, False otherwise.
        """
        jti = jwt_payload["jti"]
        return jti in token_blacklist
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload: dict) -> tuple:
        """Handle expired token errors.
        
        Args:
            jwt_header: JWT header data.
            jwt_payload: JWT payload containing token data.
        
        Returns:
            JSON response with error details and 401 status code.
        """
        return jsonify({
            'error': 'Token has expired',
            'code': 'TOKEN_EXPIRED'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error: str) -> tuple:
        """Handle invalid token errors.
        
        Args:
            error: Error message.
        
        Returns:
            JSON response with error details and 401 status code.
        """
        app.logger.error(f"Invalid token error: {error}")
        return jsonify({
            'error': f'Invalid token: {error}',
            'code': 'INVALID_TOKEN'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error: str) -> tuple:
        """Handle missing token errors.
        
        Args:
            error: Error message.
        
        Returns:
            JSON response with error details and 401 status code.
        """
        return jsonify({
            'error': 'Authorization token is missing',
            'code': 'MISSING_TOKEN'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload: dict) -> tuple:
        """Handle revoked token errors.
        
        Args:
            jwt_header: JWT header data.
            jwt_payload: JWT payload containing token data.
        
        Returns:
            JSON response with error details and 401 status code.
        """
        return jsonify({
            'error': 'Token has been revoked',
            'code': 'TOKEN_REVOKED'
        }), 401


def register_error_handlers(app: Flask) -> None:
    """Register error handlers for consistent error response format.
    
    All errors return JSON in the format:
    {
        "error": "Error message",
        "code": "ERROR_CODE"
    }
    
    Args:
        app: Flask application instance.
    """
    
    @app.errorhandler(400)
    def bad_request(error: HTTPException) -> tuple:
        """Handle 400 Bad Request errors.
        
        Args:
            error: HTTPException instance.
        
        Returns:
            JSON response with error details and 400 status code.
        """
        return jsonify({
            'error': error.description or 'Bad request',
            'code': 'BAD_REQUEST'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error: HTTPException) -> tuple:
        """Handle 401 Unauthorized errors.
        
        Args:
            error: HTTPException instance.
        
        Returns:
            JSON response with error details and 401 status code.
        """
        return jsonify({
            'error': error.description or 'Unauthorized',
            'code': 'UNAUTHORIZED'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error: HTTPException) -> tuple:
        """Handle 403 Forbidden errors.
        
        Args:
            error: HTTPException instance.
        
        Returns:
            JSON response with error details and 403 status code.
        """
        return jsonify({
            'error': error.description or 'Forbidden',
            'code': 'FORBIDDEN'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error: HTTPException) -> tuple:
        """Handle 404 Not Found errors.
        
        Args:
            error: HTTPException instance.
        
        Returns:
            JSON response with error details and 404 status code.
        """
        return jsonify({
            'error': error.description or 'Resource not found',
            'code': 'NOT_FOUND'
        }), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error: HTTPException) -> tuple:
        """Handle 429 Too Many Requests errors.
        
        Args:
            error: HTTPException instance.
        
        Returns:
            JSON response with error details and 429 status code.
        """
        return jsonify({
            'error': error.description or 'Rate limit exceeded',
            'code': 'RATE_LIMIT_EXCEEDED'
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error: HTTPException) -> tuple:
        """Handle 500 Internal Server Error.
        
        Args:
            error: HTTPException instance.
        
        Returns:
            JSON response with error details and 500 status code.
        """
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_SERVER_ERROR'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple:
        """Handle unexpected errors.
        
        Args:
            error: Exception instance.
        
        Returns:
            JSON response with error details and 500 status code.
        """
        # Log the error for debugging
        app.logger.error(f'Unexpected error: {str(error)}', exc_info=True)
        
        return jsonify({
            'error': 'An unexpected error occurred',
            'code': 'INTERNAL_SERVER_ERROR'
        }), 500
