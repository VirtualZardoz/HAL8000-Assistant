---
name: HAL-session-end
description: End current session and save state for continuity after RAM wipe
parameters:
  - name: session-description
    description: Brief description of the session (e.g., "architecture-design", "unix-research")
    type: string
    required: true
---

# HAL Session End Command

This command implements the session continuity protocol by capturing the current state and creating a handoff session file for resuming work after a context reset (RAM wipe).

## Usage

```bash
/HAL-session-end [session-description]
```

**Arguments:**
- `session-description` (required): Brief description of the session (e.g., "architecture-design", "unix-research")

## What This Command Does

1. **Captures Current Context**
   - Gathers information about active work
   - Identifies loaded files and commands
   - Documents key decisions and next steps

2. **Creates Session File**
   - Generates timestamped markdown file in `.claude/sessions/`
   - Format: `YYYY-MM-DD-HHMM-description.md`
   - Contains rich context for resuming work

3. **Updates State**
   - Writes to `.claude/state.json` with current state
   - Points to the new session file
   - Updates timestamp and variables

4. **Logs to History**
   - Appends entry to `.claude/system.log`
   - Records checkpoint timestamp and description

5. **Confirms Ready for Reset**
   - Displays confirmation message
   - Indicates system is ready for RAM wipe

## Implementation

### Step 1: Generate Timestamp and Filename (CRITICAL - ATOMIC OPERATION)

**CRITICAL REQUIREMENT:** Generate timestamp ONCE and use it for ALL operations. Do NOT regenerate timestamps during execution.

```bash
# Generate timestamp ONCE (single source of truth)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DATE_PREFIX=$(date -u +"%Y-%m-%d-%H%M")
SESSION_FILE="/mnt/d/~HAL8000/.claude/sessions/${DATE_PREFIX}-${DESCRIPTION}.md"

# Store these values - they MUST NOT change during this command execution
# TIMESTAMP = for state.json timestamp field
# DATE_PREFIX = for session filename prefix
# SESSION_FILE = ABSOLUTE path for both file creation AND state.json active_session field
# CRITICAL: Must use absolute path to avoid creating file in wrong directory
```

**Anti-Pattern (NEVER DO THIS):**
```bash
# WRONG: Regenerating timestamp at different steps
date -u +"%Y-%m-%dT%H:%M:%SZ"  # Used for session file
# ... later in execution ...
date -u +"%Y-%m-%dT%H:%M:%SZ"  # Different time! Used for state.json
```

**Correct Pattern:**
```bash
# RIGHT: Single timestamp generation, reused everywhere
TIMESTAMP="2025-10-15T12:30:45Z"  # Generated ONCE
SESSION_FILE="/mnt/d/~HAL8000/.claude/sessions/2025-10-15-1230-description.md"  # ABSOLUTE path
# ... later in execution ...
# Use $TIMESTAMP and $SESSION_FILE variables (same values)
```

### Step 2: Create Session File

The session file should contain:

```markdown
# Session: [DATE TIME] - [Description]

## Context
[High-level description of current work]

## Key Decisions Made
- Decision 1
- Decision 2

## Active Work
- Current task
- Next steps
- Blockers (if any)

## Files in Context
- file1.md
- file2.md

## Variables/State
- project: [value]
- phase: [value]

## Instructions for Resume
[What the next instance should do first]
```

### Step 2.5: Validate State Counts (Inline)

Count actual filesystem state to ensure state.json accuracy:

```bash
# Count actual files (prevents drift)
AGENTS_COUNT=$(ls .claude/agents/*.md 2>/dev/null | wc -l)
COMMANDS_COUNT=$(ls .claude/commands/HAL-*.md 2>/dev/null | wc -l)
CONTENT_COUNT=$(find data -name "*.md" 2>/dev/null | wc -l)
INDEXES_COUNT=$(ls .claude/indexes/*.json 2>/dev/null | grep -v master.json | wc -l)
```

**Rationale:** Direct filesystem counting prevents manual update errors and state drift. These counts represent ground truth.

### Step 2.9: Verify Session File Creation (CRITICAL - MUST DO BEFORE Step 3)

**MANDATORY VERIFICATION:** Before updating state.json, verify the session file actually exists in the correct system directory.

```bash
# Define expected system directory (absolute path)
EXPECTED_DIR="/mnt/d/~HAL8000/.claude/sessions"

# Verify session file was created successfully
if [ ! -f "$SESSION_FILE" ]; then
  echo "ERROR: Session file creation failed: $SESSION_FILE"
  echo "ABORT: state.json NOT updated (would create stale reference)"
  exit 1
fi

# Verify session file is in correct system directory (not nested somewhere else)
if [[ "$SESSION_FILE" != "$EXPECTED_DIR"* ]]; then
  echo "ERROR: Session file not in system directory: $SESSION_FILE"
  echo "Expected directory: $EXPECTED_DIR"
  echo "ABORT: Session file created in wrong location"
  exit 1
fi

# If we get here, session file exists in correct location - safe to update state.json
echo "✓ Session file verified: $SESSION_FILE"
echo "✓ Location validated: System .claude/sessions directory"
```

