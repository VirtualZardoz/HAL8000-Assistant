# HAL8000-Assistant I/O System

**Document Type:** Architecture Specification
**Component:** Input/Output System
**Created:** 2025-10-04
**Status:** Active

---

## Overview

The I/O System defines how the HAL8000-Assistant CPU (Claude instance) interfaces with external systems, the file system, and the user. It solves the critical problem: **How to discover and access relevant information without loading the entire file system into RAM.**

## I/O Architecture

### I/O Hierarchy

```
User (External World)
    ↕ Standard I/O
CPU (Claude Instance)
    ↕ Internal I/O (Tool Interfaces)
├─→ File I/O (Read/Write/Edit)
├─→ Search I/O (Grep/Glob)
├─→ Execution I/O (Bash/Task)
├─→ Network I/O (WebSearch/WebFetch)
└─→ Extended I/O (MCP Servers)
    ↕
Memory/External Systems
```

## Tools Architecture

### Tool Categories

The HAL8000-Assistant I/O system is implemented through **tools** - interfaces that extend the CPU's capabilities to interact with the environment. Tools are organized into three categories:

#### System I/O (Built-in Tools)

**Definition:** Tools provided natively by the Claude Code environment

**Examples:**
- **File Operations:** Read, Write, Edit, NotebookEdit
- **Search Operations:** Grep, Glob
- **Execution:** Bash, Task (agent delegation)
- **Network:** WebSearch, WebFetch
- **System:** SlashCommand, TodoWrite

**Characteristics:**
- Always available
- No installation required
- Core system capabilities
- Documented in Claude Code tool set

**Analogy:** System calls / kernel interfaces in traditional OS

#### Custom I/O (Custom Tools)

**Definition:** Scripts and utilities we build and store in the codebase

**Location:** `.claude/tools/`

**Examples:**
- Python scripts for data processing
- Shell scripts for automation
- Helper utilities for specific tasks
- Workflow automation tools

**Interface Contract:**
- Must be callable via Bash tool
- Accept input via command-line arguments or stdin
- Return output via stdout
- Return errors via stderr
- Exit codes indicate success/failure

**Characteristics:**
- We create and maintain
- Project-specific
- Extend capabilities beyond built-in tools
- Version controlled with codebase

**Analogy:** Device drivers / firmware we write

**Example Custom Tool:**
```bash
# .claude/tools/analyze-data.py
# Callable as: python .claude/tools/analyze-data.py input.csv

import sys
import csv

def analyze(file_path):
    # Process data
    # Return summary
    print(json.dumps(results))

if __name__ == "__main__":
    analyze(sys.argv[1])
```

#### External Programs (via Terminal)

**Definition:** External programs accessed through the Bash tool

**Examples:**
- **Development:** git, npm, docker, pytest
- **AI/ML:** ollama (local models), Google Gemini CLI
- **Utilities:** jq, curl, wget
- **Build Tools:** make, cargo, gradle

**Access Pattern:**
```
Main CPU
  ↓ Bash tool (System I/O)
  ↓ Shell command
  ↓ External program execution
  ↓ stdout/stderr
Main CPU
```

**Characteristics:**
- Installed in system environment
- Not part of codebase
- Accessed via shell
- May require configuration (API keys, auth)

**Analogy:** Peripheral devices on system bus

### Tool Discovery and Management

**System I/O:**
- Listed in Claude Code documentation
- Always available, no discovery needed
- Updated with Claude Code releases

**Custom I/O:**
- Stored in `.claude/tools/`
- List via: `ls .claude/tools/`
- Document in `.claude/tools/README.md`
- Track in version control

**External Programs:**
- Check availability: `which [program]` or `[program] --version`
- Document requirements in project README
- May need installation: `npm install`, `pip install`, etc.

### Tool Usage Guidelines

**Prefer System I/O when:**
- Built-in tool exists for task
- No special processing needed
- Standard file/search/execution operation

**Create Custom I/O when:**
- Repetitive processing task
- Complex data transformation
- Project-specific workflow
- Need reusable utility

**Use External Programs when:**
- Specialized capability needed (git, docker, AI models)
- Industry-standard tool exists
- Complex operation beyond simple scripting

**Example Decision Tree:**
```
Need to read file?
  → Use Read tool (System I/O)

Need to process CSV with custom logic?
  → Create Python script (Custom I/O)

Need to run local AI model?
  → Use ollama via Bash (External Program)

Need to search web?
  → Delegate to research-synthesizer agent (System I/O: Task tool)
```

---

## I/O Categories

