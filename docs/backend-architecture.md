# Backend Architecture Documentation

This document describes the architecture and design patterns of the Thought Diary backend application. For API usage, see [Backend API](backend-api.md).

## Overview

The backend is built using Flask with a modular, scalable architecture following industry best practices. The application uses the **Application Factory Pattern** for configuration flexibility and **Blueprint Pattern** for feature organization.

### Key Architectural Principles

1. **Separation of Concerns**: Clear boundaries between routes, business logic, data access, and utilities
2. **Modularity**: Features organized as blueprints with independent routes, schemas, and logic
3. **Scalability**: Stateless design with database-backed sessions, ready for horizontal scaling
4. **Testability**: Dependency injection and factory pattern enable comprehensive testing
5. **Security**: Defense in depth with JWT, rate limiting, CORS, input validation, and secure headers

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                          │
│  (Frontend Vue App, Mobile Apps, Third-party Clients)      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Rate Limiting (Flask-Limiter + Redis)               │  │
│  │  CORS (Flask-CORS)                                   │  │
│  │  Security Headers                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer (Flask)                  │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Auth     │  │  Diaries   │  │   System   │           │
│  │ Blueprint  │  │ Blueprint  │  │ Blueprint  │           │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘           │
│         │               │               │                   │
│         ▼               ▼               ▼                   │
│  ┌──────────────────────────────────────────────┐          │
│  │         Route Handlers & Schemas             │          │
│  │  (Request Validation, Response Serialization)│          │
│  └──────────────────┬───────────────────────────┘          │
│                     │                                       │
│                     ▼                                       │
│  ┌──────────────────────────────────────────────┐          │
│  │          Business Logic Layer                │          │
│  │  ┌──────────────┐  ┌──────────────┐         │          │
│  │  │ AI Service   │  │  Utilities   │         │          │
│  │  │ (Sentiment)  │  │  (Password,  │         │          │
│  │  │              │  │  Validators) │         │          │
│  │  └──────────────┘  └──────────────┘         │          │
│  └──────────────────┬───────────────────────────┘          │
│                     │                                       │
│                     ▼                                       │
│  ┌──────────────────────────────────────────────┐          │
│  │         Data Access Layer (ORM)              │          │
│  │  ┌──────────────┐  ┌──────────────┐         │          │
│  │  │ User Model   │  │ ThoughtDiary │         │          │
│  │  │              │  │    Model     │         │          │
│  │  └──────────────┘  └──────────────┘         │          │
│  └──────────────────┬───────────────────────────┘          │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Database    │  │    Redis     │  │   GitHub     │     │
│  │ (SQLite/     │  │ (Rate Limit  │  │   Models     │     │
│  │  PostgreSQL) │  │  Storage)    │  │     API      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Design Patterns

### 1. Application Factory Pattern

**Purpose**: Create multiple Flask app instances with different configurations (dev, test, prod).

**Implementation**: [app/__init__.py](../backend/app/__init__.py)

```python
def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure Flask application instance.
    
    Args:
        config_name: 'development', 'testing', or 'production'
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # ... more extensions
    
    # Register blueprints
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
```

**Benefits**:
- Separate configurations for different environments
- Easy to test with different settings
- Avoid global state issues
- Multiple app instances in same process

### 2. Blueprint Pattern

**Purpose**: Organize related routes and views into modular components.

**Implementation**: [app/blueprints/](../backend/app/blueprints/)

```python
# app/blueprints/auth/__init__.py
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.blueprints.auth import routes

# app/blueprints/auth/routes.py
from app.blueprints.auth import bp

@bp.route('/register', methods=['POST'])
def register():
    """Register new user."""
    # Implementation
```

