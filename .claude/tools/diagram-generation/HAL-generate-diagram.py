#!/usr/bin/env python3
"""
HAL Diagram Generation Command
Generate professional workflow diagrams from templates or custom specifications.

Usage: /HAL-generate-diagram [type] [title] [options]

Diagram Types:
- process-flow: Sequential chronological workflows
- swimlane: Multi-actor/system processes
- bpmn: Business Process Model Notation
- sipoc: Supplier-Input-Process-Output-Customer

Examples:
/HAL-generate-diagram process-flow "HAL Brainstorming Workflow"
/HAL-generate-diagram swimlane "User-HAL-Agent Interaction" --template=basic
/HAL-generate-diagram bpmn "System Architecture" --custom="path/to/spec.md"
"""

import argparse
import sys
import os
from pathlib import Path
import subprocess
import json
from datetime import datetime, timedelta

# HAL System Paths
HAL_ROOT = Path("/mnt/d/~HAL8000-Assistant")
TOOLS_DIR = HAL_ROOT / ".claude" / "tools" / "diagram-generation"
TEMPLATES_DIR = TOOLS_DIR / "templates"
OUTPUT_DIR = HAL_ROOT / "data" / "diagrams"

# Supported diagram types and their tools
DIAGRAM_TOOLS = {
    "process-flow": "mermaid",
    "swimlane": "mermaid",
    "bpmn": "mermaid",
    "sipoc": "mermaid"
}

def cleanup_old_temp_files(days_old=7):
    """Clean up temporary files older than specified days."""
    temp_dir = TOOLS_DIR / "temp"
    if not temp_dir.exists():
        return

    cutoff_date = datetime.now() - timedelta(days=days_old)
    cleaned_count = 0

    for file_path in temp_dir.glob("*"):
        if file_path.is_file():
            # Get file modification time
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_time < cutoff_date:
                try:
                    file_path.unlink()
                    cleaned_count += 1
                except Exception as e:
                    print(f"[WARNING] Could not delete {file_path}: {e}")

    if cleaned_count > 0:
        print(f"[CLEANUP] Removed {cleaned_count} temp files older than {days_old} days")

def ensure_directories():
    """Ensure required directories exist."""
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    (TOOLS_DIR / "temp").mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Automatic cleanup on startup
    cleanup_old_temp_files()

def get_template_path(diagram_type, template_name="default"):
    """Get path to diagram template."""
    template_file = f"{diagram_type}_{template_name}.txt"
    return TEMPLATES_DIR / template_file

def load_template(diagram_type, template_name="default"):
    """Load diagram template content."""
    template_path = get_template_path(diagram_type, template_name)

    if not template_path.exists():
        # Return basic template if specific not found
        return get_basic_template(diagram_type)

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_basic_template(diagram_type):
    """Generate basic template for diagram type."""
    templates = {
        "process-flow": """flowchart TD
    A[Start] --> B[Process Step]
    B --> C{Decision?}
    C -->|Yes| D[Action A]
    C -->|No| E[Action B]
    D --> F[End]
    E --> F""",

        "swimlane": """flowchart TD
    subgraph User ["👤 User"]
        A[Request]
        F[Review Result]
    end

    subgraph HAL ["🤖 HAL"]
        B[Process Request]
        E[Deliver Result]
    end

    subgraph System ["⚙️ System"]
        C[Execute]
        D[Generate Output]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F""",

        "bpmn": """@startuml
!theme plain

start
:Process Input;
if (Condition?) then (yes)
  :Action A;
else (no)
  :Action B;
endif
:Generate Output;
stop

@enduml""",

        "sipoc": """flowchart LR
    subgraph S ["Supplier"]
        S1[Input Provider]
    end

    subgraph I ["Input"]
        I1[Data/Request]
    end

    subgraph P ["Process"]
        P1[Core Process]
        P2[Transformation]
    end

    subgraph O ["Output"]
        O1[Result/Product]
    end

    subgraph C ["Customer"]
        C1[End User]
    end

    S1 --> I1
    I1 --> P1
    P1 --> P2
    P2 --> O1
    O1 --> C1"""
    }

    return templates.get(diagram_type, "")

