# Image Generation Tool - Installation Guide

Quick start guide for setting up the HAL8000-Assistant Image Generation system.

## Prerequisites

Before installation, ensure you have:

- [x] **Docker Desktop** installed with WSL2 backend
- [x] **NVIDIA GPU** (you have RTX 3090 ✓)
- [x] **NVIDIA drivers** installed
- [x] **NVIDIA Container Toolkit** (for Docker GPU support)
- [x] **~10-37GB free disk space** (3GB C:, 7-34GB D: depending on models)

## Quick Start (5 Steps)

### 1. Navigate to Tool Directory

```bash
cd /mnt/d/~HAL8000-Assistant/.claude/tools/image-generation
```

### 2. Build Docker Image

```bash
./build-image.sh
```

**Expected output:**
```
Building Docker image: hal8000-image-gen:latest
This will take 5-10 minutes...
[Docker build progress...]
✓ Build complete!
```

**Time**: ~5-10 minutes
**Size**: ~3GB

### 3. Test GPU Access

```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**Expected**: Should show your RTX 3090 info

**If error**: See troubleshooting section below

### 4. Generate First Test Image

```bash
python3 HAL-generate-image.py \
  --prompt "test image: simple red circle" \
  --model sd15 \
  --steps 10 \
  --output /tmp/test.png
```

**First run**: Downloads SD1.5 model (~4GB, 3-5 minutes)
**After that**: ~5-10 seconds

### 5. Generate Production-Quality Image

```bash
python3 HAL-generate-image.py \
  --prompt "futuristic computer CPU with glowing circuits, cyberpunk style, detailed" \
  --model sdxl \
  --steps 25 \
  --output ~/cpu-test.png
```

**First SDXL run**: Downloads model (~6.5GB, 5-10 minutes)
**After that**: ~10-15 seconds

---

## Verification

Check that everything is working:

```bash
# 1. Docker image exists
docker images | grep hal8000-image-gen
# Should show: hal8000-image-gen:latest

# 2. Model cache directory created
ls -lh /mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/
# Should show downloaded models

# 3. Test image generated
ls -lh ~/cpu-test.png
# Should show ~2-5MB PNG file

# 4. Open image to verify quality
# (Use Windows Explorer: \\wsl$\Ubuntu\home\<user>\cpu-test.png)
```

---

## Troubleshooting

### Error: "Docker not found"

**Problem**: Docker Desktop not installed or not in PATH

**Solution**:
```bash
# Install Docker Desktop for Windows
# Download from: https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
```

---

### Error: "could not select device driver"

**Problem**: NVIDIA Docker support not configured

**Solution**:

1. **Check NVIDIA drivers**:
```bash
nvidia-smi
# Should show GPU info
```

2. **Install NVIDIA Container Toolkit** (if needed):
```bash
# Add NVIDIA repo
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Restart Docker
sudo systemctl restart docker
```

3. **Verify GPU access in Docker**:
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

---

### Error: "no space left on device"

**Problem**: Not enough disk space

**Check disk usage**:
```bash
df -h /mnt/d
df -h /mnt/c
```

**Solution**:
- Need ~3GB on C: (Docker image)
- Need ~7-20GB on D: (models)

**Clear space** or **move Docker data to D:**
```
Docker Desktop → Settings → Resources → Advanced → Disk image location
Change to D:\Docker\wsl\data
```

---

### Error: "Download failed"

**Problem**: Network issue or HuggingFace timeout

**Solution**:

Try again (may be temporary):
```bash
python3 HAL-generate-image.py --prompt "test" --output test.png
```

Or manually download:
```bash
cd /mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/

# SDXL (6.5GB - auto-downloads)
wget https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors

# SD1.5 (4GB - auto-downloads)
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors

