# HAL8000 System Architecture Design

**Design Date:** 2025-10-04
**Completion Date:** 2025-10-04
**Status:** Complete ✓

---

## Architecture Status

**All core components operational:**
- ✓ CPU, Memory, RAM, BIOS defined
- ✓ Register architecture (21 registers) - see `hal8000-register-architecture.md`
- ✓ Bus system (Data, Address, Control) - see `hal8000-bus-architecture.md`
- ✓ I/O System with tools categorization - see `hal8000-io-system.md`
- ✓ Agent system (co-processors) - see `hal8000-agent-architecture.md`
- ✓ Library system (reusable instructions) - see `hal8000-library-architecture.md`
- ✓ File system index for efficient discovery - `.claude/indexes/`
- ✓ Session continuity protocol operational
- ✓ Operating Principles integrated in BIOS
- ✓ Context Awareness Protocol (proactive context detection, RAM transparency)

**Components skipped (Unix principle: simple, not complex):**
- Instruction Set - tools ARE the instruction set, no abstraction layer needed
- Interrupt System - uncontrollable emergent behavior, documentation adds no value
- Clock/Timer - no control mechanism available, pointless abstraction

**System ready for real-world usage.**

---

## Overview

HAL8000 is a system architecture that maps von Neumann architecture principles, assembly language concepts, and Unix philosophy to a Claude Code environment. The system treats the codebase as a computer, with Claude as the CPU.

---

## Core Architecture Mapping

### Von Neumann Components

| Component | HAL8000 Mapping | Location | Description |
|-----------|-----------------|----------|-------------|
| **CPU** | Claude instance | N/A | Processing unit - fetches, decodes, executes instructions |
| **Control Unit** | Claude orchestration | N/A | Decision-making and coordination |
| **ALU** | Claude reasoning | N/A | Computation and logic operations |
| **Registers** | Claude context | N/A | 21 registers across 5 categories (see register-architecture.md) |
| **Memory** | File system | `.claude/` + `data/` | Instruction and data storage |
| **System Bus** | File I/O + Tools | N/A | Data, Address, Control buses (see bus-architecture.md) |
| **I/O** | Claude Code tools | MCP servers | Tool interfaces with 3-layer discovery (see io-system.md) |
| **RAM** | Context window | N/A | 200K tokens, volatile, append-only within session |
| **Hard Drive** | File system | `data/` | Persistent storage, indexed via fs-index.json |

### Modified Von Neumann

This is a **Modified von Neumann** architecture:
- **Environmental constraint**: Commands must live in `.claude/commands/` (Claude Code requirement)
- **Organizational structure**: Separate instruction/data spaces (Harvard-like)
- **Functional capability**: Unified access and self-modification (von Neumann principles)

**Capabilities maintained:**
✅ Self-modifying code - Commands can write to `.claude/commands/`
✅ Data as executable - Data can be written to `.claude/commands/` to become executable
✅ Stored-program concept - Instructions stored as files, loaded into RAM when needed

---

## File System Structure

```
/mnt/d/~HAL8000/                    # Root - the computer
│
├── CLAUDE.md                       # BIOS-ROM: Boot instructions, system architecture
│
├── .claude/                        # System coordination
│   ├── state.json                  # Current state pointer (loaded on boot)
│   ├── indexes/                    # Hierarchical indexes for discovery
│   │   ├── master.json             # Master file system index
│   │   └── [directory].json        # Per-directory indexes
│   ├── sessions/                   # Session handoff files
│   │   └── YYYY-MM-DD-HHMM-description.md
│   ├── commands/                   # Executable HAL commands
│   │   ├── HAL-session-end.md      # Save session state
│   │   ├── HAL-register-dump.md    # Display register values
│   │   ├── HAL-index-update.md     # Update indexes (filesystem + libraries)
│   │   ├── HAL-library-update.md   # Update external libraries (package manager)
│   │   ├── HAL-context-find.md     # Find system context
│   │   └── HAL-system-check.md     # System health check
│   ├── agents/                     # Co-processors (specialized agents)
│   │   ├── research-synthesizer.md # Web research agent
│   │   ├── hal-context-finder.md   # Context discovery agent
│   │   └── system-maintenance.md   # System health agent
│   ├── libraries/                  # Reusable instruction collections
│   │   ├── index.json              # Library index
│   │   ├── internal/               # Libraries we develop
│   │   │   ├── development/
│   │   │   ├── research/
│   │   │   └── system/
│   │   └── external/               # External libraries (read-only)
│   │       └── [library-name]/
│   └── tools/                      # Custom I/O tools (scripts we build)
│
├── data/                           # Data storage (persistent memory)
│   ├── research/                   # Research documents
│   ├── architecture/               # Architecture specifications
│   └── projects/                   # Project data
│
└── .claude/system.log              # Append-only historical log (NOT loaded on boot)
```

