# Backend Development Guide

This guide covers setting up your development environment and working with the Thought Diary backend. For deployment, see [Backend Deployment](backend-deployment.md).

## Prerequisites

Ensure you have the following installed:

- **Python 3.13+**: [Download Python](https://www.python.org/downloads/)
- **uv**: Python project manager
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Git**: For version control
- **SQLite**: Included with Python (for development)
- **Redis** (optional): For rate limiting in development
  ```bash
  # macOS
  brew install redis
  
  # Ubuntu/Debian
  sudo apt install redis-server
  
  # Run Redis
  redis-server
  ```

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR-USERNAME/thought-diary-app.git
cd thought-diary-app/backend
```

### 2. Install Dependencies

```bash
# Install all dependencies using uv
uv sync

# Or install specific dependency
uv add <package-name>
```

Dependencies are managed in `pyproject.toml` and locked in `uv.lock`.

### 3. Environment Configuration

Create `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Flask configuration
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database (SQLite for development)
DATABASE_URL=sqlite:///dev.db

# GitHub Models API (required for sentiment analysis)
GITHUB_TOKEN=your-github-token-here
GITHUB_MODEL_NAME=gpt-4o

# CORS (frontend URL)
CORS_ORIGINS=http://localhost:5173

# Redis (optional for development)
REDIS_URL=redis://localhost:6379/0
```

**Getting GitHub Token**:
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`
4. Copy token to `.env`

### 4. Initialize Database

```bash
# Apply database migrations
uv run flask db upgrade

# (Optional) Seed with sample data
uv run flask seed
```

### 5. Run Development Server

```bash
# Run Flask development server with debug mode
uv run flask --debug run

# Server starts at http://localhost:5000
```

---

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── config.py              # Configuration classes
├── pyproject.toml         # Dependencies and project metadata
├── uv.lock                # Dependency lock file
├── .env                   # Environment variables (not in git)
├── .env.example           # Environment template
│
├── app/                   # Application package
│   ├── __init__.py        # Application factory
│   ├── extensions.py      # Flask extensions initialization
│   │
│   ├── blueprints/        # API endpoints organized by feature
│   │   ├── auth/          # Authentication endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── diaries/       # Thought diary endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   └── system/        # System endpoints (health, version)
│   │       ├── __init__.py
│   │       └── routes.py
│   │
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   ├── user.py        # User model
│   │   └── thought_diary.py  # ThoughtDiary model
│   │
│   ├── services/          # Business logic and external services
│   │   ├── __init__.py
│   │   └── ai_service.py  # GitHub Models AI integration
│   │
│   └── utils/             # Helper functions
│       ├── __init__.py
│       ├── password.py    # Password validation and hashing
│       ├── validators.py  # Input validation
│       └── seed.py        # Development seed data
│
├── migrations/            # Database migration files
│   ├── alembic.ini
│   ├── env.py
│   └── versions/          # Migration version files
│
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest configuration and fixtures
│   └── unit/              # Unit tests (mirrors app structure)
│       ├── blueprints/
│       ├── services/
│       ├── utils/
│       └── test_models.py
│
└── instance/              # Instance-specific files (not in git)
    └── dev.db             # SQLite database file
```

---

## Development Workflow

### Running the Application

**Development server** (with auto-reload):
```bash
cd backend
uv run flask --debug run
```

**Production-like server** (with Gunicorn):
```bash
cd backend
uv run gunicorn -b 0.0.0.0:5000 -w 4 "app:create_app()"
```

**Custom host/port**:
```bash
uv run flask --debug run --host 0.0.0.0 --port 8000
```

### Environment Variables

The app uses environment-specific configurations:

- **Development**: `FLASK_ENV=development` (default)
  - Debug mode enabled
  - SQLite database
  - Auto-reload on code changes
  - Relaxed CORS

- **Testing**: `FLASK_ENV=testing`
  - In-memory database
  - Rate limiting disabled
  - Fast token expiration

- **Production**: `FLASK_ENV=production`
  - Debug disabled
  - PostgreSQL database
  - Redis required
  - Strict security headers

### Flask CLI Commands

**Database commands**:
```bash
uv run flask db init         # Initialize migrations (one-time)
uv run flask db migrate -m "Description"  # Create migration
uv run flask db upgrade      # Apply migrations
uv run flask db downgrade    # Rollback migration
uv run flask db current      # Show current revision
uv run flask db history      # Show migration history
```

**Seed data commands**:
```bash
uv run flask seed            # Add sample data
uv run flask seed --clear    # Clear all data first
```

**Custom commands** (create in `app/cli.py`):
```python
@app.cli.command()
def custom_command():
    """Custom Flask CLI command."""
    click.echo("Running custom command")
```

---

## Testing

### Running Tests

**Run all tests**:
```bash
cd backend
uv run pytest
```

**Run with coverage**:
```bash
uv run pytest --cov=app --cov-report=html --cov-report=term
```

**Run specific test file**:
```bash
uv run pytest tests/unit/test_models.py
```

**Run specific test**:
```bash
uv run pytest tests/unit/test_models.py::TestUserModel::test_create_user
```

**Run with verbose output**:
```bash
uv run pytest -v
```

**Run and stop on first failure**:
```bash
uv run pytest -x
```

### Test Coverage

View coverage report:
```bash
# Generate HTML report
uv run pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Coverage requirements**: Maintain 80%+ test coverage.

### Test Structure

Tests mirror the application structure:

```
tests/
├── conftest.py              # Shared fixtures
└── unit/
    ├── blueprints/
    │   ├── test_auth_routes.py
    │   ├── test_diary_routes.py
    │   └── test_system_routes.py
    ├── services/
    │   └── test_ai_service.py
    ├── utils/
    │   ├── test_password.py
    │   └── test_validators.py
    └── test_models.py
```

### Writing Tests

**Example test file**:

```python
"""Tests for User model."""

import pytest
from app.models import User
from app.extensions import db


class TestUserModel:
    """Test cases for User model."""
    
    def test_create_user(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User(email="test@example.com")
            user.set_password("Test1234!")
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.email == "test@example.com"
            assert user.check_password("Test1234!")
    
    def test_invalid_email(self, app):
        """Test email validation."""
        assert not User.validate_email("invalid-email")
        assert User.validate_email("valid@example.com")
```

**Using fixtures** (from `conftest.py`):

```python
def test_authenticated_request(client, auth_headers):
    """Test endpoint with authentication."""
    response = client.get('/auth/me', headers=auth_headers)
    assert response.status_code == 200
```

**Mocking external services**:

```python
from unittest.mock import patch, MagicMock

def test_ai_service(monkeypatch):
    """Test AI service with mocked API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Analyzed text"}}]
    }
    mock_response.status_code = 200
    
    with patch('requests.post', return_value=mock_response):
        result = analyze_sentiment("Test content")
        assert result is not None
```

### Test Fixtures

Common fixtures in `conftest.py`:

- `app`: Flask application instance
- `client`: Test client for making requests
- `db`: Database instance
- `test_user`: Sample user for testing
- `auth_headers`: JWT authentication headers
- `test_diary`: Sample diary entry

---

## Database Management

### Migrations

**Create migration after model changes**:
```bash
uv run flask db migrate -m "Add new field to User model"
```

**Review generated migration** in `migrations/versions/`:
```python
def upgrade():
    # Review auto-generated changes
    op.add_column('users', sa.Column('new_field', sa.String(50)))

def downgrade():
    op.drop_column('users', 'new_field')
```

**Apply migration**:
```bash
uv run flask db upgrade
```

**Rollback if needed**:
```bash
uv run flask db downgrade
```

### Working with Database

**Interactive Python shell** with app context:
```bash
cd backend
uv run flask shell
```

In the shell:
```python
>>> from app.models import User, ThoughtDiary
>>> from app.extensions import db

>>> # Create user
>>> user = User(email="test@example.com")
>>> user.set_password("Test1234!")
>>> db.session.add(user)
>>> db.session.commit()

>>> # Query users
>>> users = User.query.all()
>>> user = User.query.filter_by(email="test@example.com").first()

>>> # Create diary
>>> diary = ThoughtDiary(user_id=user.id, content="Test diary")
>>> db.session.add(diary)
>>> db.session.commit()

>>> # Query diaries
>>> diaries = user.thought_diaries.all()
```

### Resetting Database

**Development**:
```bash
# Delete database file
rm backend/instance/dev.db

# Recreate with migrations
uv run flask db upgrade

# Add seed data
uv run flask seed
```

**Testing**: Automatic reset between test sessions.

---

## Debugging

### Debug Mode

Enable debug mode in `.env`:
```env
FLASK_ENV=development
```

Or run with `--debug` flag:
```bash
uv run flask --debug run
```

**Features**:
- Auto-reload on code changes
- Interactive debugger on errors
- Detailed error pages

### Logging

Configure logging in `config.py`:

```python
import logging

# Set log level
logging.basicConfig(level=logging.DEBUG)

# In your code
from flask import current_app

current_app.logger.debug("Debug message")
current_app.logger.info("Info message")
current_app.logger.warning("Warning message")
current_app.logger.error("Error message")
```

### SQL Query Logging

Enable in `config.py`:
```python
SQLALCHEMY_ECHO = True  # Print all SQL queries
```

### Using Python Debugger

Add breakpoint in code:
```python
import pdb; pdb.set_trace()  # Python 3.6+
# Or
breakpoint()  # Python 3.7+
```

Debug commands:
- `n` (next): Execute next line
- `s` (step): Step into function
- `c` (continue): Continue execution
- `l` (list): Show current code
- `p variable`: Print variable value
- `q` (quit): Exit debugger

### API Testing

**Using cURL**:
```bash
# Health check
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}'

# List diaries (replace TOKEN)
curl http://localhost:5000/diaries \
  -H "Authorization: Bearer TOKEN"
```

**Using Bruno**:
1. Install Bruno API client
2. Create new collection
3. Add requests for each endpoint
4. Configure environment variables
5. Test API interactively

**Using Swagger UI**:
1. Start development server
2. Open http://localhost:5000/docs
3. Click "Authorize" and enter JWT token
4. Test endpoints interactively

---

## Code Style and Quality

### Code Formatting

**PEP 8 compliance**:
- 4 spaces for indentation
- Max line length: 100 characters
- 2 blank lines between top-level definitions
- 1 blank line between method definitions

**Type hints** (PEP 484):
```python
from typing import Optional, List, Dict

def get_user(user_id: int) -> Optional[User]:
    """Get user by ID."""
    return User.query.get(user_id)
```

**Docstrings** (PEP 257):
```python
def validate_email(email: str) -> bool:
    """Validate email format using regex pattern.
    
    Args:
        email: Email address to validate.
        
    Returns:
        True if email format is valid, False otherwise.
        
    Example:
        >>> validate_email("user@example.com")
        True
    """
    # Implementation
```

### Linting and Formatting Tools

**Install development tools**:
```bash
uv add --dev ruff black mypy
```

**Run linter** (Ruff):
```bash
uv run ruff check app tests
```

**Format code** (Black):
```bash
uv run black app tests
```

**Type checking** (mypy):
```bash
uv run mypy app
```

**Configure in `pyproject.toml`**:
```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.black]
line-length = 100
target-version = ['py313']

[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
```

---

## Common Tasks

### Adding a New Endpoint

1. **Create route in blueprint**:
```python
# app/blueprints/diaries/routes.py
@bp.route('/diaries/search', methods=['GET'])
@jwt_required()
def search_diaries():
    """Search diary entries."""
    query = request.args.get('q', '')
    # Implementation
    return jsonify(results)
```

2. **Add schema** (if needed):
```python
# app/blueprints/diaries/schemas.py
class SearchSchema(Schema):
    query = fields.Str(required=True, validate=validate.Length(min=1))
```

3. **Add tests**:
```python
# tests/unit/blueprints/test_diary_routes.py
def test_search_diaries(client, auth_headers):
    """Test diary search endpoint."""
    response = client.get('/diaries/search?q=happy', headers=auth_headers)
    assert response.status_code == 200
```

4. **Update documentation** in [backend-api.md](backend-api.md)

### Adding a New Model

1. **Create model file**:
```python
# app/models/new_model.py
from app.extensions import db
from datetime import datetime, timezone

class NewModel(db.Model):
    __tablename__ = 'new_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

2. **Import in models/__init__.py**:
```python
from .new_model import NewModel
```

3. **Create migration**:
```bash
uv run flask db migrate -m "Add NewModel"
uv run flask db upgrade
```

4. **Add tests**:
```python
# tests/unit/test_models.py
def test_new_model(app):
    """Test NewModel creation."""
    with app.app_context():
        model = NewModel(name="Test")
        db.session.add(model)
        db.session.commit()
        assert model.id is not None
```

### Adding a New Service

1. **Create service file**:
```python
# app/services/new_service.py
from typing import Optional

def process_data(data: str) -> Optional[str]:
    """Process data and return result."""
    # Implementation
    return processed_data
```

2. **Import in services/__init__.py**:
```python
from .new_service import process_data
```

3. **Add tests**:
```python
# tests/unit/services/test_new_service.py
from app.services.new_service import process_data

def test_process_data():
    """Test data processing."""
    result = process_data("input")
    assert result == "expected output"
```

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'app'`
```
Solution: Ensure you're in the backend directory and run with uv:
cd backend
uv run flask run
```

**Issue**: `Database is locked` (SQLite)
```
Solution: Close all database connections or delete dev.db and recreate:
rm instance/dev.db
uv run flask db upgrade
```

**Issue**: Migration conflicts
```
Solution: Check migration history and resolve conflicts:
uv run flask db history
uv run flask db heads
```

**Issue**: JWT token errors
```
Solution: Ensure JWT_SECRET_KEY is set in .env and consistent across requests
```

**Issue**: CORS errors
```
Solution: Check CORS_ORIGINS in .env matches frontend URL:
CORS_ORIGINS=http://localhost:5173
```

**Issue**: Import errors
```
Solution: Ensure virtual environment is activated or use uv run:
uv run python -c "import app; print('OK')"
```

---

## Best Practices

### Security

- Never commit `.env` file to version control
- Use strong, unique SECRET_KEY and JWT_SECRET_KEY in production
- Validate and sanitize all user inputs
- Use parameterized queries (SQLAlchemy handles this)
- Keep dependencies updated: `uv sync --upgrade`

### Performance

- Use database indexes on frequently queried fields
- Implement pagination for large result sets
- Cache expensive computations
- Use connection pooling in production
- Monitor query performance with SQLALCHEMY_ECHO

### Code Organization

- Keep routes thin, move logic to services
- Use blueprints to organize related endpoints
- Write self-documenting code with clear names
- Add type hints for better IDE support
- Write comprehensive docstrings

### Testing

- Write tests before or alongside code (TDD)
- Aim for 80%+ test coverage
- Test edge cases and error conditions
- Mock external services (GitHub API, etc.)
- Use fixtures to reduce test duplication

---

## Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)

### Related Project Docs
- [Backend API](backend-api.md)
- [Backend Database](backend-database.md)
- [Backend Architecture](backend-architecture.md)
- [Backend Deployment](backend-deployment.md)

### Getting Help

- Check existing tests for examples
- Review Flask documentation
- Search GitHub issues
- Ask in project discussions
