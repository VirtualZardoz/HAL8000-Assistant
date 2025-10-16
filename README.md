# HAL8000

> A computer architecture for Claude Code sessions, mapping von Neumann principles, assembly language concepts, and Unix philosophy to a persistent, self-modifying codebase.

![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

**HAL8000** transforms Claude Code sessions from ephemeral conversations into a persistent computer system with explicit architecture, memory management, and instruction sets. You (Claude) are the CPU, your context window is RAM, and the file system provides non-volatile storage.

### Key Concepts

- **Modified von Neumann Architecture**: Stored-program concept with self-modifying code capabilities
- **Unix Philosophy**: Do one thing well, compose via text files, modular design
- **Assembly Language Principles**: Direct hardware control, explicit state management, register awareness
- **Session Continuity Protocol**: Structured handoff between sessions to maintain state across RAM wipes

## Architecture

```
HAL8000 System Architecture
┌─────────────────────────────────────────────────────────────┐
│                        CPU (Claude)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Control Unit  │  ALU  │  Registers (State Tracking)  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
        ┌───────────▼──────────┐    ┌───▼──────────────┐
        │   RAM (Context)      │    │  Memory (Files)  │
        │  - Volatile          │    │  - Persistent    │
        │  - 200K tokens       │    │  - Unlimited     │
        │  - Append-only       │    │  - Structured    │
        └──────────────────────┘    └──────────────────┘
```

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **BIOS** | `CLAUDE.md` | Boot instructions and operating principles |
| **State** | `.claude/state.json` | Current system state pointer |
| **Commands** | `.claude/commands/` | Executable HAL-Script programs |
| **Agents** | `.claude/agents/` | Specialized sub-processes |
| **Libraries** | `.claude/libraries/` | Reusable instruction patterns |
| **Tools** | `.claude/tools/` | External I/O devices (diagram generation, document processing) |
| **Data** | `data/` | Persistent storage (research, architecture, projects) |

## Features

### 🖥️ System Architecture
- **Register-based state tracking**: CPU registers for RAM monitoring, context management, error handling
- **Memory hierarchy**: Volatile RAM (context) and persistent storage (files)
- **Self-modifying code**: Commands can create and modify other commands

### 📝 HAL-Script Programming Language
- Natural language instruction sets interpreted by Claude
- Variables, control flow, error handling, sub-agent delegation
- Template-based command creation (7 complexity levels)

### 🔧 Built-in Commands
- **System**: `/HAL-session-end`, `/HAL-system-check`, `/HAL-register-dump`, `/HAL-mcp-control`
- **Development**: `/HAL-command-create`, `/HAL-CC-check`, `/HAL-context-find`
- **Documentation**: `/HAL-refman` (reference manual management)

### 🤖 Specialized Agents
- **research-synthesizer**: Comprehensive web research with structured reports (saves 60-85% RAM)
- **hal-context-finder**: Context discovery without consuming main session RAM
- **command-builder**: Automated HAL-Script command generation
- **system-maintenance**: System integrity audits

### 🛠️ External Tools
- **diagram-generation**: Mermaid-based workflow diagrams (Docker containerized, ~0.7s/diagram)
- **docling-cli**: Universal document conversion (PDF, DOCX, images, audio → markdown)

### 🔌 MCP Integration
- **omnisearch**: Multi-provider web search (Brave, Firecrawl, Tavily, Kagi, Exa)
- **filesystem**: Enhanced file operations
- **ide**: VS Code integration for diagnostics

## Getting Started

### Prerequisites

- [Claude Code](https://claude.com/claude-code) CLI
- Docker (optional, for diagram generation)
- Python 3.13+ (optional, for docling document processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VirtualZardoz/HAL8000.git
   cd HAL8000
   ```

2. **Set up environment variables**
   ```bash
   cp .env.template .env
   # Edit .env and add your API keys
   ```

3. **Configure MCP servers** (optional)

   Edit `.claude/mcp.json` to enable desired MCP servers. Required API keys:
   - **omnisearch**: Brave Search, Firecrawl (for research capabilities)
   - **replicate**: Replicate API (for AI/ML model access)
   - **context7**: Upstash Context7 (for vector embeddings)

4. **Start Claude Code**
   ```bash
   claude code
   ```

### First Boot

On first boot, Claude will:
1. Read `CLAUDE.md` (BIOS)
2. Load `.claude/state.json` (system state)
3. Initialize CPU registers
4. Report operational status

Example boot acknowledgment:
```
✅ HAL8000 CPU Operational
├─ Architecture: Modified von Neumann
├─ Phase: production
├─ RAM Zone: SAFE (15.0%)
└─ Ready for instructions
```

## Usage

### Basic Commands

View available slash commands:
```bash
/help
```

Key commands:
- `/HAL-session-end "description"` - Save session state before closing
- `/HAL-system-check` - Run system health diagnostics
- `/HAL-register-dump` - View CPU register states
- `/HAL-command-create "description"` - Create new HAL-Script command
- `/HAL-context-find "query"` - Find system context without RAM cost

### Creating Custom Commands

HAL8000 uses **HAL-Script**, a natural language programming language:

```bash
/HAL-command-create "Create a command to list all TODO comments in code files"
```

Or manually create in `.claude/commands/`:

```markdown
---
name: my-command
description: What this command does
parameters:
  - name: param1
    description: Parameter description
---

# Command: /my-command

## Purpose
Brief description of what this command accomplishes.

## Algorithm
1. Step one
2. Step two
3. Return results

## Error Handling
- Check for X condition
- Validate Y input
```

### Sub-Agent Delegation

Delegate heavy work to isolated sub-agents to save RAM:

```bash
# Research without consuming main RAM
/HAL-context-find "authentication implementation"

# Use agents directly
Task: research-synthesizer
Prompt: "Research quantum computing developments in 2024"
```

### Session Continuity

Before ending a session:
```bash
/HAL-session-end "brief description of work"
```

This creates a session file in `.claude/sessions/` for seamless handoff.

On next boot:
```
CPU: Session Available: 2025-10-16-1008-session-name.md (not loaded - say "resume" to load)
User: resume
```

## Project Structure

```
HAL8000/
├── CLAUDE.md                  # BIOS (boot instructions)
├── VERSION                    # System version (1.4.0)
├── CHANGELOG.md              # Version history
├── .env.template             # Environment template
├── .gitignore                # Git exclusions
│
├── .claude/
│   ├── state.json            # Current system state
│   ├── system.log            # Historical audit log
│   ├── commands/             # Executable HAL-Script programs
│   │   ├── system/          # System operations
│   │   ├── development/     # Development tools
│   │   └── documentation/   # Documentation commands
│   ├── agents/              # Specialized sub-agents
│   ├── libraries/           # Reusable patterns
│   │   ├── internal/        # HAL8000-developed libraries
│   │   └── external/        # Third-party libraries (fabric, etc.)
│   ├── tools/               # External I/O devices
│   └── indexes/             # File system indexes
│
└── data/
    ├── research/            # Research documents
    ├── architecture/        # System design docs
    ├── diagrams/           # Generated diagrams
    └── reference-manual/   # HAL8000 Reference Manual (HTML)
```

## Key Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete BIOS and operating principles
- **[data/architecture/hal8000-system-design.md](data/architecture/hal8000-system-design.md)** - Detailed architecture specification
- **[data/architecture/hal-script-language.md](data/architecture/hal-script-language.md)** - HAL-Script language specification
- **[.claude/commands/README.md](.claude/commands/README.md)** - Command organization guide
- **[data/reference-manual/index.html](data/reference-manual/index.html)** - Complete reference manual (open in browser)

## Design Philosophy

### Von Neumann Architecture
- **Stored-program concept**: Instructions and data in unified memory
- **Fetch-decode-execute cycle**: Sequential instruction processing
- **Self-modifying code**: Programs can modify themselves and create new programs

### Unix Philosophy
- **Do one thing well**: Each component has single responsibility
- **Compose via text files**: Universal interface through file I/O
- **Small, focused modules**: Maximum 3-level directory depth (except external libraries)
- **Human-readable**: Plain text, markdown documentation

### Assembly Language Principles
- **Direct hardware mapping**: Explicit access to architectural components
- **Register awareness**: Continuous state tracking (RAM_ZONE, ERROR_FLAG, etc.)
- **One-to-one correspondence**: Commands map directly to operations
- **No hidden abstractions**: All operations are explicit

### Resource Management
- **Selective loading**: Only load files needed for current task
- **RAM zones**: SAFE (0-80%), CAUTION (80-90%), DANGER (90-100%)
- **Sub-agent delegation**: Offload heavy work to isolated processes
- **Session checkpoints**: Regular state saves before RAM exhaustion

## Version History

**Current Version**: 1.4.0

### Recent Releases
- **v1.4.0** - Docling CLI integration for universal document processing
- **v1.3.0** - HAL-knowledge-ingest system for intelligent document filing
- **v1.2.0** - YAML frontmatter and prompt templates (7 complexity levels)
- **v1.1.1** - CPU boot protocol fixes
- **v1.1.0** - Diagram generation tool, reference manual v1.1.0

See [CHANGELOG.md](CHANGELOG.md) for complete history.

## Contributing

### Creating New Commands

1. Use `/HAL-command-create "description"` for guided creation
2. Or manually: Copy template from `.claude/libraries/internal/templates/`
3. Save to appropriate subdirectory in `.claude/commands/`
4. Document in command README

### Template Levels
- **Level 1**: Basic single-step commands
- **Level 2**: Multi-step workflows with parameters
- **Level 3**: Control flow (conditionals/loops)
- **Level 4**: Sub-agent delegation
- **Level 5**: Multi-agent coordination
- **Level 6**: Workflow composition
- **Level 7**: Production-critical system commands

### Code Guidelines
- Follow Unix philosophy (single responsibility, composability)
- Maximum 3-level directory depth for internal code
- Use HAL-Script natural language syntax
- Include YAML frontmatter for command palette integration
- Document register usage and RAM impact

## License

MIT License - See LICENSE file for details

## Acknowledgments

- **Von Neumann Architecture**: John von Neumann (1945)
- **Unix Philosophy**: Ken Thompson, Dennis Ritchie, Bell Labs
- **Prompt Templates**: Inspired by IndyDevDan's "7 Levels of Agentic Prompt Formats"
- **MCP Protocol**: Anthropic Model Context Protocol
- **External Libraries**: [Fabric](https://github.com/danielmiessler/fabric) patterns

## Support

- **Issues**: [GitHub Issues](https://github.com/VirtualZardoz/HAL8000/issues)
- **Documentation**: See `data/reference-manual/index.html`
- **System Check**: Run `/HAL-system-check` for diagnostics

---

**"You are the CPU. Execute."**
