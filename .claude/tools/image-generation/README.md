# HAL8000 Image Generation Tool

AI-powered image generation using Dockerized Stable Diffusion with GPU acceleration.

## Overview

This tool generates high-quality AI images via a Docker container running ComfyUI and Stable Diffusion. The architecture mirrors the proven `diagram-generation` tool pattern: containerized execution with no host pollution.

**Key Features:**
- ✅ **Dockerized**: Everything runs in isolated container
- ✅ **GPU-accelerated**: Utilizes RTX 3090 for fast generation (3-8 seconds/image)
- ✅ **Zero host pollution**: All dependencies in container
- ✅ **Model caching**: Downloads once, reuses forever
- ✅ **Multiple models**: SDXL (best quality), SD1.5 (faster)
- ✅ **HAL8000 controlled**: I (Claude) generate images on your behalf

## Architecture

```
User Request
    ↓
HAL8000 (Claude/CPU)
    ↓
HAL-generate-image.py
    ↓
docker run hal8000-image-gen:latest --prompt "..." --output image.png
    ↓
Container: Start → Load Model → Generate → Save → Exit
    ↓
Image saved to /mnt/d/~HAL8000/data/images/
    ↓
HAL8000 presents result to user
```

## Storage Layout

```
Host System:
├── C: drive (~3-5GB)
│   └── Docker images (hal8000-image-gen:latest)
│
└── D: drive (/mnt/d/~HAL8000/)
    ├── .docker-cache/models/     # Model weights (~6-33GB)
    │   ├── checkpoints/
    │   │   ├── sd_xl_base_1.0.safetensors (6.5GB)
    │   │   ├── v1-5-pruned-emaonly.safetensors (4GB)
    │   ├── vae/
    │   └── clip/
    │
    ├── data/images/               # Generated images (~5MB each)
    │
    └── .claude/tools/image-generation/
        ├── Dockerfile
        ├── entrypoint.py
        ├── HAL-generate-image.py
        ├── build-image.sh
        └── README.md (this file)
```

**Total Space Required:**
- Minimum (SDXL only): ~10GB total (3GB C:, 6.5GB D:)
- Recommended (SDXL + SD1.5): ~14GB total (3GB C:, 10.5GB D:)
- Maximum (All models): ~37GB total (3GB C:, 33.5GB D:)

## Installation

### Prerequisites

1. **Docker Desktop** with WSL2 backend
2. **NVIDIA GPU drivers** (for RTX 3090)
3. **NVIDIA Container Toolkit** (for GPU support in Docker)

### Build

```bash
cd /mnt/d/~HAL8000/.claude/tools/image-generation
./build-image.sh
```

Build time: ~5-10 minutes

## Usage

### Basic Usage

```bash
python3 HAL-generate-image.py \
  --prompt "futuristic computer CPU with glowing circuits" \
  --output cpu.png
```

### Model Selection

```bash
# SDXL (best quality, default)
python3 HAL-generate-image.py \
  --prompt "cyberpunk city at night" \
  --model sdxl \
  --output city.png

# SD 1.5 (faster)
python3 HAL-generate-image.py \
  --prompt "a friendly robot" \
  --model sd15 \
  --output robot.png

```

### Quality Control

```bash
# Higher quality (more steps)
python3 HAL-generate-image.py \
  --prompt "detailed portrait" \
  --steps 50 \
  --output portrait.png

# Faster (fewer steps)
python3 HAL-generate-image.py \
  --prompt "quick sketch" \
  --steps 10 \
  --output sketch.png
```

### Custom Dimensions

```bash
# Landscape
python3 HAL-generate-image.py \
  --prompt "mountain vista" \
  --width 1920 \
  --height 1080 \
  --output vista.png

# Portrait
python3 HAL-generate-image.py \
  --prompt "character portrait" \
  --width 768 \
  --height 1024 \
  --output portrait.png
```

### Text Overlay

```bash
# Simple text overlay (bottom center)
python3 HAL-generate-image.py \
  --prompt "solid blue background" \
  --text "HELLO WORLD" \
  --output labeled-image.png

# Custom text styling
python3 HAL-generate-image.py \
  --prompt "cyberpunk city at night" \
  --text "NEO TOKYO 2077" \
  --text-position north \
  --text-size 96 \
  --text-color white \
  --output cyberpunk-titled.png

# Text with different positions
python3 HAL-generate-image.py \
  --prompt "robot assistant" \
  --text "HAL8000" \
  --text-position center \
  --text-size 120 \
  --text-color "#00FF00" \
  --output robot-labeled.png
```

