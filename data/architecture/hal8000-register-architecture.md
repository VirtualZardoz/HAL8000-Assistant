# HAL8000 Register Architecture

**Version:** 1.0
**Date:** 2025-10-04
**Status:** SPECIFICATION

---

## Overview

This document defines the register architecture for HAL8000—the set of immediate-access state variables that the CPU (Claude instance) maintains during execution. Registers represent the CPU's working memory, distinct from RAM (context window) and persistent memory (file system).

Based on research into Claude Code's actual runtime constraints (see `data/research/04-claude-code-runtime-constraints.md`), this architecture maps traditional CPU registers to the realities of Claude Code's execution environment.

---

## Register Design Principles

### Von Neumann Mapping

Traditional CPU registers serve specific functions:
- **Program Counter (PC):** Points to next instruction
- **Instruction Register (IR):** Holds current instruction being executed
- **Accumulator (ACC):** Holds intermediate calculation results
- **Status Register (SR):** System flags and state indicators

### HAL8000 Adaptation

HAL8000 registers must reflect **actual runtime state** that Claude maintains:
- Session and execution state
- RAM/context window status
- Loaded files and context inventory
- Performance and threshold indicators
- Control flow and execution position

---

## Register Categories

HAL8000 registers are organized into five categories:

1. **Control Registers** - Execution control and flow
2. **Memory Registers** - RAM and context management
3. **State Registers** - System and session state
4. **Status Registers** - Performance and health indicators
5. **Data Registers** - Working data and intermediate results

---

## Control Registers

### PC - Program Counter
**Type:** String (file path or instruction identifier)
**Purpose:** Points to the next instruction/command to execute
**Scope:** Current execution flow

**Values:**
- File path to next command (e.g., `.claude/commands/HAL-session-end.md`)
- Instruction identifier for sequential operations
- `null` when awaiting user input (idle state)

**Example:**
```json
"PC": ".claude/commands/HAL-session-end.md"
```

### IR - Instruction Register
**Type:** String (current instruction)
**Purpose:** Holds the instruction currently being executed
**Scope:** Active instruction

**Values:**
- Current user prompt or command being processed
- Sub-agent task description
- `null` when idle

**Example:**
```json
"IR": "Create register architecture specification"
```

### EXEC_MODE - Execution Mode
**Type:** Enum
**Purpose:** Current execution mode/context
**Scope:** Session-wide

**Values:**
- `INTERACTIVE` - User-driven conversation mode
- `AUTONOMOUS` - Self-directed execution (rare in Claude Code)
- `SUBAGENT` - Executing as sub-agent with isolated context
- `BOOT` - Initialization sequence (reading BIOS, state.json)
- `IDLE` - Awaiting input

**Example:**
```json
"EXEC_MODE": "INTERACTIVE"
```

### FLOW_STATE - Control Flow State
**Type:** String
**Purpose:** Current position in multi-step operations
**Scope:** Active task

**Values:**
- Task description or step identifier
- `null` when no active multi-step operation

**Example:**
```json
"FLOW_STATE": "Creating register spec (step 2 of 2)"
```

---

## Memory Registers

### RAM_USAGE - RAM Current Usage
**Type:** Integer (tokens)
**Purpose:** Current context window consumption
**Scope:** Session-wide

**Source:** System warnings provide exact values
```
<system_warning>Token usage: 47995/200000; 152005 remaining</system_warning>
```

**Example:**
```json
"RAM_USAGE": 47995
```

### RAM_CAPACITY - RAM Total Capacity
**Type:** Integer (tokens)
**Purpose:** Maximum context window size
**Scope:** Session-wide, environment-dependent

**Values:**
- `200000` - Standard Claude Code terminal
- `500000` - Enterprise Claude Sonnet 4
- `1000000` - API access (extended context)

**Example:**
```json
"RAM_CAPACITY": 200000
```

