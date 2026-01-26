# Backend API Documentation

This document provides comprehensive API documentation for the Thought Diary application backend. For implementation details, see [Backend Architecture](backend-architecture.md).

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: Configure via deployment settings

## API Version

- **Current Version**: 0.1.0
- **API Level**: v1

## Authentication

All protected endpoints require JWT authentication using Bearer tokens.

### Token Format
```
Authorization: Bearer <access_token>
```

### Token Lifecycle
- **Access Token**: 15 minutes (for API requests)
- **Refresh Token**: 7 days (for token renewal)

### Security Notes
- Tokens are signed using HS256 algorithm
- Access tokens should be stored securely (e.g., memory, secure storage)
- Refresh tokens should be stored in HttpOnly cookies or secure storage
- Logout invalidates tokens via server-side blacklist

## Rate Limiting

Rate limits are applied to prevent API abuse:

- **Register**: 3 requests per hour per IP
- **Login**: 5 requests per 15 minutes per IP

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time when limit resets

## Error Handling

All errors return consistent JSON format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message"
}
```

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no content to return |
| 400 | Bad Request | Invalid request data or validation error |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Authenticated but not authorized for resource |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Request validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error occurred |

### Common Error Codes

- `validation_error`: Input validation failed
- `invalid_credentials`: Email or password incorrect
- `user_exists`: Email already registered
- `token_expired`: JWT token has expired
- `token_invalid`: JWT token is malformed or invalid
- `token_revoked`: Token was invalidated via logout
- `unauthorized`: Authentication required
- `forbidden`: Insufficient permissions
- `not_found`: Resource not found
- `rate_limit_exceeded`: Too many requests

---

## System Endpoints

### Health Check

Check API health status.

**Endpoint**: `GET /health`

**Authentication**: None required

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2026-01-14T12:00:00.000Z"
}
```

### Version Information

Get API version and level.

**Endpoint**: `GET /version`

**Authentication**: None required

**Response**: `200 OK`
```json
{
  "version": "0.1.0",
  "api_level": "v1"
}
```

### API Documentation

Interactive Swagger UI for API exploration.

**Endpoint**: `GET /docs`

**Authentication**: None required

**Response**: Swagger UI HTML page

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint**: `POST /auth/register`

**Rate Limit**: 3 requests per hour

**Authentication**: None required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Validation Rules**:
- Email: Valid email format, max 120 characters
- Password: Min 8 characters, must contain:
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character (!@#$%^&*(),.?":{}|<>)

**Response**: `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2026-01-14T12:00:00.000Z"
  }
}
```

**Errors**:
- `400`: Validation error or user already exists
- `429`: Rate limit exceeded

### Login

Authenticate user and receive JWT tokens.

**Endpoint**: `POST /auth/login`

**Rate Limit**: 5 requests per 15 minutes

**Authentication**: None required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response**: `200 OK`
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

**Errors**:
- `401`: Invalid credentials
- `429`: Rate limit exceeded

### Refresh Token

Obtain a new access token using refresh token.

**Endpoint**: `POST /auth/refresh`

**Authentication**: Refresh token required
```
Authorization: Bearer <refresh_token>
```

**Request Body**: None

**Response**: `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors**:
- `401`: Invalid or expired refresh token
- `422`: Token revoked

### Logout

Invalidate current access token.

**Endpoint**: `POST /auth/logout`

**Authentication**: Access token required

**Request Body**: None

**Response**: `200 OK`
```json
{
  "message": "Logout successful"
}
```

**Errors**:
- `401`: Token invalid or missing

### Get Current User

Retrieve authenticated user's profile.

**Endpoint**: `GET /auth/me`

**Authentication**: Access token required

**Request Body**: None

**Response**: `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-01-14T12:00:00.000Z",
  "updated_at": "2026-01-14T12:00:00.000Z"
}
```

**Errors**:
- `401`: Token invalid or missing

---

## Thought Diary Endpoints

All diary endpoints require JWT authentication.

### List Diaries

Retrieve paginated list of user's diary entries.

**Endpoint**: `GET /diaries`

**Authentication**: Access token required

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10, max: 100)

**Example**: `GET /diaries?page=2&per_page=20`

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "content": "Original diary text...",
      "analyzed_content": "Text with <span class=\"positive\">positive</span> and <span class=\"negative\">negative</span> sentiment",
      "positive_count": 5,
      "negative_count": 2,
      "created_at": "2026-01-14T12:00:00.000Z",
      "updated_at": "2026-01-14T12:00:00.000Z"
    }
  ],
  "page": 2,
  "per_page": 20,
  "total": 45,
  "pages": 3
}
```

**Notes**:
- Results are sorted by `created_at` in descending order (newest first)
- Only returns diaries owned by authenticated user

**Errors**:
- `401`: Authentication required
- `400`: Invalid pagination parameters

### Create Diary

Create a new thought diary entry with AI sentiment analysis.

**Endpoint**: `POST /diaries`

**Authentication**: Access token required

**Request Body**:
```json
{
  "content": "I felt both excitement and anxious after I got elected to join a team for international math competition."
}
```

**Validation Rules**:
- Content: Required, min 10 characters, max 5000 characters

