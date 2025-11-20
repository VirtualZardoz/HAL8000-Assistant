#!/usr/bin/env python3
"""
HAL8000-Assistant Image Generation Tool

Generates AI images via Dockerized Stable Diffusion.
Architecture mirrors HAL-generate-diagram.py (proven pattern).

Usage:
    python3 HAL-generate-image.py --prompt "a robot" --output image.png
    python3 HAL-generate-image.py --prompt "cyberpunk city" --model sdxl --steps 30 --output city.png
"""

import argparse
import subprocess
import sys
from pathlib import Path

def generate_image(
    prompt,
    output_path,
    model='sdxl',
    width=1024,
    height=1024,
    steps=20,
    text=None,
    text_position='south',
    text_size=72,
    text_color='white'
):
    """
    Generate AI image using Docker container with GPU acceleration.

    Args:
        prompt: Text description of desired image
        output_path: Where to save generated image (absolute or relative)
        model: Which model to use ('sdxl', 'sd15')
        width: Image width in pixels (default: 1024)
        height: Image height in pixels (default: 1024)
        steps: Generation steps - more = better quality but slower (default: 20)
        text: Optional text to overlay on image (default: None)
        text_position: Position of text overlay (default: 'south')
        text_size: Font size for text overlay (default: 72)
        text_color: Color of text overlay (default: 'white')

    Returns:
        Path to generated image

    Raises:
        RuntimeError: If Docker command fails
    """

    # Resolve paths
    output_path = Path(output_path).resolve()
    output_dir = output_path.parent
    output_filename = output_path.name

    # Model cache on D: drive (hybrid approach)
    model_cache = Path('/mnt/d/~HAL8000-Assistant/.docker-cache/models')
    model_cache.mkdir(parents=True, exist_ok=True)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build Docker command
    cmd = [
        'docker', 'run',
        '--rm',                                    # Remove container after completion
        '--gpus', 'all',                           # Enable GPU access (RTX 3090)
        '-v', f'{model_cache}:/models',            # Model cache (persistent)
        '-v', f'{output_dir}:/output',             # Output directory
        'hal8000-image-gen:latest',                # Our Docker image
        '--prompt', prompt,
        '--model', model,
        '--output', f'/output/{output_filename}',
        '--width', str(width),
        '--height', str(height),
        '--steps', str(steps)
    ]

    # Add text overlay parameters if provided
    if text:
        cmd.extend(['--text', text])
        cmd.extend(['--text-position', text_position])
        cmd.extend(['--text-size', str(text_size)])
        cmd.extend(['--text-color', text_color])

    # Display generation info
    print(f"Generating image with {model.upper()}...", file=sys.stderr)
    print(f"Prompt: {prompt}", file=sys.stderr)
    print(f"Output: {output_path}", file=sys.stderr)
    print(f"Parameters: {width}x{height}, {steps} steps", file=sys.stderr)
    print("", file=sys.stderr)

    # Run container
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

    # Check for errors
    if result.returncode != 0:
        print(f"\nError during image generation:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Docker container exited with code {result.returncode}")

    # Verify output exists
    if not output_path.exists():
        raise RuntimeError(f"Image generation completed but output file not found: {output_path}")

    # Success
    file_size = output_path.stat().st_size / (1024 * 1024)
    print(f"\n✓ Image saved: {output_path}", file=sys.stderr)
    print(f"✓ File size: {file_size:.2f} MB", file=sys.stderr)

    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='HAL8000-Assistant AI Image Generation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage:
    %(prog)s --prompt "futuristic CPU" --output cpu.png

  High quality with SDXL (default):
    %(prog)s --prompt "cyberpunk city at night" --steps 30 --output city.png

  Fast generation with SD 1.5:
    %(prog)s --prompt "a robot assistant" --model sd15 --output robot.png

  Custom dimensions (landscape):
    %(prog)s --prompt "mountain vista" --width 1920 --height 1080 --output vista.png

  Maximum quality:
    %(prog)s --prompt "detailed portrait" --model sdxl --steps 50 --output portrait.png

Models:
  sdxl    - Stable Diffusion XL (best quality, ~6.5GB, 3-5s on RTX 3090)
  sd15    - Stable Diffusion 1.5 (faster, ~4GB, 1-2s on RTX 3090)

Notes:
  - First run downloads model (~6.5GB SDXL, ~4GB SD1.5)
  - Models cached in /mnt/d/~HAL8000-Assistant/.docker-cache/models/
  - Subsequent runs use cached models (much faster)
  - Requires Docker with GPU support (nvidia-docker)
  - Container runs isolated, no host pollution
        """
    )

    parser.add_argument(
        '--prompt',
        required=True,
        help='Text description of image to generate'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Output file path (e.g., image.png or /full/path/to/image.png)'
    )

    parser.add_argument(
        '--model',
        default='sdxl',
        choices=['sdxl', 'sd15'],
        help='Model to use (default: sdxl for best quality)'
    )

    parser.add_argument(
        '--width',
        type=int,
        default=1024,
        help='Image width in pixels (default: 1024)'
    )

    parser.add_argument(
        '--height',
        type=int,
        default=1024,
        help='Image height in pixels (default: 1024)'
    )

    parser.add_argument(
        '--steps',
        type=int,
        default=20,
        help='Generation steps: more = better quality, slower (default: 20, range: 10-50)'
    )

    parser.add_argument(
        '--text',
        help='Optional text to overlay on image'
    )

    parser.add_argument(
        '--text-position',
        default='south',
        choices=['north', 'south', 'east', 'west', 'center'],
        help='Text position (default: south - bottom of image)'
    )

    parser.add_argument(
        '--text-size',
        type=int,
        default=72,
        help='Text font size (default: 72)'
    )

    parser.add_argument(
        '--text-color',
        default='white',
        help='Text color: white, black, red, blue, or hex #RRGGBB (default: white)'
    )

    args = parser.parse_args()

    # Validate parameters
    if args.steps < 1 or args.steps > 100:
        parser.error("steps must be between 1 and 100")

    if args.width < 256 or args.width > 2048:
        parser.error("width must be between 256 and 2048")

    if args.height < 256 or args.height > 2048:
        parser.error("height must be between 256 and 2048")

    # Generate image
    try:
        generate_image(
            prompt=args.prompt,
            output_path=args.output,
            model=args.model,
            width=args.width,
            height=args.height,
            steps=args.steps,
            text=args.text,
            text_position=args.text_position,
            text_size=args.text_size,
            text_color=args.text_color
        )
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