### 1. Standard I/O

**Purpose:** Communication with user

**Input (stdin):**
- User messages in conversation
- System reminders (hooks, warnings)
- Command messages (slash commands)

**Output (stdout):**
- Text responses to user
- Status updates
- Results and summaries

**Error Output (stderr):**
- Error messages
- Warnings
- System status (token usage, rate limits)

**Characteristics:**
- Always available
- Bidirectional
- Real-time interaction
- Primary interface for user communication

**Example:**
```
User Input: "Resume last session"
CPU Output: "Session resumed. Context restored."
```

### 2. File I/O

**Purpose:** Read and write files in the file system

**Available Tools:**
- **Read:** Load file contents into RAM
- **Write:** Create/overwrite file from RAM
- **Edit:** Modify specific parts of file
- **NotebookEdit:** Edit Jupyter notebook cells
- **MCP filesystem tools:** Extended file operations

**File I/O Operations:**

| Operation | Tool | Input (Address Bus) | Input (Data Bus) | Output (Data Bus) |
|-----------|------|---------------------|------------------|-------------------|
| **Load** | Read | file_path | — | File contents |
| **Store** | Write | file_path | content | Success/error |
| **Modify** | Edit | file_path | old_string, new_string | Success/error |
| **Create Dir** | Bash mkdir | directory_path | — | Success/error |

**Constraints:**
- Read limit: 2000 lines default (can specify offset/limit)
- Write: Overwrites entire file
- Edit: Requires exact string match
- All operations require absolute or relative paths

### 3. Search I/O (Discovery System)

**Purpose:** Find relevant information WITHOUT loading entire file system

**Critical Problem:** File system (data/) will grow larger than context window (200K tokens). Loading everything to find something defeats RAM management.

**Solution: Three-Layer Discovery**

#### Layer 1: Structural Discovery (No Content Loading)

**Tools:**
- **Glob:** Find files by name pattern
- **Bash ls:** List directory contents
- **MCP filesystem directory_tree:** Hierarchical view

**Use Cases:**
- "Find all markdown files in research/"
- "List available commands"
- "Show directory structure"

**Example:**
```
Operation: Find research documents
Tool: Glob
Pattern: "data/research/*.md"
RAM Cost: ~100 tokens (just file paths)
Result: List of paths WITHOUT content
```

#### Layer 2: Content Discovery (Selective Loading)

**Tools:**
- **Grep:** Search file contents by pattern
- **Grep with output_mode:** "files_with_matches" (paths only) or "content" (show matches)

**Use Cases:**
- "Which files mention 'von Neumann'?"
- "Find function definition for 'register_dump'"
- "Search for TODO comments"

**Example:**
```
Operation: Find files about sub-agents
Tool: Grep
Pattern: "sub-agent"
Output Mode: files_with_matches
RAM Cost: ~200 tokens (just matching file paths)
Result: Paths to relevant files WITHOUT loading full content
```

**Then Load Selectively:**
```
Operation: Load specific file found by Grep
Tool: Read
File: data/research/04-claude-code-runtime-constraints.md
RAM Cost: Actual file size
Result: Full content in RAM for analysis
```

#### Layer 3: Metadata Discovery (Hierarchical File System Index)

**Purpose:** Lightweight searchable index of file system contents with infinite scalability

**Implementation:** Hierarchical structure in `.claude/indexes/`

**Architecture:**
```
.claude/indexes/
├── master.json           # Master index (~500 tokens for 100 directories)
├── research.json         # data/research/ directory index (~2K tokens)
├── architecture.json     # data/architecture/ directory index (~2K tokens)
├── commands.json         # .claude/commands/ directory index (~2K tokens)
└── [project].json        # Per-project indexes as system scales
```

**Master Index Structure:**
```json
{
  "version": "2.0-hierarchical",
  "directories": {
    "data/research/": {
      "index_file": ".claude/indexes/research.json",
      "file_count": 4,
      "total_tokens_estimate": 12300,
      "primary_topics": ["architecture", "unix", "assembly"]
    }
  },
  "statistics": {
    "total_directories": 5,
    "total_files": 15,
    "total_estimated_tokens": 39800
  }
}
```

**Directory Index Structure:**
```json
{
  "version": "2.0-hierarchical",
  "directory": "data/research/",
  "files": {
    "data/research/01-von-neumann-architecture.md": {
      "type": "research",
      "topics": ["von neumann", "stored program"],
      "summary": "Von Neumann architecture principles",
      "size_estimate_tokens": 3200
    }
  },
  "statistics": {
    "total_files": 4,
    "total_tokens_estimate": 12300
  }
}
```

