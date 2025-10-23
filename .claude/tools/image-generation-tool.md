# Image Generation Tool - External I/O Device

**Category:** External Tool (Dockerized)
**Interface:** Python CLI wrapper + Docker container
**GPU:** RTX 3090 (24GB VRAM)
**Backend:** ComfyUI + Stable Diffusion
**Installation:** Requires Docker build
**Path:** `.claude/tools/image-generation/HAL-generate-image.py`
**Version:** 1.0.0

---

## Overview

AI-powered image generation system running in isolated Docker containers. Architecture mirrors the proven `diagram-generation` tool pattern: containerized execution with GPU acceleration and zero host pollution.

**Architectural Position:**
```
HAL8000 (Claude, 200K context)
    ↓ command
Docker Container (ComfyUI + SDXL, isolated)
    ↓ GPU processing (RTX 3090)
Returns image file
    ↓ result
HAL8000 (RAM += file path only, ~10 tokens)
```

---

## Tool Classification

| Tool Type | Context | Control | Use Case |
|-----------|---------|---------|----------|
| **Image Generation** (Docker) | External | HAL8000 controls | AI image generation |
| **Diagram Generation** (Docker) | External | HAL8000 controls | Technical diagrams |
| **Gemini CLI** (External) | 1M tokens | HAL8000 delegates | Heavy analysis |
| **Sub-Agents** (Task) | 200K | HAL8000 spawns | Research, context discovery |

---

## When to Use

### ALWAYS Use for:

1. **User Requests Visual Content**
   - "Generate an image of..."
   - "Create a picture of..."
   - "Show me what [X] looks like"
   - "Make an illustration of..."

2. **Conceptual Visualization**
   - Abstract concepts that benefit from visual representation
   - Design mockups or prototypes
   - Character/scene descriptions
   - Technical visualizations

3. **Creative Content**
   - Artistic interpretations
   - Style explorations
   - Visual brainstorming

### NEVER Use for:

- Technical diagrams (use diagram-generation tool instead)
- Text-heavy content (use document generation)
- Simple shapes/charts (use diagram-generation)
- Real-time image editing (not supported)

---

## Command Pattern

### Basic Usage

```bash
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "futuristic CPU with glowing circuits, cyberpunk style" \
  --output data/images/cpu.png
```

### With Quality Control

```bash
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "detailed portrait of AI assistant robot" \
  --model sdxl \
  --steps 30 \
  --width 1024 \
  --height 1024 \
  --output data/images/robot-portrait.png
```

### Fast Generation

```bash
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "simple robot sketch" \
  --model sd15 \
  --steps 15 \
  --output data/images/quick-sketch.png
```

---

## Available Models

| Model | Size | VRAM | Speed (RTX 3090) | Quality | Best For |
|-------|------|------|------------------|---------|----------|
| **sdxl** (default) | 6.5GB | 6-8GB | 3-5s | ⭐⭐⭐⭐⭐ | High quality, production |
| **sd15** | 4GB | 4-5GB | 1-2s | ⭐⭐⭐⭐ | Fast iterations, prototypes |

**RTX 3090 Capacity**: 24GB VRAM - can handle all models with room to spare

---

## Usage Protocol

### Step 1: Enhance User Prompt

```
User: "Generate an image of a robot"
    ↓
Claude enhances:
  "friendly humanoid robot assistant, modern design, clean background,
   detailed rendering, professional quality, no text, no watermarks"
```

**Best Practices**:
- Add style descriptors (detailed, professional, clean, modern, etc.)
- Specify quality (high quality, detailed, professional)
- Add negative guidance (no text, no watermarks, no blurry)
- Include context (background, lighting, perspective)

### Step 2: Select Appropriate Model

```python
# Default: High quality
--model sdxl --steps 20-25

# User wants fast result
--model sd15 --steps 15

# User wants maximum quality
--model sdxl --steps 40-50
```

