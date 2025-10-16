# HAL8000 Commands Directory

**Location:** `.claude/commands/`
**Purpose:** Executable HAL-Script programs for system operations and applications

---

## What Are Commands?

Commands are **executable markdown files** containing instructions written in HAL-Script (natural language programming). They are the primary way to extend HAL8000's capabilities.

**Technical definition:** Commands are HAL-Script modules/programs

**Invocation:**
- Slash command syntax: `/HAL-command-name` (registered in Claude Code)
- Explicit execution: "Run the [command-name] command"
- Direct load: "Load and execute .claude/commands/path/to/file.md"

---

## Directory Organization

Commands are organized by purpose into subdirectories:

### `system/` - System Operations

**Purpose:** Core infrastructure and maintenance operations

**Commands:**
- `HAL-session-end` - Session checkpointing and state preservation
- `HAL-system-check` - System health and integrity validation
- `HAL-register-dump` - CPU register state display (debugging)
- `HAL-index-update` - File system and library index maintenance
- `HAL-library-update` - External library package management
- `HAL-mcp-control` - MCP server dynamic control

**Characteristics:**
- Critical to system operation
- Infrastructure-focused
- Typically invoked via slash commands
- `HAL-*` naming convention (system prefix)

---

### `development/` - Development & Validation

**Purpose:** Development tools and quality assurance

**Commands:**
- `HAL-CC-check` - External Claude Code compatibility validation
- `HAL-context-find` - Context discovery via sub-agent (RAM-efficient)

**Characteristics:**
- Development workflow support
- Quality assurance tools
- May invoke specialized sub-agents
- `HAL-*` naming convention

---

### `documentation/` - Documentation & Applications

**Purpose:** Documentation management and domain-specific applications

**Commands:**
- `HAL-refman` - HAL8000 Reference Manual lifecycle management

**Characteristics:**
- Application-level workflows
- Domain-specific logic
- May be complex multi-step programs
- Can use `HAL-*` or custom naming

---

## Creating New Commands

### Method 1: Template-Based Creation (Recommended)

**Start with a template** from `.claude/libraries/internal/templates/`:

1. **Choose your template:**
   - `level-1-basic.md` - Simple single-step commands
   - `level-2-workflow.md` - Multi-step sequential workflows
   - `level-3-control-flow.md` - Commands with conditionals/loops
   - `level-4-delegate.md` - Commands that invoke sub-agents
   - `level-5-supervisor.md` - Commands coordinating multiple agents
   - `level-6-workflow-composition.md` - Commands composing other commands
   - `level-7-system.md` - Production-critical system commands
   - `master-prompt-template.md` - All sections (custom composition)

2. **Copy template to your command file:**
   ```bash
   cp .claude/libraries/internal/templates/level-2-workflow.md \
      .claude/commands/development/my-new-command.md
   ```

3. **Customize the template:**
   - Remove unused sections
   - Fill in your specific logic
   - Add custom sections if needed (rare)

4. **Save to appropriate directory** (`system/`, `development/`, `documentation/`)

**See:** `.claude/libraries/internal/templates/template-guide.md` for detailed template usage guide.

**Benefits:**
- No missing sections (template shows all possibilities)
- Consistent structure across commands
- Faster creation (copy→customize vs. start from scratch)
- Built-in best practices

---

### Method 2: Manual Creation (From Scratch)

If not using templates, follow this basic structure:

```markdown
# Command Name

## Purpose
What this command does and why it exists

## Usage
How to invoke the command (syntax, arguments)

## Instructions
Step-by-step instructions in HAL-Script:
1. First, do this
2. Then, do that
3. Finally, complete with this

## Output Format
What the command produces
```

**Note:** Templates provide more comprehensive structure and are recommended for most use cases.

---

### Naming Conventions

**System commands:** Use `HAL-*` prefix
- Examples: `HAL-session-end`, `HAL-system-check`
- Indicates core system operation
- Typically slash-command registered

