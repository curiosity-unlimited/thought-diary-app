# Backend API Implementation Plan

**Objective**: Build a complete Flask REST API for the Thought Diary application from scratch, including JWT authentication, thought diary CRUD operations, AI sentiment analysis integration, and comprehensive pytest unit tests achieving 80%+ coverage.

**Date**: January 6, 2026

---

## Step 1: Set up Flask Application Infrastructure

### Tasks

1. Install all required dependencies via `uv add`:
   - Core: `flask`, `flask-sqlalchemy`, `flask-migrate`, `flask-marshmallow`, `marshmallow-sqlalchemy`
   - Auth/Security: `flask-jwt-extended`, `flask-limiter`, `bcrypt`, `flask-cors`
   - AI Integration: `requests`
   - Production: `gunicorn`, `redis`
   - Development: `python-dotenv`
   - Testing: `pytest`, `pytest-cov`, `pytest-flask`

2. Create `config.py` with environment-based configurations:
   - Development, Testing, Production config classes
   - JWT token expiration settings (15min access, 7 days refresh)
   - Database URI configuration (SQLite dev, PostgreSQL prod)
   - CORS origins (allow `http://localhost:5173` for Vite)
   - Rate limiting configuration
   - GitHub Models API settings

3. Implement application factory in `app/__init__.py`:
   - `create_app()` function with config parameter
   - Blueprint registration (auth, diaries, system)
   - CORS configuration for specific localhost ports
   - Error handlers for consistent error format
   - Extension initialization

4. Initialize extensions in `app/extensions.py`:
   - SQLAlchemy instance
   - Migrate instance
   - Marshmallow instance
   - JWT Manager instance
   - Limiter instance
   - CORS instance

5. Create `.env.example` with required environment variables:
   - `FLASK_ENV=development`
   - `SECRET_KEY=your-secret-key-here`
   - `JWT_SECRET_KEY=your-jwt-secret-key-here`
   - `DATABASE_URL=sqlite:///dev.db`
   - `GITHUB_TOKEN=your-github-token-here`
   - `GITHUB_MODEL_NAME=gpt-4o`
   - `CORS_ORIGINS=http://localhost:5173`
   - `REDIS_URL=redis://localhost:6379/0` (optional for dev)

6. Update `main.py` with Flask app entry point

### Checklist

- [ ] All dependencies installed via `uv add`
- [ ] `pyproject.toml` updated with all dependencies
- [ ] `config.py` created with Dev/Test/Prod classes
- [ ] JWT expiration configured (15min access, 7 days refresh)
- [ ] `app/__init__.py` implements application factory pattern
- [ ] CORS configured for `http://localhost:5173`
- [ ] Consistent error format handler: `{"error": "message", "code": "ERROR_CODE"}`
- [ ] `app/extensions.py` initializes all extensions
- [ ] `.env.example` created with all required variables
- [ ] `GITHUB_MODEL_NAME=gpt-4o` set in `.env.example`
- [ ] `main.py` updated as Flask entry point
- [ ] App starts successfully with `uv run flask run`

---

## Step 2: Implement Database Models and Migrations

### Tasks

1. Create `User` model in `app/models/user.py`:
   - Fields: `id`, `email` (unique, indexed), `password_hash`, `created_at`, `updated_at`
   - Email validation method
   - Password hashing method using bcrypt
   - Password verification method
   - Relationship to `ThoughtDiary` (one-to-many)
   - Type hints (PEP 484)
   - Comprehensive docstrings (PEP 257)

2. Create `ThoughtDiary` model in `app/models/thought_diary.py`:
   - Fields: `id`, `user_id` (foreign key), `content`, `analyzed_content`, `positive_count`, `negative_count`, `created_at`, `updated_at`
   - Relationship to `User` (many-to-one)
   - Validation methods for content
   - Type hints and docstrings

3. Create `app/models/__init__.py` to export models

4. Set up Flask-Migrate:
   - Run `uv run flask db init` to create migrations directory
   - Generate initial migration with `uv run flask db migrate -m "Initial migration"`
   - Apply migration with `uv run flask db upgrade`

