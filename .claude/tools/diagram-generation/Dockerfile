# HAL8000 Diagram Generation Container
# Purpose: Isolated Mermaid CLI environment with all dependencies
# Architecture: Container as I/O device for diagram rendering

FROM node:20-slim

# Install Chrome dependencies for Puppeteer
# These are the system libraries Puppeteer/Chrome needs to render diagrams
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI globally
RUN npm install -g @mermaid-js/mermaid-cli

# Create working directory
WORKDIR /workspace

# Set environment variables for Puppeteer
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=false
ENV PUPPETEER_ARGS="--no-sandbox"

# Create puppeteer config file that sets --no-sandbox (required for root execution in container)
RUN echo '{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}' > /workspace/puppeteer-config.json

# Container runs mmdc command directly
# The --puppeteerConfigFile is added automatically by wrapper script
# Usage: docker run -v /host/path:/workspace hal8000-mermaid -i input.mmd -o output.png
ENTRYPOINT ["sh", "-c", "mmdc --puppeteerConfigFile /workspace/puppeteer-config.json \"$@\"", "--"]
