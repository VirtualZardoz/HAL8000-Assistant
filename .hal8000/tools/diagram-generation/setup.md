# Diagram Generation Tools Setup

## Required CLI Tools

### 1. Mermaid CLI
Install mermaid-cli for flowcharts and sequence diagrams:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### 2. PlantUML
Download PlantUML jar file and set up alias:
```bash
# Download plantuml.jar
# Create plantuml.bat wrapper or add to PATH
```

### 3. Alternative: Python Libraries
If CLI tools unavailable, can use Python libraries:
```bash
pip install graphviz
pip install mermaid-py
```

## Verification
Run the command with `--help` to verify installation:
```bash
python .claude/commands/HAL-generate-diagram.py --help
```

## Directory Structure
```
.claude/tools/diagram-generation/
├── setup.md                    # This file
├── templates/                  # Diagram templates
│   ├── process-flow_default.txt
│   ├── swimlane_default.txt
│   ├── bpmn_default.txt
│   └── sipoc_default.txt
└── scripts/                    # Helper scripts
```

## Output Directory
Generated diagrams are saved to: `inbox/diagrams/`