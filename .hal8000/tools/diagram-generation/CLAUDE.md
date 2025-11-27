# HAL 7000 Diagram Generation Tool

## Purpose
Generate professional workflow diagrams from templates using Mermaid CLI and PlantUML, supporting HAL's visualization needs with UFC-compliant output management.

## Core Philosophy
- **Template-Driven Generation** - Reusable diagram patterns
- **Professional Quality** - Publication-ready output
- **HAL Workflow Integration** - Built-in HAL brainstorming workflow template
- **UFC Compliance** - Clean output management via inbox system

## Installation & Setup

### Prerequisites
- Node.js 20+
- Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`
- PlantUML (optional): For BPMN diagrams

### Directory Structure
```
.claude/context/tools/diagram-generation/
├── CLAUDE.md                           # This documentation
├── HAL-generate-diagram.py             # Main executable
├── setup.md                           # Installation guide
├── templates/                         # Diagram templates
│   └── process-flow_hal-brainstorming.txt
└── temp/                             # Temporary source files
```

## Usage

### Command Syntax
```bash
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py [type] [title] [options]
```

### Diagram Types
- **process-flow**: Sequential chronological workflows
- **swimlane**: Multi-actor/system processes
- **bpmn**: Business Process Model Notation
- **sipoc**: Supplier-Input-Process-Output-Customer

### Examples
```bash
# Generate HAL brainstorming workflow
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py process-flow "HAL Brainstorming Workflow" --template=hal-brainstorming

# Generate swimlane diagram
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py swimlane "User-HAL Interaction" --template=default

# Generate high-resolution diagram (4x scale)
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py process-flow "High Quality Workflow" --scale=4.0

# Generate with specific dimensions
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py bpmn "Business Process" --width=1920 --height=1080

# Generate from custom specification with high quality
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py bpmn "Custom Process" --custom="path/to/spec.md" --scale=3.0

# Generate SVG for vector graphics
python .claude/context/tools/diagram-generation/HAL-generate-diagram.py sipoc "Process Analysis" --format=svg --scale=2.0
```

## Output Management

### Generated Files
- **Diagrams**: `inbox/diagrams/` (PNG, SVG, PDF) - Final output for use
- **Source Files**: `.claude/context/tools/diagram-generation/temp/` (Mermaid, PlantUML) - Reusable source templates

### File Management
- **Automatic Cleanup**: Temp files older than 7 days are automatically removed
- **Source Preservation**: Recent `.mmd` files kept for reuse and iteration
- **Clean Separation**: Main tool directory contains only documentation and scripts

### Naming Convention
```
[Title]_[Timestamp].[extension]
HAL_Brainstorming_Workflow_20250919_094546.png  # Final diagram in inbox/diagrams/
HAL_Brainstorming_Workflow_20250919_094546.mmd  # Source template in temp/
```

## Templates

### Built-in Templates
- **hal-brainstorming**: Complete 6-stage HAL brainstorming workflow (process-flow only)
- **default**: Professional templates for all diagram types:
  - **process-flow**: Basic sequential workflow
  - **swimlane**: User-HAL-System interaction
  - **bpmn**: Business process with decision points and gateways
  - **sipoc**: Supplier-Input-Process-Output-Customer analysis

### Template Variables
- `{{TITLE}}`: Diagram title
- `{{DATE}}`: Current date
- `{{TIMESTAMP}}`: Current timestamp

### Custom Templates
Place custom templates in `templates/` directory:
- Format: `[type]_[name].txt`
- Example: `process-flow_custom.txt`

## Integration Points

### HAL Commands
- Command documentation: `.claude/context/commands/HAL-generate-diagram.md`
- Executable location: `.claude/context/tools/diagram-generation/HAL-generate-diagram.py`

### UFC System
- Output follows UFC inbox conventions
- Templates stored in UFC-compliant structure
- Documentation integrated with tools context

## Technical Details

### Supported Output Formats
- PNG (default) - Raster format, good for web/presentations
- SVG (vector graphics) - Scalable format, best for high-quality printing
- PDF (print-ready) - Document format

### Quality Options
- `--scale` - Resolution multiplier (1.0=default, 2.0=2x, 4.0=4x)
- `--width` - Specific width in pixels
- `--height` - Specific height in pixels
- **Default**: 2x scale for better quality than standard output

### CLI Tools Used
- **Mermaid CLI**: `npx mmdc` for all diagram types (flowcharts, swimlanes, BPMN, SIPOC)
- **PlantUML**: Future option for BPMN 2.0 compliance (see `plantuml-future-reference.md`)

### Error Handling
- Graceful CLI tool detection
- Template validation
- Output directory creation
- Unicode-safe console output

## Maintenance

### Adding New Templates
1. Create template file in `templates/`
2. Follow naming convention: `[type]_[name].txt`
3. Use template variables for dynamic content
4. Test with command

### Adding New Diagram Types
1. Update `DIAGRAM_TOOLS` dictionary in script
2. Add basic template in `get_basic_template()`
3. Update documentation and examples

## Security Notes
- Scripts execute with shell=True for Windows compatibility
- File paths are sanitized for safe naming
- No external network dependencies beyond CLI tools

## Future Enhancements
- Python Graphviz integration for advanced layouts
- Custom styling and themes
- Batch diagram generation
- Integration with HAL system architecture diagrams