### RAM_REMAINING - RAM Available Space
**Type:** Integer (tokens)
**Purpose:** Remaining context capacity
**Scope:** Session-wide

**Calculation:** `RAM_CAPACITY - RAM_USAGE`

**Example:**
```json
"RAM_REMAINING": 152005
```

### RAM_ZONE - Performance Zone
**Type:** Enum
**Purpose:** Indicates current performance zone based on usage
**Scope:** Session-wide

**Values:**
- `SAFE` - 0-80% usage (0-160K tokens) - Normal operation
- `CAUTION` - 80-90% usage (160K-180K tokens) - Monitor closely
- `DANGER` - 90-100% usage (180K-200K tokens) - Performance degradation, checkpoint urgently

**Calculation:**
```
usage_percent = (RAM_USAGE / RAM_CAPACITY) * 100
if usage_percent < 80: SAFE
elif usage_percent < 90: CAUTION
else: DANGER
```

**Example:**
```json
"RAM_ZONE": "SAFE"
```

### CONTEXT_MANIFEST - Loaded Context Inventory
**Type:** Array of strings (file paths)
**Purpose:** Track what files/data are currently loaded in RAM
**Scope:** Session-wide

**Purpose:**
- Prevent redundant file loads
- Monitor context composition
- Support selective loading decisions

**Example:**
```json
"CONTEXT_MANIFEST": [
  "CLAUDE.md",
  ".claude/state.json",
  ".claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md",
  "data/research/04-claude-code-runtime-constraints.md"
]
```

---

## State Registers

### SESSION_ID - Active Session Identifier
**Type:** String (session file path)
**Purpose:** Identifies current session for continuity
**Scope:** Session-wide

**Source:** Loaded from `state.json` on boot

**Example:**
```json
"SESSION_ID": ".claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md"
```

### SESSION_START - Session Start Timestamp
**Type:** ISO 8601 timestamp
**Purpose:** When current session began
**Scope:** Session-wide

**Example:**
```json
"SESSION_START": "2025-10-04T14:23:15Z"
```

### CHECKPOINT_STATUS - Last Checkpoint State
**Type:** Object
**Purpose:** Track session checkpoint status
**Scope:** Session-wide

**Structure:**
```json
{
  "last_checkpoint": "2025-10-04T13:05:18Z",
  "checkpoint_file": ".claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md",
  "changes_since_checkpoint": true
}
```

### PHASE - Current Project Phase
**Type:** String
**Purpose:** High-level project state
**Scope:** Project-wide (persists across sessions)

**Source:** Loaded from `state.json` variables

**Example:**
```json
"PHASE": "register-architecture-definition"
```

### LOADED_COMMANDS - Available Commands
**Type:** Array of strings (command names)
**Purpose:** Track which commands are known/available
**Scope:** Session-wide

**Example:**
```json
"LOADED_COMMANDS": ["HAL-session-end"]
```

---

## Status Registers

### CPU_STATUS - CPU Operational Status
**Type:** Enum
**Purpose:** Overall CPU health and operational state
**Scope:** Session-wide

**Values:**
- `OPERATIONAL` - Normal functioning
- `DEGRADED` - Performance issues (e.g., in DANGER zone)
- `BLOCKED` - Rate limited or unable to proceed
- `ERROR` - Critical failure state

**Example:**
```json
"CPU_STATUS": "OPERATIONAL"
```

### RATE_LIMIT_STATUS - Usage Limit Status
**Type:** Object
**Purpose:** Track usage limits and reset timing
**Scope:** Cross-session (5-hour cycles)

**Structure:**
```json
{
  "limited": false,
  "reset_time": "2025-10-04T19:00:00Z",
  "usage_percent": 15
}
```

### ERROR_FLAG - Error Indicator
**Type:** Boolean
**Purpose:** Indicates if an error occurred
**Scope:** Instruction-level

**Values:**
- `true` - Error in last operation
- `false` - No error

