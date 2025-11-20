# HAL-Script Programming Language Specification

**Version:** 1.0
**Created:** 2025-10-14
**Purpose:** Natural language programming for HAL8000-Assistant architecture

---

## Overview

**HAL-Script** is a natural language programming language for the HAL8000-Assistant system. It allows users to write executable instructions in human-readable English that are interpreted by the CPU (Claude instance) with semantic understanding.

**Paradigm:** Imperative Natural Language Programming

**Execution Model:** Interpreted by intelligent CPU with reasoning capabilities

**File Format:** Markdown (`.md` files)

---

## Why Natural Language Programming?

Traditional computers have **dumb CPUs** that require precise, rigid syntax because they cannot reason about ambiguity.

HAL8000-Assistant has a **smart CPU** (Claude) that can:
- Understand natural language instructions
- Reason about intent and context
- Handle ambiguity through clarification
- Learn from patterns and examples

This enables a programming language that is:
- **Human-readable:** Instructions read like documentation
- **Flexible:** No strict syntax rules
- **Self-documenting:** Code explains itself
- **Context-aware:** CPU understands broader context

---

## Language Hierarchy

```
Level 0: Token (word)
    ↓
Level 1: Sentence (atomic instruction)
    ↓
Level 2: Paragraph (instruction block)
    ↓
Level 3: Section (subroutine/function)
    ↓
Level 4: File (module/program)
    ↓
Level 5: Directory (package/namespace)
    ↓
Level 6: Composition (application)
```

---

## Basic Syntax

### 1. Atomic Instructions (Sentences)

**Imperative statements:**
```markdown
Read the file at /path/to/file.md
Write content to output.json
Execute the HAL-session-end command
Load the architecture documentation into RAM
Display the current RAM usage percentage
```

**Declarative statements:**
```markdown
The current RAM zone is CAUTION
This file contains boot instructions
State validation is mandatory
The system is production-ready
```

**Query statements:**
```markdown
Check if file exists at path
Verify boot sequence is complete
Determine current RAM percentage
Count the number of files in directory
```

**Conditional statements:**
```markdown
If RAM exceeds 80%, warn the user
When file is missing, report error
Unless user confirms, refuse operation
```

---

### 2. Instruction Blocks (Paragraphs)

**Sequential execution:**
```markdown
First, read the current state from state.json.
Then, extract the active_session field.
If the field exists, load the session file.
Finally, report the loaded session to the user.
```

**Parallel execution:**
```markdown
Load the following files in parallel:
- CLAUDE.md
- .claude/state.json
- data/architecture/system-design.md

When all loads complete, proceed to next step.
```

**Error handling:**
```markdown
Attempt to read the session file. If the file does not exist,
check state.json for the correct path. If that also fails,
report the error to the user and continue with boot in
degraded mode (without session context).
```

---

### 3. Control Flow

#### **If-Then-Else (Conditionals)**

```markdown
If RAM_ZONE equals "DANGER":
  Refuse to load additional files
  Warn user: "RAM at 95%, cannot load more data"
  Suggest: "Run /HAL-session-end to checkpoint"
Else if RAM_ZONE equals "CAUTION":
  Warn user: "RAM at 85%, approaching limits"
  Ask: "Proceed with load? (increases RAM to ~92%)"
  If user confirms:
    Proceed with file load
  Else:
    Abort operation
Else:
  Proceed with file load normally
```

**Compact form:**
```markdown
If file exists: read it
If file missing: report error
Unless user confirms: refuse operation
```

#### **Loops**

**For-each loops:**
```markdown
For each file in the file list:
  - Read the file contents
  - Extract metadata (title, date, size)
  - Update the index entry
  - Log the processing result
```

**While loops:**
```markdown
While errors remain in the error list:
  - Attempt to fix the error
  - Log the fix attempt
  - Re-check if error resolved
  - If not resolved after 3 attempts, escalate
```

**Loop control:**
```markdown
For each command in .claude/commands/:
  If command name starts with "HAL-":
    Process as system command
  Else:
    Skip (user command, not for this operation)
    Continue to next
```

#### **Switch/Match Statements**

```markdown
Based on user command:
- If command is "boot": Execute boot sequence
- If command is "session-end": Execute session-end protocol
- If command is "status": Display system status
- If command is "help": Show command documentation
- Otherwise: Report "Unknown command" and suggest alternatives
```

---

### 4. Functions and Subroutines