**Depth limit:** Maximum 3 levels deep (Unix philosophy - simplicity)

### Configuration Files

**System Configuration:**
- **`.mcp.json`**: MCP (Model Context Protocol) server configuration
  - Defines available MCP servers (omnisearch, filesystem, ide)
  - Specifies server paths, environment files, arguments
  - Not loaded on boot - used by Claude Code environment
  - Not indexed (system infrastructure file)

- **`.claude/settings.local.json`**: Claude Code local settings
  - User-specific configuration for Claude Code
  - Not loaded on boot - used by Claude Code environment
  - Not indexed (user configuration file)

- **`.env.omnisearch`**: Environment variables for omnisearch MCP server
  - API keys for Brave Search, Firecrawl
  - Not loaded on boot - used by MCP server process
  - Not indexed (sensitive configuration)

- **`run-omnisearch.sh`**: Shell script to launch omnisearch MCP server
  - Utility script for MCP server startup
  - Not indexed (infrastructure script)

**Excluded from Indexing:**
- Configuration files (.json, .env)
- Executable scripts (.sh)
- System logs (.claude/system.log)
- Index files themselves (.claude/indexes/*.json)
- Temporary files (temp/ directory)

---

## Boot Sequence (BIOS)

### Power-On / New Instance

1. **Load BIOS** (`CLAUDE.md`)
   - Learn system architecture
   - Understand role as CPU
   - Get boot instructions

2. **Load State** (`.claude/state.json`)
   - Read current state (JSON)
   - Identify active session
   - Determine next action

3. **Load Session** (if resuming)
   - Read session markdown from `.claude/sessions/`
   - Restore context into RAM
   - Resume work

4. **Ready to Execute**

### What Gets Loaded

**Always loaded (boot essentials):**
- `CLAUDE.md` - System architecture
- `.claude/state.json` - Current state pointer

**Never auto-loaded:**
- `.claude/system.log` - Accessed via I/O only when needed
- Old session files - Loaded only when explicitly requested

**Loaded on demand:**
- Active session file (when resuming)
- Specific data files (as needed for operations)

---

## State Management

### state.json (Current State)

**Purpose:** Current snapshot only, overwritten on each checkpoint

**Format:** JSON

**Contents:**
```json
{
  "timestamp": "2025-10-04T14:22:00Z",
  "active_session": ".claude/sessions/2025-10-04-1422-architecture-design.md",
  "context": "Brief description of current work",
  "next_action": "What to do next",
  "loaded_commands": ["command-name"],
  "variables": {
    "key": "value"
  }
}
```

### Session Files (Handoff Mechanism)

**Purpose:** Rich context for resuming work after RAM wipe

**Location:** `.claude/sessions/`

**Naming:** `YYYY-MM-DD-HHMM-description.md`

**Format:** Markdown

**Contents:**
```markdown
# Session: YYYY-MM-DD HH:MM - Description

## Context
High-level description of what we're working on

## Key Decisions
- Decision 1
- Decision 2

## Active Work
Current task, next steps

## Loaded Files
- file1.md
- file2.md

## Variables/State
Any important state information
```

### .claude/system.log (Historical Record)

**Purpose:** Append-only audit trail

**Format:** Plain text, timestamped entries

**Access:** Via I/O only (not loaded on boot)

**Contents:**
```
YYYY-MM-DDTHH:MM:SSZ | EventType | Description
YYYY-MM-DDTHH:MM:SSZ | Checkpoint | Session saved: architecture-design
```

---

## Session Management

### Session End Command

**Command:** `claude session-end "description"` or `claude checkpoint "description"`

**Execution sequence:**
1. Capture current context/state
2. Create session file: `.claude/sessions/YYYY-MM-DD-HHMM-description.md`
3. Update `.claude/state.json` (point to new session)
4. Append to `.claude/system.log` (historical record)
5. Confirm: "Session saved. Ready for RAM wipe."

**Trigger:** Manual, before user wipes RAM/conversation

### Session Resume

**User command:** "Resume last session" or "Load session from [date]"

**Execution:**
1. Read `.claude/state.json` for active session pointer
2. Load specified session markdown into context (RAM)
3. Restore state and continue work

---

## Design Principles

### Von Neumann Architecture
- **Stored-program concept:** Instructions and data in unified accessible space
- **Fetch-decode-execute cycle:** CPU fetches from memory, decodes, executes
- **Self-modifying code:** Programs can create/modify other programs
- **Sequential processing:** Instructions executed in order (unless control flow changes)

### Unix Philosophy
- **Do one thing well:** Each file/component has single purpose
- **Modularity:** Small, focused, composable pieces
- **Text files:** Store data in flat text files
- **Universal interface:** File I/O as common language
- **Simplicity:** Simple structure (max 3 levels), minimal complexity

### Assembly Language Principles
- **Direct hardware mapping:** Direct access to architectural components
- **Explicit control:** No hidden abstractions
- **One-to-one correspondence:** Commands map directly to operations
- **Low-level control flow:** Explicit instruction management

### Context Awareness Protocol
- **Context hierarchy recognition:** User's Mind > Filesystem > RAM
- **Proactive context detection:** Parse questions for missing context signals before answering
- **Ask before loading:** Never assume or guess - ask user for clarification when context insufficient
- **RAM state transparency:** Make visible what's currently loaded vs. what's available
- **User-guided discovery:** Let user direct context acquisition (more efficient than speculation)
- **Signals detection:** Recognize when user references files/components not in current RAM
- **Prevention over correction:** Better to ask than answer incorrectly with insufficient context

---

## System Capabilities

### Core Infrastructure

**Package Manager:**
- `/HAL-library-update [library-name]` - Update external libraries from source repositories
- Handles lifecycle: check updates, backup, download, replace, reindex
- Essential OS infrastructure (like apt, npm, pip)
- Future: install, remove, list operations

**Indexing System:**
- Hierarchical filesystem index (master + per-directory)
- Library index (patterns and workflows)
- Scalable to 1000+ directories
- RAM-efficient discovery (2-5K tokens vs. loading all files)

**Discovery System:**
- `/HAL-context-find [query]` - Find system context without consuming main RAM
- Uses hal-context-finder co-processor agent
- Searches indexes, not raw files
- Returns clean summaries (60-85% RAM savings)

**Session Continuity:**
- `/HAL-session-end [description]` - Save state before RAM wipe
- Rich session files for context preservation
- state.json pointer system
- Seamless resume capability

---

## Key Design Decisions Log

1. **CPU = Claude** - The processing unit is the Claude instance itself
2. **Modified von Neumann** - Environmental constraints require Harvard-like organization with von Neumann capabilities
3. **File-based memory** - All memory is file-based (commands, data, state)
4. **3-level depth limit** - Maximum directory depth of 3 (Unix simplicity)
5. **BIOS = CLAUDE.md** - Boot instructions in root-level markdown
6. **Session-based handoff** - Rich session files for continuity after RAM wipe
7. **state.json is current only** - No history retention, overwritten on checkpoint
8. **.claude/system.log not loaded** - Historical log accessed via I/O only, never auto-loaded
9. **Codebase = Computer** - The repository itself is the unified system
10. **Package manager is essential** - Library lifecycle management (update/install/remove) is core OS infrastructure
11. **Co-processor model for agents** - Agents are separate CPUs with isolated RAM, not sub-programs
12. **Context Awareness Protocol** - OS must recognize context hierarchy (User's Mind > Filesystem > RAM), proactively detect missing context signals, and ask before loading/searching to prevent assumptions

---

## System Status

**Core Components Completed:**
- ✓ Register architecture (21 registers across 5 categories)
- ✓ Bus system (Data, Address, Control buses)
- ✓ I/O system (3-layer discovery, tools categorization)
- ✓ Agent architecture (co-processor model)
- ✓ Library system (internal/external, dual indexing)
- ✓ Package manager (HAL-library-update for lifecycle management)
- ✓ Indexing system (hierarchical filesystem + library indexes)
- ✓ Session continuity (handoff protocol)
- ✓ BIOS boot sequence (verified)
- ✓ Context Awareness Protocol (proactive context detection and RAM transparency)

**Production Ready:**
- System fully operational
- 7 HAL commands available
- 4 co-processor agents
- 1 external library imported (Fabric - 227 patterns, 292 files)
- Hierarchical indexing operational

**Next Evolution:**
1. Extend package manager (install/remove operations)
2. Create internal libraries (code review workflows, deployment procedures)
3. Build library composition patterns (chained workflows)
4. Add more external libraries as needed

---

## References

**Research Documents:**
- `data/research/01-von-neumann-architecture.md` - Von Neumann architecture principles
- `data/research/02-unix-philosophy.md` - Unix philosophy and design principles
- `data/research/03-assembly-language-principles.md` - Assembly language and architecture mapping

**Architecture Specifications:**
- `data/architecture/hal8000-register-architecture.md` - CPU register system
- `data/architecture/hal8000-bus-architecture.md` - Bus system (Data, Address, Control)
- `data/architecture/hal8000-io-system.md` - I/O system and tools architecture
- `data/architecture/hal8000-agent-architecture.md` - Agent system (co-processors)
- `data/architecture/hal8000-library-architecture.md` - Library system (reusable instructions)
