# Backend Deployment Guide

This guide covers deploying the Thought Diary backend to production environments. For development setup, see [Backend Development](backend-development.md).

## Overview

The backend can be deployed in various environments:

- **Cloud Platforms**: AWS, Google Cloud, Azure, Heroku, Railway, Render
- **Container Platforms**: Docker, Kubernetes
- **Traditional Hosting**: VPS with Nginx/Apache + Gunicorn

## Prerequisites

### Production Requirements

- **Python 3.13+**: Runtime environment
- **PostgreSQL 13+**: Production database
- **Redis 6+**: Rate limiting and session storage
- **Web Server**: Nginx or Apache (as reverse proxy)
- **WSGI Server**: Gunicorn (handles Flask application)
- **SSL Certificate**: For HTTPS (Let's Encrypt recommended)
- **GitHub Token**: For AI sentiment analysis API

### Recommended Specifications

**Minimum**:
- 1 CPU core
- 512 MB RAM
- 10 GB disk space
- Supports ~100 concurrent users

**Recommended**:
- 2 CPU cores
- 2 GB RAM
- 20 GB disk space
- Supports ~1000 concurrent users

**High Traffic**:
- 4+ CPU cores
- 4+ GB RAM
- 50+ GB disk space
- Horizontal scaling with load balancer

---

## Production Configuration

### Environment Variables

Create `.env` file or configure platform environment:

```env
# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=production
SECRET_KEY=<generate-secure-random-key>
JWT_SECRET_KEY=<generate-secure-random-key>

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# GitHub Models API
GITHUB_TOKEN=<your-github-token>
GITHUB_MODEL_NAME=gpt-4o

# CORS (Frontend URL)
CORS_ORIGINS=https://your-frontend-domain.com

# Redis (for rate limiting)
REDIS_URL=redis://localhost:6379/0

# Gunicorn Configuration
WORKERS=4
WORKER_CLASS=sync
TIMEOUT=30
BIND=0.0.0.0:5000
```

### Generating Secret Keys

**Secure random keys** for production:

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Important**: Never commit secret keys to version control!

### Database Setup

**PostgreSQL**:

```bash
# Create database
createdb thought_diary

# Create user
createuser thought_diary_user

# Grant permissions
psql thought_diary -c "GRANT ALL PRIVILEGES ON DATABASE thought_diary TO thought_diary_user;"

# Set password
psql -c "ALTER USER thought_diary_user WITH PASSWORD 'secure_password';"
```

**Connection URL**:
```
postgresql://thought_diary_user:secure_password@localhost:5432/thought_diary
```

### Redis Setup

**Install Redis**:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# macOS
brew install redis

# Start Redis
sudo systemctl start redis   # Linux
brew services start redis    # macOS
```

**Configure Redis** (`/etc/redis/redis.conf`):
```
bind 127.0.0.1
port 6379
requirepass your_redis_password
maxmemory 256mb
maxmemory-policy allkeys-lru
```

**Connection URL with auth**:
```
redis://:your_redis_password@localhost:6379/0
```

---

## Deployment Options

### Option 1: Traditional VPS Deployment

Deploy to a Virtual Private Server (DigitalOcean, Linode, AWS EC2, etc.)

#### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.13 python3-pip python3-venv
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y nginx
sudo apt install -y certbot python3-certbot-nginx

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Step 2: Application Setup

```bash
# Create app user
sudo useradd -m -s /bin/bash thoughtdiary
sudo su - thoughtdiary

# Clone repository
git clone https://github.com/your-username/thought-diary-app.git
cd thought-diary-app/backend

# Install dependencies
uv sync --frozen

# Configure environment
cp .env.example .env
nano .env  # Edit with production values
```

#### Step 3: Database Migration

```bash
# Run migrations
uv run flask db upgrade

# (Optional) Create initial admin user
uv run flask shell
>>> from app.models import User
>>> from app.extensions import db
>>> admin = User(email="admin@example.com")
>>> admin.set_password("SecurePassword123!")
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

#### Step 4: Gunicorn Setup

**Create systemd service** `/etc/systemd/system/thoughtdiary.service`:

```ini
[Unit]
Description=Thought Diary Backend
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=thoughtdiary
Group=thoughtdiary
WorkingDirectory=/home/thoughtdiary/thought-diary-app/backend
Environment="PATH=/home/thoughtdiary/.local/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/thoughtdiary/.local/bin/uv run gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --worker-class sync \
    --timeout 30 \
    --access-logfile - \
    --error-logfile - \
    "app:create_app()"

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Start service**:

```bash
sudo systemctl daemon-reload
sudo systemctl start thoughtdiary
sudo systemctl enable thoughtdiary
sudo systemctl status thoughtdiary
```

#### Step 5: Nginx Configuration

**Create Nginx config** `/etc/nginx/sites-available/thoughtdiary`:

```nginx
upstream thoughtdiary {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL Configuration (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Max upload size
    client_max_body_size 10M;

    # Proxy settings
    location / {
        proxy_pass http://thoughtdiary;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (if any)
    location /static/ {
        alias /home/thoughtdiary/thought-diary-app/backend/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Health check endpoint (no auth required)
    location /health {
        proxy_pass http://thoughtdiary;
        access_log off;
    }
}
```

**Enable site and restart Nginx**:

```bash
sudo ln -s /etc/nginx/sites-available/thoughtdiary /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 6: SSL Certificate

**Using Let's Encrypt**:

```bash
sudo certbot --nginx -d api.yourdomain.com
```

**Auto-renewal** (automatic with Certbot):
```bash
sudo systemctl status certbot.timer
```

#### Step 7: Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

---

### Option 2: Docker Deployment

#### Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run with gunicorn
CMD ["uv", "run", "gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:create_app()"]
```

#### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: thought_diary
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/thought_diary
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0
      GITHUB_TOKEN: ${GITHUB_TOKEN}
      CORS_ORIGINS: ${CORS_ORIGINS}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

#### Deploy with Docker Compose

```bash
# Create .env file
cat > .env << EOF
DB_PASSWORD=secure_db_password
REDIS_PASSWORD=secure_redis_password
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
GITHUB_TOKEN=your_github_token
CORS_ORIGINS=https://your-frontend-domain.com
EOF

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend uv run flask db upgrade

# Stop services
docker-compose down
```

---

### Option 3: Heroku Deployment

#### Prerequisites

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

#### Procfile

Create `backend/Procfile`:

```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 30 "app:create_app()"
release: flask db upgrade
```

#### Deploy

```bash
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
heroku config:set JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
heroku config:set GITHUB_TOKEN=your_github_token
heroku config:set CORS_ORIGINS=https://your-frontend-domain.com

# Deploy
git push heroku main

# Run migrations
heroku run flask db upgrade

# View logs
heroku logs --tail
```

---

### Option 4: Cloud Platform Deployment

#### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.13 thought-diary-backend

# Create environment
eb create production

# Deploy
eb deploy

# Set environment variables
eb setenv FLASK_ENV=production SECRET_KEY=xxx ...

# View logs
eb logs
```

#### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/thought-diary-backend

# Deploy
gcloud run deploy thought-diary-backend \
    --image gcr.io/PROJECT_ID/thought-diary-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars FLASK_ENV=production,SECRET_KEY=xxx
```

#### Azure App Service

```bash
# Create resource group
az group create --name thought-diary-rg --location eastus

# Create App Service plan
az appservice plan create --name thought-diary-plan \
    --resource-group thought-diary-rg --sku B1 --is-linux

# Create web app
az webapp create --name thought-diary-backend \
    --resource-group thought-diary-rg \
    --plan thought-diary-plan \
    --runtime "PYTHON:3.13"

# Deploy
az webapp up --name thought-diary-backend
```

---

## Database Management

### Backup Strategy

**PostgreSQL backups**:

```bash
# Manual backup
pg_dump -h localhost -U postgres thought_diary > backup_$(date +%Y%m%d).sql

# Restore
psql -h localhost -U postgres thought_diary < backup_20260114.sql
```

**Automated backups** (cron job):

```bash
# Add to crontab: daily backup at 2 AM
0 2 * * * /usr/bin/pg_dump thought_diary > /backups/thought_diary_$(date +\%Y\%m\%d).sql
```

**Cloud-managed backups**:
- AWS RDS: Automated backups with point-in-time recovery
- Heroku Postgres: Continuous protection with rollback
- Google Cloud SQL: Automated backups and replicas

### Migration Strategy

**Zero-downtime migrations**:

1. **Backward compatible migrations**: Add columns as nullable first
2. **Blue-green deployment**: Deploy new version alongside old
3. **Database rollback plan**: Test downgrade before production
4. **Data migration script**: Separate from schema changes

**Example safe migration**:

```python
# Add nullable column first
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(50), nullable=True))

# Populate data
# Then in next migration, make it non-nullable
def upgrade_v2():
    op.alter_column('users', 'new_field', nullable=False)
```

---

## Monitoring & Logging

### Application Monitoring

**Health checks**:
```bash
# Endpoint for monitoring tools
curl https://api.yourdomain.com/health
```

**Monitoring Tools**:
- **Uptime monitoring**: UptimeRobot, Pingdom, StatusCake
- **APM**: New Relic, DataDog, Sentry
- **Log aggregation**: Papertrail, Loggly, ELK Stack

### Logging Configuration

**Production logging** in `config.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

class ProductionConfig(Config):
    @staticmethod
    def init_app(app):
        # Log to file with rotation
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
```

**Structured logging** (JSON):

```python
import json
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
app.logger.addHandler(logHandler)
```

### Error Tracking

**Sentry integration**:

```bash
uv add sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    environment="production"
)
```

---

## Performance Optimization

### Gunicorn Configuration

**Optimal worker settings**:

```python
# Number of workers = (2 × CPU cores) + 1
workers = (2 * cpu_count()) + 1

# Or set explicitly
workers = 4

# Worker class
worker_class = 'sync'  # For CPU-bound tasks
# worker_class = 'gevent'  # For I/O-bound tasks

# Timeout (seconds)
timeout = 30
keepalive = 5

# Max requests per worker (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 50
```

### Database Optimization

**Connection pooling**:

```python
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = 3600
```

**Query optimization**:
- Use indexes on frequently queried columns
- Implement pagination for large result sets
- Use eager loading to avoid N+1 queries
- Monitor slow queries with EXPLAIN

### Caching Strategy

**Redis caching** (future enhancement):

```python
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

@cache.cached(timeout=300)
def get_user_stats(user_id):
    # Expensive computation
    return stats
```

---

## Security Checklist

### Pre-Deployment Security

- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure CORS with specific origins (not *)
- [ ] Set secure password requirements
- [ ] Enable rate limiting with Redis
- [ ] Configure security headers (CSP, HSTS, X-Frame-Options)
- [ ] Use environment variables for secrets
- [ ] Set up database user with minimal permissions
- [ ] Enable firewall on server
- [ ] Configure Redis password authentication
- [ ] Review and minimize exposed ports
- [ ] Set up automated backups
- [ ] Configure log retention and rotation
- [ ] Test authentication and authorization
- [ ] Validate all user inputs
- [ ] Sanitize error messages (no stack traces to users)

### Regular Security Maintenance

- [ ] Keep dependencies updated (`uv sync --upgrade`)
- [ ] Monitor security advisories
- [ ] Review access logs regularly
- [ ] Rotate secrets periodically
- [ ] Audit database permissions
- [ ] Test backup restoration
- [ ] Review and update firewall rules
- [ ] Check for CVEs in dependencies

---

## Troubleshooting Production Issues

### Common Issues

**Issue**: Application won't start
```bash
# Check logs
sudo journalctl -u thoughtdiary -n 50

# Check Gunicorn process
ps aux | grep gunicorn

# Check port availability
sudo lsof -i :5000
```

**Issue**: Database connection errors
```bash
# Test database connection
psql -h localhost -U postgres thought_diary

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

**Issue**: Redis connection errors
```bash
# Test Redis connection
redis-cli ping

# Check Redis status
sudo systemctl status redis

# View Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

**Issue**: Nginx 502 Bad Gateway
```bash
# Check Nginx error log
sudo tail -f /var/log/nginx/error.log

# Test Nginx config
sudo nginx -t

# Verify backend is running
curl http://localhost:5000/health
```

**Issue**: High memory usage
```bash
# Check memory usage
free -h
top

# Restart application
sudo systemctl restart thoughtdiary

# Adjust Gunicorn workers
# Edit: /etc/systemd/system/thoughtdiary.service
# Reduce --workers value
```

### Performance Debugging

**Slow responses**:
```python
# Enable query logging
SQLALCHEMY_ECHO = True

# Add request timing
import time
@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if diff > 1.0:  # Log slow requests
        app.logger.warning(f"Slow request: {request.path} took {diff:.2f}s")
    return response
```

---

## Rollback Strategy

### Application Rollback

**Git-based deployment**:
```bash
# Get previous commit hash
git log --oneline

# Rollback to previous version
git checkout <previous-commit>
sudo systemctl restart thoughtdiary
```

**Docker deployment**:
```bash
# List previous images
docker images

# Run previous version
docker run -d --name backend <previous-image-tag>
```

### Database Rollback

**Rollback migration**:
```bash
uv run flask db downgrade
```

**Restore from backup**:
```bash
# Stop application
sudo systemctl stop thoughtdiary

# Restore database
psql -U postgres thought_diary < backup_20260114.sql

# Restart application
sudo systemctl start thoughtdiary
```

---

## Scaling Strategies

### Horizontal Scaling

**Load Balancer Configuration** (Nginx):

```nginx
upstream backend_cluster {
    least_conn;
    server backend1.internal:5000;
    server backend2.internal:5000;
    server backend3.internal:5000;
}

server {
    location / {
        proxy_pass http://backend_cluster;
    }
}
```

### Database Scaling

**Read replicas** (PostgreSQL):
- Primary: Write operations
- Replicas: Read operations
- Connection routing in application

**Connection pooling** (PgBouncer):
```bash
sudo apt install pgbouncer
# Configure connection pooling
```

### Caching Layer

**Redis cluster** for distributed caching:
```bash
# Multiple Redis instances
redis-server --port 6379
redis-server --port 6380
redis-server --port 6381
```

---

## Related Documentation

- [Backend API](backend-api.md) - API endpoints and usage
- [Backend Database](backend-database.md) - Database operations
- [Backend Development](backend-development.md) - Development workflow
- [Backend Architecture](backend-architecture.md) - System design