**Response**: `201 Created`
```json
{
  "id": 1,
  "content": "I felt both excitement and anxious after I got elected to join a team for international math competition.",
  "analyzed_content": "I felt both <span class=\"positive\">excitement</span> and <span class=\"negative\">anxious</span> after I got elected to join a team for international math competition.",
  "positive_count": 1,
  "negative_count": 1,
  "created_at": "2026-01-14T12:00:00.000Z",
  "updated_at": "2026-01-14T12:00:00.000Z"
}
```

**AI Processing**:
- Content is automatically analyzed for sentiment
- Positive phrases are wrapped in `<span class="positive">...</span>`
- Negative phrases are wrapped in `<span class="negative">...</span>`
- Sentiment counts are calculated automatically
- If AI analysis fails, original content is stored without analysis

**Errors**:
- `401`: Authentication required
- `400`: Validation error (content too short/long)

### Get Diary

Retrieve a specific diary entry.

**Endpoint**: `GET /diaries/<id>`

**Authentication**: Access token required

**Path Parameters**:
- `id`: Diary entry ID (integer)

**Example**: `GET /diaries/1`

**Response**: `200 OK`
```json
{
  "id": 1,
  "content": "Original diary text...",
  "analyzed_content": "Text with <span class=\"positive\">positive</span> sentiment",
  "positive_count": 3,
  "negative_count": 0,
  "created_at": "2026-01-14T12:00:00.000Z",
  "updated_at": "2026-01-14T12:00:00.000Z"
}
```

**Errors**:
- `401`: Authentication required
- `403`: Diary belongs to another user
- `404`: Diary not found

### Update Diary

Update an existing diary entry and re-analyze sentiment.

**Endpoint**: `PUT /diaries/<id>`

**Authentication**: Access token required

**Path Parameters**:
- `id`: Diary entry ID (integer)

**Request Body**:
```json
{
  "content": "Updated diary content..."
}
```

**Validation Rules**:
- Content: Required, min 10 characters, max 5000 characters

**Response**: `200 OK`
```json
{
  "id": 1,
  "content": "Updated diary content...",
  "analyzed_content": "Updated diary <span class=\"positive\">content</span>...",
  "positive_count": 1,
  "negative_count": 0,
  "created_at": "2026-01-14T12:00:00.000Z",
  "updated_at": "2026-01-14T13:00:00.000Z"
}
```

**Notes**:
- Content is re-analyzed for sentiment on update
- Timestamps are updated automatically

**Errors**:
- `401`: Authentication required
- `403`: Diary belongs to another user
- `404`: Diary not found
- `400`: Validation error

### Delete Diary

Delete a diary entry permanently.

**Endpoint**: `DELETE /diaries/<id>`

**Authentication**: Access token required

**Path Parameters**:
- `id`: Diary entry ID (integer)

**Request Body**: None

**Response**: `204 No Content`

**Errors**:
- `401`: Authentication required
- `403`: Diary belongs to another user
- `404`: Diary not found

### Get Statistics

Retrieve user's diary statistics.

**Endpoint**: `GET /diaries/stats`

**Authentication**: Access token required

**Request Body**: None

**Response**: `200 OK`
```json
{
  "total_entries": 25,
  "positive_entries": 15,
  "negative_entries": 5,
  "neutral_entries": 5
}
```

**Notes**:
- **Positive entries**: More positive than negative sentiment markers
- **Negative entries**: More negative than positive sentiment markers
- **Neutral entries**: Equal positive and negative markers, or no markers

**Errors**:
- `401`: Authentication required

---

## Frontend Integration

### CORS Configuration

The API allows cross-origin requests from configured origins (default: `http://localhost:5173`).

CORS headers included:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`
- `Access-Control-Allow-Credentials`

### Example API Client (JavaScript)

```javascript
// Configure base URL
const API_BASE_URL = 'http://localhost:5000';

// Login and store tokens
async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const data = await response.json();
  // Store tokens securely
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  return data;
}

// Make authenticated request
async function getDiaries(page = 1) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${API_BASE_URL}/diaries?page=${page}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (response.status === 401) {
    // Token expired, try refresh
    await refreshToken();
    return getDiaries(page); // Retry request
  }
  
  return response.json();
}

// Refresh access token
async function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${refreshToken}`,
    },
  });
  
  if (!response.ok) {
    // Refresh failed, redirect to login
    window.location.href = '/login';
    return;
  }
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
}
```

---

## Testing the API

### Using cURL

```bash
# Register a new user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234!"}'

# Create diary (replace <token> with your access token)
curl -X POST http://localhost:5000/diaries \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"content":"Today was a great day! I felt happy and accomplished."}'

# List diaries
curl -X GET http://localhost:5000/diaries \
  -H "Authorization: Bearer <token>"
```

### Using Bruno

Import the API collection from the project repository:
1. Open Bruno
2. Import collection from `backend/bruno/` directory (if available)
3. Configure environment variables
4. Execute requests

### Using Swagger UI

1. Navigate to `http://localhost:5000/docs`
2. Click "Authorize" button
3. Enter JWT token in format: `Bearer <your_token>`
4. Test endpoints interactively

---

## Related Documentation

- [Database Schema](backend-database.md) - Data models and relationships
- [Architecture](backend-architecture.md) - Application design and structure
- [Development Guide](backend-development.md) - Setup and development workflow
- [Deployment Guide](backend-deployment.md) - Production deployment instructions