**User/Application commands:** Any name without `HAL-` prefix
- Examples: `architecture-analysis`, `code-review`, `test-runner`
- Domain-specific operations
- Custom workflows and applications

### Where to Put New Commands

**System operation?** → `system/`
**Development tool?** → `development/`
**Documentation/Application?** → `documentation/`
**User-created?** → Consider adding `user/` subdirectory

---

## HAL-Script Language

Commands are written in **HAL-Script**, HAL8000's natural language programming language.

### Basic Syntax

**Imperative instructions:**
```markdown
Read the file at path/to/file.md
Write content to output.json
Execute the HAL-session-end command
```

**Conditionals:**
```markdown
If RAM exceeds 80%, warn the user
When file is missing, report error
Unless user confirms, refuse operation
```

**Loops:**
```markdown
For each file in the list:
  - Read the file
  - Extract metadata
  - Update index
```

**Function calls (invoke other commands/agents):**
```markdown
Launch the system-maintenance sub-agent
Execute the HAL-index-update command
Run the validation subroutine defined above
```

### Complete Language Documentation

See `data/architecture/hal-script-language.md` for complete HAL-Script specification and examples.

---

## Execution Model

**CPU:** Claude instance (intelligent interpreter)
**Interpreter:** Reads HAL-Script and executes instructions
**Execution:** Sequential by default, parallel when explicitly requested
**Context:** CPU maintains state in registers (RAM) during execution
**Persistence:** Results written to files (disk) for session continuity

---

## Command Composition

Commands can compose to form larger programs:

**Example workflow:**
```
Application: Architecture Audit
  ↓
Step 1: Run HAL-context-find (load architecture docs)
  ↓
Step 2: Run HAL-system-check (verify system health)
  ↓
Step 3: Generate report (custom logic)
  ↓
Step 4: Run HAL-session-end (checkpoint results)
```

This is a **program** composed of multiple **commands** (modules).

---

## Best Practices

### 1. Single Responsibility
Each command should do one thing well (Unix philosophy)

### 2. Clear Documentation
- Purpose section explains WHY
- Implementation section explains HOW
- Expected output section shows WHAT

### 3. Error Handling
Always include error handling logic:
```markdown
If operation fails:
  - Report error with context
  - Suggest recovery action
  - Abort or continue gracefully
```

### 4. RAM Awareness
Commands should check RAM before heavy operations:
```markdown
If RAM_ZONE equals "DANGER":
  Refuse operation
  Suggest session-end checkpoint
```

### 5. Idempotency
Where possible, commands should be safe to run multiple times

### 6. Composability
Design commands to work well with other commands

---

## Examples

### Simple Command (Display Information)
```markdown
# HAL-register-dump

## Purpose
Display current CPU register states for debugging

## Implementation
Read register values from CPU context.
Format as structured table.
Display to user.

## Output
Table of all registers with current values
```

### Complex Command (Multi-step Workflow)
```markdown
# HAL-session-end

## Implementation
1. Capture current context (identify work, decisions, state)
2. Generate timestamp and session filename
3. Create session file in .claude/sessions/
4. Update .claude/state.json with new state
5. Append entry to .claude/system.log
6. Display confirmation message
```

---

## See Also

- `.claude/libraries/internal/templates/` - **Prompt templates for command creation**
  - `template-guide.md` - Comprehensive guide to using templates
  - `level-1-basic.md` through `level-7-system.md` - 7 progressive templates
  - `master-prompt-template.md` - Complete Lego block catalog
- `CLAUDE.md` - BIOS containing boot sequence and operating principles
- `data/architecture/hal-script-language.md` - Complete HAL-Script language specification
- `.claude/agents/` - Specialized sub-agents (co-processors)
- `.claude/libraries/` - Reusable instruction collections

---

**Commands are HAL8000's programming interface. Create commands to extend the system.**

**Use templates** (`.claude/libraries/internal/templates/`) for faster, more consistent command creation.