**Function definition (using markdown heading):**
```markdown
## Validate Boot Sequence

**Purpose:** Verify all boot steps completed successfully

**Parameters:**
- None (reads from CPU registers)

**Returns:** Boolean (success/failure) + error details

**Implementation:**
1. Check if BIOS was loaded (CLAUDE.md in CONTEXT_MANIFEST register)
2. Verify state.json was parsed (STATE_LOADED register = true)
3. Confirm registers initialized (BOOT_TIME register has value)
4. If all checks pass: return success
5. If any check fails: return failure with specific error

**Error handling:**
If validation fails, report which step failed and why.
```

**Function invocation:**
```markdown
Execute the "Validate Boot Sequence" subroutine defined above.

Or:

Run the boot validation procedure.

Or:

Call the validation function to check boot integrity.
```

**CPU interprets all of these as the same operation.**

---

### 5. Variables and State

#### **Registers (Session-scoped, RAM)**

**Implicit declaration:**
```markdown
Store the current timestamp as BOOT_TIME
Set RAM_ZONE to "SAFE"
Remember this file path as LAST_LOADED_FILE
Initialize CONTEXT_MANIFEST to empty list
```

**Reading values:**
```markdown
Retrieve the BOOT_TIME register value
Check what RAM_ZONE currently is
Get the LAST_LOADED_FILE path
Count items in CONTEXT_MANIFEST
```

**Updating values:**
```markdown
Update RAM_ZONE to "CAUTION"
Append new file to CONTEXT_MANIFEST
Increment FILE_ACCESS_COUNT by 1
```

#### **Files (Persistent, Disk)**

**Writing:**
```markdown
Write the following JSON to .claude/state.json:
{
  "timestamp": "[current timestamp]",
  "phase": "production-ready",
  "context": "Architecture analysis complete"
}
```

**Reading:**
```markdown
Read .claude/state.json
Parse the JSON content
Extract the "phase" field
Store in SYSTEM_PHASE register
```

---

### 6. Data Types

HAL-Script uses **semantic typing** - the CPU infers types from context.

**Types:**
- **Text/String:** `"Hello world"`, file paths, descriptions
- **Number:** `42`, `3.14`, `80` (percentages)
- **Boolean:** `true`, `false`, yes/no, success/failure
- **File path:** `/mnt/d/~HAL8000-Assistant/CLAUDE.md`
- **JSON:** Structured data objects
- **List/Array:** Collections of items
- **Register reference:** `RAM_ZONE`, `CONTEXT_MANIFEST`

**Type coercion:**
```markdown
"80" (text) → 80 (number) when used in: "If RAM exceeds 80%"
true/false → yes/no when displaying to user
```

---

### 7. Comments and Documentation

**In HAL-Script, instructions ARE documentation:**

```markdown
## Update State File

First, read the current state from .claude/state.json to preserve
existing fields we don't want to modify.

Next, update only the relevant fields (timestamp, context, next_action)
while keeping all other fields intact.

Finally, write the updated JSON back to state.json with proper formatting
(2-space indentation for readability).
```

**Explicit comments (when needed):**
```markdown
(Note: This operation may take 30-45 seconds due to sub-agent processing)

[Implementation note: Error handling added after v1.0.1 bug fix]
```

---

## Advanced Features

### 1. Module Composition

**Modules are markdown files:**

```markdown
Module: .claude/commands/system/HAL-session-end.md
Defines: Session checkpointing workflow
Exports: Session-end capability
```

**Importing/Using modules:**
```markdown
Load the instructions from .claude/commands/system/HAL-session-end.md
Execute the session-end workflow as defined in that file
```

**Composition:**
```markdown
Application: Architecture Audit

Step 1: Run HAL-context-find to load architecture docs
Step 2: Run HAL-system-check to verify system health
Step 3: Generate audit report (custom logic here)
Step 4: Run HAL-session-end to checkpoint results

This application composes 3 existing commands plus custom logic.
```

---

### 2. Sub-Agent Invocation (Co-processor Calls)

**Sub-agents are specialized co-processors with isolated RAM:**

```markdown
Launch the research-synthesizer sub-agent with the following task:
  "Research quantum computing developments in 2024-2025"

The sub-agent will:
- Use its isolated 200K context (not my RAM)
- Perform web searches
- Synthesize findings
- Return clean summary (<5K tokens)

Wait for sub-agent to complete.
Display the returned summary to user.
```