### Checklist

- [ ] `app/models/user.py` created with all fields
- [ ] User model has email validation
- [ ] User model has bcrypt password hashing/verification
- [ ] User model has relationship to ThoughtDiary
- [ ] `app/models/thought_diary.py` created with all fields
- [ ] ThoughtDiary model has user relationship
- [ ] ThoughtDiary model has sentiment count fields
- [ ] Both models have type hints (PEP 484)
- [ ] Both models have comprehensive docstrings (PEP 257)
- [ ] `app/models/__init__.py` exports both models
- [ ] Migrations directory created with `flask db init`
- [ ] Initial migration generated successfully
- [ ] Migration applied to database
- [ ] Database file created (SQLite in dev)

---

## Step 3: Build Authentication System

### Tasks

1. Implement password utilities in `app/utils/password.py`:
   - Password validation with strict rules:
     - Minimum 8 characters
     - At least one uppercase letter
     - At least one lowercase letter
     - At least one number
     - At least one special character
   - Bcrypt hashing function
   - Hash verification function
   - Type hints and docstrings

2. Implement validators in `app/utils/validators.py`:
   - Email format validation
   - Input sanitization helpers
   - Type hints and docstrings

3. Create auth schemas in `app/blueprints/auth/schemas.py`:
   - `RegisterSchema` (email, password validation)
   - `LoginSchema` (email, password)
   - `UserSchema` (serialization, excludes password_hash)
   - `TokenSchema` (access_token, refresh_token)

4. Create auth blueprint in `app/blueprints/auth/routes.py`:
   - `POST /auth/register` - User registration with validation
   - `POST /auth/login` - Login with JWT token generation
   - `POST /auth/refresh` - Refresh access token
   - `POST /auth/logout` - Token invalidation (blacklist)
   - `GET /auth/me` - Get current user profile (protected)

5. Configure JWT-Extended:
   - JWT token generation in login
   - Refresh token mechanism
   - Token blacklist for logout
   - `@jwt_required()` decorator usage

6. Implement rate limiting:
   - Register endpoint: 3 requests per hour
   - Login endpoint: 5 requests per 15 minutes

7. Ensure consistent error format:
   - All errors return: `{"error": "message", "code": "ERROR_CODE"}`
   - Standard error codes (e.g., `INVALID_CREDENTIALS`, `EMAIL_EXISTS`, etc.)

### Checklist

- [ ] `app/utils/password.py` created with strict validation
- [ ] Password requires: min 8 chars, uppercase, lowercase, number, special char
- [ ] Bcrypt hashing/verification implemented
- [ ] `app/utils/validators.py` created with email validation
- [ ] `app/blueprints/auth/schemas.py` created with all schemas
- [ ] RegisterSchema validates email and password
- [ ] UserSchema excludes password_hash
- [ ] `app/blueprints/auth/routes.py` created with all endpoints
- [ ] POST `/auth/register` implemented with validation
- [ ] POST `/auth/login` returns JWT tokens
- [ ] POST `/auth/refresh` refreshes access token
- [ ] POST `/auth/logout` invalidates tokens
- [ ] GET `/auth/me` returns current user (protected)
- [ ] JWT configured with 15min access, 7 days refresh
- [ ] Rate limiting: 3/hour on register
- [ ] Rate limiting: 5/15min on login
- [ ] All errors use consistent format: `{"error": "...", "code": "..."}`
- [ ] Auth blueprint registered in app factory

---

## Step 4: Develop AI Sentiment Analysis Service

### Tasks

1. Create `app/services/ai_service.py`:
   - Function to call GitHub Models API (gpt-4o)
   - Send diary content for sentiment analysis
   - Request HTML response with span tags for positive/negative words
   - Parse response to extract analyzed HTML content
   - Count positive markers (`<span class="positive">`)
   - Count negative markers (`<span class="negative">`)
   - Handle API errors gracefully with consistent error format
   - Support environment variables: `GITHUB_TOKEN`, `GITHUB_MODEL_NAME`
   - Type hints and comprehensive docstrings

