# Backend Database Documentation

This document provides comprehensive documentation for the Thought Diary application database. For API usage, see [Backend API](backend-api.md).

## Database Overview

The application uses SQLAlchemy ORM for database operations with support for multiple database backends:

- **Development**: SQLite (file-based, `dev.db`)
- **Testing**: SQLite (in-memory)
- **Production**: PostgreSQL (recommended for production)

## Database Configuration

Database settings are configured in [config.py](../backend/config.py):

```python
# Development
SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

# Testing
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Production
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐         ┌──────────────────────┐
│     User        │         │   ThoughtDiary       │
├─────────────────┤         ├──────────────────────┤
│ id (PK)         │1      ∞│ id (PK)              │
│ email (unique)  ├─────────│ user_id (FK)         │
│ password_hash   │         │ content              │
│ created_at      │         │ analyzed_content     │
│ updated_at      │         │ positive_count       │
│                 │         │ negative_count       │
│                 │         │ created_at           │
│                 │         │ updated_at           │
└─────────────────┘         └──────────────────────┘
```

**Relationship**: One User has many ThoughtDiary entries (1:∞)

---

## Models

### User Model

**Table Name**: `users`

**Purpose**: Store user authentication and profile information

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key | Unique user identifier |
| `email` | String(255) | Unique, Not Null, Indexed | User's email address |
| `password_hash` | String(255) | Not Null | Bcrypt hashed password |
| `created_at` | DateTime | Not Null, Default: UTC now | Account creation timestamp |
| `updated_at` | DateTime | Not Null, Default: UTC now, Auto-update | Last modification timestamp |

**Indexes**:
- Primary key on `id` (automatic)
- Unique index on `email` for fast lookups and uniqueness enforcement

**Relationships**:
- `thought_diaries`: One-to-many relationship with ThoughtDiary model
  - Lazy loading: `dynamic` (returns query object)
  - Cascade: `all, delete-orphan` (deleting user deletes all diaries)
  - Backref: `user` (access user from diary via `diary.user`)

**Model Methods**:

```python
@staticmethod
def validate_email(email: str) -> bool:
    """Validate email format using RFC 5322 simplified pattern."""
    
def set_password(password: str) -> None:
    """Hash password using bcrypt with generated salt."""
    
def check_password(password: str) -> bool:
    """Verify password against stored bcrypt hash."""
```

**Example Usage**:

```python
# Create new user
user = User(email="user@example.com")
user.set_password("SecurePass123!")
db.session.add(user)
db.session.commit()

# Validate credentials
if user.check_password("password"):
    print("Authentication successful")

# Access user's diaries
for diary in user.thought_diaries:
    print(diary.content)
```

**Password Security**:
- Passwords are hashed using bcrypt with auto-generated salt
- Hash uses 12 rounds by default (configurable)
- Bcrypt automatically handles salt generation and verification
- Plain text passwords are never stored

---

### ThoughtDiary Model

**Table Name**: `thought_diaries`

**Purpose**: Store user thought diary entries with AI sentiment analysis

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key | Unique diary entry identifier |
| `user_id` | Integer | Foreign Key (users.id), Not Null, Indexed | Owner of the diary entry |
| `content` | Text | Not Null | Original plain text diary content |
| `analyzed_content` | Text | Nullable | HTML content with sentiment markers |
| `positive_count` | Integer | Not Null, Default: 0 | Count of positive sentiment markers |
| `negative_count` | Integer | Not Null, Default: 0 | Count of negative sentiment markers |
| `created_at` | DateTime | Not Null, Default: UTC now, Indexed | Entry creation timestamp |
| `updated_at` | DateTime | Not Null, Default: UTC now, Auto-update | Last modification timestamp |

**Indexes**:
- Primary key on `id` (automatic)
- Index on `user_id` for efficient user diary queries
- Index on `created_at` for efficient date-based sorting

**Relationships**:
- `user`: Many-to-one relationship with User model
  - Access via `diary.user`
  - Cascade delete: If user is deleted, all their diaries are deleted

**Model Methods**:

```python
@staticmethod
def validate_content(content: str) -> bool:
    """Validate diary content (non-empty, max 10000 chars)."""
    
def get_sentiment(self) -> str:
    """Return 'positive', 'negative', or 'neutral' based on counts."""
    
def to_dict(self) -> dict:
    """Convert model instance to dictionary for JSON serialization."""
```

**Example Usage**:

```python
# Create new diary entry
diary = ThoughtDiary(
    user_id=user.id,
    content="I felt happy today!",
    analyzed_content="I felt <span class='positive'>happy</span> today!",
    positive_count=1,
    negative_count=0
)
db.session.add(diary)
db.session.commit()

# Get sentiment classification
sentiment = diary.get_sentiment()  # Returns 'positive'

# Query user's diaries
diaries = ThoughtDiary.query.filter_by(user_id=user.id)\
    .order_by(ThoughtDiary.created_at.desc())\
    .limit(10)\
    .all()
```

