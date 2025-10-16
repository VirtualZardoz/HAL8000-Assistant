# Diagram Generation Tool - Export Guide

## Package Contents

### Core Files (Required)
- `HAL-generate-diagram.py` - Main executable script
- `CLAUDE.md` - Complete documentation
- `setup.md` - Installation instructions
- `templates/` - Diagram template library
- `temp/` - Temporary working directory (will auto-populate)

### Reference Files (Optional but Recommended)
- `inline-work-management-workflow-diagram-2-2x.jpg` - Visual reference for diagram types
- `plantuml-future-reference.md` - Future enhancement notes
- `project-archive/` - Original project documentation

## Installation Requirements

### System Dependencies
1. **Node.js 20+** - Required for Mermaid CLI
2. **Mermaid CLI** - Install globally:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

### Verification
```bash
npx mmdc --version  # Should show Mermaid CLI version
```

## Adaptation for Other Agents

### Path Adjustments
The script uses relative paths. Update these if your directory structure differs:

**Current structure (HAL 7000)**:
```
working-directory/
├── .claude/tools/diagram-generation/  # Tool location
└── inbox/diagrams/                    # Output location
```

**Path variables to adjust** (in `HAL-generate-diagram.py`):
- `OUTPUT_DIR` - Where final diagrams are saved
- `TEMP_DIR` - Where source .mmd files are stored
- `TEMPLATE_DIR` - Where templates are loaded from

### Example Adaptation
```python
# Original (HAL 7000)
OUTPUT_DIR = "inbox/diagrams"
TEMP_DIR = ".claude/tools/diagram-generation/temp"

# Adapted for different agent
OUTPUT_DIR = "output/diagrams"  # Your preferred output location
TEMP_DIR = "tools/diagram-generation/temp"  # Relative to your working directory
```

## Usage After Export

### Basic Command
```bash
python HAL-generate-diagram.py [type] [title] [options]
```

### Diagram Types
- `process-flow` - Sequential workflows
- `swimlane` - Multi-actor processes
- `bpmn` - Business Process Model Notation
- `sipoc` - Supplier-Input-Process-Output-Customer

### Common Examples
```bash
# Using built-in template
python HAL-generate-diagram.py process-flow "My Workflow" --template=hal-brainstorming

# High-resolution output
python HAL-generate-diagram.py swimlane "User Flow" --scale=4.0

# SVG vector format
python HAL-generate-diagram.py bpmn "Business Process" --format=svg

# Custom dimensions
python HAL-generate-diagram.py sipoc "Analysis" --width=1920 --height=1080
```

## Output Management

### Generated Files
- **Diagrams**: `[OUTPUT_DIR]/` - Final PNG/SVG/PDF files
- **Source**: `[TEMP_DIR]/` - Reusable .mmd templates

### Automatic Cleanup
- Temp files older than 7 days are auto-removed
- Keep recent source files for iteration

## Templates

### Built-in Templates
Located in `templates/` directory:
- `process-flow_hal-brainstorming.txt` - Complete 6-stage HAL workflow
- Default templates for all diagram types (generated if not found)

### Adding Custom Templates
1. Create file: `templates/[type]_[name].txt`
2. Use variables: `{{TITLE}}`, `{{DATE}}`, `{{TIMESTAMP}}`
3. Use with: `--template=[name]`

## Integration Notes

### For AI Agents
- Script provides clear console output and error messages
- Returns exit code 0 on success, 1 on error
- Handles Unicode characters safely
- Creates directories automatically

### For Human Users
- Professional quality output (default 2x scale)
- Publication-ready diagrams
- Iterative refinement via source file preservation

## Troubleshooting

### Common Issues
1. **"Mermaid CLI not found"**
   - Install: `npm install -g @mermaid-js/mermaid-cli`
   - Verify: `npx mmdc --version`

2. **"Template not found"**
   - Check templates/ directory exists
   - Use `--template=default` for basic templates
   - Verify template naming: `[type]_[name].txt`

3. **Output directory errors**
   - Script auto-creates directories
   - Check write permissions on output path

### Support
- Full documentation in `CLAUDE.md`
- Installation guide in `setup.md`
- Template examples in `templates/`

## Version Information
- **Status**: Phase 1 Complete (Production Ready)
- **Export Date**: 2025-10-13
- **Source System**: HAL 7000 Personal Assistant
- **Compatibility**: Any Python 3.x environment with Node.js

## License & Attribution
Exported from HAL 7000 system for reuse by other AI agents and automation systems.