2. Define analysis prompt/format:
   - Instruct model to identify positive and negative sentiment words
   - Return HTML with `<span class="positive">word</span>` for positive
   - Return HTML with `<span class="negative">word</span>` for negative
   - Keep neutral words unmarked

3. Error handling:
   - Catch API connection errors
   - Handle timeout scenarios
   - Return original content if analysis fails
   - Log errors appropriately

### Checklist

- [ ] `app/services/ai_service.py` created
- [ ] Function to analyze text with GitHub Models API (gpt-4o)
- [ ] Reads `GITHUB_TOKEN` from environment
- [ ] Reads `GITHUB_MODEL_NAME` from environment (gpt-4o)
- [ ] Sends appropriate prompt for sentiment analysis
- [ ] Receives HTML with positive/negative span tags
- [ ] Counts positive markers correctly
- [ ] Counts negative markers correctly
- [ ] Handles API connection errors gracefully
- [ ] Returns original content on failure
- [ ] Uses consistent error format if needed
- [ ] Type hints and docstrings present
- [ ] Ready to integrate with diary endpoints

---

## Step 5: Implement Thought Diary Endpoints

### Tasks

1. Create diary schemas in `app/blueprints/diaries/schemas.py`:
   - `DiaryCreateSchema` (content validation, max length)
   - `DiaryUpdateSchema` (content validation)
   - `DiarySchema` (serialization with analyzed_content)
   - `DiaryListSchema` (pagination metadata)
   - `DiaryStatsSchema` (total, positive, negative, neutral counts)

2. Create diaries blueprint in `app/blueprints/diaries/routes.py`:
   - `GET /diaries` - List diaries with pagination (10 per page, descending date)
   - `POST /diaries` - Create diary with AI analysis
   - `GET /diaries/<id>` - Get specific diary
   - `PUT /diaries/<id>` - Update diary with AI analysis
   - `DELETE /diaries/<id>` - Delete diary
   - `GET /diaries/stats` - Get user statistics

3. Integrate AI analysis:
   - On create: analyze content, save analyzed_content and counts
   - On update: re-analyze content, update analyzed_content and counts
   - Handle analysis failures gracefully

4. Implement pagination:
   - Default page size: 10 items
   - Sort by created_at descending
   - Return pagination metadata (page, per_page, total, pages)

5. Implement authorization:
   - All endpoints require JWT authentication (`@jwt_required()`)
   - Users can only access their own diaries
   - Return 403 if accessing another user's diary

6. Implement statistics endpoint:
   - Count total entries
   - Count positive entries (positive_count > negative_count)
   - Count negative entries (negative_count > positive_count)
   - Count neutral entries (positive_count == negative_count)

### Checklist

- [ ] `app/blueprints/diaries/schemas.py` created with all schemas
- [ ] DiaryCreateSchema validates content
- [ ] DiarySchema includes analyzed_content
- [ ] DiaryStatsSchema defined
- [ ] `app/blueprints/diaries/routes.py` created
- [ ] GET `/diaries` lists diaries with pagination
- [ ] Pagination set to 10 items per page
- [ ] Diaries sorted by created_at descending
- [ ] POST `/diaries` creates with AI analysis
- [ ] GET `/diaries/<id>` returns specific diary
- [ ] PUT `/diaries/<id>` updates with AI re-analysis
- [ ] DELETE `/diaries/<id>` deletes diary
- [ ] GET `/diaries/stats` returns statistics
- [ ] All endpoints protected with JWT
- [ ] Users can only access own diaries
- [ ] Returns 403 for unauthorized access
- [ ] AI analysis integrated on create/update
- [ ] Handles analysis failures gracefully
- [ ] Consistent error format used
- [ ] Diaries blueprint registered in app factory

---

## Step 6: Create Comprehensive Test Suite

### Tasks

