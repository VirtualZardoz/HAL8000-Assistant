#!/bin/bash

# Load environment variables from .env file
if [ -f "/mnt/d/~HAL8000/.env" ]; then
    export $(cat "/mnt/d/~HAL8000/.env" | grep -v '^#' | grep -v '^$' | xargs)
fi

# Run mcp-omnisearch with loaded environment variables
exec npx -y mcp-omnisearch