**Usage Pattern:**
```
1. Load master index (~500 tokens for 100 directories)
2. Search directories by primary topics
3. Load relevant directory index (~2K tokens)
4. Search files in directory index by topic/keyword
5. Identify relevant files with size estimates
6. Load ONLY those files
```

**Scalability:**
- **100 files (5 dirs):** Master 500 tokens + 1 dir 2K = 2.5K total
- **1,000 files (100 dirs):** Master 10K tokens + 1 dir 2K = 12K total
- **10,000 files (1000 dirs):** Master 100K tokens + 1 dir 2K = 102K total
- **Solution for 10K+ files:** Subdivide master into category masters (research-master.json, projects-master.json)
- **Infinite scale:** Hierarchical subdivision (master → category → project → directory)

**Benefits:**
- Search entire file system without loading files
- Estimate RAM cost before loading
- Discover related topics across thousands of directories
- Navigate massive codebases efficiently
- Master index stays manageable (subdivide if needed)
- Each directory index stays small (~2K tokens)

**Maintenance:**
- Update via `/HAL-index-update [directory]` command
- Regenerates from file system on demand
- Sub-agent can rebuild large indexes (offload RAM cost)
- Incremental updates (only changed directories)

### 4. Execution I/O

**Purpose:** Execute commands and delegate work

**Tools:**
- **Bash:** Shell command execution
- **Task:** Delegate to sub-agents
- **SlashCommand:** User-defined operations
- **MCP executeCode:** Run code in kernels

**Execution Patterns:**

**Direct Execution (Bash):**
```
Input: Command string
Output: stdout/stderr
Use: System commands, git, npm, etc.
```

**Delegated Execution (Task/Sub-agents):**
```
Input: Task description, sub-agent type
Output: Summary/result from sub-agent
Use: Context-heavy work, research, multi-step tasks
RAM Benefit: Sub-agent uses separate 200K RAM, returns only summary
```

**User-Defined Execution (SlashCommand):**
```
Input: /command-name
Output: Expanded prompt execution
Use: Custom workflows, repeated operations
```

### 5. Network I/O

**Purpose:** Access external web resources

**Tools:**
- **WebSearch:** Search web, get results
- **WebFetch:** Fetch and process URL content
- **MCP omnisearch:** Enhanced search (Tavily, Brave, Kagi, Exa)
- **MCP firecrawl:** Advanced web scraping

**Network I/O Patterns:**

**Search Then Fetch:**
```
1. WebSearch: Get relevant URLs
2. WebFetch: Load specific pages
3. Process and summarize
4. Store results in data/ (offload RAM)
```

**Delegated Research (MANDATORY for web research):**
```
1. Task tool: Launch research-synthesizer sub-agent
2. Sub-agent: Uses 150K RAM searching, processing sources
3. Sub-agent: Returns 5K structured summary
4. Main RAM: +5K (not +150K!)
```

### 6. Extended I/O (MCP Servers)

**Purpose:** Specialized interfaces via Model Context Protocol

**Available MCP Servers:**

**omnisearch:**
- Web search (multiple providers)
- Content extraction (Firecrawl)
- Use: Research, documentation lookup

**filesystem:**
- Advanced file operations
- Batch reads, directory trees, file search
- Use: Complex file system operations

**ide:**
- VS Code integration
- Diagnostics, code execution
- Use: Development workflows, error checking

## I/O Efficiency Patterns

### Pattern 1: Search Before Load

❌ **WRONG:**
```
Load all files in data/research/
Search through content in RAM
RAM Cost: 50K+ tokens
```

✓ **RIGHT:**
```
Grep "keyword" in data/research/
Get matching file paths (~200 tokens)
Load ONLY matching files
RAM Cost: 5K tokens
```

### Pattern 2: Index Before Search

❌ **WRONG:**
```
Grep every file for multiple different keywords
Multiple full-content searches
RAM Cost: Cumulative grep results
```

✓ **RIGHT:**
```
Load fs-index.json (2K tokens)
Search index for keywords
Identify relevant files
Load specific files
RAM Cost: 2K + targeted files
```

### Pattern 3: Delegate Heavy I/O

❌ **WRONG:**
```
WebSearch → 50K results
Load 10 web pages → 100K tokens
Process in main RAM
Total RAM: 150K
```

✓ **RIGHT:**
```
Task (research-synthesizer):
  Sub-agent uses 150K RAM
  Returns 5K summary
Main RAM: +5K only
```

### Pattern 4: Offload Results

