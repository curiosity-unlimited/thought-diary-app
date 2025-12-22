#!/bin/bash

set -e

echo "🚀 Initializing development environment..."

# Use backend directory for Python project
pushd backend >/dev/null

# Initialize backend project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "📝 Initializing Python backend project..."
    uv python pin 3.13
    uv init
    # Remove uv-generated files (we keep root-level ones)
    rm -f .gitignore README.md
fi

# Python virtual environment setup (in backend/.venv)
echo "📦 Setting up Python virtual environment..."

# Create virtual environment only if it doesn't exist
if [ ! -d ".venv" ]; then
    uv venv --python 3.13
fi

uv sync

popd >/dev/null

# Frontend dependencies
echo "📚 Installing Node.js packages..."
echo "Node.js version: $(node --version)"
# cd frontend
# npm install

echo "✅ Development environment setup complete!"
# echo "📌 Start backend: uv run flask --debug run"
# echo "📌 Start frontend: cd frontend && npm run dev"