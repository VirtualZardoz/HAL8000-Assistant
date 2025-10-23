# Image Generation Tool - HAL8000 Integration

**Category:** External Tool (Dockerized)
**Purpose:** AI image generation via Stable Diffusion
**Architecture:** Docker container with GPU acceleration
**Pattern:** Mirrors diagram-generation tool (proven architecture)

---

## Quick Reference for Claude (HAL8000 CPU)

### When to Use

Use this tool when the user requests:
- "Generate an image of..."
- "Create a picture of..."
- "Make an illustration of..."
- "Show me what [X] looks like"
- Any visual content creation request

### How to Use

```bash
# Basic usage
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "user's request with style enhancements" \
  --model sdxl \
  --output data/images/descriptive-filename.png

# With text overlay
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "background or scene description" \
  --text "OVERLAY TEXT" \
  --text-position south \
  --text-size 96 \
  --output data/images/labeled-image.png
```

### Prompt Enhancement

**User says**: "Generate an image of a robot"
**Claude executes**:
```bash
python3 .claude/tools/image-generation/HAL-generate-image.py \
  --prompt "friendly humanoid robot assistant, modern design, clean background, detailed, professional" \
  --model sdxl \
  --steps 25 \
  --output data/images/robot-assistant.png
```

**Best Practices**:
- Enhance user prompts with style descriptors (detailed, professional, clean, modern, etc.)
- Add negative context in prompt if needed (avoid text, no watermarks, etc.)
- Choose appropriate model (sdxl for quality, sd15 for speed)
- Use descriptive filenames with hyphens

### Model Selection

```python
# Quality priority (default)
--model sdxl --steps 25

# Speed priority
--model sd15 --steps 15

# Maximum quality
--model sdxl --steps 40-50
```

### Common Use Cases

**1. Technical Diagrams**
```bash
--prompt "detailed technical diagram of [subject], clean, professional, white background"
--model sdxl
```

**2. Conceptual Art**
```bash
--prompt "concept art of [subject], detailed, professional illustration"
--model sdxl --steps 30
```

**3. Quick Sketches**
```bash
--prompt "simple sketch of [subject]"
--model sd15 --steps 15
```

**4. Portraits/Characters**
```bash
--prompt "portrait of [description], professional photography, detailed"
--model sdxl --steps 30
```

**5. Labeled Images (Text Overlay)**
```bash
--prompt "clean background for [subject]"
--text "TITLE OR LABEL"
--text-position south  # or north, center, east, west
--text-size 96
--text-color white
```

**Note on Text**: SD models cannot generate readable text - they produce gibberish. Use `--text` overlay for any text requirements. Text is rendered with ImageMagick (black stroke outline for readability).

### File Locations

**Generated Images**: `/mnt/d/~HAL8000/data/images/`
**Model Cache**: `/mnt/d/~HAL8000/.docker-cache/models/`
**Tool Directory**: `/mnt/d/~HAL8000/.claude/tools/image-generation/`

### First-Time Setup

If image generation fails with "image not found" error:
1. Build Docker image first: `cd .claude/tools/image-generation && ./build-image.sh`
2. First generation downloads models (~6.5GB, takes 5-10 minutes)
3. Subsequent generations use cached models (fast)

### Error Handling

```python
try:
    result = subprocess.run([...], check=True)
    print(f"Image generated: {output_path}")
except subprocess.CalledProcessError:
    print("Image generation failed. Possible causes:")
    print("1. Docker image not built (run ./build-image.sh)")
    print("2. GPU not accessible")
    print("3. Out of disk space")
```

### Performance Expectations

**RTX 3090**:
- SDXL: 3-5s (after model load)
- SD1.5: 1-2s (after model load)
- First run: +5-10 minutes (model download)
- Container overhead: ~5s

**Total time** (cached): ~10-15s per image

### Integration Pattern

```
User Request
    ↓
Claude (You) enhances prompt
    ↓
Execute HAL-generate-image.py
    ↓
Docker container generates image
    ↓
Return path to user
```

### Storage Impact

- **Docker image**: ~3GB (C: drive)
- **Model cache**: ~6.5GB SDXL + 4GB SD1.5 (D: drive)
- **Generated images**: ~2-5MB each (D: drive)

### RAM Impact on HAL8000 Session

**This tool has ZERO RAM impact!**
- Runs in external Docker container
- No context loaded into HAL8000 RAM
- Only returns image path (minimal tokens)

### Comparison to Other Tools

| Tool | Type | RAM Impact | Speed | Use Case |
|------|------|-----------|-------|----------|
| **image-generation** | External (Docker) | Zero | 10-15s | Visual content |
| **diagram-generation** | External (Docker) | Zero | <1s | Technical diagrams |
| **gemini-cli** | External (CLI) | Zero | Variable | Heavy analysis |
| **research-synthesizer** | Sub-agent | Isolated 200K | Variable | Research tasks |

---

## Architecture Details

### Why Docker?

Same proven pattern as diagram-generation:
- ✅ No host pollution (clean isolation)
- ✅ GPU access via `--gpus all`
- ✅ Reproducible results
- ✅ Easy maintenance (rebuild container)
- ✅ Portable (works on any Docker+GPU system)

### Container Lifecycle

```
Start (2s) → Load Model (3-5s) → Generate (3-8s) → Save → Exit (1s)
                   ↓
         Cached after first use
```

### File Flow

```
HAL-generate-image.py
    ↓ mounts volumes
Container sees:
    /models → /mnt/d/~HAL8000/.docker-cache/models (persistent)
    /output → /mnt/d/~HAL8000/data/images (persistent)
    ↓
Generated image saved to /output/filename.png
    ↓
Maps back to: /mnt/d/~HAL8000/data/images/filename.png
```

---

## Troubleshooting for Claude

### "Docker image not found"
→ Image not built yet. Guide user to run `./build-image.sh`

### "GPU not accessible"
→ NVIDIA Docker support issue. User needs to check Docker Desktop GPU settings

### "Model download failed"
→ Network issue or HuggingFace down. Suggest retry or manual download

### "Out of memory"
→ Shouldn't happen on RTX 3090 (24GB). Suggest reducing resolution or using SD1.5

---

## Version

**v1.0.0** - Initial implementation (2025-10-22)

**Future Enhancements**:
- Additional models (custom checkpoints, LoRA support)
- ControlNet support (pose guidance)
- LoRA support (style variations)
- Batch generation (multiple images at once)
- Cloud fallback (Replicate API if Docker unavailable)