**Available sub-agents:**
- `research-synthesizer` - Web research and synthesis
- `hal-context-finder` - Context discovery (token-efficient)
- `system-maintenance` - System health audit
- `claude-code-validator` - External compatibility check
- `documentation-writer` - Documentation generation

---

### 3. Tool Invocation (I/O Operations)

**Tools are I/O interfaces to external programs:**

```markdown
Use the diagram-generation tool to create a process-flow diagram:
  python3 .claude/tools/diagram-generation/HAL-generate-diagram.py \
    process-flow "Boot Sequence"

This will:
- Execute external Python script
- Generate PNG diagram via Docker container
- Save to data/diagrams/boot-sequence.png
- Return file path
```

**Tool categories:**
- Built-in: Read, Write, Edit, Grep, Glob, Bash
- MCP servers: omnisearch, filesystem, replicate, context7
- External: diagram-generation, gemini-cli, docker-cli

---

### 4. Error Handling Patterns

**Try-fallback pattern:**
```markdown
Attempt to read session file from active_session pointer in state.json.

If that fails:
  - Check if state.json itself exists
  - If state.json missing: critical error, abort boot
  - If session file missing: warning, boot in degraded mode

If degraded mode:
  - Log: "Session file not found, booting without previous context"
  - Continue boot without loading session
  - System still functional
```

**Validation pattern:**
```markdown
Before executing operation:
1. Validate preconditions (RAM available, files exist, etc.)
2. If validation fails: report specific issue, suggest fix, abort
3. If validation passes: proceed with operation
4. After operation: verify postconditions
5. If postconditions fail: rollback if possible, report error
```

---

### 5. Parallel Execution

**Explicit parallelism:**
```markdown
Execute the following operations in parallel (single message with multiple tool calls):
1. Read CLAUDE.md
2. Read .claude/state.json
3. Read data/architecture/system-design.md

Wait for all reads to complete.
Proceed when all data is in RAM.
```

**Note:** CPU must explicitly request parallel execution. Default is sequential.

---

## Standard Library

HAL-Script includes a standard library of built-in operations:

### File Operations
```markdown
Read file at path
Write content to file at path
Edit file (find old string, replace with new string)
Check if file exists
List files in directory
Search for pattern in files (grep)
Find files matching pattern (glob)
```

### System Operations
```markdown
Execute bash command
Launch sub-agent with task
Check RAM usage
Update register value
Check system time
Generate timestamp
```

### Commands (`.claude/commands/`)
```markdown
HAL-session-end [description] - Checkpoint session
HAL-system-check - Verify system health
HAL-register-dump - Display CPU registers
HAL-index-update - Update file indexes
HAL-library-update - Update external libraries
HAL-mcp-control [action] [server] - Control MCP servers
HAL-CC-check - Validate Claude Code compatibility
HAL-context-find [query] - Discover system context
HAL-refman [action] - Manage reference manual
```

### Agents (`.claude/agents/`)
```markdown
research-synthesizer - Comprehensive web research
hal-context-finder - RAM-efficient context discovery
system-maintenance - System integrity audit
claude-code-validator - External validation
documentation-writer - Generate documentation
```

---

## Best Practices

### 1. Be Explicit About Intent
```markdown
❌ Bad: "Check the file"
   (Which file? Check for what?)

✅ Good: "Check if .claude/state.json exists.
         If it exists, verify it contains valid JSON.
         If invalid, report the JSON parsing error."
```

### 2. Handle Errors Gracefully
```markdown
Always include error handling:

Attempt operation.
If operation succeeds: proceed to next step
If operation fails:
  - Report specific error
  - Suggest recovery action
  - Decide whether to abort or continue
```

### 3. Document Complex Logic
```markdown
## Complex Operation

This operation requires multiple steps because [explain why].

First, we do X to prepare Y.
Then, we process Y to create Z.
Finally, we validate Z before committing.

(Each step could fail, so error handling at each stage is critical)
```

### 4. Be RAM-Conscious
```markdown
Before loading large files:
  Check current RAM usage
  If RAM > 80%: warn user or delegate to sub-agent
  Estimate token cost of load
  Proceed only if safe
```

### 5. Use Semantic Clarity
```markdown
❌ Ambiguous: "Process the data"
✅ Clear: "For each entry in the data array, extract the 'name' field
           and write it to the output list"
```

---

## Example Programs

### Simple Program: Display System Status