### Step 3: Choose Output Location

```bash
# Standard location
--output data/images/descriptive-name.png

# Use descriptive, hyphenated filenames
--output data/images/cyberpunk-city-night.png
```

### Step 4: Execute and Return Path

```bash
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "enhanced prompt" \
  --model sdxl \
  --output data/images/filename.png

# Return to user
"Image generated: data/images/filename.png"
```

---

## RAM Efficiency Pattern

**❌ WRONG (Hypothetical):**
```
Load image processing library → Process in HAL8000 RAM
Result: RAM += 50K-100K tokens
```

**✅ RIGHT (Docker External):**
```
Delegate to Docker container → Process externally
Container returns file path → Load only path
Result: RAM += ~10 tokens (file path only)
```

**RAM Savings**: 99.99% (path vs full processing)

---

## Performance Expectations

### First-Time Setup
```
Build Docker image: 5-10 minutes (one-time)
Download SDXL model: 5-10 minutes (one-time, 6.5GB)
Total setup: ~15-20 minutes
```

### Subsequent Usage
```
Container startup:  2 seconds
Model load:         3-5 seconds
Image generation:   3-8 seconds (depending on steps)
Container cleanup:  1 second
─────────────────────────────────
Total per image:    ~10-15 seconds
```

### Batch Generation
If generating multiple images in sequence, consider suggesting batch workflow to user for efficiency.

---

## Storage Layout

```
C: drive (~3-5GB):
  └── Docker images/
      └── hal8000-image-gen:latest (~3GB)

D: drive (/mnt/d/~HAL8000/):
  ├── .docker-cache/models/          (~6-20GB)
  │   └── checkpoints/
  │       ├── sd_xl_base_1.0.safetensors (6.5GB)
  │       └── v1-5-pruned-emaonly.safetensors (4GB)
  │
  ├── data/images/                   (grows)
  │   └── *.png (2-5MB each)
  │
  └── .claude/tools/image-generation/
      ├── Dockerfile
      ├── entrypoint.py
      ├── HAL-generate-image.py
      ├── build-image.sh
      ├── README.md
      └── CLAUDE.md
```

---

## Example Scenarios

### Scenario 1: Technical Illustration

```
User: "Generate an image of quantum computer hardware"

Claude:
  --prompt "detailed technical illustration of quantum computer hardware,
            professional diagram style, clean background, high detail,
            technical accuracy, no text labels"
  --model sdxl
  --steps 25
  --output data/images/quantum-computer-hardware.png
```

### Scenario 2: Conceptual Art

```
User: "Create a picture of a futuristic city"

Claude:
  --prompt "futuristic cyberpunk city at night, neon lights, flying cars,
            towering skyscrapers, atmospheric, detailed architecture,
            professional concept art, cinematic"
  --model sdxl
  --steps 30
  --output data/images/futuristic-city-concept.png
```

### Scenario 3: Character Design

```
User: "Show me what an AI assistant robot would look like"

Claude:
  --prompt "friendly humanoid AI assistant robot, modern sleek design,
            white and blue color scheme, approachable appearance,
            professional rendering, clean studio background, detailed"
  --model sdxl
  --steps 30
  --output data/images/ai-assistant-robot.png
```

### Scenario 4: Fast Iteration

```
User: "Quick sketch of a spaceship"

Claude:
  --prompt "simple sketch of futuristic spaceship, line art style"
  --model sd15
  --steps 15
  --output data/images/spaceship-sketch.png
```

---

## Error Handling

### Image Not Built Yet

```
Error: "docker: image 'hal8000-image-gen:latest' not found"

Response to user:
"The image generation system needs to be set up first.
 Please run: cd .claude/tools/image-generation && ./build-image.sh
 This is a one-time setup that takes about 10 minutes."
```

### GPU Not Accessible

