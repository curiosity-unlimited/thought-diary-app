# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-12

### Backend [0.1.0]
#### Added
- Flask application infrastructure with application factory pattern
- Environment-based configuration system (Development, Testing, Production)
- Flask extensions initialization (SQLAlchemy, Flask-Migrate, Flask-Marshmallow, Flask-JWT-Extended, Flask-Limiter, Flask-CORS)
- Comprehensive error handlers with consistent JSON error format
- JWT authentication configuration with 15-minute access tokens and 7-day refresh tokens
- CORS configuration for frontend integration (http://localhost:5173)
- Rate limiting infrastructure with Redis support
- GitHub Models API configuration for AI sentiment analysis (gpt-4o)
- Environment variables documentation in .env.example
- Type hints (PEP 484) and comprehensive docstrings (PEP 257) throughout codebase
- Development dependencies: pytest, pytest-cov, pytest-flask
- Production dependencies: flask, flask-sqlalchemy, flask-migrate, flask-marshmallow, marshmallow-sqlalchemy, flask-jwt-extended, flask-limiter, bcrypt, flask-cors, requests, gunicorn, redis, python-dotenv
- User model with email validation, bcrypt password hashing, and verification methods
- ThoughtDiary model with content validation, sentiment analysis support, and user relationship
- Database models registered with SQLAlchemy for proper ORM functionality
- Flask-Migrate integration with initial migration for User and ThoughtDiary tables
- One-to-many relationship between User and ThoughtDiary with cascade delete
- Model helper methods: User.validate_email(), User.set_password(), User.check_password()
- Model helper methods: ThoughtDiary.validate_content(), ThoughtDiary.get_sentiment(), ThoughtDiary.to_dict()
- Database indexes on User.email, ThoughtDiary.user_id, and ThoughtDiary.created_at for query optimization- Password utility functions with strict validation requirements (8+ chars, uppercase, lowercase, number, special character)
- Bcrypt-based password hashing and verification functions
- Email format validation and input sanitization utilities
- Marshmallow schemas for authentication (RegisterSchema, LoginSchema, UserSchema, TokenSchema)
- Authentication blueprint with complete user auth endpoints
- POST /auth/register endpoint with rate limiting (3 requests/hour)
- POST /auth/login endpoint with JWT token generation and rate limiting (5 requests/15min)
- POST /auth/refresh endpoint for access token renewal
- POST /auth/logout endpoint with token blacklist support
- GET /auth/me endpoint for current user profile retrieval
- JWT token blacklist functionality for secure logout
- JWT callbacks for token validation and error handling (expired, invalid, missing, revoked tokens)
- Consistent error responses across all auth endpoints with error codes
- Integration between auth system and User model with secure password handling
- AI sentiment analysis service using GitHub Models API (gpt-4o)
- analyze_sentiment() function to identify positive and negative sentiment words
- HTML-based sentiment markers with <span class="positive"> and <span class="negative"> tags
- Automatic counting of positive and negative sentiment markers
- Comprehensive error handling for API timeouts, connection errors, and HTTP errors
- Graceful fallback to original content when sentiment analysis fails
- get_sentiment_summary() helper function for overall sentiment classification
- Environment variable configuration for GITHUB_TOKEN and GITHUB_MODEL_NAME
- Request timeout set to 30 seconds for AI API calls
- Detailed logging of sentiment analysis results and errors
- Thought Diary endpoints blueprint (app/blueprints/diaries/)
- Marshmallow schemas for diary operations (DiaryCreateSchema, DiaryUpdateSchema, DiarySchema, DiaryListSchema, DiaryStatsSchema)
- GET /diaries endpoint - List user's diaries with pagination (10 per page, descending by created_at)
- POST /diaries endpoint - Create new diary with automatic AI sentiment analysis
- GET /diaries/<id> endpoint - Get specific diary entry
- PUT /diaries/<id> endpoint - Update diary with automatic AI sentiment re-analysis
- DELETE /diaries/<id> endpoint - Delete diary entry
- GET /diaries/stats endpoint - Get user statistics (total, positive, negative, neutral entries)
- Authorization checks ensuring users can only access their own diaries (403 on unauthorized access)
- AI sentiment analysis integration on diary create and update operations
- Pagination support with configurable page size (default 10, max 100 items)
- JWT authentication required for all diary endpoints (@jwt_required decorator)
- Comprehensive error handling with consistent error format for all diary operations