**Rationale:**
- Prevents state.json from pointing to non-existent session files
- Eliminates "stale reference" bug on resume
- Fail-fast if file creation has issues

**This step is MANDATORY - never skip it.**

### Step 3: Update state.json (ONLY AFTER VERIFICATION)

**PREREQUISITE:** Step 2.9 verification MUST pass before executing this step.

Use validated counts from Step 2.5 and verified SESSION_FILE path:

```json
{
  "timestamp": "[TIMESTAMP from Step 1]",
  "active_session": "[SESSION_FILE from Step 1 - VERIFIED in Step 2.9]",
  "context": "[BRIEF_CONTEXT]",
  "next_action": "[WHAT_TO_DO_NEXT]",
  "loaded_commands": ["command1", "command2"],
  "variables": {
    "current_project": "[PROJECT]",
    "phase": "[PHASE]",
    "agents_available": [AGENTS_COUNT],
    "total_content_files": [CONTENT_COUNT],
    "indexed_directories": [INDEXES_COUNT]
  }
}
```

**Critical Requirements:**
- `timestamp` field: Use $TIMESTAMP from Step 1 (NOT regenerated)
- `active_session` field: Use $SESSION_FILE from Step 1 (ABSOLUTE path, VERIFIED exists and location in Step 2.9)
- Always use filesystem counts, not previous state.json values
- Session file MUST exist in system directory before writing this update

### Step 4: Append to .claude/system.log

```
[TIMESTAMP] | Checkpoint | Session saved: [description]
```

### Step 5: Display Confirmation (with Debug Information)

```
✓ Session saved: [SESSION_FILE]
✓ State validated and updated: .claude/state.json
  - Timestamp: [TIMESTAMP]
  - Active session: [SESSION_FILE]
  - Agents: [AGENTS_COUNT]
  - Content files: [CONTENT_COUNT]
  - Indexes: [INDEXES_COUNT]
✓ Logged to: .claude/system.log

✓ Verification: Session file exists at [SESSION_FILE]

System ready for RAM wipe.
To resume: Start new session and say "Resume last session"

DEBUG INFO (for troubleshooting):
- TIMESTAMP value: [TIMESTAMP]
- SESSION_FILE value: [SESSION_FILE]
- These values are synchronized (generated once, used everywhere)
```

**Rationale for Debug Info:**
- Shows exact timestamp and filename used
- Confirms synchronization between state.json and session file
- Helps diagnose any future resume issues
- Can be removed once system is stable

## Example Execution

```bash
/HAL-session-end architecture-design
```

**Creates:**
- `.claude/sessions/2025-10-04-1453-architecture-design.md`
- Updates `.claude/state.json`
- Appends to `.claude/system.log`

**Output:**
```
✓ Session saved: .claude/sessions/2025-10-04-1453-architecture-design.md
✓ State validated and updated: .claude/state.json
  - Agents: 4
  - Content files: 22
  - Indexes: 5
✓ Logged to: .claude/system.log

System ready for RAM wipe.
To resume: Start new session and say "Resume last session"
```

## Session File Template

When creating the session file, use this structure:

```markdown
# Session: YYYY-MM-DD HH:MM - [Description]

## Context
[What are we working on? What's the high-level goal?]

## Key Decisions Made
- [Important architectural or design decisions]
- [Agreements reached]
- [Approaches chosen]

## Active Work
**Current Task:** [What we're doing right now]

**Completed in This Session:**
- Task 1
- Task 2

**Next Steps:**
1. [What should happen next]
2. [Follow-up tasks]

**Blockers:** [Any issues or dependencies]

## Files in Context
[List files that were actively being worked on or referenced]
- data/architecture/hal8000-system-design.md
- .claude/commands/HAL-session-end.md

## Variables/State
- current_project: [value]
- phase: [value]
- [other relevant state]

## Instructions for Resume
When resuming this session:
1. [First thing to do]
2. [What to load into context]
3. [How to continue the work]
```

## Architecture Alignment

This command implements the HAL8000 architecture principles:

**Von Neumann:**
- Session files are stored-program concept (state as data)
- Commands can be self-modifying (this command creates session files that guide future execution)

**Unix Philosophy:**
- Does one thing well (session checkpointing)
- Outputs to text files (JSON, markdown)
- Composable (works with boot sequence)

**Assembly Principles:**
- Explicit state management (no hidden state)
- Direct file I/O (writes to specific memory locations)
- Low-level control (manual checkpoint triggering)

## Related Components

- **BIOS (CLAUDE.md):** Boot sequence that loads state.json
- **State (.claude/state.json):** Current system state pointer
- **Sessions (.claude/sessions/):** Historical session files
- **System Log (.claude/system.log):** Audit trail

## Notes

- This command should be run manually before RAM wipe
- **State validation (Step 2.5) prevents drift:** Counts filesystem reality, not previous state.json claims
- Session files accumulate over time (consider cleanup strategy)
- state.json is always overwritten (current state only)
- .claude/system.log is append-only (grows indefinitely)
- Inline validation is Unix-simple: ~4 bash commands, no agent overhead