```
Error: "could not select device driver"

Response to user:
"GPU support is not available. Please check:
 1. NVIDIA drivers are installed
 2. Docker Desktop has GPU support enabled
 3. NVIDIA Container Toolkit is installed"
```

### Out of Disk Space

```
Error: "no space left on device"

Response to user:
"Not enough disk space. The model cache requires ~6.5GB on D: drive.
 Current models location: /mnt/d/~HAL8000/.docker-cache/models/
 You can free space or move the cache."
```

---

## Integration with HAL8000 Architecture

### Tool Discovery

Discoverable via:
1. **Tool index**: `.claude/indexes/tools.json` (when updated)
2. **Direct path**: `.claude/tools/image-generation-tool.md` (this file)
3. **File system search**: Indexed for keyword discovery
4. **Context finder**: `/HAL-context-find image` loads this doc

### Architectural Consistency

**Follows HAL8000 Principles**:
- ✅ **Von Neumann**: External I/O device pattern
- ✅ **Unix Philosophy**: Single responsibility (image generation only)
- ✅ **Assembly**: Direct hardware access (GPU via Docker)
- ✅ **Zero RAM Impact**: External execution, minimal context
- ✅ **Proven Pattern**: Mirrors diagram-generation architecture

### Comparison to Other Tools

| Tool | Type | RAM Impact | Speed | Context | Best For |
|------|------|-----------|-------|---------|----------|
| **image-generation** | Docker | 0 | 10-15s | External | Visual content |
| **diagram-generation** | Docker | 0 | <1s | External | Technical diagrams |
| **docling-cli** | PowerShell | 0 | Variable | External | Document processing |
| **gemini-cli** | CLI | 0 | Variable | 1M tokens | Heavy analysis |
| **research-synthesizer** | Agent | Isolated | Variable | 200K | Research tasks |

---

## Maintenance

### Update Docker Image

```bash
cd .claude/tools/image-generation
docker rmi hal8000-image-gen:latest
./build-image.sh
```

### Clear Model Cache

```bash
# Free up ~6-20GB (models will re-download on next use)
rm -rf /mnt/d/~HAL8000/.docker-cache/models/*
```

### Check Disk Usage

```bash
# Docker images
docker images | grep hal8000-image-gen

# Model cache
du -sh /mnt/d/~HAL8000/.docker-cache/models/

# Generated images
du -sh /mnt/d/~HAL8000/data/images/
```

---

## Version & Status

**Current Version**: 1.0.0
**Status**: Production-ready (requires initial build)
**Created**: 2025-10-22
**Last Updated**: 2025-10-22

**Tested On**:
- Docker Desktop with WSL2
- RTX 3090 (24GB VRAM)
- Ubuntu 22.04 (WSL2)

**Future Enhancements**:
- Additional models (FLUX, custom checkpoints)
- ControlNet support (pose guidance, depth maps)
- LoRA support (style variations)
- Batch generation (multiple images at once)
- Cloud fallback (Replicate API if Docker unavailable)
- Inpainting/outpainting support
- Image-to-image transformation

---

## Credentials & Configuration

**No API Keys Required**: Fully local execution
**GPU Required**: Yes (CUDA-capable NVIDIA GPU)
**Docker Required**: Yes (Docker Desktop with GPU support)
**Internet Required**: Only for initial model download
**Offline Capable**: Yes (after models downloaded)

---

## Summary

Image Generation Tool is HAL8000's **visual content creation device**:
- **Docker-based** for isolation and reproducibility
- **GPU-accelerated** for fast generation (RTX 3090)
- **Zero RAM impact** on HAL8000 session
- **Production-ready** quality with SDXL
- **Proactively used** when user requests visual content
- **Returns file paths** not raw image data

**Integration Pattern:**
```
User Request → HAL8000 enhances prompt → Docker generates → File saved → Path returned
```

This extends HAL8000's capabilities to visual domain while maintaining efficient resource usage and architectural consistency.