**Sentiment Analysis Fields**:

- `analyzed_content`: Contains HTML with sentiment markers
  ```html
  I felt <span class="positive">excited</span> and <span class="negative">anxious</span>.
  ```
- `positive_count`: Automatically calculated from `<span class="positive">` tags
- `negative_count`: Automatically calculated from `<span class="negative">` tags

**Sentiment Classification**:
- **Positive**: `positive_count > negative_count`
- **Negative**: `negative_count > positive_count`
- **Neutral**: `positive_count == negative_count`

---

## Database Migrations

The application uses Flask-Migrate (Alembic) for database schema management.

### Migration Files Location

```
backend/migrations/
├── alembic.ini          # Alembic configuration
├── env.py               # Migration environment script
├── script.py.mako       # Migration template
└── versions/            # Migration version files
    └── 3edc1c1ea583_initial_migration_add_user_and_.py
```

### Migration Commands

**Initialize migrations** (one-time setup):
```bash
cd backend
uv run flask db init
```

**Create a new migration**:
```bash
cd backend
uv run flask db migrate -m "Description of changes"
```

**Apply migrations**:
```bash
cd backend
uv run flask db upgrade
```

**Rollback last migration**:
```bash
cd backend
uv run flask db downgrade
```

**View migration history**:
```bash
cd backend
uv run flask db history
```

**View current revision**:
```bash
cd backend
uv run flask db current
```

### Initial Migration

The initial migration (`3edc1c1ea583`) creates:
- `users` table with all columns and indexes
- `thought_diaries` table with all columns and indexes
- Foreign key constraint from `thought_diaries.user_id` to `users.id`
- Cascade delete on foreign key

### Creating New Migrations

When modifying models:

1. Update the model class in `app/models/`
2. Generate migration script:
   ```bash
   uv run flask db migrate -m "Add new field to User"
   ```
3. Review generated migration in `migrations/versions/`
4. Apply migration:
   ```bash
   uv run flask db upgrade
   ```
5. Test migration with sample data
6. Commit migration file to version control

**Important**: Always review auto-generated migrations before applying them.

---

## Database Operations

### Common Queries

**Find user by email**:
```python
user = User.query.filter_by(email="user@example.com").first()
```

**Get user's diary count**:
```python
count = ThoughtDiary.query.filter_by(user_id=user_id).count()
```

**Get recent diaries with pagination**:
```python
page = 1
per_page = 10
diaries = ThoughtDiary.query\
    .filter_by(user_id=user_id)\
    .order_by(ThoughtDiary.created_at.desc())\
    .paginate(page=page, per_page=per_page, error_out=False)
```

**Get sentiment statistics**:
```python
from sqlalchemy import func

stats = db.session.query(
    func.count(ThoughtDiary.id).label('total'),
    func.sum(
        db.case((ThoughtDiary.positive_count > ThoughtDiary.negative_count, 1), else_=0)
    ).label('positive'),
    func.sum(
        db.case((ThoughtDiary.negative_count > ThoughtDiary.positive_count, 1), else_=0)
    ).label('negative')
).filter_by(user_id=user_id).first()
```

**Delete user and cascade delete diaries**:
```python
user = User.query.get(user_id)
db.session.delete(user)
db.session.commit()  # All user's diaries are automatically deleted
```

### Transaction Management

SQLAlchemy manages transactions automatically:

```python
try:
    user = User(email="test@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()  # Commit transaction
except Exception as e:
    db.session.rollback()  # Rollback on error
    raise
```

For complex operations:

```python
from app.extensions import db

with db.session.begin():
    # Multiple operations in single transaction
    user = User(email="test@example.com")
    db.session.add(user)
    db.session.flush()  # Get user.id without committing
    
    diary = ThoughtDiary(user_id=user.id, content="First entry")
    db.session.add(diary)
    # Automatic commit at end of block
```

---

## Development Seed Data

The application includes a seed data script for development.

### Seed Command

```bash
cd backend
uv run flask seed              # Add sample data
uv run flask seed --clear      # Clear all data first, then seed
```

### Sample Data Created

**Users**:
- `alice@example.com` / `Alice2024!`
- `bob@example.com` / `Bob2024!`

**Diaries**: 10 entries per user with:
- Realistic diary content
- Pre-analyzed sentiment
- Backdated timestamps (1-10 days ago)
- Mix of positive, negative, and neutral entries

### Seed Script Location

[backend/app/utils/seed.py](../backend/app/utils/seed.py)

