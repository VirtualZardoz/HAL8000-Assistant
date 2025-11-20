# Installation

## Quick Start

1. Build Docker image:
   ```bash
   cd .claude/tools/image-generation
   ./build-image.sh
   ```

2. Generate image (models download automatically on first use):
   ```bash
   python3 HAL-generate-image.py --prompt "test image" --output test.png
   ```

## Models

Models download automatically on first use:
- **SDXL**: ~6.5GB (best quality)
- **SD1.5**: ~4GB (faster)

Cached in: /mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/

## GPU Requirements

- NVIDIA GPU with CUDA support
- Docker with nvidia-docker2
- Minimum 8GB VRAM (16GB+ recommended for SDXL)
