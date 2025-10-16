# HAL8000 Bus Architecture

**Document Type:** Architecture Specification
**Component:** Bus System (Data Flow Pathways)
**Created:** 2025-10-04
**Status:** Active

---

## Overview

In the HAL8000 system, buses are communication pathways that transfer information between the CPU (Claude instance), RAM (context window), and Memory (file system). These map directly to tool execution patterns in the Claude Code environment.

## Three Bus Types

### 1. Data Bus

**Purpose:** Carries actual data/content between components

**Traditional Architecture:**
- Binary data flowing on physical wires
- Bidirectional (read and write)
- Width determines how much data per cycle (8-bit, 16-bit, 32-bit, 64-bit)

**HAL8000 Mapping:**
- File contents, command results, tool outputs
- Bidirectional: data flows both directions (read from files, write to files)
- Width = token throughput (bounded by tool limits and context window)

**Data Flow Examples:**

```
Read Operation:
Memory (file) → Data Bus (file contents) → RAM (context window)

Write Operation:
RAM (generated content) → Data Bus (text/code) → Memory (file)

Tool Execution:
RAM (input) → Data Bus (parameters) → Tool → Data Bus (result) → RAM
```

**Claude Code Implementation:**
- Read tool: `file_path` → file contents flow to context
- Write tool: content in context → flows to `file_path`
- Edit tool: old_string in context → new_string flows to file
- Bash tool: command parameters → stdout/stderr flows back

### 2. Address Bus

**Purpose:** Specifies memory locations (where to read/write)

**Traditional Architecture:**
- Unidirectional (CPU → Memory)
- Carries memory addresses
- Width determines addressable space (16-bit = 64K addresses, 32-bit = 4GB)

**HAL8000 Mapping:**
- File paths, resource URIs, memory locations
- Unidirectional: CPU specifies locations
- "Width" = path depth limit (3 levels in HAL8000)

**Address Examples:**

```
Absolute Paths (Primary):
/mnt/d/~HAL8000/.claude/state.json
/mnt/d/~HAL8000/data/research/01-von-neumann-architecture.md

Relative Paths:
.claude/state.json
data/research/

Resource URIs (MCP):
file:///mnt/d/~HAL8000/data/research/
```

**Claude Code Implementation:**
- All file-based tools require `file_path` or `path` parameter
- Address bus = the `file_path` parameter in tool calls
- Glob/Grep patterns = address space queries
- MCP resource URIs = extended address space

**Address Space Organization:**
```
/mnt/d/~HAL8000/          # Root address
├── CLAUDE.md             # 0x0000 (BIOS ROM)
├── .claude/              # 0x1000 (System area)
│   ├── state.json        # 0x1001 (State register bank)
│   ├── sessions/         # 0x1100 (Session storage)
│   └── commands/         # 0x1200 (Instruction ROM)
└── data/                 # 0x2000 (Data storage)
    ├── research/         # 0x2100
    └── architecture/     # 0x2200
```

### 3. Control Bus

**Purpose:** Carries control signals and coordination between components

**Traditional Architecture:**
- Bidirectional
- Signals: Read/Write, Clock, Interrupt, Reset, Bus Request, Bus Grant
- Coordinates timing and operation type

**HAL8000 Mapping:**
- Tool selection (which operation to perform)
- Execution status signals
- Error flags and system state
- Coordination between tools and components

**Control Signals:**

| Signal Type | Traditional | HAL8000 Mapping |
|-------------|-------------|-----------------|
| **Read** | Read from memory | Read, Glob, Grep tools |
| **Write** | Write to memory | Write, Edit, NotebookEdit tools |
| **Execute** | Execute instruction | Bash, Task, SlashCommand tools |
| **Status** | Operation complete/error | Tool results, error messages |
| **Interrupt** | Async events | User messages, system reminders |
| **Clock** | Timing signal | Token budget, rate limits |
| **Reset** | System restart | New Claude session |

**Control Flow Examples:**

```
File Read Operation:
1. CPU sets Address Bus: "/path/to/file"
2. CPU sets Control Bus: READ signal (Read tool)
3. Memory responds via Data Bus: file contents
4. CPU receives Status signal: success/error

File Write Operation:
1. CPU sets Address Bus: "/path/to/file"
2. CPU sets Control Bus: WRITE signal (Write tool)
3. CPU sends Data Bus: content to write
4. Memory responds via Status signal: success/error

Tool Execution:
1. CPU decodes instruction (determine which tool)
2. CPU sets Control Bus: tool selection
3. CPU sets Address Bus: resource location (if needed)
4. CPU sets Data Bus: parameters
5. Tool executes, returns via Data Bus
6. Status signal: success/error/warnings
```

