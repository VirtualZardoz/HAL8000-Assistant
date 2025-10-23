#!/bin/bash
# Build HAL8000 Image Generation Docker Image
# Similar to diagram-generation/build-image.sh

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "HAL8000 Image Generation System - Build Script"
echo "=================================================="
echo ""

# Check Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker Desktop."
    exit 1
fi

# Check NVIDIA Docker support
if ! docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "WARNING: GPU support not detected or not working."
    echo "Make sure you have:"
    echo "  1. NVIDIA GPU drivers installed"
    echo "  2. Docker Desktop with WSL2 backend"
    echo "  3. NVIDIA Container Toolkit installed"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create model cache directory
MODEL_CACHE="/mnt/d/~HAL8000/.docker-cache/models"
echo "Creating model cache directory: $MODEL_CACHE"
mkdir -p "$MODEL_CACHE"
mkdir -p "$MODEL_CACHE/checkpoints"
mkdir -p "$MODEL_CACHE/vae"
mkdir -p "$MODEL_CACHE/clip"

# Create output directory
OUTPUT_DIR="/mnt/d/~HAL8000/data/images"
echo "Creating output directory: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo ""
echo "Building Docker image: hal8000-image-gen:latest"
echo "This will take 5-10 minutes..."
echo ""

# Build Docker image
docker build -t hal8000-image-gen:latest .

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Build complete!"
    echo "=================================================="
    echo ""
    echo "Docker image: hal8000-image-gen:latest"
    echo "Model cache:  $MODEL_CACHE"
    echo "Output dir:   $OUTPUT_DIR"
    echo ""
    echo "Usage:"
    echo "  python3 HAL-generate-image.py --prompt 'your prompt' --output image.png"
    echo ""
    echo "Examples:"
    echo "  python3 HAL-generate-image.py --prompt 'futuristic CPU' --output cpu.png"
    echo "  python3 HAL-generate-image.py --prompt 'robot' --model sd15 --output robot.png"
    echo ""
    echo "First run will download models:"
    echo "  - SDXL: ~6.5GB (recommended, best quality)"
    echo "  - SD1.5: ~4GB (faster, good quality)"
    echo ""
    echo "Models are cached in $MODEL_CACHE"
    echo "Subsequent runs will be much faster!"
    echo ""
else
    echo ""
    echo "ERROR: Docker build failed!"
    echo "Check the error messages above."
    exit 1
fi
