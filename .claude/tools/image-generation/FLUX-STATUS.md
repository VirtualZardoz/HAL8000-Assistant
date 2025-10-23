# FLUX Model Status

**Status**: NOT SUPPORTED (Removed in v1.6.0)

## Investigation Summary

FLUX.1-dev was investigated during October 2025 development but found to be incompatible with our HAL8000 setup:

- **Model Size**: 23GB (UNet + CLIP encoders + VAE)
- **Performance**: Timeouts after 15 minutes with low GPU utilization (21%)
- **Root Cause**: Likely ComfyUI compatibility issues or missing custom nodes
- **Decision**: Removed from supported models list

## What Worked

- ✅ Downloaded all FLUX model files successfully
- ✅ Implemented proper DualCLIPLoader + UNETLoader workflow
- ✅ Model files loaded into ComfyUI

## What Didn't Work

- ❌ Generation always timed out (15 minutes)
- ❌ Low GPU utilization despite 24GB VRAM available
- ❌ No clear error messages from ComfyUI

## Current Recommendation

Use SDXL instead:
- **Quality**: Excellent (⭐⭐⭐⭐⭐)
- **Speed**: 3-5 seconds (after model load)
- **Size**: 6.5GB (much more manageable)
- **Reliability**: 100% success rate

## Future Investigation

FLUX could be revisited if:
1. ComfyUI compatibility improves
2. Custom nodes become available for FLUX
3. Alternative backends emerge (e.g., direct PyTorch implementation)
4. Cloud-based FLUX services become viable

For now, SDXL + SD1.5 + text overlay provides excellent results without the complexity.
