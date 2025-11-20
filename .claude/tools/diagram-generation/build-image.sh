#!/bin/bash
# HAL8000-Assistant Diagram Generation - Docker Image Builder
# Builds the Mermaid CLI container image

set -e

IMAGE_NAME="hal8000-mermaid"
IMAGE_TAG="latest"

echo "🐳 Building HAL8000-Assistant Diagram Generation Docker Image..."
echo "   Name: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""

cd "$(dirname "$0")"

docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo ""
echo "✅ Image built successfully!"
echo "   Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
echo "Test the image:"
echo "  docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} --version"