1. Set up pytest configuration:
   - Create `tests/conftest.py` with fixtures:
     - `app` fixture (test app with test config)
     - `client` fixture (test client)
     - `db` fixture (database setup/teardown)
     - `test_user` fixture (creates test user)
     - `auth_headers` fixture (JWT headers)

2. Create test structure mirroring source:
   - `tests/unit/test_models.py`
   - `tests/unit/blueprints/test_auth_routes.py`
   - `tests/unit/blueprints/test_diary_routes.py`
   - `tests/unit/blueprints/test_system_routes.py`
   - `tests/unit/services/test_ai_service.py`
   - `tests/unit/utils/test_password.py`
   - `tests/unit/utils/test_validators.py`

3. Write model tests in `test_models.py`:
   - Test User model creation
   - Test password hashing/verification
   - Test email validation
   - Test User-ThoughtDiary relationship
   - Test ThoughtDiary model creation
   - Test field validations

4. Write auth endpoint tests in `test_auth_routes.py`:
   - Test POST `/auth/register` success
   - Test POST `/auth/register` with invalid email
   - Test POST `/auth/register` with weak password
   - Test POST `/auth/register` with duplicate email
   - Test POST `/auth/login` success
   - Test POST `/auth/login` with invalid credentials
   - Test POST `/auth/refresh` token refresh
   - Test POST `/auth/logout` token invalidation
   - Test GET `/auth/me` returns current user
   - Test rate limiting on register/login

5. Write diary endpoint tests in `test_diary_routes.py`:
   - Test GET `/diaries` with pagination
   - Test GET `/diaries` without auth (401)
   - Test POST `/diaries` creates diary
   - Test POST `/diaries` triggers AI analysis (mocked)
   - Test GET `/diaries/<id>` returns diary
   - Test GET `/diaries/<id>` for another user's diary (403)
   - Test PUT `/diaries/<id>` updates diary
   - Test PUT `/diaries/<id>` re-analyzes content (mocked)
   - Test DELETE `/diaries/<id>` deletes diary
   - Test GET `/diaries/stats` returns correct statistics

6. Write AI service tests in `test_ai_service.py`:
   - Mock GitHub Models API calls
   - Test successful sentiment analysis
   - Test positive/negative counting
   - Test API error handling
   - Test timeout scenarios
   - Test returns original content on failure

7. Write utility tests:
   - `test_password.py`: validation rules, hashing, verification
   - `test_validators.py`: email validation, input sanitization

8. Ensure test coverage:
   - Run `pytest --cov=app --cov-report=html`
   - Verify 80%+ coverage
   - Generate coverage report

### Checklist

- [ ] `tests/conftest.py` created with all fixtures
- [ ] App fixture with test configuration
- [ ] Client fixture for API testing
- [ ] Database fixture with setup/teardown
- [ ] Test user fixture
- [ ] Auth headers fixture with JWT
- [ ] Test directory structure mirrors source
- [ ] `tests/unit/test_models.py` created
- [ ] User model tests comprehensive
- [ ] ThoughtDiary model tests comprehensive
- [ ] `tests/unit/blueprints/test_auth_routes.py` created
- [ ] All auth endpoints tested (register, login, refresh, logout, me)
- [ ] Edge cases tested (invalid input, duplicates, rate limiting)
- [ ] `tests/unit/blueprints/test_diary_routes.py` created
- [ ] All diary endpoints tested (list, create, get, update, delete, stats)
- [ ] Pagination tested
- [ ] Authorization tested (403 for other users)
- [ ] AI analysis integration tested with mocks
- [ ] `tests/unit/services/test_ai_service.py` created
- [ ] GitHub API calls mocked
- [ ] Sentiment counting tested
- [ ] Error handling tested
- [ ] `tests/unit/utils/test_password.py` created
- [ ] Password validation rules tested
- [ ] `tests/unit/utils/test_validators.py` created
- [ ] Email validation tested
- [ ] All tests pass: `pytest`
- [ ] 80%+ test coverage achieved
- [ ] Coverage report generated

---

## Step 7: Add System Endpoints with OpenAPI

### Tasks

