# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-07

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