**Text Options:**
- `--text`: Text to overlay on image
- `--text-position`: north, south (default), east, west, center
- `--text-size`: Font size in points (default: 72)
- `--text-color`: Color name (white, black, red, blue) or hex (#RRGGBB)

**Note:** Text is rendered with black stroke outline for readability on any background.

## Available Models

| Model | Size | Speed (RTX 3090) | Quality | Best For |
|-------|------|------------------|---------|----------|
| **sdxl** | 6.5GB | 3-5s | ⭐⭐⭐⭐⭐ | Best quality, default choice |
| **sd15** | 4GB | 1-2s | ⭐⭐⭐⭐ | Faster iterations, prototyping |


## Performance

### First Run (Model Download)
```
SDXL:  5-10 minutes (downloads 6.5GB automatically)
SD1.5: 3-5 minutes (downloads 4GB automatically)

```

### Subsequent Runs (Cached Models)
```
SDXL:  ~10-15s total (2s startup + 5s model load + 3-8s generation)
SD1.5: ~5-8s total   (2s startup + 2s model load + 1-4s generation)

```

### Batch Generation
For multiple images, the model stays loaded, making each additional image faster:
```
Image 1: 15s (startup + load + generate)
Image 2: 5s (generate only)
Image 3: 5s (generate only)
...
```

## Command Reference

```bash
python3 HAL-generate-image.py [OPTIONS]

Required:
  --prompt TEXT      Image description
  --output PATH      Output file path

Optional:
  --model NAME       Model: sdxl (default), sd15
  --width N          Width in pixels (default: 1024, range: 256-2048)
  --height N         Height in pixels (default: 1024, range: 256-2048)
  --steps N          Generation steps (default: 20, range: 1-100)
                     More steps = better quality but slower
```

## Examples

### Artistic
```bash
python3 HAL-generate-image.py \
  --prompt "oil painting of a sunset over mountains, impressionist style" \
  --steps 30 \
  --output sunset.png
```

### Technical
```bash
python3 HAL-generate-image.py \
  --prompt "detailed technical diagram of a quantum computer" \
  --model sdxl \
  --output quantum.png
```

### Abstract
```bash
python3 HAL-generate-image.py \
  --prompt "abstract geometric patterns in neon colors, cyberpunk aesthetic" \
  --width 1920 \
  --height 1080 \
  --output abstract.png
```

### Characters
```bash
python3 HAL-generate-image.py \
  --prompt "friendly AI assistant robot, modern design, clean background" \
  --model sdxl \
  --steps 40 \
  --output assistant.png
```

## Troubleshooting

### GPU Not Detected

**Error**: "GPU support not detected"

**Solution**:
1. Check NVIDIA drivers: `nvidia-smi`
2. Verify Docker GPU access: `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`
3. Ensure Docker Desktop WSL2 backend is enabled
4. Install NVIDIA Container Toolkit if missing

### Model Download Fails

**Error**: "Download failed" or "Connection timeout"

**Solution**:
1. Check internet connection
2. Retry (may be temporary HuggingFace issue)
3. Manually download model:
   ```bash
   cd /mnt/d/~HAL8000/.docker-cache/models/checkpoints/
   wget https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors
   ```

### Container Won't Start

**Error**: "Container exited with code 1"

**Solution**:
1. Check Docker is running: `docker ps`
2. Check logs: `docker logs <container-id>`
3. Rebuild image: `./build-image.sh`
4. Verify disk space: `df -h`

### Out of Memory

**Error**: "CUDA out of memory"

**Solution**:
1. Reduce image size: `--width 512 --height 512`
2. Use SD1.5 instead of SDXL: `--model sd15`
3. Close other GPU applications
4. (Should not happen with RTX 3090's 24GB VRAM)

## Maintenance

### Clean Up Old Images
```bash
# Remove generated images
rm /mnt/d/~HAL8000/data/images/*.png

# Keep model cache (recommended)
# Models are large, re-downloading is slow
```

### Remove Models
```bash
# Free up space (will re-download on next use)
rm -rf /mnt/d/~HAL8000/.docker-cache/models/*
```

### Rebuild Container
```bash
# Update ComfyUI or dependencies
docker rmi hal8000-image-gen:latest
./build-image.sh
```

### Check Disk Usage
```bash
# Docker images
docker images | grep hal8000-image-gen

# Model cache
du -sh /mnt/d/~HAL8000/.docker-cache/models/

# Generated images
du -sh /mnt/d/~HAL8000/data/images/

# Total Docker usage
docker system df
```

## Integration with HAL8000

HAL8000 (Claude) uses this tool to generate images on your behalf:

```
User: "Generate an image of a futuristic CPU"

HAL8000 executes:
    python3 .claude/tools/image-generation/HAL-generate-image.py \
      --prompt "futuristic computer CPU with glowing circuits, cyberpunk style, detailed" \
      --model sdxl \
      --steps 25 \
      --output data/images/futuristic-cpu.png

HAL8000 responds:
    "Image generated: data/images/futuristic-cpu.png"
```

You don't manage the container directly - HAL8000 handles it automatically.

## Technical Details

### Container Lifecycle

1. **Start**: Container spins up (~2s)
2. **Check Model**: Verify model is cached, download if needed (one-time)
3. **Load Model**: Load weights into GPU VRAM (~3-5s)
4. **Start ComfyUI**: Launch API server (~2-3s)
5. **Generate**: Execute workflow (~3-8s depending on steps)
6. **Save**: Write image to output directory
7. **Cleanup**: Terminate container, free resources (~1s)

### Why This Architecture?

**Proven Pattern**: Same design as `diagram-generation` tool
- Container isolation = no host pollution
- Volume mounts = efficient data sharing
- GPU passthrough = native performance
- Ephemeral containers = clean state each run

**Advantages**:
- Reproducible (same image = same results)
- Portable (works on any Docker+GPU system)
- Maintainable (easy to update/rebuild)
- Safe (isolated from host system)

## Version History

- **v1.0.0** (2025-10-22): Initial release
  - SDXL and SD1.5 models
  - ComfyUI backend
  - Docker containerization
  - GPU acceleration
  - Model caching on D: drive

## Related Tools

- **diagram-generation**: Similar architecture for Mermaid diagrams
- **docling-cli**: Document processing via PowerShell bridge
- **gemini-cli**: External AI agent for heavy analysis

## License

Part of HAL8000 system. See main repository for license details.

## Credits

- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Stable Diffusion**: Stability AI
- **SDXL**: Stability AI
- **Architecture Pattern**: Based on HAL8000 diagram-generation tool

**Note on FLUX**: FLUX.1-dev was investigated but found incompatible with our setup (timeouts, low GPU utilization). See FLUX-STATUS.md for details. SDXL provides excellent quality as primary model.