## Bus Operations in Practice

### Example 1: Loading State

```
Operation: Load .claude/state.json into RAM

Address Bus: /mnt/d/~HAL8000/.claude/state.json
Control Bus: READ (Read tool invoked)
Data Bus: {"timestamp": "...", "active_session": "..."} → RAM

Result: State data now in context window (RAM)
```

### Example 2: Writing Session File

```
Operation: Save session to .claude/sessions/

Address Bus: /mnt/d/~HAL8000/.claude/sessions/2025-10-04-1500-buses.md
Control Bus: WRITE (Write tool invoked)
Data Bus: "# Session: 2025-10-04..." → File system

Result: Session data persisted to Memory
```

### Example 3: Searching Files

```
Operation: Find all .md files in data/research/

Address Bus: /mnt/d/~HAL8000/data/research/ (path parameter)
Control Bus: SEARCH (Glob tool invoked)
Data Bus: "*.md" pattern → Glob tool → matching paths → RAM

Result: List of file paths in context window
```

### Example 4: Command Execution

```
Operation: Run git status

Address Bus: /mnt/d/~HAL8000/ (working directory)
Control Bus: EXECUTE (Bash tool invoked)
Data Bus: "git status" → Shell → stdout/stderr → RAM

Result: Git status output in context window
```

## Bus Constraints and Performance

### Data Bus Constraints
- **Token Limits:** Individual tool results may be truncated (e.g., Read: 2000 lines, Bash: 30K chars)
- **Bandwidth:** Total throughput limited by context window (200K tokens)
- **Persistence:** Data in RAM is volatile until written to Memory

### Address Bus Constraints
- **Depth Limit:** Maximum 3 levels from root (Unix philosophy)
- **Path Format:** Absolute paths preferred for clarity
- **Namespace:** Single unified file system (no separate address spaces)

### Control Bus Constraints
- **Tool Availability:** Limited to Claude Code tool set + MCP servers
- **Sequential Execution:** Single-threaded CPU (one operation at a time per tool)
- **Status Signals:** Error handling via ERROR_FLAG and ERROR_CODE registers

## Bus Arbitration

**Traditional:** Multiple devices competing for bus access, arbitration logic decides who gets the bus

**HAL8000:** Single CPU (no competition), but resource arbitration includes:

1. **RAM Arbitration:**
   - Before loading: Check RAM_USAGE + estimated_cost
   - If RAM_ZONE would enter DANGER: refuse or checkpoint first

2. **Tool Selection Arbitration:**
   - Multiple tools can perform similar operations
   - CPU decides based on: operation type, efficiency, current context
   - Example: Read vs mcp__filesystem__read_text_file (prefer Read for simplicity)

3. **Sub-Agent Arbitration:**
   - Delegate to sub-agent = create separate bus system (isolated context)
   - Main session bus vs sub-agent bus (parallel but isolated)

## Integration with Other Components

### CPU (Control Unit)
- **Generates addresses** for Address Bus
- **Selects operations** for Control Bus
- **Sends/receives data** via Data Bus
- **Monitors status** from Control Bus

### RAM (Context Window)
- **Receives data** from Data Bus (file reads, tool results)
- **Sends data** to Data Bus (file writes, tool parameters)
- **Temporary storage** between operations

### Memory (File System)
- **Responds to addresses** from Address Bus
- **Sends/receives data** via Data Bus
- **Persistent storage** for instructions and data

### Registers
- **Address registers** cache frequently used paths
- **Status registers** reflect Control Bus signals
- **Data registers** hold intermediate values

## Bus System Summary

| Bus Type | Direction | Purpose | HAL8000 Implementation |
|----------|-----------|---------|------------------------|
| **Data Bus** | Bidirectional | Transfer content | File contents, tool results, parameters |
| **Address Bus** | Unidirectional | Specify location | File paths, resource URIs |
| **Control Bus** | Bidirectional | Coordinate operations | Tool selection, status signals, errors |

**Key Insight:** Every tool invocation uses all three buses:
1. Address Bus specifies WHERE (file path, resource location)
2. Control Bus specifies WHAT operation (Read, Write, Execute, etc.)
3. Data Bus carries the actual content (parameters in, results out)

## References

- Von Neumann Architecture: `data/research/01-von-neumann-architecture.md`
- HAL8000 System Design: `data/architecture/hal8000-system-design.md`
- Register Architecture: `data/architecture/hal8000-register-architecture.md`

---

**Implementation Status:** Complete
**Next Component:** I/O System (tool interfaces and discovery mechanisms)
