#!/usr/bin/env python3
"""
HAL8000-Assistant Image Generation Container Entrypoint

Handles model downloading, ComfyUI server management, and image generation.
"""

import argparse
import os
import sys
import json
import time
import subprocess
import urllib.request
from pathlib import Path

def log(message):
    """Print to stderr to keep stdout clean"""
    print(f"[HAL-IMAGE-GEN] {message}", file=sys.stderr)

def download_model(url, output_path):
    """Download a model file with progress reporting"""
    log(f"Downloading model to {output_path}...")

    def report_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(downloaded * 100 / total_size, 100)
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            sys.stderr.write(f"\r[HAL-IMAGE-GEN] Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)")
            sys.stderr.flush()

    urllib.request.urlretrieve(url, output_path, reporthook=report_progress)
    sys.stderr.write("\n")
    log(f"Download complete: {output_path}")

def ensure_model(model_name, models_dir):
    """Download model if not already cached"""

    # Model registry
    models = {
        'sdxl': {
            'filename': 'sd_xl_base_1.0.safetensors',
            'url': 'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors',
            'size_gb': 6.5
        },
        'sd15': {
            'filename': 'v1-5-pruned-emaonly.safetensors',
            'url': 'https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors',
            'size_gb': 4.0
        }
    }

    if model_name not in models:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(models.keys())}")

    model_info = models[model_name]

    # All models go in checkpoints/
    model_path = Path(models_dir) / 'checkpoints' / model_info['filename']

    if model_path.exists():
        log(f"Model {model_name} already cached at {model_path}")
        return str(model_path)

    log(f"Model {model_name} not found. Downloading (~{model_info['size_gb']}GB)...")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    download_model(model_info['url'], str(model_path))

    return str(model_path)

def start_comfyui_server():
    """Start ComfyUI server and wait for it to be ready"""
    log("Starting ComfyUI server...")

    proc = subprocess.Popen(
        ["python3", "main.py", "--listen", "127.0.0.1", "--port", "8188"],
        cwd="/app/ComfyUI",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for server to be ready (max 60 seconds)
    import socket
    for attempt in range(60):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 8188))
            sock.close()
            if result == 0:
                log("ComfyUI server ready")
                return proc
        except:
            pass
        time.sleep(1)

    proc.terminate()
    raise RuntimeError("ComfyUI server failed to start within 60 seconds")

def generate_image_via_api(prompt, model_path, output_path, width=1024, height=1024, steps=20):
    """Generate image using ComfyUI API"""
    import requests

    log(f"Generating image: '{prompt[:50]}...'")
    log(f"Parameters: {width}x{height}, {steps} steps")

    # Get model filename
    model_filename = Path(model_path).name

    # Build workflow: SDXL/SD1.5 use CheckpointLoaderSimple
    workflow = {
        "3": {
            "inputs": {
                "seed": int(time.time() * 1000) % (2**32),
                "steps": steps,
                "cfg": 7.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {"ckpt_name": model_filename},
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {"text": prompt, "clip": ["4", 1]},
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {"text": "text, watermark, blurry, low quality", "clip": ["4", 1]},
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        }
    }

    # Submit to API
    log("Submitting generation request...")
    response = requests.post(
        "http://127.0.0.1:8188/prompt",
        json={"prompt": workflow}
    )

    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.text}")

    result = response.json()
    prompt_id = result.get('prompt_id')

    if not prompt_id:
        raise RuntimeError(f"No prompt_id in response: {result}")

    log(f"Generation queued (ID: {prompt_id}). Waiting for completion...")

    # Poll for completion
    output_dir = Path("/app/ComfyUI/output")

    # Timeout: 10 minutes (generous for first-time model load into VRAM)
    max_wait = 600

    start_time = time.time()

    while time.time() - start_time < max_wait:
        # Check history endpoint
        try:
            hist_response = requests.get(f"http://127.0.0.1:8188/history/{prompt_id}")
            if hist_response.status_code == 200:
                history = hist_response.json()
                if prompt_id in history:
                    outputs = history[prompt_id].get('outputs', {})
                    if outputs:
                        log("Generation complete!")

                        # Find the generated image
                        for node_id, node_output in outputs.items():
                            if 'images' in node_output:
                                for img in node_output['images']:
                                    filename = img.get('filename')
                                    if filename:
                                        src_path = output_dir / filename
                                        if src_path.exists():
                                            # Move to desired output location
                                            import shutil
                                            shutil.copy2(src_path, output_path)
                                            log(f"Image saved to {output_path}")
                                            return output_path
        except Exception as e:
            log(f"Polling error (retrying): {e}")

        time.sleep(2)

    raise RuntimeError(f"Image generation timed out after {max_wait}s")

def add_text_overlay(image_path, text, position='south', fontsize=72, color='white'):
    """Add text overlay to generated image using ImageMagick"""
    import subprocess

    log(f"Adding text overlay: '{text}'")

    # Temporary file for output
    temp_output = image_path + ".tmp"

    # Build ImageMagick command
    cmd = [
        'convert', image_path,
        '-pointsize', str(fontsize),
        '-fill', color,
        '-stroke', 'black',
        '-strokewidth', '2',
        '-gravity', position,
        '-annotate', '+0+20', text,
        temp_output
    ]

    # Execute
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Text overlay failed: {result.stderr}")

    # Replace original with overlay version
    import shutil
    shutil.move(temp_output, image_path)
    log(f"Text overlay applied: '{text}'")

def main():
    parser = argparse.ArgumentParser(description='HAL8000-Assistant Image Generation Container')
    parser.add_argument('--prompt', required=True, help='Image generation prompt')
    parser.add_argument('--model', default='sdxl', choices=['sdxl', 'sd15'],
                        help='Model to use')
    parser.add_argument('--output', required=True, help='Output image path')
    parser.add_argument('--width', type=int, default=1024, help='Image width')
    parser.add_argument('--height', type=int, default=1024, help='Image height')
    parser.add_argument('--steps', type=int, default=20, help='Generation steps')
    parser.add_argument('--text', help='Optional text to overlay on image')
    parser.add_argument('--text-position', default='south',
                        choices=['north', 'south', 'east', 'west', 'center'],
                        help='Text position (default: south)')
    parser.add_argument('--text-size', type=int, default=72, help='Text font size (default: 72)')
    parser.add_argument('--text-color', default='white', help='Text color (default: white)')

    args = parser.parse_args()

    server_proc = None

    try:
        # 1. Ensure model is available
        model_path = ensure_model(args.model, "/models")

        # 2. Start ComfyUI server
        server_proc = start_comfyui_server()

        # 3. Generate image
        generate_image_via_api(
            prompt=args.prompt,
            model_path=model_path,
            output_path=args.output,
            width=args.width,
            height=args.height,
            steps=args.steps
        )

        # 4. Add text overlay if requested
        if args.text:
            add_text_overlay(
                image_path=args.output,
                text=args.text,
                position=args.text_position,
                fontsize=args.text_size,
                color=args.text_color
            )

        log("SUCCESS: Image generation complete")
        sys.exit(0)

    except Exception as e:
        log(f"ERROR: {e}")
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    finally:
        # Cleanup
        if server_proc:
            log("Shutting down ComfyUI server...")
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except:
                server_proc.kill()

if __name__ == '__main__':
    main()
