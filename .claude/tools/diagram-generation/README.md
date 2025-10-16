# HAL8000 Diagram Generation Tool

## Overview

Professional workflow diagram generation using Mermaid CLI running in Docker container. This tool provides isolated, dependency-free diagram rendering with publication-quality output.

## Architecture

**Container as I/O Device Pattern:**
- Docker container = isolated rendering environment
- Python script = device driver (interfaces between HAL8000 and container)
- Volume mounts = data bus (file exchange)
- No host dependencies beyond Docker

## Installation

### Prerequisites
1. **Docker** - Required (tested with Docker Desktop on WSL2)
2. **Python 3** - Already available on system
3. **Node.js** - NOT required (containerized)

### Build the Image

```bash
cd .claude/tools/diagram-generation
./build-image.sh
```

This creates the `hal8000-mermaid:latest` image (~500MB) with:
- Node.js 20
- Mermaid CLI 11.12.0
- All Chrome/Puppeteer dependencies
- Configured for rootless execution

## Usage

### Basic Command

```bash
python3 .claude/tools/diagram-generation/HAL-generate-diagram.py [type] [title] [options]
```

### Diagram Types

- `process-flow` - Sequential chronological workflows
- `swimlane` - Multi-actor/system processes
- `bpmn` - Business Process Model Notation
- `sipoc` - Supplier-Input-Process-Output-Customer

### Examples

```bash
# Basic diagram (default 2x scale)
python3 .claude/tools/diagram-generation/HAL-generate-diagram.py process-flow "My Workflow"

# High-resolution (4x scale)
python3 .claude/tools/diagram-generation/HAL-generate-diagram.py swimlane "User Flow" --scale=4.0

# SVG vector output
python3 .claude/tools/diagram-generation/HAL-generate-diagram.py bpmn "Business Process" --format=svg

# Custom dimensions
python3 .claude/tools/diagram-generation/HAL-generate-diagram.py sipoc "Analysis" --width=1920 --height=1080

# Use built-in template
python3 .claude/tools/diagram-generation/HAL-generate-diagram.py process-flow "HAL Workflow" --template=hal-brainstorming
```

## Output Management

### Generated Files

- **Diagrams**: `/mnt/d/~HAL8000/data/diagrams/` - Final PNG/SVG/PDF files
- **Source**: `.claude/tools/diagram-generation/temp/` - Reusable .mmd templates

### File Naming

```
[Title]_[Timestamp].[extension]
My_Workflow_20251013_100234.png
```

### Automatic Cleanup

- Temp `.mmd` files older than 7 days are automatically removed on each run
- Keeps recent source files for iteration and debugging

## Performance

**Measured Performance (WSL2 + Docker Desktop):**
- Container startup: ~0.1s
- Diagram rendering (2x scale): ~0.6s
- **Total**: ~0.7-0.8s per diagram

**Scaling:**
- 2x scale (default): 610x1162px, ~37KB
- 4x scale (high-res): 1220x2324px, ~78KB

## Templates

### Built-in Templates

Located in `templates/` directory:
- `process-flow_hal-brainstorming.txt` - HAL 7000's complete 6-stage brainstorming workflow
- `process-flow_default.txt` - Basic sequential workflow
- `swimlane_default.txt` - User-HAL-System interaction
- `bpmn_default.txt` - Business process with gateways
- `sipoc_default.txt` - Process analysis framework

### Template Variables

- `{{TITLE}}` - Diagram title
- `{{DATE}}` - Current date
- `{{TIMESTAMP}}` - Current timestamp

### Creating Custom Templates

1. Create file: `templates/[type]_[name].txt`
2. Use Mermaid syntax for diagram content
3. Include template variables as needed
4. Use with: `--template=[name]`

## Docker Image Details

**Image**: `hal8000-mermaid:latest`
**Size**: ~500MB (includes full Chrome browser for rendering)
**Base**: `node:20-slim`

**What's Inside:**
- Node.js 20.19.5
- Mermaid CLI 11.12.0
- Puppeteer + Chrome headless
- All rendering dependencies (no host pollution)

**Security:**
- Runs with `--no-sandbox` flag (required for containerized Chrome)
- No network access needed after image build
- File access limited to mounted volumes

## Architecture Integration

**HAL8000 Principles:**

✅ **Unix Philosophy**
- Do one thing well: Render diagrams
- Compose via file I/O: Volume mounts
- Delegate specialized work: Container handles complex rendering

✅ **Von Neumann Architecture**
- Container = External I/O device
- Python script = Device driver
- File system = Shared memory bus

✅ **Assembly Language Principles**
- Explicit control: Dockerfile shows all dependencies
- One-to-one mapping: Command → Docker run → Output
- Low-level visibility: Can inspect container, volumes, processes

## Troubleshooting

### Image Not Found
```bash
cd .claude/tools/diagram-generation
./build-image.sh
```

### Permission Errors
- Ensure Docker Desktop is running
- Check WSL2 integration is enabled for your distro

### Rendering Failures
- Check `.mmd` file syntax in `temp/` directory
- Verify volume mounts have read/write permissions
- Inspect container logs: Add `2>&1` to command

### Performance Issues
- First run downloads Puppeteer/Chrome (~120MB)
- Subsequent runs use cached browser
- Container startup overhead: ~100ms

## Maintenance

### Rebuilding Image

When updating Dockerfile or dependencies:
```bash
cd .claude/tools/diagram-generation
./build-image.sh
```

### Cleaning Up

```bash
# Remove old diagrams
rm /mnt/d/~HAL8000/data/diagrams/*.png

# Remove temp files (or wait for auto-cleanup after 7 days)
rm .claude/tools/diagram-generation/temp/*.mmd

# Remove Docker image
docker rmi hal8000-mermaid:latest
```

## Lessons Learned

**Why Containerization Won:**
1. System dependencies (12+ packages) too invasive for host
2. Chrome/Puppeteer requires specific library versions
3. Complete isolation = no version conflicts
4. Reproducible across systems
5. Easy to remove (delete image = clean system)

**Trade-offs:**
- ⚖️ ~100ms container startup overhead vs. no host pollution
- ⚖️ 500MB image size vs. portable, self-contained
- ⚖️ Slightly complex setup vs. simple ongoing use

**Performance Result:**
- <1 second total time is acceptable for diagram generation
- Container overhead negligible compared to rendering time
- WSL2 + Docker Desktop integration works seamlessly

## Future Enhancements

- PlantUML support for BPMN 2.0 compliance
- Batch diagram generation
- Custom styling and themes
- Integration with HAL8000 system architecture diagrams
- Direct .mmd file editing workflow

---

**Version**: 1.0.0-HAL8000
**Ported from**: HAL 7000 Personal Assistant
**Integration date**: 2025-10-13
**Status**: Production Ready
