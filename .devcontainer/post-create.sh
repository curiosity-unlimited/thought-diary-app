#!/bin/bash

set -e

echo "🚀 Initializing development environment..."

# Use backend directory for Python project
pushd backend >/dev/null

PYTHON_VERSION=3.13

# Initialize backend project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "📝 Initializing Python backend project..."
    uv python pin $PYTHON_VERSION
    uv init
    # Remove uv-generated files (we keep root-level ones)
    rm -f .gitignore README.md
fi

# Python virtual environment setup (in backend/.venv)
echo "📦 Setting up Python virtual environment..."

# Create virtual environment only if it doesn't exist
if [ ! -d ".venv" ]; then
    uv venv --python $PYTHON_VERSION
fi

# Python dependencies
echo "📚 Installing Python packages..."
echo "Python version: $PYTHON_VERSION"
uv sync

popd >/dev/null

# Use frontend directory for Node.js project
pushd frontend >/dev/null

# Initialize frontend project if package.json doesn't exist
if [ ! -f "package.json" ]; then
    echo "📝 Initializing Node.js frontend project..."
    yes | npm create vite@latest . -- --template vue-ts --no-interactive
    # Remove npm-generated files (we keep root-level ones)
    rm -f .gitignore README.md
    rm -rf .vscode
fi

# Node.js dependencies
echo "📚 Installing Node.js packages..."
echo "Node.js version: $(node --version)"
npm install

popd >/dev/null

echo "✅ Development environment setup complete!"