1. Install OpenAPI dependencies:
   - Add `flasgger` or `flask-swagger-ui` via `uv add`

2. Create system blueprint in `app/blueprints/system/routes.py`:
   - `GET /health` - Health check endpoint
     - Returns: `{"status": "healthy", "timestamp": "..."}`
   - `GET /version` - API version information
     - Returns: `{"version": "1.0.0", "api": "v1"}`
   - `GET /docs` - OpenAPI documentation UI

3. Configure OpenAPI/Swagger:
   - Initialize Swagger in app factory
   - Configure Swagger UI route at `/docs`
   - Set API metadata (title, version, description)

4. Document all endpoints with OpenAPI specs:
   - Add docstrings with YAML specs to all route functions
   - Document request schemas
   - Document response schemas
   - Document error responses
   - Include example requests/responses
   - Document authentication requirements

5. Add comprehensive API documentation:
   - Document all auth endpoints with examples
   - Document all diary endpoints with examples
   - Document error codes and formats
   - Document rate limiting rules
   - Document authentication flow

### Checklist

- [ ] `flasgger` or `flask-swagger-ui` installed
- [ ] `app/blueprints/system/routes.py` created
- [ ] GET `/health` returns health status
- [ ] GET `/version` returns version info
- [ ] GET `/docs` serves OpenAPI documentation UI
- [ ] Swagger initialized in app factory
- [ ] API metadata configured (title, version, description)
- [ ] Auth endpoints documented with OpenAPI specs
- [ ] Diary endpoints documented with OpenAPI specs
- [ ] System endpoints documented with OpenAPI specs
- [ ] Request schemas documented
- [ ] Response schemas documented
- [ ] Error responses documented with codes
- [ ] Rate limiting documented
- [ ] Authentication flow documented
- [ ] Example requests/responses included
- [ ] System blueprint registered in app factory
- [ ] `/docs` accessible in browser

---

## Step 8: Create Development Seed Data

### Tasks

1. Create seed script in `app/utils/seed.py` or `scripts/seed_data.py`:
   - Create sample users with hashed passwords
   - Create thought diary entries for each user
   - Include analyzed content with positive/negative spans
   - Set appropriate positive/negative counts
   - Use realistic diary content examples

2. Implement seeding functionality:
   - Function to clear existing data (optional)
   - Function to create sample users
   - Function to create sample diaries
   - Main function to run all seeding
   - Make it idempotent (can run multiple times safely)

3. Create sample data:
   - At least 2 test users with simple passwords (for dev only)
   - At least 5-10 diary entries per user
   - Mix of positive, negative, and neutral entries
   - Realistic diary content examples

4. Add Flask CLI command:
   - Register custom command: `flask seed`
   - Run with: `uv run flask seed`

### Checklist

- [ ] Seed script created (`app/utils/seed.py` or `scripts/seed_data.py`)
- [ ] Function to clear existing data
- [ ] Function to create sample users
- [ ] Sample users have bcrypt hashed passwords
- [ ] Function to create sample diaries
- [ ] Sample diaries have analyzed_content with spans
- [ ] Sample diaries have correct positive/negative counts
- [ ] Mix of positive, negative, neutral entries
- [ ] Realistic diary content used
- [ ] Seed script is idempotent
- [ ] Flask CLI command registered: `flask seed`
- [ ] Command runs successfully: `uv run flask seed`
- [ ] Database populated with sample data
- [ ] Sample data viewable via API

---

## Final Verification Checklist

### Application Structure
- [ ] Directory structure matches plan
- [ ] All modules properly organized
- [ ] All `__init__.py` files present
- [ ] Imports work correctly

### Configuration & Environment
- [ ] `.env.example` complete and accurate
- [ ] Configuration classes working (dev/test/prod)
- [ ] JWT expiration configured correctly
- [ ] CORS configured for `http://localhost:5173`
- [ ] GitHub Models API configured with gpt-4o

### Database
- [ ] Migrations directory created
- [ ] Initial migration applied
- [ ] User model complete and tested
- [ ] ThoughtDiary model complete and tested
- [ ] Relationships working correctly

