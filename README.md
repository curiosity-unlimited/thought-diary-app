# Thought Diary App
- An AI-powered, full-stack web application that allows users to write [Thought Diaries](https://positivepsychology.com/thought-diary/), which help identify & challenge negative thinking patterns, promoting healthier mental habits.

## Prerequisites
- [Git](https://git-scm.com/downloads) for version control
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python project management
- [Node.js](https://github.com/nodejs/node?tab=readme-ov-file) a JavaScript runtime
- [SQLite](https://sqlite.org/) for development database
- [PostgreSQL](https://www.postgresql.org/) optional, for production database
- [Redis](https://redis.io/) optional, for production rate limiting persistence

## Project Architecture
A modern, comprehensive full-stack web application with a robust Flask API backend and a modern Vue 3 frontend as well as clear separation between frontend and backend.

### Backend Technologies (`./backend`)
- **Runtime**: Python 3.13+ with Flask framework
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **API**: RESTful API with JSON serialization using Flask-Marshmallow
- **Authentication**: JWT-based authentication with refresh token support
- **AI Integration**: Sentiment analysis of thought diary entries using GitHub Models API
- **Testing**: Pytest with 80%+ coverage requirement
- **Documentation**: Type hints (PEP 484), comprehensive docstrings and API documentation with OpenAPI

### Frontend Technologies (`./frontend/`)
- **Framework**: Vue 3 with Composition API and TypeScript
- **Build Tool**: Vite with optimized production builds and hot reload
- **State**: Pinia store with persistent storage and real-time sync
- **UI**: Tailwind CSS with Headless UI components and accessibility
- **Testing**: Vitest (unit) with Vue Test Utils, 80%+ coverage requirement
- **PWA**: Service worker, offline support, installable app

### Data Models
- **User**: Authentication model with secure password handling using bcrypt
  - Fields: email, password_hash, created_at, updated_at
  - Features: Email validation, password strength validation, secure hashing
- **ThoughtDiary**: Model for storing and analyzing user thought diary entries
  - Fields: user_id, content, analyzed_content, positive_count, negative_count, created_at, updated_at
  - Features: Relationship with User model, pagination support, sentiment analysis storage and statistics

## Features

### Authentication
- Users can register, log in, and log out securely.

### Thought Diary Management
- After logging in, users can:
    - view the dashboard page showing:
        - statistics for diary entries like:
            - Total Entries
            - Positive Entries
            - Negative Entries
            - Neutral Entries
        - recent diary entries
        - ability to add a diary entry
    - navigate to Dashboard, Diaries, Profile and About pages from Navbar
- Thought diaries are added as plain text only.
- All thought diaries are listed in descending date order with pagination.
- Users can edit and delete thought diaries from the list.

### AI-Powered Sentiment Analysis
- The app leverages [model inference from GitHub Models](https://docs.github.com/en/rest/models/inference?apiVersion=2022-11-28#run-an-inference-request) to analyze thought diaries.
- Words and phrases are marked for positive/negative thinking and feelings with green/red background colors.
    - For example, when a user adds or edits a thought diary:
        ```text
        I felt both excitement and anxious after I got elected to join a team for international math competition.
        ```
    - The backend sends the text to GitHub for model inference and receives HTML-labeled text:
        ```html
        I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after I got elected to join a team for international math competition.
        ```
    - The backend saves the labeled text in the database.
    - The frontend retrieves and displays the text using CSS:
        ```css
        span.positive {
            background-color: green;
            color: white; /* Optional: Change text color for better contrast */
        }
        span.negative {
            background-color: red;
            color: white; /* Optional: Change text color for better contrast */
        }
        ```

### User Experience
- **Progressive Web App**: Installable with native app-like experience
- **Real-time Updates**: Live data synchronization with optimistic UI updates
- **Responsive Design**: Mobile-first with CSS Grid and Flexbox
- **Accessibility**: WCAG 2.1 AA compliant interface

### Authentication & Security
- **JWT Authentication**: Secure token-based authentication with refresh mechanism
- **Enterprise Security**: Redis rate limiting, HTTPS enforcement, security headers, custom middleware
- **Password Security**: Bcrypt hashing with salt and comprehensive validation
- **Input Validation**: Client and server-side validation with sanitization
- **Protected Routes**: Frontend route guards with backend JWT verification
- **CORS Configuration**: Controlled cross-origin resource sharing for secure API access
- **HTTPS Enforcement**: Automatic HTTPS redirect in production
- **Security Headers**: XSS protection, CSRF prevention, content security policy

### Environment-Specific Deployment

**Development:**
- Backend: Flask development server with debug mode
- Frontend: Vite dev server with hot reload
- Database: SQLite for simplicity
- Security: Relaxed for development ease

**Production:**
- Backend: Gunicorn with multiple workers, PostgreSQL, Redis
- Frontend: Static hosting with CDN, optimized builds
- Database: PostgreSQL with connection pooling
- Security: Enforce all security features like Redis rate limiting, HTTPS enforcement, security headers, CORS, etc.

### Environment-Specific Settings

- **Development**: Debug enabled, auto-generated keys, CORS relaxed
- **Testing**: Rate limiting disabled, optimized for testing, mock data
- **Production**: HTTPS enforced, security headers, Redis required

### API Endpoints

#### Authentication Endpoints
- `POST /auth/register` - Register new user (rate limited: 3/hour)
- `POST /auth/login` - User login, returns JWT token (rate limited: 5/15min)
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/logout` - Invalidate current token
- `GET /auth/me` - Get current user profile information

#### Thought Diaries Endpoints
- `GET /diaries` - List all thought diaries with pagination (protected)
- `POST /diaries` - Create a new thought diary (protected)
- `GET /diaries/{id}` - Get a specific thought diary (protected)
- `PUT /diaries/{id}` - Update a specific thought diary (protected)
- `DELETE /diaries/{id}` - Delete a specific thought diary (protected)
- `GET /diaries/stats` - Get statistics about user's thought diaries (protected)

#### System Endpoints
- `GET /health` - Health check endpoint
- `GET /version` - API version information
- `GET /docs` - API documentation

## Documentation

Comprehensive documentation is available in the `docs/` directory

## Getting Started
1. Fork the Repository on GitHub
    1. Go to the repository: https://github.com/curiosity-unlimited/thought-diary-app
    2. Click the "Fork" button in the top-right corner
    3. **IMPORTANT: Please uncheck the "Copy the DEFAULT branch only" option when forking in order to copy all branches into the new fork.**
    4. GitHub will create a copy under your account: https://github.com/YOUR-USERNAME/thought-diary-app

2. Clone the repository from YOUR fork (not the original):
    ```bash
    # Replace YOUR-USERNAME with your GitHub Account
    git clone https://github.com/YOUR-USERNAME/thought-diary-app
    cd thought-diary-app
    ```

3. Fetch all branches and tags so that you can see both the initial code and the instructor's implementation:
    ```bash
    git fetch origin --tags
    ```

4. Check all branches and make sure `demo` is in the list:
    ```bash
    git branch -a
    ```

5. Make sure you're on the `main` branch:
    ```bash
    git checkout main
    ```

6. Create a new branch, `develop` for example, for your own work:
    ```bash
    git checkout -b develop
    ```

7. Create feature branches from that branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```

8. Merge feature branches to `develop`:
    ```bash
    # Via GitHub PR or locally:
    git checkout develop
    git merge feature/your-feature-name
    ```

9. To compare your progress with the instructor's:
    ```bash
    # List all milesones
    git tag -n
    # Compare with a specific milestone
    git diff your-branch-name..tag-name
    # See all differences between your work and the reference
    git diff your-branch-name..demo
    ```

10. For a more comprehensive guide, please follow instructions in [`CONTRIBUTING.md`](./CONTRIBUTING.md)

## License

[MIT](LICENSE)