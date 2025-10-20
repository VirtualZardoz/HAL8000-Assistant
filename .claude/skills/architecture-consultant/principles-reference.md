# HAL8000 Architecture Principles - Quick Reference

This document provides quick-lookup principles for the architecture-consultant Skill.

## Modified von Neumann Architecture

### Key Concepts
- **Unified Memory**: Instructions and data in same accessible space
- **Stored-Program**: Commands stored as files, executed by CPU
- **Self-Modifying**: Commands can create/modify other commands
- **Sequential Processing**: Fetch-decode-execute cycle

### HAL8000-Specific Adaptations
- **Append-Only RAM**: Context window accumulates, no eviction
- **Session Boundaries**: Only way to garbage-collect RAM
- **Selective Loading**: Permanent commitment on file read
- **File System State**: Persistence via storage, not RAM

### Common Violations
- Speculative file loading
- Assuming RAM can be freed mid-session
- Storing critical state only in context
- Ignoring token costs

---

## Unix Philosophy

### Core Principles
1. **Do one thing well** - Single responsibility
2. **Build once, reuse always** - Avoid duplication
3. **Compose via interfaces** - File I/O as universal interface
4. **Delegate specialized work** - Use sub-agents/external tools
5. **Simple, not complex** - Max 3-level depth
6. **Text streams** - Plain text, human-readable

### HAL8000 Structural Rules
- **Max depth: 3 levels** (except `.claude/libraries/external/`)
- **One purpose per file/component**
- **Plain text formats** (Markdown, JSON, text)
- **Reusable patterns over one-offs**

### Common Violations
- Multi-responsibility components
- Directory depth > 3
- Binary/opaque formats
- Duplicated functionality
- Unnecessary complexity
- Not delegating to specialized agents

---

## Assembly Language Principles

### Core Concepts
1. **Explicit Control** - No hidden operations
2. **Register Awareness** - Track CPU state
3. **Sequential Execution** - Clear control flow
4. **One-to-One Mapping** - Command = operation
5. **Low-Level Visibility** - Inspectable state

### HAL8000 Mappings
- **Registers**: CPU state tracking (see /HAL-register-dump)
- **Instructions**: HAL-Script commands
- **Fetch-Decode-Execute**: Command interpretation cycle
- **Control Flow**: Explicit state transitions

### Common Violations
- Hidden state mutations
- Unclear command mappings
- Opaque system state
- Implicit control flow

---

## Depth Limit Examples

### ✅ Compliant (≤3 levels)
```
/mnt/d/~HAL8000/                    # Level 0 (root)
├── .claude/                        # Level 1
│   ├── commands/                   # Level 2
│   │   └── system/                 # Level 3 ✓
│   ├── agents/                     # Level 2
│   │   └── research-synthesizer.md # Level 3 ✓
│   └── skills/                     # Level 2
│       └── context-awareness/      # Level 3 ✓
└── data/                           # Level 1
    ├── research/                   # Level 2
    │   └── 01-von-neumann.md       # Level 3 ✓
    └── architecture/               # Level 2
        └── hal8000-design.md       # Level 3 ✓
```

### ❌ Violation (>3 levels)
```
.claude/commands/system/utilities/helpers/  # Level 5 - TOO DEEP
data/projects/app/modules/auth/utils/       # Level 6 - TOO DEEP
```

### ✓ Exception
```
.claude/libraries/external/fabric/patterns/analyze/  # OK - external library
```

---

## Sub-Agent Delegation Pattern

### When to Delegate

**ALWAYS delegate:**
- Web research → research-synthesizer
- System context discovery → hal-context-finder
- Large file analysis (>30K tokens)
- Multi-step tasks needing extensive intermediate data
- Operations where input >> output

**Benefits:**
- Isolated 200K context (doesn't pollute main RAM)
- Automatic cleanup after completion
- Specialized capabilities
- Returns only essential summaries

### Pattern
```
Main Session (Limited RAM)
    ↓ delegate
Sub-Agent (Fresh 200K RAM, isolated)
    ↓ process heavy work
Returns clean summary (not raw data)
    ↓ result
Main Session (RAM += summary only)
```

---

## Resource Management Zones

### RAM_ZONE Register
```
SAFE (0-80%)     : Normal operation, load freely
CAUTION (80-90%) : Monitor closely, prepare checkpoint
DANGER (90-100%) : Checkpoint urgently, degraded performance
```

### Before Loading Any File
1. Check CONTEXT_MANIFEST (already loaded?)
2. Estimate token cost
3. Calculate: RAM_USAGE + cost
4. Evaluate resulting RAM_ZONE
5. Proceed/Warn/Refuse accordingly

---

## File Organization Standards

### Commands
- Location: `.claude/commands/`
- Subdirectories: `system/`, `development/`, `documentation/`
- Format: HAL-Script (Markdown with YAML frontmatter)
- Naming: `HAL-command-name.md`

### Agents
- Location: `.claude/agents/`
- Format: Markdown with YAML frontmatter
- Tool whitelisting via `allowed-tools`
- Single responsibility per agent

### Skills
- Location: `.claude/skills/`
- Format: `SKILL.md` with YAML frontmatter
- Model-invoked (autonomous activation)
- Supporting files in same directory

### Data
- Location: `data/`
- Subdirectories: `research/`, `architecture/`, `projects/`, `operations/`
- Format: Markdown (human-readable)
- Persistent storage (survives sessions)

---

## State Management

### Volatile (RAM)
- Current context
- Loaded files
- Sub-agent results (until persisted)
- Wiped at session boundary

### Persistent (File System)
- `.claude/state.json` (state pointer)
- `.claude/sessions/` (handoff files)
- `.claude/system.log` (historical audit)
- `data/` (all data storage)

### Critical Protocol
- Complete sub-agent work within session
- Persist results to files before session-end
- Never rely on RAM across session boundaries
- Use `/HAL-session-end` to save state

---

## Common Design Patterns

### ✅ Good Patterns
- Single-purpose commands/agents/Skills
- Delegate context-heavy work to sub-agents
- Return summaries, not raw data
- Reusable components via templates
- Plain text for all system data
- Max 3-level directory depth

### ❌ Anti-Patterns
- Multi-responsibility components
- Loading files speculatively
- Keeping large data in RAM
- Duplicating functionality
- Binary/opaque formats
- Deep nested directories (>3)
- Assuming RAM persists across sessions