### Authentication
- [ ] Password validation strict (8+ chars, upper, lower, number, special)
- [ ] Bcrypt hashing working
- [ ] JWT tokens generated correctly (15min access, 7 days refresh)
- [ ] All auth endpoints functional
- [ ] Rate limiting working (3/hour register, 5/15min login)
- [ ] Error format consistent

### Thought Diaries
- [ ] All diary endpoints functional
- [ ] Pagination working (10 per page, descending date)
- [ ] AI sentiment analysis working
- [ ] Positive/negative counting accurate
- [ ] Authorization working (users can't access others' diaries)
- [ ] Statistics endpoint accurate

### Testing
- [ ] All tests pass
- [ ] 80%+ test coverage achieved
- [ ] External APIs mocked
- [ ] Edge cases covered

### Documentation
- [ ] OpenAPI documentation accessible at `/docs`
- [ ] All endpoints documented
- [ ] Request/response schemas documented
- [ ] Error codes documented
- [ ] Examples included

### Development Experience
- [ ] Seed data script working
- [ ] Sample data useful for testing
- [ ] App runs without errors: `uv run flask run`
- [ ] Health endpoint responds: `GET /health`
- [ ] Can register, login, create diary via API

### Code Quality
- [ ] Type hints present (PEP 484)
- [ ] Docstrings comprehensive (PEP 257)
- [ ] PEP 8 style followed
- [ ] Code readable and maintainable
- [ ] Error handling comprehensive
- [ ] No hardcoded secrets

### Documentation Updates
- [ ] Update [CHANGELOG.md](../../CHANGELOG.md) with backend implementation
- [ ] Follow Keep a Changelog format
- [ ] Include version numbers and date
- [ ] List all added features

---

## Implementation Notes

### Key Decisions
- **JWT Expiration**: 15 minutes for access tokens, 7 days for refresh tokens
- **Password Policy**: Strict requirements (min 8 chars, uppercase, lowercase, number, special char)
- **Pagination**: 10 items per page for diary listings
- **Error Format**: Consistent JSON structure: `{"error": "message", "code": "ERROR_CODE"}`
- **CORS**: Restricted to `http://localhost:5173` for development
- **AI Model**: GitHub Models API with gpt-4o for sentiment analysis
- **OpenAPI**: Use flasgger or flask-swagger-ui for documentation

### Environment Variables Required
- `FLASK_ENV`: development/testing/production
- `SECRET_KEY`: Application secret key
- `JWT_SECRET_KEY`: JWT signing key
- `DATABASE_URL`: Database connection string
- `GITHUB_TOKEN`: GitHub API token for model inference
- `GITHUB_MODEL_NAME`: gpt-4o
- `CORS_ORIGINS`: http://localhost:5173
- `REDIS_URL`: Optional for production rate limiting

### Testing Strategy
- Use pytest with fixtures for setup/teardown
- Mock external APIs (GitHub Models)
- Test all endpoints with valid and invalid inputs
- Test authorization and authentication
- Test edge cases and error handling
- Achieve 80%+ code coverage

### Deployment Considerations
- SQLite for development
- PostgreSQL for production (future)
- Redis for production rate limiting (future)
- Gunicorn as production server (future)
- Security headers and HTTPS enforcement (future)

---

## Success Criteria

✅ Backend API fully functional with all endpoints
✅ Authentication working with JWT (15min/7day expiration)
✅ Thought diary CRUD operations complete
✅ AI sentiment analysis integrated with gpt-4o
✅ Pagination working (10 per page, descending date)
✅ Rate limiting enforced on auth endpoints
✅ Comprehensive test suite with 80%+ coverage
✅ OpenAPI documentation accessible at `/docs`
✅ Seed data script for development testing
✅ Consistent error format across all endpoints
✅ Strict password validation implemented
✅ CORS configured for specific localhost port
✅ All code follows PEP 8, PEP 257, PEP 484
✅ CHANGELOG.md updated with implementation details