**Blueprints**:
- `auth`: Authentication endpoints (/auth/register, /auth/login, etc.)
- `diaries`: Thought diary CRUD operations (/diaries/*)
- `system`: System endpoints (/health, /version, /docs)

**Benefits**:
- Modular code organization
- Easy to add/remove features
- Clear separation of concerns
- Can be developed independently

### 3. Repository Pattern (via ORM)

**Purpose**: Abstract data access logic from business logic.

**Implementation**: SQLAlchemy models act as repositories

```python
# Data access through model class methods
user = User.query.filter_by(email=email).first()
diaries = ThoughtDiary.query.filter_by(user_id=user_id).all()

# Business logic in separate layer
from app.services.ai_service import analyze_sentiment
analyzed = analyze_sentiment(diary.content)
```

**Benefits**:
- Database-agnostic business logic
- Easy to swap database implementations
- Simplified testing with mock repositories

### 4. Dependency Injection

**Purpose**: Inject dependencies rather than creating them internally.

**Implementation**: Flask extensions initialized separately

```python
# app/extensions.py
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Injected into app in factory
def create_app(config_name):
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
```

**Benefits**:
- Easier unit testing with mocks
- Flexible configuration
- Loose coupling between components

### 5. Schema Validation Pattern

**Purpose**: Validate and serialize request/response data.

**Implementation**: Marshmallow schemas

```python
# app/blueprints/auth/schemas.py
class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

# Usage in route
schema = RegisterSchema()
data = schema.load(request.json)  # Validates and deserializes
```

**Benefits**:
- Centralized validation logic
- Automatic error messages
- Type safety and documentation
- Consistent API responses

---

## Component Architecture

### Application Core

**File**: [app/__init__.py](../backend/app/__init__.py)

**Responsibilities**:
- Create Flask application instance
- Load configuration
- Initialize extensions (database, JWT, CORS, etc.)
- Register blueprints
- Configure error handlers
- Setup JWT callbacks
- Configure OpenAPI/Swagger documentation

**Key Functions**:
- `create_app(config_name)`: Application factory
- `configure_jwt_callbacks(app)`: Setup JWT handlers

**CORS Configuration**:
```python
# Enhanced CORS setup for preflight requests
cors.init_app(
    app,
    origins=cors_origins,
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
```
- Explicitly allows Content-Type and Authorization headers
- Supports OPTIONS method for preflight requests
- Configured origins from CORS_ORIGINS environment variable

### Configuration System

**File**: [config.py](../backend/config.py)

**Classes**:
- `Config`: Base configuration with common settings
- `DevelopmentConfig`: Development-specific settings
- `TestingConfig`: Test-specific settings
- `ProductionConfig`: Production-specific settings

**Configuration Hierarchy**:
```python
Config (base)
  ├── DevelopmentConfig
  │   - DEBUG = True
  │   - SQLALCHEMY_DATABASE_URI = sqlite:///dev.db
  │
  ├── TestingConfig
  │   - TESTING = True
  │   - SQLALCHEMY_DATABASE_URI = sqlite:///:memory:
  │   - RATELIMIT_ENABLED = False
  │
  └── ProductionConfig
      - DEBUG = False
      - SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
      - Strict security settings
```

**Environment Variables**:
- Loaded from `.env` file (development)
- Injected by platform (production)
- Validated on startup

### Extensions Layer

**File**: [app/extensions.py](../backend/app/extensions.py)

**Extensions**:
- `db`: SQLAlchemy database instance
- `migrate`: Flask-Migrate for database migrations
- `ma`: Marshmallow for serialization
- `jwt`: Flask-JWT-Extended for authentication
- `limiter`: Flask-Limiter for rate limiting
- `cors`: Flask-CORS for cross-origin requests

**Pattern**: Extensions created without app, initialized later in factory.

### Blueprints Layer

Blueprints organize features into self-contained modules.

#### Auth Blueprint

**Location**: [app/blueprints/auth/](../backend/app/blueprints/auth/)

**Files**:
- `routes.py`: Authentication endpoints
- `schemas.py`: Marshmallow validation schemas

**Endpoints**:
- `POST /auth/register`: User registration
- `POST /auth/login`: User login with JWT
- `POST /auth/refresh`: Refresh access token
- `POST /auth/logout`: Invalidate token
- `GET /auth/me`: Get current user profile

**Features**:
- Rate limiting on register (3/hour) and login (5/15min)
- Password hashing with bcrypt
- JWT token generation and validation
- Token blacklist for logout

#### Diaries Blueprint

**Location**: [app/blueprints/diaries/](../backend/app/blueprints/diaries/)

**Files**:
- `routes.py`: Diary CRUD endpoints
- `schemas.py`: Request/response schemas

**Endpoints**:
- `GET /diaries`: List user diaries (paginated)
- `POST /diaries`: Create diary with AI analysis
- `GET /diaries/<id>`: Get specific diary
- `PUT /diaries/<id>`: Update diary with re-analysis
- `DELETE /diaries/<id>`: Delete diary
- `GET /diaries/stats`: Get user statistics

**Features**:
- JWT authentication required
- Authorization checks (user can only access own diaries)
- AI sentiment analysis integration
- Pagination support

#### System Blueprint

**Location**: [app/blueprints/system/](../backend/app/blueprints/system/)

**Files**:
- `routes.py`: System endpoints

**Endpoints**:
- `GET /health`: Health check
- `GET /version`: API version info
- `GET /docs`: Swagger UI

**Features**:
- No authentication required
- Monitoring integration points

### Models Layer

**Location**: [app/models/](../backend/app/models/)

**Models**:
- `User`: Authentication and user profile
- `ThoughtDiary`: Diary entries with sentiment data

**Responsibilities**:
- Define database schema
- Provide query interfaces
- Implement model-specific logic
- Define relationships

**Key Features**:
- SQLAlchemy ORM integration
- Automatic timestamps (created_at, updated_at)
- Cascade delete (user deletion removes diaries)
- Helper methods (validation, sentiment calculation)

See [Backend Database](backend-database.md) for detailed schema documentation.

### Services Layer

**Location**: [app/services/](../backend/app/services/)

**Purpose**: Business logic and external service integration

#### AI Service

**File**: [app/services/ai_service.py](../backend/app/services/ai_service.py)

**Functions**:
- `analyze_sentiment(content: str) -> tuple`: Analyze text sentiment
- `get_sentiment_summary(positive: int, negative: int) -> str`: Classify overall sentiment

**Implementation**:
```python
def analyze_sentiment(content: str) -> tuple[str, int, int]:
    """Analyze sentiment using GitHub Models API.
    
    Args:
        content: Text to analyze
        
    Returns:
        Tuple of (analyzed_html, positive_count, negative_count)
    """
    # Call GitHub Models API
    # Parse response for sentiment markers
    # Count positive/negative phrases
    # Return marked-up HTML with counts
```

**Integration**:
- Uses GitHub Models API (gpt-4o)
- HTTP requests with timeout
- Error handling with fallback
- Logging for debugging

### Utilities Layer

**Location**: [app/utils/](../backend/app/utils/)

**Purpose**: Reusable helper functions

#### Password Utilities

**File**: [app/utils/password.py](../backend/app/utils/password.py)

**Functions**:
- `validate_password(password: str) -> tuple[bool, str]`: Validate password strength
- `hash_password(password: str) -> str`: Hash password with bcrypt
- `verify_password(password: str, hashed: str) -> bool`: Verify password

**Requirements**:
- Min 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

#### Validators

**File**: [app/utils/validators.py](../backend/app/utils/validators.py)

**Functions**:
- `validate_email_format(email: str) -> bool`: Validate email format
- `normalize_email(email: str) -> str`: Normalize email (lowercase, trim)
- `sanitize_input(text: str) -> str`: Remove dangerous characters

#### Seed Data

**File**: [app/utils/seed.py](../backend/app/utils/seed.py)

**Purpose**: Populate database with sample data for development

**Command**: `flask seed [--clear]`

**Features**:
- Creates sample users and diaries
- Idempotent (safe to run multiple times)
- Transaction-based (atomic operation)
- Optional clear before seeding

---

## Security Architecture

### Defense in Depth

Multiple layers of security controls:

1. **Transport Security**: HTTPS in production (enforced by config)
2. **Authentication**: JWT tokens with expiration
3. **Authorization**: User ownership checks on resources
4. **Rate Limiting**: Prevent brute force and DoS attacks
5. **Input Validation**: All inputs validated and sanitized
6. **Output Encoding**: XSS prevention via proper HTML handling
7. **CORS**: Restrict origins for API access
8. **Security Headers**: XSS, clickjacking, and MIME sniffing protection

### Authentication Flow

```
┌──────────┐                          ┌──────────┐
│  Client  │                          │  Server  │
└────┬─────┘                          └────┬─────┘
     │                                      │
     │  POST /auth/register                 │
     │  {email, password}                   │
     ├─────────────────────────────────────>│
     │                                      │
     │                     Hash password    │
     │                     Save to database │
     │                                      │
     │  201 Created {user}                  │
     │<─────────────────────────────────────┤
     │                                      │
     │  POST /auth/login                    │
     │  {email, password}                   │
     ├─────────────────────────────────────>│
     │                                      │
     │                     Verify password  │
     │                     Generate tokens  │
     │                                      │
     │  200 OK {access_token, refresh_token}│
     │<─────────────────────────────────────┤
     │                                      │
     │  GET /diaries                        │
     │  Authorization: Bearer <access_token>│
     ├─────────────────────────────────────>│
     │                                      │
     │                     Verify token     │
     │                     Extract user_id  │
     │                     Query diaries    │
     │                                      │
     │  200 OK {diaries}                    │
     │<─────────────────────────────────────┤
     │                                      │
     │  POST /auth/refresh                  │
     │  Authorization: Bearer <refresh_token>│
     ├─────────────────────────────────────>│
     │                                      │
     │                     Verify refresh   │
     │                     Generate new     │
     │                     access token     │
     │                                      │
     │  200 OK {access_token}               │
     │<─────────────────────────────────────┤
     │                                      │
```

### JWT Token Structure

**Access Token** (15 minutes):
```json
{
  "sub": 123,              // User ID
  "type": "access",
  "fresh": true,
  "iat": 1704980400,       // Issued at
  "exp": 1704981300,       // Expires at
  "jti": "abc123..."       // JWT ID (for blacklist)
}
```

**Refresh Token** (7 days):
```json
{
  "sub": 123,
  "type": "refresh",
  "iat": 1704980400,
  "exp": 1705585200,
  "jti": "def456..."
}
```

**Security Features**:
- Short-lived access tokens (15 min)
- Longer-lived refresh tokens (7 days)
- Token blacklist on logout
- Secure secret keys
- HS256 algorithm

### Rate Limiting Strategy

**Implementation**: Flask-Limiter with Redis backend

**Limits**:
- Register: `3 per hour` per IP
- Login: `5 per 15 minutes` per IP
- Other endpoints: No limit (authenticated by JWT)

**Storage**:
- Development: In-memory (single process)
- Production: Redis (distributed, persistent)

**Response Headers**:
```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 3
X-RateLimit-Reset: 1704981000
```

**HTTP 429 Response**:
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please try again later."
}
```

---

## Data Flow

### Create Diary Entry Flow

```
1. Client Request
   POST /diaries
   Authorization: Bearer <token>
   {
     "content": "I felt happy today!"
   }
   
2. Flask Route Handler
   - Validate JWT token
   - Extract user_id from token
   - Validate request body with DiaryCreateSchema
   
3. AI Service Layer
   - Call analyze_sentiment(content)
   - Send request to GitHub Models API
   - Parse response for sentiment markers
   - Count positive/negative phrases
   - Return (analyzed_html, positive_count, negative_count)
   
4. Data Access Layer
   - Create ThoughtDiary instance
   - Set content, analyzed_content, counts
   - Save to database via SQLAlchemy
   - Commit transaction
   
5. Response Serialization
   - Serialize diary with DiarySchema
   - Return JSON response
   
6. Client Response
   201 Created
   {
     "id": 1,
     "content": "I felt happy today!",
     "analyzed_content": "I felt <span class='positive'>happy</span> today!",
     "positive_count": 1,
     "negative_count": 0,
     "created_at": "2026-01-14T12:00:00Z",
     "updated_at": "2026-01-14T12:00:00Z"
   }
```

### Authentication Flow

See "Authentication Flow" diagram in Security Architecture section above.

---

## Error Handling

### Error Handler Architecture

**Global Error Handlers** in [app/__init__.py](../backend/app/__init__.py):

```python
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions (400, 404, 500, etc.)."""
    return jsonify({
        'error': e.name.lower().replace(' ', '_'),
        'message': e.description
    }), e.code

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle Marshmallow validation errors."""
    return jsonify({
        'error': 'validation_error',
        'message': str(e)
    }), 400
```

### JWT Error Handlers

**Configured in** `configure_jwt_callbacks()`:

- `expired_signature_callback`: Token expired
- `invalid_token_callback`: Malformed token
- `unauthorized_callback`: Token missing
- `revoked_token_callback`: Token blacklisted

### Consistent Error Format

All errors return:
```json
{
  "error": "error_code",
  "message": "Human-readable description"
}
```

---

## Testing Architecture

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
└── unit/                    # Unit tests
    ├── blueprints/          # Route tests
    ├── services/            # Service tests
    ├── utils/               # Utility tests
    └── test_models.py       # Model tests
```

### Test Fixtures

**Key Fixtures** in [tests/conftest.py](../backend/tests/conftest.py):

```python
@pytest.fixture
def app():
    """Create test application instance."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create sample user for testing."""
    user = User(email="test@example.com")
    user.set_password("Test1234!")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_headers(client, test_user):
    """Generate authentication headers with JWT."""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'Test1234!'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
```

### Test Coverage

**Current Coverage**: 95% (exceeds 80% requirement)

**Coverage by Module**:
- Models: 100%
- Blueprints: 95%
- Services: 92%
- Utils: 98%

### Mocking Strategy

**External Services Mocked**:
- GitHub Models API (in AI service tests)
- Database (in-memory SQLite for tests)
- Redis (not required in test config)

**Example Mock**:
```python
from unittest.mock import patch, MagicMock

def test_ai_service(monkeypatch):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Analyzed text"}}]
    }
    
    with patch('requests.post', return_value=mock_response):
        result = analyze_sentiment("Test")
        assert result is not None
```

---

## Performance Considerations

### Database Query Optimization

**Indexes**:
- `users.email`: Fast user lookup
- `thought_diaries.user_id`: Efficient user diary queries
- `thought_diaries.created_at`: Fast date sorting

**Pagination**:
- Default: 10 items per page
- Max: 100 items per page
- Uses LIMIT/OFFSET with indexed columns

**Lazy Loading**:
- `User.thought_diaries`: Dynamic lazy loading (returns query object)
- Prevents N+1 query problems

### Caching Strategy

**Current**: No caching implemented (stateless API)

**Future Considerations**:
- Cache AI sentiment analysis results
- Cache user statistics
- Use Redis for session cache
- Cache frequently accessed diaries

### API Response Times

**Target Response Times**:
- Authentication: < 200ms
- Diary list (paginated): < 100ms
- Diary create (with AI): < 3s
- Diary update (with AI): < 3s
- Other CRUD: < 100ms

**Bottlenecks**:
- AI sentiment analysis: 1-3s (external API call)
- Database queries: < 10ms (with indexes)
- JWT verification: < 1ms

---

## Scalability Architecture

### Horizontal Scaling

**Stateless Design**:
- No server-side sessions (JWT tokens)
- Database-backed state only
- Can run multiple instances behind load balancer

**Load Balancing**:
```
         ┌─────────────┐
         │Load Balancer│
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│App     │ │App     │ │App     │
│Instance│ │Instance│ │Instance│
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    └──────────┼──────────┘
               ▼
        ┌────────────┐
        │ PostgreSQL │
        │  (Primary) │
        └────────────┘
```

### Vertical Scaling

**Resource Requirements**:
- Small deployment: 1 CPU, 512MB RAM
- Medium deployment: 2 CPU, 1GB RAM
- Large deployment: 4+ CPU, 2GB+ RAM

**Database Connection Pooling**:
```python
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_TIMEOUT = 30
```

### Monitoring & Observability

**Health Checks**:
- `GET /health`: Liveness probe
- `GET /version`: Readiness probe

**Logging**:
- Flask built-in logging
- Configurable log levels
- Structured logging recommended

**Metrics** (future):
- Request rate
- Response times
- Error rates
- Database query performance
- Cache hit rates

---

## Extensibility

### Adding New Features

The architecture supports easy extension:

1. **New Endpoint**: Add route to existing blueprint or create new blueprint
2. **New Model**: Create model file, add migration, register in `__init__.py`
3. **New Service**: Create service file in `app/services/`
4. **New Validation**: Add Marshmallow schema in blueprint's `schemas.py`
5. **New Extension**: Initialize in `extensions.py`, configure in factory

### Integration Points

**External Service Integration**:
- Add to `app/services/`
- Use environment variables for configuration
- Implement error handling and fallbacks
- Add comprehensive tests with mocks

**Database Integration**:
- Define SQLAlchemy models
- Create migrations
- Add indexes for performance
- Implement cascade rules

**Frontend Integration**:
- RESTful JSON API
- CORS configured
- OpenAPI/Swagger documentation
- Consistent error responses

---

## Related Documentation

- [Backend API](backend-api.md) - API endpoints and usage
- [Backend Database](backend-database.md) - Database schema and operations
- [Backend Development](backend-development.md) - Development setup and workflow
- [Backend Deployment](backend-deployment.md) - Production deployment guide
