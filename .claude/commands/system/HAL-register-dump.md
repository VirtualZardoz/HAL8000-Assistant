---
name: HAL-register-dump
description: Display current CPU register state for system introspection
---

# HAL-register-dump

**Command:** `/HAL-register-dump`
**Category:** System Introspection
**Purpose:** Display current CPU register state

---

## Description

Dumps the current state of all HAL8000-Assistant CPU registers, providing a snapshot of the system's immediate working memory. This command allows inspection of the CPU's internal state without modifying it.

Registers are virtual - they represent actual runtime state scattered across the system. This command aggregates and formats that state for human-readable output.

---

## Usage

```bash
/HAL-register-dump
```

No arguments required.

---

## Behavior

When executed, the CPU will:

1. **Read all register values** from their actual sources:
   - Memory registers from system warnings
   - State registers from `state.json` and runtime context
   - Control registers from current execution state
   - Status registers from system conditions
   - Data registers from working memory

2. **Generate formatted output** showing:
   - All 21 registers organized by category
   - Current values with human-readable formatting
   - Status indicators and warnings
   - Timestamp of snapshot

3. **Display register dump** in terminal

---

## Output Format

```
================================================================================
                        HAL8000-Assistant REGISTER DUMP
================================================================================
Timestamp: 2025-10-04T15:30:45Z
Model: claude-sonnet-4-5-20250929

[CONTROL REGISTERS]
  PC (Program Counter)        : null
  IR (Instruction Register)   : Show register state
  EXEC_MODE                   : INTERACTIVE
  FLOW_STATE                  : Executing register dump command

[MEMORY REGISTERS]
  RAM_USAGE                   : 58,432 tokens
  RAM_CAPACITY                : 200,000 tokens
  RAM_REMAINING               : 141,568 tokens
  RAM_ZONE                    : SAFE (29% used)
  CONTEXT_MANIFEST            : 5 files loaded
    - CLAUDE.md
    - .claude/state.json
    - .claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md
    - data/research/04-claude-code-runtime-constraints.md
    - .claude/commands/HAL-register-dump.md

[STATE REGISTERS]
  SESSION_ID                  : .claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md
  SESSION_START               : 2025-10-04T14:23:15Z
  SESSION_DURATION            : 1h 7m 30s
  CHECKPOINT_STATUS           :
    - Last checkpoint         : 2025-10-04T13:05:18Z
    - Checkpoint file         : .claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md
    - Changes since checkpoint: true
  PHASE                       : register-architecture-complete
  LOADED_COMMANDS             : 2 commands
    - HAL-session-end
    - HAL-register-dump

[STATUS REGISTERS]
  CPU_STATUS                  : OPERATIONAL ✓
  RATE_LIMIT_STATUS           :
    - Limited                 : false
    - Usage estimate          : ~15%
    - Reset cycle             : 5 hours
  ERROR_FLAG                  : false
  ERROR_CODE                  : null

[DATA REGISTERS]
  ACC (Accumulator)           : Executing register dump
  VARS (Session Variables)    : 4 variables
    - current_project         : HAL8000-Assistant architecture
    - architecture_type       : Modified von Neumann
    - depth_limit             : 3
    - phase                   : register-architecture-complete
  RESULT (Last Operation)     : Command file created successfully

================================================================================
                            SYSTEM STATUS: OPERATIONAL
RAM: SAFE | CPU: OPERATIONAL | Session: Active | Errors: None
================================================================================
```

---

## Implementation

The CPU executes this command by:

1. **Extracting RAM state** from most recent system warning
   ```
   <system_warning>Token usage: 58432/200000; 141568 remaining</system_warning>
   ```

2. **Reading state.json** for persistent state:
   ```json
   {
     "active_session": "...",
     "variables": {...},
     "loaded_commands": [...]
   }
   ```

3. **Evaluating runtime state**:
   - Current instruction (IR) = user's command
   - Execution mode (EXEC_MODE) = current context
   - CPU status = system health evaluation
   - Error state = last operation result

4. **Calculating derived values**:
   - RAM_ZONE from usage percentage
   - SESSION_DURATION from SESSION_START
   - Rate limit estimate (approximate)

5. **Formatting output** with clear categorization and human-readable values

---

## Use Cases

### Debugging
Check system state when troubleshooting issues:
```
User: "Why did that operation fail?"
User: /HAL-register-dump
Output: Shows ERROR_FLAG=true, ERROR_CODE="File not found"
```

### Resource Monitoring
Monitor RAM usage during intensive operations:
```
User: /HAL-register-dump
Output: RAM_ZONE: CAUTION (85% used) - Consider /compact
```

### Session Inspection
Understand current session state:
```
User: "What session am I in?"
User: /HAL-register-dump
Output: Shows SESSION_ID, SESSION_START, PHASE
```

### System Verification
Verify CPU operational status:
```
User: /HAL-register-dump
Output: CPU_STATUS: OPERATIONAL ✓, no errors, SAFE zone
```

### Learning
Understand how the system works:
```
User: "Show me what registers look like during execution"
User: /HAL-register-dump
Output: Complete register snapshot with explanations
```

---

## Notes

**Read-Only Operation:**
- This command does NOT modify any registers
- It only reads and displays current state
- Safe to run at any time

**Snapshot Nature:**
- Values reflect state at moment of execution
- Registers continuously update during operation
- Run again to see updated values

**Virtual Registers:**
- Registers are not stored in a file
- This command aggregates state from multiple sources
- The "register file" is virtual, constructed on-demand

**Performance Impact:**
- Minimal - only reads existing state
- Adds ~2-3K tokens to context (the output itself)
- No file I/O required (reads from runtime state)

---

## Related Commands

- `/HAL-session-end` - Checkpoint session (updates CHECKPOINT_STATUS register)
- `/compact` - Reduce context size (affects RAM_USAGE)
- `/clear` - Reset session (clears volatile registers)
- `/context` - Debug context issues (v1.0.86+)

---

## Register Documentation

For complete register specifications, see:
- `data/architecture/hal8000-register-architecture.md` - Full register architecture spec
- `data/research/04-claude-code-runtime-constraints.md` - Runtime constraints
- `CLAUDE.md` - System architecture overview

---

## Example Session

```
$ You: /HAL-register-dump

[CPU generates and displays register dump]

$ You: "How much RAM can I use before I should checkpoint?"

CPU: Based on RAM registers:
- Current: 58K tokens (29%)
- SAFE zone extends to 160K tokens (80%)
- You have ~102K tokens of SAFE headroom
- Recommend checkpoint before 180K (CAUTION zone)

$ You: "What files are currently loaded?"

CPU: From CONTEXT_MANIFEST register:
- CLAUDE.md (BIOS)
- state.json
- Active session file
- Runtime constraints research
- This command file
Total: 5 files, ~58K tokens
```

---

## Architecture Notes

This command implements the **introspection capability** fundamental to assembly-level programming. In traditional assembly, developers can inspect CPU registers directly (e.g., `REGISTER DUMP` or debugger commands).

HAL8000-Assistant provides the same capability for the virtual CPU, enabling:
- System state visibility
- Debugging support
- Educational understanding
- Operational transparency

The command embodies the principle: **"The system should be inspectable at the lowest level."**
