FROM mcr.microsoft.com/devcontainers/python:3.13

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    # Cypress dependencies
    libgtk-3-0 \
    libgbm-dev \
    libnotify-dev \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    xauth \
    xvfb \
    # Python related
    && rm -rf /var/lib/apt/lists/*

# Switch to vscode user before installing uv
USER vscode

# Install uv and other Python tools
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> /home/vscode/.bashrc