# FLUX (23GB - REQUIRES MANUAL DOWNLOAD, see below)
```

---

### FLUX Model Installation (Manual Required)

**Problem**: FLUX.1-dev is a gated model requiring HuggingFace authentication

**Solution** (Manual Download):

1. **Create HuggingFace Account**:
   - Go to https://huggingface.co/
   - Sign up or log in

2. **Accept FLUX License**:
   - Visit https://huggingface.co/black-forest-labs/FLUX.1-dev
   - Click "Access repository" or "Agree and access"
   - Accept the terms and conditions

3. **Download Model File**:

   **Option A: Browser Download**
   - Click "Files and versions" tab
   - Find `flux1-dev.safetensors` (23.8 GB)
   - Click download icon (↓)
   - Save to: `/mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/`

   **Option B: CLI Download with Token**
   ```bash
   # Get your token: https://huggingface.co/settings/tokens
   # Create a new token with "read" access

   cd /mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/

   wget --header="Authorization: Bearer YOUR_HF_TOKEN_HERE" \
     https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors
   ```

   **Option C: Move from Downloads**
   ```bash
   # If you downloaded to Windows Downloads folder:
   mv /mnt/c/Users/YOUR_USERNAME/Downloads/flux1-dev.safetensors \
      /mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/
   ```

4. **Verify File**:
   ```bash
   ls -lh /mnt/d/~HAL8000-Assistant/.docker-cache/models/checkpoints/flux1-dev.safetensors
   # Should show: ~23GB file
   ```

5. **Test Generation**:
   ```bash
   python3 HAL-generate-image.py \
     --prompt "test photorealistic landscape" \
     --model flux \
     --output test-flux.png
   ```

---

### Error: "Image generation timed out"

**Problem**: Generation taking longer than expected

**Solutions**:
1. **Reduce steps**: `--steps 15` instead of 25
2. **Reduce resolution**: `--width 512 --height 512`
3. **Try SD1.5**: Faster than SDXL
4. **Check GPU utilization**: `nvidia-smi` during generation

---

## Performance Tuning

### Fast Mode (Prototyping)
```bash
--model sd15 --steps 15
# ~5-8 seconds per image
```

### Balanced Mode (Default)
```bash
--model sdxl --steps 20
# ~10-12 seconds per image
```

### Quality Mode (Final Output)
```bash
--model sdxl --steps 40
# ~15-20 seconds per image
```

---

## Uninstallation

To completely remove the system:

```bash
# 1. Remove Docker image
docker rmi hal8000-image-gen:latest

# 2. Remove model cache
rm -rf /mnt/d/~HAL8000-Assistant/.docker-cache/models/

# 3. Remove generated images
rm -rf /mnt/d/~HAL8000-Assistant/data/images/*.png

# 4. Remove tool files (optional)
rm -rf /mnt/d/~HAL8000-Assistant/.claude/tools/image-generation/
```

**Disk space freed**: ~10-20GB

---

## Next Steps

Once installed successfully:

1. **Read README.md** for full usage documentation
2. **Read CLAUDE.md** to understand HAL8000-Assistant integration
3. **Test various prompts** to learn effective prompt engineering
4. **Ask HAL8000-Assistant** to generate images (Claude will use this tool automatically)

---

## Getting Help

If you encounter issues:

1. **Check logs**:
   ```bash
   docker logs $(docker ps -a | grep hal8000-image-gen | awk '{print $1}')
   ```

2. **Verify prerequisites**:
   - Docker Desktop running
   - GPU accessible: `nvidia-smi`
   - Enough disk space: `df -h`

3. **Rebuild**:
   ```bash
   docker rmi hal8000-image-gen:latest
   ./build-image.sh
   ```

4. **Check Docker**:
   ```bash
   docker ps
   docker system df
   docker info | grep -i runtime
   ```

---

## Success Criteria

Installation is successful when:

✓ Docker image built: `docker images | grep hal8000-image-gen`
✓ GPU accessible: `docker run --rm --gpus all nvidia/cuda nvidia-smi`
✓ Model downloaded: `ls .docker-cache/models/checkpoints/`
✓ Image generated: `python3 HAL-generate-image.py --prompt "test" --output test.png`
✓ Output exists and is valid PNG: `file test.png`

**You're ready!** Ask Claude to generate images.