**Features**:
- Idempotent: Safe to run multiple times
- Uses transaction for atomic operations
- Includes error handling and logging
- Can clear existing data with `--clear` flag

---

## Database Performance

### Indexing Strategy

**Existing Indexes**:
1. `users.email` - Unique index for fast user lookups
2. `thought_diaries.user_id` - For efficient user diary queries
3. `thought_diaries.created_at` - For date-based sorting

**Query Performance**:
- Email login: O(log n) via indexed email lookup
- List user diaries: O(log n) via indexed user_id + created_at
- Pagination: Efficient with LIMIT/OFFSET on indexed columns

### Connection Pooling

SQLAlchemy automatically manages connection pooling:

**Development** (SQLite):
- Single connection
- No pooling needed

**Production** (PostgreSQL):
- Configure pool size via environment variables
- Recommended settings:
  ```python
  SQLALCHEMY_POOL_SIZE = 10
  SQLALCHEMY_MAX_OVERFLOW = 20
  SQLALCHEMY_POOL_TIMEOUT = 30
  SQLALCHEMY_POOL_RECYCLE = 3600
  ```

### Query Optimization Tips

1. **Use lazy loading appropriately**:
   ```python
   # Good: Only load needed data
   user = User.query.get(user_id)
   
   # Avoid N+1 queries with eager loading
   users = User.query.options(db.joinedload(User.thought_diaries)).all()
   ```

2. **Use pagination for large result sets**:
   ```python
   # Good: Load page at a time
   diaries = ThoughtDiary.query.paginate(page=1, per_page=10)
   
   # Avoid: Loading all records
   diaries = ThoughtDiary.query.all()
   ```

3. **Select only needed columns**:
   ```python
   # Good: Select specific columns
   emails = db.session.query(User.email).all()
   
   # Avoid: Loading entire objects when not needed
   users = User.query.all()
   emails = [u.email for u in users]
   ```

---

## Database Backup and Restore

### SQLite (Development)

**Backup**:
```bash
cp backend/instance/dev.db backend/instance/dev.db.backup
```

**Restore**:
```bash
cp backend/instance/dev.db.backup backend/instance/dev.db
```

### PostgreSQL (Production)

**Backup**:
```bash
pg_dump -h localhost -U postgres thought_diary > backup.sql
```

**Restore**:
```bash
psql -h localhost -U postgres thought_diary < backup.sql
```

**Automated backups**: Configure via cron job or cloud provider backup service.

---

## Database Security

### Security Best Practices

1. **Password Storage**:
   - Never store plain text passwords
   - Use bcrypt with sufficient rounds (12+)
   - Salt is automatically included in bcrypt hash

2. **SQL Injection Prevention**:
   - Always use SQLAlchemy ORM parameterized queries
   - Never concatenate user input into raw SQL
   - Validate and sanitize all inputs

3. **Access Control**:
   - Use environment variables for database credentials
   - Never commit credentials to version control
   - Use separate credentials for development/production
   - Apply principle of least privilege for database users

4. **Sensitive Data**:
   - Email addresses are indexed but not encrypted (consider PII requirements)
   - Consider encryption at rest for production databases
   - Implement audit logging for sensitive operations

### Database User Permissions

**Development**: Full access for ease of development

**Production**: Restrict permissions:
```sql
-- Create application user with limited permissions
CREATE USER thought_diary_app WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE thought_diary TO thought_diary_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO thought_diary_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO thought_diary_app;
```

---

## Troubleshooting

### Common Issues

**Issue**: Migration conflicts
```
ERROR: Can't locate revision identified by 'abc123'
```
**Solution**: Reset migration history or manually fix version conflicts

**Issue**: Foreign key constraint violation
```
IntegrityError: FOREIGN KEY constraint failed
```
**Solution**: Ensure user exists before creating diary, check cascade settings

**Issue**: Database locked (SQLite)
```
OperationalError: database is locked
```
**Solution**: Close all database connections, use WAL mode, or switch to PostgreSQL

**Issue**: Connection pool exhausted (PostgreSQL)
```
OperationalError: connection pool exhausted
```
**Solution**: Increase pool size or fix connection leaks in application code

### Debugging Queries

Enable SQLAlchemy query logging:

```python
# In config.py
SQLALCHEMY_ECHO = True  # Print all SQL queries
```

Or use Flask-DebugToolbar in development:

```bash
uv add flask-debugtoolbar
```

---

## Related Documentation

- [Backend API](backend-api.md) - API endpoints and usage
- [Backend Architecture](backend-architecture.md) - Application structure
- [Backend Development](backend-development.md) - Development setup and workflow
- [Backend Deployment](backend-deployment.md) - Production deployment