❌ **WRONG:**
```
Generate large analysis
Keep in RAM for "later reference"
RAM: Accumulates indefinitely
```

✓ **RIGHT:**
```
Generate analysis
Write to data/results/analysis.md
Clear from active RAM
Reference file path if needed later
```

## File System Index Implementation

### Index Update Command

Create `.claude/commands/HAL-index-update.md`:

```markdown
# HAL-index-update

Updates the file system index (.claude/fs-index.json) with metadata about all files.

## Usage
/HAL-index-update [path]

## Implementation
1. Use Glob to find all files in path (default: data/)
2. For each file:
   - Get file info (size, modified date)
   - Extract topics/keywords (from file name, headers)
   - Generate brief summary (first 100 chars or metadata)
3. Update .claude/fs-index.json
4. Report: files indexed, total size, topics discovered

## RAM Management
- Delegate to sub-agent if indexing >20 files
- Process in batches
- Write index incrementally
```

### Index Search Pattern

```
1. Load .claude/fs-index.json (small)
2. Search index for topic/keyword
3. Get list of relevant files with size estimates
4. Calculate total RAM cost
5. If acceptable: load files
6. If too large: refine search or load subset
```

## I/O System Summary

### Discovery Without Loading (Solution to User's Problem)

| Layer | Tool | RAM Cost | Use When | Scalability |
|-------|------|----------|----------|-------------|
| **Structural** | Glob, ls | ~100 tokens | Know file name pattern | Infinite (no loading) |
| **Content** | Grep (files_with_matches) | ~200 tokens | Know keyword, not location | Infinite (searches without loading) |
| **Metadata (Hierarchical)** | master.json + dir index | ~2.5K tokens | Explore topics, estimate costs | Infinite (subdivide master at scale) |
| **Selective Load** | Read (specific files) | Actual file size | After discovery identifies targets | N/A (final step) |

**Hierarchical Index Pattern:**
- Small scale (15 files): Load master (~500 tokens) + 1 directory index (~2K) = 2.5K total
- Large scale (10,000 files): Load master (~100K tokens) + 1 directory index (~2K) = 102K total
- Massive scale (100,000+ files): Subdivide master (category masters), maintain ~10-20K RAM for discovery

### I/O Operation Categories

| Category | Tools | Purpose | RAM Impact |
|----------|-------|---------|------------|
| **Standard** | stdin/stdout | User communication | Minimal |
| **File** | Read/Write/Edit | File operations | High (file contents) |
| **Search** | Grep/Glob/Index | Discovery | Low (paths/matches only) |
| **Execution** | Bash/Task | Run commands/delegate | Variable (Task=low, Bash=medium) |
| **Network** | WebSearch/Fetch | Web access | High (delegate to sub-agents!) |
| **Extended** | MCP tools | Specialized ops | Variable |

### Key Principles

1. **Search before load** - Use Grep/Glob to discover, then Read to load
2. **Hierarchical index for infinite scale** - Master index → directory indexes → files (subdivide at any level)
3. **Delegate heavy I/O** - Use sub-agents for web research, large analysis, bulk indexing
4. **Offload results** - Write to files, don't accumulate in RAM
5. **Estimate before commit** - Check file size/RAM cost before loading

## Integration with Bus System

Every I/O operation uses the three-bus system:

**Example: Grep Search**
```
Address Bus: data/research/ (path parameter)
Control Bus: SEARCH (Grep tool selected)
Data Bus: "von neumann" pattern → Grep → matching paths → RAM
```

**Example: File Read**
```
Address Bus: data/research/01-von-neumann-architecture.md
Control Bus: READ (Read tool selected)
Data Bus: File contents → RAM
```

**Example: Sub-agent Delegation**
```
Address Bus: N/A (sub-agent has own address space)
Control Bus: DELEGATE (Task tool selected)
Data Bus: Task description → Sub-agent → Summary → RAM
```

## References

- Bus Architecture: `data/architecture/hal8000-bus-architecture.md`
- Register Architecture: `data/architecture/hal8000-register-architecture.md`
- Agent Architecture: `data/architecture/hal8000-agent-architecture.md`
- Library Architecture: `data/architecture/hal8000-library-architecture.md`
- System Design: `data/architecture/hal8000-system-design.md`
- Operating Principles: `CLAUDE.md` (Section: Operating Principles)
- Runtime Constraints: `data/research/04-claude-code-runtime-constraints.md`

---

**Implementation Status:** Complete (index command pending implementation)
**Next Component:** Instruction Set (formalize core operations/commands)