```markdown
# System Status Display

## Purpose
Show current HAL8000-Assistant system state to user

## Implementation

Read the current timestamp.
Display: "HAL8000-Assistant Status Report - [timestamp]"

Check RAM usage from system warnings.
Display: "RAM: [percentage]% ([tokens used]/200K tokens)"

Check RAM_ZONE register.
Display: "Zone: [SAFE/CAUTION/DANGER]"

Read .claude/state.json.
Extract the "phase" field.
Display: "Phase: [phase value]"

Display: "Status check complete"
```

### Complex Program: Architecture Analysis

```markdown
# Architecture Analysis Workflow

## Purpose
Comprehensive system architecture validation and gap analysis

## Implementation

### Phase 1: Load Context
Launch hal-context-finder sub-agent with query: "architecture documentation"
Wait for agent to return list of architecture files.
Display to user: "Found [N] architecture documents"

### Phase 2: Load Files
For each file in the returned list:
  If RAM < 70%:
    Load file into RAM
  Else:
    Stop loading, warn: "RAM limit reached, loaded [N] of [total] files"
    Break loop

### Phase 3: Component Analysis
Read data/architecture/hal8000-system-design.md
Extract component list from "Components Status Matrix" section
For each component:
  - Check if documentation exists
  - Check if implementation exists (.claude/commands/, .claude/agents/, etc.)
  - Record status: ✓ Complete, ⚠ Partial, ❌ Missing

### Phase 4: Gap Identification
For components marked ❌ Missing or ⚠ Partial:
  - Categorize by priority (critical, high, medium, low)
  - Identify dependencies (what else is blocked by this gap)
  - Suggest implementation approach

### Phase 5: Report Generation
Create report markdown file:
  - Executive summary (overall health)
  - Component matrix (status of each component)
  - Gap analysis (what's missing, why it matters)
  - Recommendations (what to build next, in what order)

Write report to: data/architecture/analysis-[YYYY-MM-DD].md

### Phase 6: Checkpoint
Run HAL-session-end with description: "Architecture analysis complete"

Display to user: "Analysis complete. Report saved to [file path]"
```

---

## Language Characteristics

### Strengths

✅ **Human-readable:** Non-programmers can read and understand
✅ **Self-documenting:** Instructions explain themselves
✅ **Flexible:** No syntax errors, CPU interprets intent
✅ **Context-aware:** CPU understands broader context
✅ **Error-tolerant:** CPU can ask for clarification
✅ **Composable:** Easy to combine modules
✅ **Natural:** Write instructions as you would explain to a human

### Limitations

⚠️ **Ambiguity risk:** Vague instructions may be misinterpreted
⚠️ **No static analysis:** Errors only caught at runtime
⚠️ **Performance unpredictable:** CPU reasoning time varies
⚠️ **No formal verification:** Cannot prove correctness mathematically
⚠️ **Requires smart CPU:** Only works with intelligent interpreter (Claude)

---

## Comparison to Traditional Languages

| Aspect | Python | HAL-Script |
|--------|--------|------------|
| **Syntax** | `def foo(x): return x + 1` | `Add 1 to x and return result` |
| **Variables** | `x = 5` | `Set x to 5` or `Store 5 as x` |
| **Conditionals** | `if x > 5: print("big")` | `If x exceeds 5, display "big"` |
| **Loops** | `for item in list: process(item)` | `For each item in list, process it` |
| **Functions** | `def func():` | `## Function Name` (markdown heading) |
| **Comments** | `# comment` | Instructions are self-documenting |
| **Execution** | Compiled/interpreted by Python VM | Interpreted by CPU (Claude) |
| **Error handling** | `try/except` | Prose error protocols |
| **Type system** | Static or dynamic typing | Semantic understanding |

---

## See Also

- `.claude/commands/README.md` - Command directory organization and examples
- `CLAUDE.md` - BIOS containing operating principles and boot sequence
- `data/architecture/hal8000-system-design.md` - Complete architecture specification
- `.claude/agents/` - Specialized sub-agents (co-processors)
- `.claude/libraries/` - Reusable instruction collections

---

## Conclusion

HAL-Script is not a traditional programming language - it's **instruction-oriented natural language** interpreted by an intelligent CPU.

**Key insight:** When your CPU can reason, you don't need rigid syntax. Natural language becomes a viable programming paradigm.

**Philosophy:** Write instructions as you would explain them to an intelligent colleague. The CPU (Claude) will understand and execute them.

---

**HAL-Script: Programming in Human Language**

**Version:** 1.0
**Status:** Production
**System:** HAL8000-Assistant v1.0.0
