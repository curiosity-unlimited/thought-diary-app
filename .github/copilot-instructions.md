# GitHub Copilot Instructions & AI Rules

## General Guidelines

### Operator Interaction
- When asked to fix code, first explain the problems found.
- When asked to generate tests, first explain what tests will be created.
- When making multiple changes, provide a step-by-step overview first.
- After generating code, explain what was changed and why.

### Security
- Check the code for vulnerabilities after generating.
- Avoid hardcoding sensitive information like credentials or API keys.
- Use secure coding practices and validate all inputs.

### Environment Variables
- If a `**/.env` file exists, use it for local environment variables.
- Document the environment variables in `**/.env.example` and [`README.md`](../README.md).
- Provide example values in the `**/.env.example` files.
- Coordinate environment variables between frontend and backend when they affect integration.
- Ensure production environment variables are properly documented for deployment.

### CODING PRACTICES
- Write concise, modular, efficient, idiomatic and well-documented code that is also easily understandable.
- Always prioritize readability and clarity.
- Handle edge cases and write clear exception handling.
- Use consistent naming conventions and follow language-specific best practices.
- Use code generators to maintain consistency across similar packages or modules.

## Guidelines for VERSION CONTROL

### GIT
- Use [Conventional Branch](https://conventional-branch.github.io/) to create descriptive branch names.
- Use [Conventional Commits](https://www.conventionalcommits.org/) to create meaningful commit messages.
- Write meaningful commit messages that explain why changes were made, not just what.
- Keep commits atomic and focused on single logical changes to facilitate code review and bisection.
- Update [`.gitignore`](../.gitignore) for new build artifacts or dependencies.

## Guidelines for DOCUMENTATION

### DOC UPDATES
- Update relevant documentation in [docs/*.md](../docs/) when modifying features.
- Keep [`README.md`](../README.md) in sync with new capabilities.
- When generating code, always note the changes in [`CHANGELOG.md`](../CHANGELOG.md).
- All changelog entries must follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:
  - Follow [Semantic Versioning Guidelines](https://semver.org/spec/v2.0.0.html).
  - Provide combined project version.
  - Provide independent versions for frontend and backend.
  - Include the date and a description of the change.
  - For example, use the following format:
    ```markdown
      ## [project version] - YYYY-MM-DD

      ### Backend [backend version]
      #### Added
      - Description of new features.

      #### Changed
      - Description of changes to existing functionality.

      #### Fixed
      - Description of bug fixes.

      ### Frontend [frontend version]
      #### Added
      - Description of new features.

      #### Changed
      - Description of changes to existing functionality.

      #### Fixed
      - Description of bug fixes.
    ```

### PRD STRUCTURE
- Both [`README.md`](../README.md) and [docs/*.md](../docs/) serve as Product Requirements Documentation (PRD) files.
- [`README.md`](../README.md) is the high-level capability overview:
  - Focus on what the application does (features, user experience, capabilities)
  - Target audience: users, stakeholders, and new developers
  - Keep technical details minimal and link to detailed documentation in [docs/*.md](../docs/)
  - Include: project overview, prerequisites, project architecture, features, getting started, etc.
- [docs/*.md](../docs/) files contain detailed technical specifications:
  - Focus on how features are implemented (architecture, APIs, data models)
  - Target audience: developers and technical contributors
  - Include: API documentation, database schemas, deployment guides, architecture decisions
  - Reference from [`README.md`](../README.md) when high-level features need technical elaboration
- When adding new features:
  1. Update [`README.md`](../README.md) with user-facing capabilities
  2. Create or update [docs/*.md](../docs/) with implementation details
  3. Ensure bidirectional cross-references are maintained
  4. Update both documents in the same commit/PR for consistency

## Guidelines for PROJECT STRUCTURE

### Directory Organization
- **Backend code** must be located under [./backend/](../backend/)
  - All Python/Flask application code, tests, and configurations
  - Run all backend commands from [./backend/](../backend/) directory
  - Backend-specific files: `pyproject.toml`, `uv.lock`, `.env`, etc.
- **Frontend code** must be located under [./frontend/](../frontend/)
  - All Vue 3/TypeScript application code, tests, and configurations
  - Run all frontend commands from [./frontend/](../frontend/) directory
  - Frontend-specific files: `package.json`, `package-lock.json`, `.env`, etc.
- **Root-level files** are for project-wide concerns only
  - Documentation: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, etc.
  - Git configuration: `.gitignore`, `.gitattributes`
  - CI/CD: `.github/workflows/`, `.github/copilot-instructions.md`
  - Container configuration: `.devcontainer/`

### Working Directory Rules
- When generating or modifying backend code:
  - Set working directory to [./backend/](../backend/)
  - Use relative paths from [./backend/](../backend/) (e.g., `app/`, `tests/`, `migrations/`)
  - Run commands: `cd backend && uv run <command>`
- When generating or modifying frontend code:
  - Set working directory to [./frontend/](../frontend/)
  - Use relative paths from [./frontend/](../frontend/) (e.g., `src/`, `tests/`, `public/`)
  - Run commands: `cd frontend && npm run <command>`
- When working on both frontend and backend:
  - Make changes in the appropriate directory
  - Update cross-references if changes affect integration
  - Test both applications to ensure they work together

## Guidelines for BACKEND (`./backend`)

### PYTHON
- Follow PEP 8 style guidelines.
- Follow PEP 257 for comprehensive docstrings.
- Follow PEP 484 to include type hints with `typing` module.
- Use `uv` for managing Python versions and virtual environments, as well as adding dependencies.
- Always activate virtual environment before running any commands.
- Always use `uv run <command>`to run commands, such as `uv run flask --debug run`.
- Always use `uv add <package>` to add new dependencies, and make sure `pyproject.toml` and `uv.lock` are updated accordingly.

### FLASK
- Use Flask Blueprints to organize routes and views by feature or domain to improve code organization.
- Implement Flask-SQLAlchemy with proper session management to prevent connection leaks and memory issues.
- Use Flask-Migrate for database migrations to handle schema changes effectively.
  - Setup migration environment with `uv run flask db init` command.
  - Generate migration scripts with `uv run flask db migrate` command.
  - Apply migrations with `uv run flask db upgrade` command.
- Use Flask-Marshmallow for serialization and request validation of data types.
- Apply the application factory pattern to enable testing and multiple deployment configurations.
- Implement Flask-Limiter for rate limiting on public endpoints to prevent abuse of APIs.
- Use Flask-JWT-Extended for authentication with proper session timeout and refresh mechanisms.
- Configure CORS using Flask-CORS to allow frontend integration from Vite development server.

### PYTEST (UNIT TESTING)
- Use Pytest for unit testing framework.
- Include unit tests for new functionality and bug fixes.
- When generating unit tests, generate multiple, comprehensive test methods that cover a wide range of scenarios, including edge cases, exception handling, and data validation.
- Use fixtures for test setup and dependency injection.
- Implement parameterized tests for testing multiple inputs for function types.
- Add integration tests for API endpoints, generate test doubles for external services.
- Use monkeypatch for mocking dependencies.
- Ensure all required environment variables are set before running tests to avoid configuration issues.
- Place all test files in the `./backend/tests/unit/` directory to maintain a consistent structure.
- Mirror the source code directory structure within the `./backend/tests/unit/` directory.
  - For example, the test file for `./backend/utils/password.py` must be `./backend/tests/unit/utils/test_password.py`.
- Ensure 80%+ test coverage requirement.

## Guidelines for FRONTEND (`./frontend`)

### TYPESCRIPT
- Use ESLint and Prettier for linting and formatting.
- Always enable `strict` mode in `tsconfig.json` for maximum type safety.
- Use interfaces or type aliases for complex prop and state shapes.
- Use TSDoc comments for all public functions, classes, and interfaces.
- Include examples in comments where applicable.
- Use Vite with optimized production builds and hot reload.
- Use npm for package management.
  - Use `npm install <package-name>` to add new dependencies
  - Use `npm install <package-name> --save-dev` for development dependencies
  - Make sure `package.json` and `package-lock.json` are updated accordingly.
- Keep dependencies up to date and avoid unnecessary packages.

### VUE 3
- Use TypeScript for all code.
- Follow Vue 3 Composition API best practices with `<script setup>` syntax.
- Use Pinia for state management with TypeScript support.
- Follow component-based architecture with proper separation of concerns.
- Implement lazy loading with dynamic imports for route components to improve performance.
- Follow accessibility best practices (WCAG 2.1 AA compliance).
- Use `<style scoped>` for component-level styles or CSS Modules.
- Implement responsive design with Tailwind CSS.

### VITEST (UNIT TESTING)
- Use Vitest for unit testing framework.
- Include comprehensive component tests for new Vue components.
- Test Pinia stores and composables thoroughly.
- Include accessibility testing in component tests.
- Test responsive design across different screen sizes.
- Mock API calls for isolated frontend testing.
- Test files should be named `*.test.ts` and placed in the `./frontend/tests/unit/` directory.
- Mirror the source code directory structure within the `./frontend/tests/unit/` directory.
  - For example, the test file for `./frontend/src/components/Navbar.vue` must be `./frontend/tests/unit/src/components/Navbar.test.ts`.
- Ensure 80%+ test coverage requirement.

## Guidelines for FULL STACK DEVELOPMENT
- Ensure frontend and backend work together seamlessly.
- Coordinate environment variables between both applications.
- Test integration between frontend API calls and backend endpoints.
- Maintain consistent error handling across both applications.