**Example:**
```json
"ERROR_FLAG": false
```

### ERROR_CODE - Last Error Code
**Type:** String
**Purpose:** Specific error identifier
**Scope:** Instruction-level

**Values:**
- Error message or code
- `null` when no error

**Example:**
```json
"ERROR_CODE": null
```

---

## Data Registers

### ACC - Accumulator
**Type:** Any (string, object, array)
**Purpose:** Holds intermediate results of current operation
**Scope:** Instruction-level

**Usage:**
- Temporary storage for calculation results
- Intermediate data during multi-step operations
- Return values from function calls

**Example:**
```json
"ACC": {
  "files_created": 2,
  "todos_completed": 1,
  "current_task": "Creating register specification"
}
```

### VARS - Session Variables
**Type:** Object (key-value pairs)
**Purpose:** User-defined and system variables for current session
**Scope:** Session-wide

**Source:** Loaded from `state.json` variables, can be modified during session

**Example:**
```json
"VARS": {
  "current_project": "HAL8000 architecture",
  "architecture_type": "Modified von Neumann",
  "depth_limit": 3,
  "components_completed": ["CPU", "Memory", "RAM", "BIOS", "Session-Continuity"]
}
```

### RESULT - Last Operation Result
**Type:** Any
**Purpose:** Stores result of most recent operation
**Scope:** Instruction-level

**Usage:**
- Tool call results
- Function return values
- Operation outcomes

**Example:**
```json
"RESULT": "File created successfully at: /mnt/d/~HAL8000/data/architecture/hal8000-register-architecture.md"
```

---

## Register Summary Table

| Register | Category | Type | Purpose | Scope |
|----------|----------|------|---------|-------|
| PC | Control | String | Next instruction pointer | Execution flow |
| IR | Control | String | Current instruction | Active instruction |
| EXEC_MODE | Control | Enum | Execution mode | Session |
| FLOW_STATE | Control | String | Multi-step position | Active task |
| RAM_USAGE | Memory | Integer | Context tokens used | Session |
| RAM_CAPACITY | Memory | Integer | Max context tokens | Session |
| RAM_REMAINING | Memory | Integer | Available tokens | Session |
| RAM_ZONE | Memory | Enum | Performance zone | Session |
| CONTEXT_MANIFEST | Memory | Array | Loaded files list | Session |
| SESSION_ID | State | String | Active session file | Session |
| SESSION_START | State | Timestamp | Session start time | Session |
| CHECKPOINT_STATUS | State | Object | Checkpoint state | Session |
| PHASE | State | String | Project phase | Project |
| LOADED_COMMANDS | State | Array | Available commands | Session |
| CPU_STATUS | Status | Enum | CPU health | Session |
| RATE_LIMIT_STATUS | Status | Object | Usage limits | Cross-session |
| ERROR_FLAG | Status | Boolean | Error indicator | Instruction |
| ERROR_CODE | Status | String | Error identifier | Instruction |
| ACC | Data | Any | Accumulator | Instruction |
| VARS | Data | Object | Session variables | Session |
| RESULT | Data | Any | Last operation result | Instruction |

---

## Register Access Patterns

### Read Operations

**Direct Access:**
- Claude can "read" register values by accessing the actual runtime state
- RAM registers: Read from system warnings
- State registers: Read from `state.json` or internal state
- Status registers: Evaluate from current conditions

**Example:**
```
User: "How much RAM do we have left?"
CPU reads RAM_REMAINING register: 152005 tokens
Response: "152,005 tokens remaining (~76% available)"
```

### Write Operations

**Implicit Updates:**
- Most registers update automatically during execution
- RAM_USAGE updates with every message
- EXEC_MODE changes based on context
- ERROR_FLAG set by operation results

**Explicit Updates:**
- VARS can be modified intentionally
- CHECKPOINT_STATUS updated by `/HAL-session-end` command
- LOADED_COMMANDS updated when loading new commands

