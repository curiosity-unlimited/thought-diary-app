"""Authentication routes for user registration, login, and token management.

This module provides endpoints for:
- User registration with validation
- User login with JWT token generation
- Token refresh mechanism
- User logout with token invalidation
- Current user profile retrieval
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flasgger import swag_from

from app.extensions import db, limiter
from app.models.user import User
from app.blueprints.auth.schemas import (
    RegisterSchema,
    LoginSchema,
    UserSchema,
    TokenSchema,
    MessageSchema,
)
from app.utils.validators import normalize_email
import app

# Create blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Initialize schemas
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()
token_schema = TokenSchema()
message_schema = MessageSchema()


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("3 per hour")
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Register a new user',
    'description': 'Create a new user account with email and password. Rate limited to 3 requests per hour.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'example': 'user@example.com',
                    'description': 'Valid email address'
                },
                'password': {
                    'type': 'string',
                    'format': 'password',
                    'example': 'SecurePass123!',
                    'description': 'Password (min 8 chars, must include uppercase, lowercase, number, and special character)'
                }
            }
        }
    }],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'email': {'type': 'string', 'example': 'user@example.com'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Validation error or email already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Email already registered'},
                    'code': {'type': 'string', 'example': 'EMAIL_EXISTS'}
                }
            }
        },
        429: {
            'description': 'Rate limit exceeded',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Rate limit exceeded'},
                    'code': {'type': 'string', 'example': 'RATE_LIMIT_EXCEEDED'}
                }
            }
        }
    }
})
def register():
    """Register a new user.

    Request JSON:
        {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }

    Returns:
        201: User created successfully with user data
        400: Validation error or email already exists
        429: Rate limit exceeded

    Rate Limit:
        3 requests per hour per IP address
    """
    try:
        # Validate request data
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": str(err.messages), "code": "VALIDATION_ERROR"}), 400

    email = normalize_email(data["email"])
    password = data["password"]

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered", "code": "EMAIL_EXISTS"}), 400

    # Create new user
    try:
        new_user = User(email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered", "code": "EMAIL_EXISTS"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "code": "REGISTRATION_ERROR"}), 500


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per 15 minutes")
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Login user',
    'description': 'Authenticate user and return JWT access and refresh tokens. Rate limited to 5 requests per 15 minutes.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'example': 'user@example.com'
                },
                'password': {
                    'type': 'string',
                    'format': 'password',
                    'example': 'SecurePass123!'
                }
            }
        }
    }],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'description': 'JWT access token (expires in 15 minutes)'
                    },
                    'refresh_token': {
                        'type': 'string',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'description': 'JWT refresh token (expires in 7 days)'
                    },
                    'token_type': {
                        'type': 'string',
                        'example': 'Bearer'
                    }
                }
            }
        },
        400: {
            'description': 'Validation error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'VALIDATION_ERROR'}
                }
            }
        },
        401: {
            'description': 'Invalid credentials',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Invalid email or password'},
                    'code': {'type': 'string', 'example': 'INVALID_CREDENTIALS'}
                }
            }
        },
        429: {
            'description': 'Rate limit exceeded',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'RATE_LIMIT_EXCEEDED'}
                }
            }
        }
    }
})
def login():
    """Authenticate user and return JWT tokens.

    Request JSON:
        {
            "email": "user@example.com",
            "password": "SecurePass123!"
        }

    Returns:
        200: Login successful with access and refresh tokens
        400: Validation error
        401: Invalid credentials
        429: Rate limit exceeded

    Rate Limit:
        5 requests per 15 minutes per IP address
    """
    try:
        # Validate request data
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": str(err.messages), "code": "VALIDATION_ERROR"}), 400

    email = normalize_email(data["email"])
    password = data["password"]

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify credentials
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password", "code": "INVALID_CREDENTIALS"}), 401

    # Generate tokens (identity must be string for JWT-Extended)
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    response_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }

    return jsonify(response_data), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Refresh access token',
    'description': 'Generate a new access token using a valid refresh token',
    'responses': {
        200: {
            'description': 'New access token generated',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                    },
                    'token_type': {
                        'type': 'string',
                        'example': 'Bearer'
                    }
                }
            }
        },
        401: {
            'description': 'Invalid or expired refresh token',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'TOKEN_EXPIRED'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def refresh():
    """Refresh access token using refresh token.

    Requires:
        Valid refresh token in Authorization header

    Returns:
        200: New access token
        401: Invalid or expired refresh token
    """
    current_user_id = get_jwt_identity()

    # Generate new access token
    new_access_token = create_access_token(identity=current_user_id)

    return jsonify({"access_token": new_access_token, "token_type": "Bearer"}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Logout user',
    'description': 'Invalidate the current access token by adding it to the blacklist',
    'responses': {
        200: {
            'description': 'Logout successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Successfully logged out'
                    }
                }
            }
        },
        401: {
            'description': 'Invalid or missing token',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def logout():
    """Logout user by invalidating the current token.

    Requires:
        Valid access token in Authorization header

    Returns:
        200: Logout successful
        401: Invalid or missing token
    """
    jti = get_jwt()["jti"]
    app.token_blacklist.add(jti)

    return jsonify({"message": "Successfully logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Get current user profile',
    'description': 'Retrieve the profile information of the currently authenticated user',
    'responses': {
        200: {
            'description': 'User profile retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'email': {'type': 'string', 'example': 'user@example.com'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        401: {
            'description': 'Invalid or missing token',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        },
        404: {
            'description': 'User not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'User not found'},
                    'code': {'type': 'string', 'example': 'USER_NOT_FOUND'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def get_current_user():
    """Get current authenticated user profile.

    Requires:
        Valid access token in Authorization header

    Returns:
        200: User profile data
        401: Invalid or missing token
        404: User not found
    """
    current_user_id = int(get_jwt_identity())

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found", "code": "USER_NOT_FOUND"}), 404

    return jsonify(user_schema.dump(user)), 200

