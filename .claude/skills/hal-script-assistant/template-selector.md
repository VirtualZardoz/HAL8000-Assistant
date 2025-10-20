# Template Selection Decision Tree

Quick reference for choosing the right HAL-Script template.

## Decision Flow

```
START: What kind of command/agent are you creating?
    ↓
┌────────────────────────────────────┐
│ Is it a single simple operation?   │
│ (e.g., display version, read file) │
└────────────────────────────────────┘
         │
         ├─ YES → Level 1: Basic
         │
         └─ NO ↓

┌────────────────────────────────────┐
│ Does it have multiple steps but    │
│ no conditionals or loops?          │
│ (e.g., read → process → save)      │
└────────────────────────────────────┘
         │
         ├─ YES → Level 2: Workflow
         │
         └─ NO ↓

┌────────────────────────────────────┐
│ Does it need conditionals/loops?   │
│ (IF/ELSE, FOR, WHILE logic)        │
└────────────────────────────────────┘
         │
         ├─ YES → Level 3: Control Flow
         │
         └─ NO ↓

┌────────────────────────────────────┐
│ Does it delegate to ONE sub-agent? │
│ (e.g., research-synthesizer)       │
└────────────────────────────────────┘
         │
         ├─ YES → Level 4: Delegate
         │
         └─ NO ↓

┌────────────────────────────────────┐
│ Does it coordinate MULTIPLE agents?│
│ (parallel/sequential agent tasks)  │
└────────────────────────────────────┘
         │
         ├─ YES → Level 5: Supervisor
         │
         └─ NO ↓

┌────────────────────────────────────┐
│ Does it invoke other HAL commands? │
│ (composing /HAL-* commands)        │
└────────────────────────────────────┘
         │
         ├─ YES → Level 6: Workflow Composition
         │
         └─ NO ↓

┌────────────────────────────────────┐
│ Is it system-critical?             │
│ (session mgmt, state, boot, etc.)  │
└────────────────────────────────────┘
         │
         ├─ YES → Level 7: System
         │
         └─ NO → Master Template (custom)
```

## Templates by Use Case

### Level 1: Basic
**When to use:**
- Single operation
- No parameters (or one simple parameter)
- No complex logic
- Direct tool usage

**Examples:**
- Display system version
- Show register state
- Read single config file
- List available commands

**Tools typically used:** Read, Bash (simple commands)

---

### Level 2: Workflow
**When to use:**
- Multiple sequential steps
- Accepts parameters
- No branching logic
- Straightforward flow: input → process → output

**Examples:**
- Create documentation file
- Update index
- Format and save data
- Generate report

**Tools typically used:** Read, Write, Edit, Grep, Glob

---

### Level 3: Control Flow
**When to use:**
- Needs IF/ELSE decisions
- Requires loops
- Different paths based on conditions
- Error handling with branches

**Examples:**
- Validate and fix file structure
- Process different file types differently
- Conditional data transformation
- Adaptive behavior based on input

**Tools typically used:** Read, Write, Edit, Grep, Bash (with conditionals)

---

### Level 4: Delegate
**When to use:**
- Main work delegated to ONE specialized agent
- Command orchestrates single agent
- Agent does heavy lifting
- Command handles pre/post processing

**Examples:**
- Research command → research-synthesizer agent
- Context discovery → hal-context-finder agent
- System audit → system-maintenance agent

**Tools typically used:** Task (for agent), Read, Write (for pre/post)

---

### Level 5: Supervisor
**When to use:**
- Coordinates MULTIPLE agents
- Parallel or sequential agent tasks
- Synthesizes results from multiple sources
- Complex multi-stage workflows

**Examples:**
- Run research + context-finding + validation in parallel
- Multi-aspect system analysis
- Comprehensive documentation generation
- Complex project setup

**Tools typically used:** Task (multiple), Read, Write, coordination logic

---

### Level 6: Workflow Composition
**When to use:**
- Chains multiple HAL commands together
- Invokes `/HAL-*` commands in sequence
- High-level orchestration
- Reuses existing command capabilities

**Examples:**
- Update all indexes then run system check
- Research topic, document findings, update knowledge base
- Complete project setup workflow

**Tools typically used:** SlashCommand, Read, Write

---

### Level 7: System
**When to use:**
- Production-critical operations
- Session/state management
- Boot/shutdown procedures
- System integrity operations
- Failure = system compromise

**Examples:**
- /HAL-session-end (save state before RAM wipe)
- /HAL-system-check (validate system health)
- Boot sequence commands
- State persistence

**Tools typically used:** Read, Write, Edit, Bash, extensive error handling

---

### Master Template
**When to use:**
- Custom requirements not fitting other levels
- Experimental commands
- Need ALL possible sections to choose from
- Complex custom logic

**Usage:**
1. Copy master template
2. Remove sections you don't need
3. Keep only relevant "Lego blocks"
4. Implement custom logic

---

## Quick Reference Table

| Level | Complexity | Steps | Logic | Agents | Commands | Example |
|-------|------------|-------|-------|--------|----------|---------|
| 1 | Minimal | 1 | None | 0 | 0 | Show version |
| 2 | Low | 2-5 | Sequential | 0 | 0 | Create report |
| 3 | Medium | Varies | Conditionals/loops | 0 | 0 | Validate files |
| 4 | Medium | 3-5 | Sequential + delegate | 1 | 0 | Research topic |
| 5 | High | Varies | Coordination | 2+ | 0 | Multi-analysis |
| 6 | High | Varies | Orchestration | 0 | 2+ | Full workflow |
| 7 | Highest | Varies | Critical + recovery | Varies | Varies | Session-end |
| Master | Custom | Custom | Custom | Custom | Custom | Experimental |

## Common Questions

### Q: My command has parameters AND conditionals. Level 2 or 3?
**A:** Level 3. Parameters alone = Level 2, but conditionals = Level 3.

### Q: I'm delegating to an agent AND calling another command. Level 4, 5, or 6?
**A:** Level 6 if primarily composing commands, Level 5 if primarily coordinating agents. If equal, choose based on complexity.

### Q: My command is simple but system-critical. Level 1 or 7?
**A:** Level 7. Criticality overrides simplicity for system commands.

### Q: I'm not sure which level. What do I do?
**A:** Start with Master template. Copy all sections, then remove what you don't need. Over-structure is better than under-structure.

### Q: Can I mix levels?
**A:** Templates are starting points. Take the closest match and adapt. The levels are guidance, not strict rules.

## Template File Paths

```
.claude/libraries/internal/templates/
├── master-prompt-template.md       # All sections (Lego catalog)
├── level-1-basic.md                # Simple single-step
├── level-2-workflow.md             # Multi-step sequential
├── level-3-control-flow.md         # Conditionals/loops
├── level-4-delegate.md             # Single agent delegation
├── level-5-supervisor.md           # Multi-agent coordination
├── level-6-workflow-composition.md # Command composition
├── level-7-system.md               # Critical system ops
└── template-guide.md               # Complete usage guide
```

## Usage Pattern

```bash
# 1. Decide on level (use decision tree above)
# 2. Copy template
cp .claude/libraries/internal/templates/level-X-*.md /path/to/new-command.md

# 3. Edit: Remove unused sections, fill in logic
# 4. Test command
# 5. Iterate
```

## Architecture Credit

Framework inspired by **IndyDevDan's "7 Levels of Agentic Prompt Formats"**