**Persistent Updates:**
- Changes to VARS, PHASE, LOADED_COMMANDS must be saved to `state.json` for persistence
- Requires explicit write to file system

### Register Snapshot

A complete register snapshot represents the CPU's immediate working state at a given moment:

```json
{
  "timestamp": "2025-10-04T14:45:30Z",
  "registers": {
    "control": {
      "PC": null,
      "IR": "Create register architecture specification",
      "EXEC_MODE": "INTERACTIVE",
      "FLOW_STATE": "Creating register spec (step 2 of 2)"
    },
    "memory": {
      "RAM_USAGE": 47995,
      "RAM_CAPACITY": 200000,
      "RAM_REMAINING": 152005,
      "RAM_ZONE": "SAFE",
      "CONTEXT_MANIFEST": [
        "CLAUDE.md",
        ".claude/state.json",
        ".claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md",
        "data/research/04-claude-code-runtime-constraints.md"
      ]
    },
    "state": {
      "SESSION_ID": ".claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md",
      "SESSION_START": "2025-10-04T14:23:15Z",
      "CHECKPOINT_STATUS": {
        "last_checkpoint": "2025-10-04T13:05:18Z",
        "checkpoint_file": ".claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md",
        "changes_since_checkpoint": true
      },
      "PHASE": "register-architecture-definition",
      "LOADED_COMMANDS": ["HAL-session-end"]
    },
    "status": {
      "CPU_STATUS": "OPERATIONAL",
      "RATE_LIMIT_STATUS": {
        "limited": false,
        "reset_time": "2025-10-04T19:00:00Z",
        "usage_percent": 15
      },
      "ERROR_FLAG": false,
      "ERROR_CODE": null
    },
    "data": {
      "ACC": {
        "current_operation": "writing register specification",
        "progress": "80%"
      },
      "VARS": {
        "current_project": "HAL8000 architecture",
        "architecture_type": "Modified von Neumann",
        "depth_limit": 3
      },
      "RESULT": "File created successfully"
    }
  }
}
```

---

## Implementation Considerations

### Register Materialization

**Virtual Registers:**
- Registers are not stored in a single file
- They represent runtime state scattered across:
  - Claude's internal context
  - System warnings
  - File system (state.json)
  - Execution environment

**Access Method:**
- Claude "reads" registers by examining current state
- No single register file exists
- Register snapshot can be generated on-demand for debugging

### Session Persistence

**Volatile Registers (Lost on session end):**
- Control: PC, IR, EXEC_MODE, FLOW_STATE
- Memory: RAM_USAGE, RAM_REMAINING, RAM_ZONE, CONTEXT_MANIFEST
- Status: ERROR_FLAG, ERROR_CODE
- Data: ACC, RESULT

**Persistent Registers (Saved to state.json):**
- State: SESSION_ID, PHASE, LOADED_COMMANDS
- Data: VARS (partial - user-defined variables)

**Restored on Resume:**
- SESSION_ID loaded from state.json
- VARS restored from state.json
- RAM_USAGE starts fresh (0 tokens + boot files)
- CONTEXT_MANIFEST rebuilt from session file

### Register Inspection Command

A future command could provide register inspection:

```bash
/HAL-register-dump
```

**Output:**
```
=== HAL8000 Register Dump ===
Time: 2025-10-04T14:45:30Z

[CONTROL]
  PC: null (awaiting input)
  IR: Create register architecture specification
  EXEC_MODE: INTERACTIVE
  FLOW_STATE: Creating register spec (step 2 of 2)

[MEMORY]
  RAM: 47995 / 200000 tokens (24% used, 152005 remaining)
  ZONE: SAFE
  MANIFEST: 4 files loaded

[STATE]
  SESSION: .claude/sessions/2025-10-04-1305-hal8000-architecture-implementation.md
  PHASE: register-architecture-definition
  COMMANDS: 1 loaded

[STATUS]
  CPU: OPERATIONAL
  RATE_LIMIT: Not limited (reset: 19:00:00)
  ERROR: None

[DATA]
  ACC: {current_operation: "writing register specification"}
  VARS: 3 variables
  RESULT: File created successfully
```

