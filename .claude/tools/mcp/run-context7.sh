#!/bin/bash

# Load environment variables from .env file
if [ -f "/mnt/d/~HAL8000/.env" ]; then
    export $(cat "/mnt/d/~HAL8000/.env" | grep -v '^#' | grep -v '^$' | xargs)
fi

# Run context7 MCP server with loaded environment variables
# Note: Update the command below based on actual Context7 MCP server installation
exec npx -y mcp-context7