def generate_diagram(diagram_type, title, content, output_format="png", width=None, height=None, scale=None):
    """Generate diagram using appropriate tool with quality options."""
    tool = DIAGRAM_TOOLS.get(diagram_type)
    if not tool:
        raise ValueError(f"Unsupported diagram type: {diagram_type}")

    # Create temporary source file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')

    if tool == "mermaid":
        source_file = TOOLS_DIR / "temp" / f"{safe_title}_{timestamp}.mmd"
        output_file = OUTPUT_DIR / f"{safe_title}_{timestamp}.{output_format}"

        # Write mermaid source
        with open(source_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Execute mermaid CLI via Docker container
        # Container mounts temp and output directories as volumes
        # Use absolute WSL paths directly (Docker Desktop handles WSL path translation)
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{str(TOOLS_DIR / 'temp')}:/workspace/temp:rw",
            "-v", f"{str(OUTPUT_DIR)}:/workspace/output:rw",
            "hal8000-mermaid:latest",
            "-i", f"/workspace/temp/{source_file.name}",
            "-o", f"/workspace/output/{output_file.name}"
        ]

        # Add quality options if specified
        if width:
            cmd.extend(["--width", str(width)])
        if height:
            cmd.extend(["--height", str(height)])
        if scale:
            cmd.extend(["--scale", str(scale)])

        # Default high quality settings
        if not scale:
            cmd.extend(["--scale", "2"])  # Default 2x for better quality

    elif tool == "plantuml":
        source_file = TOOLS_DIR / "temp" / f"{safe_title}_{timestamp}.puml"
        output_file = OUTPUT_DIR / f"{safe_title}_{timestamp}.{output_format}"

        # Write PlantUML source
        with open(source_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Execute PlantUML
        cmd = ["plantuml", "-t" + output_format, "-o", str(OUTPUT_DIR), str(source_file)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[OK] Diagram generated: {output_file}")
        print(f"[SRC] Source saved: {source_file}")
        return str(output_file)

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error generating diagram: {e}")
        print(f"   Command: {' '.join(cmd)}")
        print(f"   Error output: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"[ERROR] Tool not found: {tool}")
        print(f"   Please install {tool} CLI tool")
        return None

def substitute_template_variables(content, title, **kwargs):
    """Replace template variables with actual values."""
    # Basic substitutions
    substitutions = {
        "{{TITLE}}": title,
        "{{DATE}}": datetime.now().strftime("%Y-%m-%d"),
        "{{TIMESTAMP}}": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Add any additional kwargs
    for key, value in kwargs.items():
        substitutions[f"{{{{{key.upper()}}}}}"] = str(value)

    # Apply substitutions
    result = content
    for placeholder, value in substitutions.items():
        result = result.replace(placeholder, value)

    return result

def main():
    parser = argparse.ArgumentParser(
        description="Generate professional workflow diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument("diagram_type",
                       choices=list(DIAGRAM_TOOLS.keys()),
                       help="Type of diagram to generate")

    parser.add_argument("title",
                       help="Title for the diagram")

    parser.add_argument("--template", "-t",
                       default="default",
                       help="Template name to use (default: default)")

    parser.add_argument("--custom", "-c",
                       help="Path to custom specification file")

    parser.add_argument("--format", "-f",
                       choices=["png", "svg", "pdf"],
                       default="png",
                       help="Output format (default: png)")

    parser.add_argument("--output", "-o",
                       help="Custom output filename")

    parser.add_argument("--width", "-w",
                       type=int,
                       help="Diagram width in pixels")

    parser.add_argument("--height",
                       type=int,
                       help="Diagram height in pixels")

    parser.add_argument("--scale", "-s",
                       type=float,
                       help="Scale factor for resolution (e.g., 2.0 for 2x, 4.0 for 4x)")

    args = parser.parse_args()

    # Ensure directories exist
    ensure_directories()

    try:
        # Get diagram content
        if args.custom:
            # Load custom specification
            custom_path = Path(args.custom)
            if not custom_path.exists():
                print(f"[ERROR] Custom specification not found: {args.custom}")
                return 1

            with open(custom_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            # Load template
            content = load_template(args.diagram_type, args.template)

        # Apply variable substitutions
        content = substitute_template_variables(content, args.title)

        # Generate diagram
        output_path = generate_diagram(
            args.diagram_type,
            args.title,
            content,
            args.format,
            width=getattr(args, 'width', None),
            height=getattr(args, 'height', None),
            scale=getattr(args, 'scale', None)
        )

        if output_path:
            print(f"\n[SUCCESS] Diagram generated!")
            print(f"   Type: {args.diagram_type}")
            print(f"   Title: {args.title}")
            print(f"   Output: {output_path}")
            return 0
        else:
            return 1

    except Exception as e:
        print(f"[ERROR] {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())