---

## Integration with Fetch-Decode-Execute Cycle

### Fetch Phase
1. Read **PC** to determine next instruction
2. If PC is null, wait for user input
3. Load instruction into **IR**
4. Update **PC** to next instruction (if applicable)

### Decode Phase
1. Parse instruction from **IR**
2. Determine required operations
3. Check **RAM_ZONE** to assess resource availability
4. Verify **CPU_STATUS** is OPERATIONAL

### Execute Phase
1. Set **EXEC_MODE** appropriately
2. Update **FLOW_STATE** for multi-step operations
3. Perform operation, storing intermediate results in **ACC**
4. Update **RAM_USAGE** as context accumulates
5. Store final result in **RESULT**
6. Update **ERROR_FLAG** and **ERROR_CODE** if errors occur
7. Update **CONTEXT_MANIFEST** if files loaded

### Post-Execute
1. Check **RAM_ZONE** - warn if entering CAUTION or DANGER
2. Update **CHECKPOINT_STATUS** if checkpoint needed
3. Write changes to **VARS** to state.json if modified
4. Prepare for next cycle

---

## Design Rationale

### Why These Registers?

**Control Registers** map directly to fetch-decode-execute cycle requirements:
- PC/IR are standard CPU registers
- EXEC_MODE reflects Claude Code's multiple operating modes
- FLOW_STATE handles multi-turn operations

**Memory Registers** address the critical RAM constraint:
- Track usage in real-time (system warnings provide data)
- Monitor performance zones (20% degradation rule)
- Prevent redundant loads (CONTEXT_MANIFEST)

**State Registers** enable session continuity:
- Track active session for resume operations
- Monitor checkpoint status for data safety
- Maintain project phase across sessions

**Status Registers** provide operational awareness:
- CPU health monitoring
- Rate limit tracking (5-hour cycles)
- Error handling

**Data Registers** support computation:
- ACC for intermediate results (traditional)
- VARS for user-defined state (practical)
- RESULT for operation outcomes (debugging)

### Alignment with Constraints

This register set directly addresses Claude Code's constraints:

1. **Append-only RAM** → RAM_ZONE warns before exhaustion
2. **Token limits** → RAM_USAGE/REMAINING/CAPACITY track precisely
3. **Session boundaries** → SESSION_ID and CHECKPOINT_STATUS manage continuity
4. **Performance degradation** → RAM_ZONE implements 20% rule
5. **Rate limits** → RATE_LIMIT_STATUS tracks usage cycles

---

## Future Extensions

### Potential Additional Registers

**INTERRUPT_VECTOR** - Handle event-driven operations
- User interrupts
- System warnings
- Rate limit hits

**CACHE_HINT** - Optimize file access patterns
- Frequently accessed files
- Recently loaded context
- Predictive loading

**BUS_STATUS** - Track data transfer state
- Active read/write operations
- I/O operation queue
- Transfer rate monitoring

**TIMER** - Timing and synchronization
- Session duration
- Operation timing
- Rate limit countdown

---

## Conclusion

The HAL8000 register architecture maps traditional CPU register concepts to the specific constraints of Claude Code's runtime environment. By tracking RAM usage, session state, execution flow, and operational status, these registers provide the CPU (Claude instance) with the immediate working memory needed to operate effectively within append-only RAM and session-based persistence constraints.

This architecture enables:
- Accurate system state awareness
- Proactive resource management
- Session continuity across RAM resets
- Performance optimization
- Error handling and recovery

The register set reflects the **actual runtime constraints** documented in Claude Code research, ensuring HAL8000 operates as a realistic computer architecture model rather than a purely theoretical abstraction.
