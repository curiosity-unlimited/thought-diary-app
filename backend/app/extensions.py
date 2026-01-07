"""Flask extensions initialization module.

This module initializes all Flask extensions used in the application.
Extensions are initialized here but configured in the application factory.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS


# Initialize SQLAlchemy for database ORM
db = SQLAlchemy()

# Initialize Flask-Migrate for database migrations
migrate = Migrate()

# Initialize Marshmallow for serialization and deserialization
ma = Marshmallow()

# Initialize JWT Manager for authentication
jwt = JWTManager()

# Initialize Limiter for rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=None  # Will be set in app factory from config
)

# Initialize CORS for cross-origin resource sharing
cors = CORS()
