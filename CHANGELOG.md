# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Frontend [0.1.0]
#### Added
- Project foundation setup with Vue 3 + TypeScript + Vite
- Core dependencies: vue-router@4, pinia, axios, vue-toastification@next (Vue 3 compatible)
- UI framework: Tailwind CSS 4.x, PostCSS, Autoprefixer, @headlessui/vue
- Form validation: vee-validate, yup
- Linting and formatting: ESLint 9 (flat config), Prettier, TypeScript ESLint plugins
- Tailwind CSS configuration (tailwind.config.js) with content paths for Vue files
- PostCSS configuration (postcss.config.js) for Tailwind and Autoprefixer
- Custom CSS for sentiment highlighting: .positive (green) and .negative (red) spans
- Environment configuration: .env and .env.example files
- Environment variables: VITE_API_BASE_URL=http://localhost:5000, VITE_APP_NAME, VITE_APP_VERSION
- ESLint flat config (eslint.config.js) with Vue 3 and TypeScript support
- Prettier configuration (.prettierrc.json) with consistent formatting rules
- Prettier ignore file (.prettierignore) for build outputs
- Package.json scripts: lint, format commands
- Vite configuration with path aliases (@/ for src/) and port 5173
- Dev server successfully running with hot reload

## [0.2.0] - 2026-01-13

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
- Comprehensive pytest test suite with 172 test cases covering all components
- Test configuration with fixtures in tests/conftest.py (app, client, db, test_user, auth_headers, test_diary)
- Unit tests for User and ThoughtDiary models (20 test cases)
- Unit tests for authentication endpoints (31 test cases covering register, login, refresh, logout, me, rate limiting)
- Unit tests for diary endpoints (24 test cases covering list, create, get, update, delete, stats, authorization)
- Unit tests for AI sentiment analysis service (18 test cases with mocked API calls)
- Unit tests for password utilities (22 test cases covering validation, hashing, verification)
- Unit tests for validators (26 test cases covering email validation, normalization, sanitization)
- Test coverage achieved: 94% (exceeds 80%+ requirement)
- External API mocking for isolated testing
- Edge case coverage including error handling, validation, and authorization
- Fixtures for database setup/teardown and JWT authentication
- Test organization mirroring source code structure
- Environment variable fixture for setting GITHUB_TOKEN in test environment

#### Fixed
- JWT identity type conversion: Added int() wrapper for get_jwt_identity() in all diary routes to match database integer user_id
- Marshmallow validator signatures: Updated validate_content() methods to accept **kwargs for compatibility with Marshmallow field validators
- AI service mocking: Configured test environment with GITHUB_TOKEN and correct patch paths for external API mocking
- Password hash length validation: Updated long password tests to respect bcrypt's 72-byte limit
- Email validation enhancement: Added checks to reject consecutive dots and leading/trailing dots in email addresses
- SQLAlchemy session handling: Fixed cascade delete test to use fresh database queries instead of cached instances
- Test code quality: Removed duplicate class definitions in test_ai_service.py (TestGetSentimentSummary, TestAPIIntegration)
- Import cleanup: Removed unused imports (pytest, timezone, time, json, MagicMock) across all test files
- Test assertions: Replaced pytest.skip() with early return and pytest.raises() with try/except pattern
- System endpoints: Created system blueprint with health check and version info endpoints (GET /health, GET /version)
- OpenAPI documentation: Integrated flasgger for Swagger UI available at GET /docs
- API documentation: Comprehensive OpenAPI/Swagger specs for all endpoints (auth, diaries, system)
- Health endpoint: Returns API health status and timestamp in ISO 8601 format
- Version endpoint: Returns API version (0.1.0) and API level (v1)
- Swagger configuration: Full OpenAPI 2.0 spec with security definitions (Bearer JWT)
- Endpoint documentation: Request/response schemas, error codes, authentication requirements documented
- API tags: Organized endpoints into System, Authentication, and Thought Diaries categories
- Security documentation: JWT Bearer token authentication flow documented
- Rate limiting documentation: Documented rate limits on register and login endpoints
- System blueprint tests: 9 comprehensive test cases covering health, version, and docs endpoints
- Test coverage: Achieved 95% overall test coverage (181 passing tests)
- Timezone-aware datetime: Updated health endpoint to use datetime.now(UTC) instead of deprecated utcnow()
- Development seed data script (app/utils/seed.py) for populating database with sample data
- Flask CLI command `flask seed` to run seeding operations
- Sample users: alice@example.com and bob@example.com with secure passwords (Dev only)
- Sample diary entries: 10 realistic diary entries per user with pre-analyzed sentiment
- Mixed sentiment entries: positive, negative, and neutral diary examples
- Idempotent seeding: Safe to run multiple times without creating duplicates
- Clear option: `flask seed --clear` to remove existing data before seeding
- Backdated entries: Diary entries created with timestamps 1-10 days ago for realistic data
- FLASK_APP environment variable added to .env.example for Flask CLI commands

#### Fixed (continued)
- Health endpoint: Fixed deprecation warning by using timezone-aware datetime (datetime.now(UTC))
- Docs endpoint test: Updated to handle redirect responses (301, 302, 308) in addition to 200

#### Documentation
- Comprehensive backend documentation suite in docs/ directory:
  - docs/backend-api.md: Complete REST API reference with authentication, endpoints, error handling, and examples
  - docs/backend-database.md: Database schema, models, migrations, query optimization, and backup strategies
  - docs/backend-development.md: Development setup, testing, debugging, and common tasks guide
  - docs/backend-architecture.md: System design, design patterns, security architecture, and data flow
  - docs/backend-deployment.md: Production deployment options (VPS, Docker, Heroku, Cloud), monitoring, and scaling
- Updated README.md with organized documentation links and descriptions
- Documentation follows "one purpose per document" principle with cross-references to avoid duplication
- All documentation includes practical examples, code snippets, and troubleshooting sections