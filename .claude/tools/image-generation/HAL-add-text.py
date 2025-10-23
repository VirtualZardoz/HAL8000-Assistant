#!/usr/bin/env python3
"""
HAL8000 Text Overlay Tool

Adds text overlay to existing images using ImageMagick (via Docker).
Fast and efficient - no image regeneration required.

Usage:
    python3 HAL-add-text.py --input image.png --text "Title" --output titled.png
"""

import argparse
import subprocess
import sys
from pathlib import Path

def add_text_overlay(
    input_path,
    output_path,
    text,
    position='south',
    fontsize=72,
    color='white'
):
    """
    Add text overlay to existing image using ImageMagick in Docker.

    Args:
        input_path: Path to existing image
        output_path: Path to save result
        text: Text to overlay
        position: Position (north, south, east, west, center)
        fontsize: Font size in points
        color: Text color

    Returns:
        Path to output image
    """

    # Resolve paths
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get directories for volume mounts
    input_dir = input_path.parent
    output_dir = output_path.parent
    input_filename = input_path.name
    output_filename = output_path.name

    # Build Docker command
    # Use the existing hal8000-image-gen image which has ImageMagick
    # Override entrypoint to run convert directly
    cmd = [
        'docker', 'run',
        '--rm',
        '--entrypoint', 'convert',  # Override Python entrypoint
        '-v', f'{input_dir}:/input:ro',  # Read-only input
        '-v', f'{output_dir}:/output',    # Writable output
        'hal8000-image-gen:latest',
        f'/input/{input_filename}',
        '-pointsize', str(fontsize),
        '-fill', color,
        '-stroke', 'black',
        '-strokewidth', '3',
        '-gravity', position,
        '-annotate', '+0+50', text,
        f'/output/{output_filename}'
    ]

    print(f"Adding text overlay to {input_path}...", file=sys.stderr)
    print(f"Text: '{text}'", file=sys.stderr)
    print(f"Position: {position}, Size: {fontsize}, Color: {color}", file=sys.stderr)
    print("", file=sys.stderr)

    # Run Docker command
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"\nError adding text overlay:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Docker container exited with code {result.returncode}")

    # Verify output exists
    if not output_path.exists():
        raise RuntimeError(f"Text overlay completed but output file not found: {output_path}")

    # Success
    file_size = output_path.stat().st_size / (1024 * 1024)
    print(f"\n✓ Text overlay complete: {output_path}", file=sys.stderr)
    print(f"✓ File size: {file_size:.2f} MB", file=sys.stderr)

    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='HAL8000 Text Overlay Tool - Add text to existing images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic title:
    %(prog)s --input photo.png --text "My Title" --output titled.png

  Large centered text:
    %(prog)s --input image.png --text "LOGO" --position center --size 150 --output logo.png

  Bottom caption:
    %(prog)s --input pic.png --text "Caption here" --position south --size 48 --output captioned.png

Positions:
  north  - Top of image
  south  - Bottom of image (default)
  east   - Right side
  west   - Left side
  center - Center of image

Notes:
  - Text has black stroke outline for readability
  - Uses ImageMagick via Docker (fast, <1 second)
  - Original image unchanged (output to new file)
  - Supports all image formats (PNG, JPG, etc.)
        """
    )

    parser.add_argument(
        '--input',
        required=True,
        help='Input image file path'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Output image file path'
    )

    parser.add_argument(
        '--text',
        required=True,
        help='Text to overlay on image'
    )

    parser.add_argument(
        '--position',
        default='south',
        choices=['north', 'south', 'east', 'west', 'center'],
        help='Text position (default: south - bottom)'
    )

    parser.add_argument(
        '--size',
        type=int,
        default=72,
        help='Font size in points (default: 72)'
    )

    parser.add_argument(
        '--color',
        default='white',
        help='Text color: white, black, red, blue, or hex #RRGGBB (default: white)'
    )

    args = parser.parse_args()

    # Add text overlay
    try:
        add_text_overlay(
            input_path=args.input,
            output_path=args.output,
            text=args.text,
            position=args.position,
            fontsize=args.size,
            color=args.color
        )
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
