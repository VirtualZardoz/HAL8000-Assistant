---
name: HAL-Script Assistant
description: Help write HAL-Script commands and agents for HAL8000. Use when creating new commands, editing existing commands, writing agent prompts, or when user asks about HAL-Script syntax, command structure, or template selection. Activate on questions about command creation, HAL-Script programming, or template usage.
allowed-tools: Read, Write, Edit, Glob
---

# HAL-Script Assistant

This Skill assists with writing HAL-Script (HAL8000's natural language programming language) for commands, agents, and Skills.

## Purpose

Guide users in creating well-structured, architecturally-sound HAL-Script programs using the template system and HAL8000 conventions.

## When to Activate

**Triggers:**
- User wants to create a new command
- User asks about HAL-Script syntax or structure
- User needs help choosing a template
- User is editing existing command/agent
- User invokes `/HAL-command-create` (automation)
- Questions about command organization or best practices

## HAL-Script Overview

**What is HAL-Script?**
- Natural language programming language interpreted by Claude (CPU)
- Markdown files with YAML frontmatter + structured instructions
- Commands = executable programs, Agents = specialized sub-processes
- Complete language: variables, control flow, functions, error handling

**Key Components:**
1. **YAML Frontmatter** - Metadata and configuration
2. **Purpose Section** - What the command does
3. **Instructions** - Step-by-step logic (the program)
4. **Parameters** - Input variables
5. **Control Flow** - Conditionals, loops, error handling
6. **Output Specification** - What to return

## Template System (The Lego Block Principle)

**Location:** `.claude/libraries/internal/templates/`

**Philosophy:** Templates show ALL possible sections (Lego blocks). Start with template, remove unused sections, fill in your logic.

### Available Templates

| Level | Template | Use Case | Complexity |
|-------|----------|----------|------------|
| Master | `master-prompt-template.md` | Custom/complex commands | All sections |
| 1 | `level-1-basic.md` | Simple single-step commands | Minimal |
| 2 | `level-2-workflow.md` | Multi-step workflows with parameters | Low |
| 3 | `level-3-control-flow.md` | Conditionals/loops | Medium |
| 4 | `level-4-delegate.md` | Sub-agent delegation | Medium |
| 5 | `level-5-supervisor.md` | Multi-agent coordination | High |
| 6 | `level-6-workflow-composition.md` | Composing multiple commands | High |
| 7 | `level-7-system.md` | Production-critical system ops | Highest |

### Template Selection Guide

**Ask these questions:**

1. **How many steps?**
   - Single step → Level 1
   - Multiple steps → Level 2+

2. **Does it need conditionals/loops?**
   - Yes → Level 3+
   - No → Level 1-2

3. **Does it delegate to agents?**
   - One agent → Level 4
   - Multiple agents → Level 5

4. **Does it compose other commands?**
   - Yes → Level 6

5. **Is it system-critical?**
   - Yes (session-end, state management) → Level 7
   - No → Lower level

**See:** `.claude/libraries/internal/templates/template-guide.md` for complete guide

## YAML Frontmatter Structure

### For Commands
```yaml
---
name: Command Name
description: Brief description (appears in command palette)
arguments:
  - name: arg_name
    description: What this argument does
    required: true/false
    default: "value" (if not required)
allowed-tools:
  - Read
  - Write
  - Bash
model: claude-sonnet-4.5 (optional, for cost/performance optimization)
---
```

### For Agents
```yaml
---
name: Agent Name
description: What this agent does and when to use it
allowed-tools:
  - Read
  - Grep
  - WebSearch
model: claude-sonnet-4 (optional, cheaper for simple tasks)
---
```

### For Skills
```yaml
---
name: Skill Name
description: What this Skill does and when Claude should activate it (critical for discovery!)
allowed-tools:
  - Read
  - AskUserQuestion
---
```

**Tool Reference:** `.claude/libraries/internal/tool-reference.md`

## Command Creation Workflow

### Manual Process

1. **Choose Template**
   ```bash
   # List templates
   ls .claude/libraries/internal/templates/

   # View template
   cat .claude/libraries/internal/templates/level-2-workflow.md
   ```

2. **Copy Template to Target Location**
   ```bash
   # System command
   cp template .claude/commands/system/HAL-my-command.md

   # Development command
   cp template .claude/commands/development/HAL-my-command.md
   ```

3. **Remove Unused Sections**
   - Delete sections you don't need
   - Keep only relevant Lego blocks

4. **Fill in Your Logic**
   - Write specific instructions
   - Define parameters
   - Specify tools needed
   - Add error handling

5. **Test**
   - Run command via `/HAL-my-command`
   - Verify behavior
   - Iterate

### Automated Process (Recommended)

Use the command-builder agent:
```bash
/HAL-command-create "Natural language description of desired command"
```

The agent will:
- Select appropriate template
- Generate HAL-Script code
- Add proper frontmatter
- Validate against architecture principles
- Save to correct location

## Best Practices

### 1. Single Responsibility
Each command does ONE thing well (Unix philosophy)

**Good:**
- `HAL-session-end` - Save session state
- `HAL-index-update` - Update indexes

**Bad:**
- `HAL-session-and-index` - Multiple unrelated operations

### 2. Clear Parameter Names
```yaml
# Good
arguments:
  - name: session_description
    description: Brief description of the session work
    required: true

# Bad
arguments:
  - name: desc
    description: Description
    required: true
```

### 3. Explicit Tool Whitelisting
Only request tools you actually need:

```yaml
# Read-only command
allowed-tools:
  - Read
  - Grep
  - Glob

# State-mutating command
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
```

### 4. Error Handling
Include error cases in instructions:

```markdown
## Instructions

1. Read target file
2. IF file not found:
   - Report error to user
   - Suggest alternative paths
   - EXIT
3. Process file contents
4. IF processing fails:
   - Set ERROR_FLAG register
   - Report specifics
   - Suggest recovery
```

### 5. Output Specification
Be explicit about what to return:

```markdown
## Output Format

Return to user:
- Success/failure status
- Summary of operations performed
- Any warnings or errors
- Next recommended action (if applicable)
```

### 6. Architecture Compliance
Check against principles:
- ✓ Single responsibility (Unix)
- ✓ Selective loading (von Neumann)
- ✓ Explicit control flow (Assembly)
- ✓ Proper depth (max 3 levels)

## Common Patterns

### Pattern 1: Read-Process-Report (Level 1-2)
```markdown
1. Read input file
2. Process content
3. Report results to user
```

### Pattern 2: Search-Load-Analyze (Level 2-3)
```markdown
1. Search for files matching criteria
2. IF found:
   - Load relevant files
   - Analyze content
   - Report findings
3. ELSE:
   - Report not found
   - Suggest alternatives
```

### Pattern 3: Delegate-Process-Persist (Level 4)
```markdown
1. Validate inputs
2. Delegate heavy work to sub-agent (research-synthesizer, hal-context-finder, etc.)
3. Process agent results
4. Persist to file system
5. Report summary to user
```

### Pattern 4: Multi-Agent Coordination (Level 5)
```markdown
1. Break task into subtasks
2. Launch agents in parallel:
   - Agent A: Subtask 1
   - Agent B: Subtask 2
3. Collect results
4. Synthesize combined output
5. Report to user
```

## Examples

### Example 1: Simple Command (Level 1)

**Task:** Display system version

```yaml
---
name: Version Display
description: Display HAL8000 system version
allowed-tools:
  - Read
---

# Version Display

## Purpose
Display current HAL8000 system version from VERSION file.

## Instructions
1. Read /mnt/d/~HAL8000/VERSION file
2. Display version to user in format: "HAL8000 v[X.Y.Z]"

## Error Handling
IF VERSION file not found:
- Report: "ERROR: VERSION file missing"
- Suggest: "System may be corrupted, check installation"
```

### Example 2: Workflow with Parameters (Level 2)

**Task:** Create session summary

```yaml
---
name: Session Summary
description: Create summary of current session work
arguments:
  - name: summary_type
    description: Type of summary (brief, detailed, technical)
    required: false
    default: "brief"
allowed-tools:
  - Read
  - Write
---

# Session Summary

## Purpose
Generate summary of current session work for documentation.

## Parameters
- `summary_type`: "brief" (key points), "detailed" (comprehensive), "technical" (code-focused)

## Instructions

1. Review current session context
2. IF summary_type == "brief":
   - Extract 3-5 key accomplishments
   - Format as bullet list
3. ELSE IF summary_type == "detailed":
   - Full chronological work log
   - Include decisions, changes, outcomes
4. ELSE IF summary_type == "technical":
   - Focus on code changes
   - Include file paths, functions modified
5. Write summary to data/sessions/summaries/[timestamp]-summary.md
6. Report location to user

## Output Format
- Summary file path
- Summary type used
- Word count
```

### Example 3: Agent Delegation (Level 4)

**Task:** Research and document topic

```yaml
---
name: Research Documentation
description: Research topic and create documentation file
arguments:
  - name: topic
    description: Topic to research
    required: true
  - name: depth
    description: Research depth (quick, standard, comprehensive)
    required: false
    default: "standard"
allowed-tools:
  - Task
  - Read
  - Write
---

# Research Documentation

## Purpose
Delegate research to research-synthesizer agent and persist results.

## Parameters
- `topic`: Subject to research
- `depth`: How thorough (quick=1-2 sources, standard=3-5, comprehensive=8-10)

## Instructions

1. Validate topic parameter (not empty)
2. Determine search scope based on depth parameter
3. Delegate to research-synthesizer agent:
   - Prompt: "Research [topic] with [depth] depth. Provide structured report with Summary, Key Findings, Detailed Analysis, Sources."
   - Wait for agent completion
4. Process agent results:
   - Extract summary
   - Format for documentation
5. Persist to data/research/[sanitized-topic-name].md
6. Update research index if exists
7. Report to user:
   - File location
   - Summary (3-4 sentences)
   - Source count

## Error Handling
IF topic is empty:
- Report error
- Request valid topic
- EXIT

IF agent fails:
- Report failure details
- Offer to retry
- Suggest manual research alternative
```

## Debugging HAL-Script

### Common Issues

1. **Command not discovered in palette**
   - Check YAML frontmatter syntax
   - Ensure `name` and `description` are present
   - Verify file is in `.claude/commands/`

2. **Tool permission denied**
   - Add tool to `allowed-tools` list
   - Check tool name spelling (exact match required)

3. **Parameters not working**
   - Verify `arguments` YAML structure
   - Check parameter name matches usage in instructions
   - Ensure required parameters have `required: true`

4. **Command does wrong thing**
   - Review instruction sequence
   - Add explicit control flow (IF/ELSE)
   - Include error handling for edge cases

## Integration with HAL8000

**Works with:**
- command-builder agent (automates creation)
- architecture-consultant Skill (validates design)
- Template library (provides structure)

**References:**
- `data/architecture/hal-script-language.md` (full spec)
- `.claude/commands/README.md` (organization guide)
- `.claude/libraries/internal/templates/template-guide.md` (template usage)

For template selection help, see [template-selector.md](template-selector.md).
