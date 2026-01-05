# Contributing to Thought Diary App

Welcome! This guide will help you learn professional development practices by contributing to this project.

## Table of Contents

- [Overview](#overview)
- [For Students](#for-students)
- [For Instructors](#for-instructors)
- [Commit Message Format](#commit-message-format)
- [Useful Git Commands](#useful-git-commands)
- [Branch Naming Convention](#branch-naming-convention)
- [Summary](#summary)

## Overview

This is a documentation designed to teach you:
- ✅ Git workflow with feature branches
- ✅ Professional code organization
- ✅ Clear commit messages
- ✅ How to learn from reference implementations

## For Students

### Getting Started

#### 1. Fork the Repository on GitHub
1. Go to the repository: https://github.com/curiosity-unlimited/thought-diary-app
2. Click the "Fork" button in the top-right corner
3. **IMPORTANT: Please uncheck the "Copy the DEFAULT branch only" option when forking in order to copy all branches into the new fork**
4. GitHub will create a copy under your account: https://github.com/YOUR-USERNAME/thought-diary-app

#### 2. Clone the repository from YOUR fork (not the original):
    ```bash
    # Clone YOUR fork (not the original)
    git clone https://github.com/YOUR-USERNAME/thought-diary-app
    cd thought-diary-app
    ```

#### 3. Fetch All Branches

```bash
git fetch origin --tags
```

This downloads all branches and tags so you can see both the initial code and the instructor's implementation.

#### 4. Open in Dev Container (Recommended)

The dev container includes everything you need:
- ✅ Python 3.13 with `uv` package manager
- ✅ Node.js and npm
- ✅ Git pre-installed
- ✅ All dependencies auto-installed

**In VS Code:**
1. Install the "Dev Containers" extension
2. Click the blue icon in the bottom-left corner
3. Select "Reopen in Container"

The environment will automatically initialize!

### Understanding the Branches

This project has a special branch structure to help you learn:

#### `main` Branch
- **Your starting point** for implementing features
- Contains the clean, initial project structure
- README.md has setup instructions only

#### `demo` Branch
- **The instructor's reference implementation**
- Shows how the features should be implemented
- Study this code to understand the approach

#### `develop` Branch
- **Your practice branches** where you do your work

### Your First Contribution

#### Step 1: View the Reference Implementation

```bash
# Check out the develop branch to see the instructor's code
git checkout demo

# View the commit history to see how features were built
git log --oneline -10

# Read through the code to understand the architecture
```

#### Step 2: Create Your Own Branch

```bash
# Always start from main for a clean slate
git checkout main

# Create a branch for your own work
git checkout -b develop

# Create feature branches from that branch
git checkout -b feature/your-feature-name
```

**Naming tips:**
- Use lowercase with hyphens: `feature/user-login`
- Be descriptive: `feature/diary-entries-crud`
- Not too long: `feature/dark-mode` not `feature/implementing-dark-mode-throughout-entire-app`

#### Step 3: Implement Your Version

Make your changes to the code. Work incrementally and commit frequently.

#### Step 4: Commit Your Changes

Write clear, descriptive commit messages:

```bash
git commit -m "feat(auth): add login form"
git commit -m "fix(diary): resolve save error"
git commit -m "docs(readme): update setup instructions"
```

See [Commit Message Format](#commit-message-format) below for details.

### Comparing Your Work

One of the best ways to learn is to compare your implementation with the instructor's reference code.

#### Compare with Milestones

The instructor may tag important points in development:

```bash
# View available milestones
git tag -l

# Compare with a specific milestone
git diff tag-name..your-branch-name
```

#### Compare Your Entire Feature

```bash
# See all differences between your work and the reference
git diff demo..your-branch-name
```

#### View Only Changed Files

```bash
# See which files you modified
git diff --name-only demo..your-branch-name
```

#### View Statistics

```bash
# See how many lines you added/removed
git diff --stat demo..your-branch-name
```

#### Compare Specific Directories

```bash
# Compare only the backend changes
git diff demo..your-branch-name -- backend/

# Compare only the frontend changes
git diff demo..your-branch-name -- frontend/
```

### Getting Help

1. - **For setup issues:** Check `.devcontainer/post-create.sh`
2. **Git issues?** Run `git help <command>`
3. **Commit format?** See [Commit Message Format](#commit-message-format)
4. **Stuck?** Check the instructor's `demo` branch for reference

### Summary

1. ✅ Fork, clone and fetch all branches
2. ✅ View reference on `demo` branch
3. ✅ Create your branch from `main`
4. ✅ Implement your version
5. ✅ Commit with clear messages
6. ✅ Compare with reference using `git diff`
7. ✅ Learn from differences

**Remember:** The goal is to learn professional development practices. Take time to understand not just *what* the code does, but *how* and *why* it's structured that way.

## For Instructors

### Setting Up Your Development Environment

The `.devcontainer/post-create.sh` script automatically:
- ✅ Initializes Python backend with `uv`
- ✅ Sets up Python virtual environment
- ✅ Prepares Node.js frontend (ready for `npm install`)
- ✅ Sets `main` as the default branch for students

No manual setup needed when opening in Dev Container!

### Development Process

#### 1. Create a Feature Branch

```bash
git checkout -b demo
git checkout -b feature/your-feature-name
```

#### 2. Make Changes and Commit

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
git commit -m "feat(auth): add login functionality"
git commit -m "feat(auth): add logout button"
git commit -m "fix(auth): handle expired tokens"
```

#### 3. Push Your Branch

```bash
git push -u origin feature/your-feature-name
```

#### 4. Create a Pull Request (on GitHub)

- Push your branch and create a PR to `demo` (not `main`)
- Add a description of what you implemented
- Link related issues if applicable

#### 5. Merge to `demo`

```bash
# Via GitHub PR or locally:
git checkout demo
git pull origin demo
git merge feature/your-feature-name
git push origin demo
```

#### 6. Delete the local & remote feature branches (cleanup)
```
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

#### 7. Tag Important Milestones (Required)

```bash
# After completing a significant feature
git checkout demo
git tag -a step-1-authentication -m "Authentication feature complete"
git push origin step-1-authentication
```

#### 8. Document the Tagged Milestones (Required)
Clearly explain what each milestone represents in the `CONTRIBUTING.md` file or a separate `MILESTONES.md` file. This helps students understand what to expect at each milestone. For example:
```markdown
## Tagged Milestones
- `v1.0.0`: Initial project setup
- `v1.1.0`: User authentication implemented
- `v1.2.0`: Thought diary CRUD functionality
- `v1.3.0`: Sentiment analysis integration
- `v1.4.0`: Frontend UI enhancements
```

#### 9. Provide Git Commands for Comparison
Include specific commands in the documentation to help students compare their work with the milestones. For example:
```markdown
# Compare your branch with milestone v1.2.0
git diff v1.2.0..your-branch-name
```

### Important Rules

⚠️ **Never:**
- Commit directly to `main` or `demo`
- Merge `demo` back into `main` (keep `main` as clean initial state)
- Force-push to shared branches
- Modify README.md on `demo` in a way that conflicts with student learning

✅ **Do:**
- Always create feature branches for your work
- Use meaningful commit messages
- Keep commits focused and logical
- Update documentation as you implement features

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) standard. This makes commit history clear and easy to understand.

### Format

```
<type>(<scope>): <description>
```

### Types

- **feat** - A new feature
- **fix** - A bug fix
- **docs** - Documentation changes
- **chore** - Updates to dependencies or tooling
- **refactor** - Code cleanup (no feature change)
- **test** - Adding or updating tests

### Scope

The scope specifies what part you modified:
- `auth` - Authentication/login
- `diary` - Diary entries
- `api` - Backend API
- `ui` - User interface
- `db` - Database

### Examples

Good commit messages:
```bash
git commit -m "feat(auth): add login form"
git commit -m "fix(diary): resolve save error on empty entries"
git commit -m "feat(diary): add search by date"
git commit -m "docs(readme): add quick start guide"
git commit -m "chore(deps): update dependencies"
```

Avoid these:
```bash
git commit -m "fix bug"              # Too vague
git commit -m "update code"          # Not descriptive
git commit -m "WIP"                  # Work in progress
git commit -m "asdf"                 # No meaning
```

## Useful Git Commands

### View Branches

```bash
# See all available branches
git branch -a

# See branches with last commit
git branch -v
```

### Switch Between Branches

```bash
# Switch to main
git checkout main

# Switch to demo (to view reference)
git checkout demo

# Switch to your feature
git checkout feature/your-feature-name
```

### View Commit History

```bash
# See recent commits
git log --oneline -5

# See full commit details
git log

# See commits on a specific branch
git log demo --oneline -10
```

### Check Your Status

```bash
# See what files you've changed
git status

# See the changes you made
git diff

# See changes in a specific file
git diff src/auth.js
```

### Undo Changes

```bash
# Discard changes to a file
git checkout -- filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard last commit entirely
git reset --hard HEAD~1
```

## Branch Naming Convention

Use Git Flow style branch names for clarity:

```bash
feature/<description>      # New features
bugfix/<description>       # Bug fixes
chore/<description>        # Maintenance, dependencies, tooling
docs/<description>         # Documentation
refactor/<description>     # Code refactoring (no feature change)
test/<description>         # Adding or updating tests
```

### Examples

```bash
git checkout -b feature/user-authentication
git checkout -b feature/diary-entries
git checkout -b bugfix/login-error
git checkout -b chore/update-dependencies
git checkout -b docs/api-reference
git checkout -b refactor/database-queries
```

## Summary

**Branch Strategy:**
- `main` = clean initial state (students branch from here)
- `demo` = reference implementation (students compare against this)
- `develop` = work branches (where all development happens)

**Workflow:**
1. Create feature branch from appropriate base
2. Make changes with descriptive commit messages
3. Push to remote
4. Merge via pull request (or directly if you're the instructor)
5. Delete feature branch (cleanup)

**Key Principles:**
- Never commit directly to `main` or `demo`
- Use conventional commits for clarity
- Keep commits focused and logical
- Reference implementation stays on `demo` for student learning

Happy coding! 🚀