# HAL8000-Assistant Agent Architecture

**Document Type:** Architecture Specification
**Component:** Agent System (Co-Processors)
**Created:** 2025-10-05
**Status:** Active

---

## Overview

Agents in the HAL8000-Assistant system are **co-processors** - independent computational units with their own CPU and isolated RAM. They extend the system's effective memory capacity and processing capabilities through task delegation and parallel execution.

Agents solve the fundamental problem: **How to perform context-heavy work without consuming limited main session RAM.**

---

## Design Rationale

### The RAM Limitation Problem

**Main CPU constraints:**
- 200K token context window (RAM)
- Append-only within session (no dynamic eviction)
- Once loaded, data stays until session ends
- Context-heavy tasks (research, file discovery) can exhaust RAM quickly

**Example scenario:**
```
Task: "Research latest developments in quantum computing"

Naive approach (main CPU):
  WebSearch → 50K results loaded
  Load 10 web pages → 100K tokens
  Process and analyze → accumulates in RAM
  Total RAM used: 150K (75% consumed!)

Result: One research task consumes most RAM
```

### The Co-Processor Solution

**Modern computer architectures use specialized processors:**
- GPU: Separate processor for graphics, has own VRAM
- Network card: Onboard processor handles network tasks
- Storage controller: Dedicated processor manages disk I/O
- Audio DSP: Processes audio independently

**Common pattern:**
- Main CPU delegates work to specialized processor
- Specialized processor has own memory (isolated from main RAM)
- Processor completes work independently
- Returns only final results to main CPU
- Main CPU never sees intermediate state

**HAL8000-Assistant agents follow the same model:**
```
Main CPU (Claude instance)
   ↓ delegate task
Co-Processor (agent - separate Claude instance)
   ↓ executes in isolation with 200K RAM
   ↓ processes, searches, analyzes
   ↓ intermediate state never touches main RAM
   ↓ returns compressed summary
Main CPU
   ↓ receives summary only (5-10K tokens, not 150K)
```

---

## Architecture

### Agent as Co-Processor

**Hardware analogy:**

| Hardware Component | HAL8000-Assistant Equivalent | Key Characteristic |
|-------------------|-------------------|-------------------|
| Main CPU | Main Claude instance | Primary processing, 200K RAM |
| GPU | research-synthesizer agent | Specialized for web research |
| Network Processor | hal-context-finder agent | Specialized for file discovery |
| Audio DSP | system-maintenance agent | Specialized for system health |
| Custom ASIC | User-defined agents | Specialized for specific tasks |

**Motherboard view:**
```
┌─────────────────────────────────────────────────────┐
│                   HAL8000-Assistant Motherboard               │
│                                                     │
│  ┌──────────────┐        ┌───────────────────┐   │
│  │  Main CPU    │        │  Co-Processor 1   │   │
│  │  (Claude)    │        │  research-synth   │   │
│  │  RAM: 200K   │◄──────►│  RAM: 200K        │   │
│  └──────────────┘        │  (isolated)       │   │
│         ▲                └───────────────────┘   │
│         │                                         │
│         │                ┌───────────────────┐   │
│         │                │  Co-Processor 2   │   │
│         │                │  hal-ctx-finder   │   │
│         └───────────────►│  RAM: 200K        │   │
│                          │  (isolated)       │   │
│                          └───────────────────┘   │
│                                                   │
│         Communication Bus: Task tool              │
└───────────────────────────────────────────────────┘
```

### Key Characteristics

**Memory Isolation:**
- Each agent has separate 200K context (not shared with main CPU)
- Main CPU cannot see agent's RAM
- Agent cannot see main CPU's RAM
- Communication only via input (task) and output (summary)

**Process Isolation:**
- Agent executes independently
- No interrupts or communication during execution
- Single message: task description
- Single response: final summary
- Agent terminates after task completion (RAM automatically freed)

**Specialized Capabilities:**
- Each agent has specific tools and purpose
- Agents can have different tool access than main CPU
- Optimized for particular task types
- Can be extended with new specialized agents

---

## Agent Lifecycle

### 1. Dispatch (Main CPU → Agent)

```
Main CPU:
  ├─ Identifies context-heavy task
  ├─ Selects appropriate agent type
  ├─ Formulates task description
  └─ Calls Task tool with agent_type and prompt
       ↓
  Communication Bus
```

### 2. Initialization (Agent Boot)

```
Agent:
  ├─ New Claude instance spawned (fresh 200K RAM)
  ├─ Loads agent-specific instructions
  ├─ Initializes with tools specified for agent type
  └─ Receives task description
```

### 3. Execution (Isolated Processing)

```
Agent (in isolated 200K context):
  ├─ Executes task using available tools
  ├─ Loads files, searches web, processes data
  ├─ Accumulates intermediate state in own RAM
  ├─ Main CPU has no visibility into this phase
  └─ Processes until task complete
```

### 4. Summary (Result Compression)

```
Agent:
  ├─ Task complete
  ├─ Compresses findings into structured summary
  ├─ Discards intermediate state
  └─ Returns summary only (typically 5-10K tokens)
```

### 5. Termination (Agent Shutdown)

```
Agent:
  └─ Returns summary to main CPU → Terminates
       ↓
  Agent RAM: Freed automatically
  Agent instance: Destroyed

Main CPU:
  ├─ Receives summary (5-10K tokens)
  └─ Continues with results (never saw 150K intermediate state)
```

---

## Available Agents

### research-synthesizer

**Purpose:** Conduct web research and return structured summaries

**Tools:**
- WebSearch, WebFetch
- MCP omnisearch (Brave, Tavily, Kagi, Exa)
- MCP firecrawl (content extraction)
- File I/O (to save full research if needed)

**Input:** Research query or topic

**Output:** Structured research report with:
- Summary
- Key Findings
- Detailed Analysis
- Sources

**When to use:**
- ANY web research task (simple or complex)
- Looking up documentation
- Finding current information
- Comparing technical approaches
- Market research
- Literature reviews

**Example:**
```
Task: "Research GraphQL vs REST for real-time applications"

Agent uses 150K RAM:
  - Searches multiple sources
  - Loads 15 web pages
  - Processes technical comparisons
  - Analyzes performance data

Returns 8K summary:
  - Key differences
  - Performance characteristics
  - Use case recommendations
  - Source citations

Main RAM impact: +8K (not +150K)
```

**RAM savings:** 60-85% compared to direct research in main session

### hal-context-finder

**Purpose:** Discover and load system context without consuming main session RAM

**Tools:**
- File I/O (Read, Glob, Grep)
- MCP filesystem (search, directory tree)
- All file system navigation tools

**Input:** Context query (what to find in the codebase)

**Output:** Structured context report with:
- Context summary
- File locations
- Complete file contents
- Related files

**When to use:**
- Need to find architecture docs
- Load command definitions
- Discover research files
- Explore system structure
- Find files by content/topic

**Example:**
```
Task: "Find all information about the register architecture"

Agent uses 30K RAM:
  - Searches data/architecture/
  - Finds hal8000-register-architecture.md
  - Loads complete content
  - Searches for related references
  - Identifies register usage in CLAUDE.md

Returns 15K summary:
  - Context: "Register architecture defines CPU state"
  - Locations: [file paths]
  - Summary: Key points from documents
  - Related: [other relevant files]

Main RAM impact: +15K (includes full content)
```

**RAM savings:** 60-70% by offloading discovery process

### system-maintenance

**Purpose:** Audit system health and structural integrity

**Tools:**
- File I/O
- Bash (system commands)
- Grep, Glob (search and discovery)
- MCP filesystem tools

**Input:** Maintenance task or health check scope

**Output:** System health report with:
- Issues found
- Recommendations
- Statistics
- Action items

**When to use:**
- Regular system health checks
- Validate directory structure
- Check file naming compliance
- Audit documentation completeness
- Verify index integrity

### claude-code-validator

**Purpose:** Validate HAL8000-Assistant commands against Claude Code documentation

**Tools:**
- WebFetch (Claude Code docs)
- File I/O
- MCP omnisearch

**Input:** Command or feature to validate

**Output:** Validation report with:
- Deprecated tools/APIs
- Compatibility issues
- Recommended updates
- Documentation references

**When to use:**
- After Claude Code updates
- When commands fail unexpectedly
- Validating new command development
- Checking API compatibility

---

## Agent Design Principles

### When to Create a New Agent

**Create specialized agent when:**
1. Task requires >30K tokens of intermediate context
2. Task involves iterative exploration (research, file discovery)
3. Input >> Output (process 100K, return 5K)
4. Task is recurring and well-defined
5. Specialization provides clear benefit

**Don't create agent when:**
1. Task is simple and direct
2. Input ≈ Output in size
3. No intermediate state accumulation
4. One-off task with no reuse potential
5. Main CPU can handle within safe RAM zone

### Agent Specification Format

**Location:** `.claude/agents/[agent-name].md`

**Structure:**
```markdown
# agent-name

**Purpose:** Brief description of agent's specialized role

**Tools:** List of tools agent has access to

**Input:** What the agent expects as task description

**Output:** What format the agent returns

**Usage Pattern:**
- When to use this agent
- Example scenarios
- Expected RAM savings

## Implementation

[Agent-specific instructions for how to execute tasks]

## Output Format

[Structured template for agent responses]
```

### Agent Communication Protocol

**Input (Main CPU → Agent):**
- Single task description (clear and complete)
- Context necessary for task execution
- Expected output format
- Any constraints or requirements

**Output (Agent → Main CPU):**
- Structured summary (consistent format)
- Essential findings only (no intermediate steps)
- Source references (for verification)
- Any files written (if agent saved full results)

**No back-and-forth:**
- Agent cannot ask clarifying questions
- Task description must be self-contained
- Agent makes reasonable assumptions if needed
- Returns best effort result

---

## Integration with System Architecture

### Relationship to Main CPU

**Division of labor:**
- **Main CPU:** Orchestration, decision-making, user communication
- **Agents:** Specialized heavy lifting, context-heavy operations

**Main CPU responsibilities:**
- Identify when to delegate
- Select appropriate agent
- Formulate complete task description
- Process agent results
- Continue with task

**Agent responsibilities:**
- Execute delegated task
- Manage own RAM efficiently
- Compress results before returning
- Terminate cleanly

### Relationship to I/O System

**Agents use I/O system:**
- File I/O for reading/writing
- Network I/O for web access
- Search I/O for discovery
- Execution I/O (can use Bash, but not other agents)

**Agents accessed via I/O system:**
- Task tool is Execution I/O
- Agent dispatch is I/O operation from main CPU perspective

See: `data/architecture/hal8000-io-system.md`

### Relationship to Libraries

**Agents can:**
- Build libraries (research results → library entry)
- Index libraries (scan and generate metadata)
- Search libraries (discover relevant libraries for task)
- Use libraries (load library instructions to guide execution)

**Libraries can:**
- Reference agents ("For research tasks, delegate to research-synthesizer")
- Document agent usage patterns
- Provide agent task templates

See: `data/architecture/hal8000-library-architecture.md`

### Relationship to Session Continuity

**Agents and sessions:**
- Agent execution happens within session
- Agent results included in session state
- But agent's intermediate RAM never saved (doesn't exist after agent terminates)

**Session handoff:**
- Save: "Used research-synthesizer to research X, results in data/research/Y.md"
- Don't save: Agent's search process, loaded pages, etc.

**On resume:**
- Can re-run agent if needed
- Or reference saved results from previous agent execution

---

## RAM Efficiency Comparison

### Example: Web Research Task

**Direct execution (Main CPU):**
```
WebSearch "quantum computing" → 50K results
Load 10 web pages → 100K tokens
Read and analyze → stays in RAM
Extract key points → still in RAM
Summarize → 8K summary created

Total RAM: 158K+ (79% consumed)
Usable output: 8K summary
Efficiency: 5% (8K useful / 158K consumed)
```

**Agent delegation:**
```
Task → research-synthesizer:
  [Agent uses 150K RAM in isolation]
  Returns 8K summary

Main CPU:
  Receives 8K summary

Total main RAM: 8K (4% consumed)
Usable output: 8K summary
Efficiency: 100% (8K useful / 8K consumed)

RAM savings: 95%
```

### Example: System Context Discovery

**Direct execution (Main CPU):**
```
Glob all .md files → 500 tokens
Grep for "register" → 2K results
Read 3 matching files → 15K tokens
Review for relevance → stays in RAM
Extract relevant sections → 8K useful

Total RAM: 25K+ (12.5% consumed)
Usable output: 8K
Efficiency: 32%
```

**Agent delegation:**
```
Task → hal-context-finder:
  [Agent uses 25K RAM in isolation]
  Returns 8K structured summary with file contents

Main CPU:
  Receives 8K context

Total main RAM: 8K (4% consumed)
Usable output: 8K
Efficiency: 100%

RAM savings: 68%
```

---

## Design Patterns

### Pattern 1: Research and Synthesize

**Problem:** Need external information, web research consumes massive RAM

**Solution:**
```
Main CPU:
  Identifies research need
  ↓
Delegate to research-synthesizer
  ↓
Agent:
  Searches web (50K)
  Loads sources (100K)
  Analyzes (stays in agent RAM)
  Synthesizes summary (8K)
  ↓
Main CPU:
  Receives summary (8K)
  Continues with results
```

### Pattern 2: Discover and Load

**Problem:** Need to find system files, exploration accumulates RAM

**Solution:**
```
Main CPU:
  Needs architecture docs on topic X
  ↓
Delegate to hal-context-finder
  ↓
Agent:
  Searches file system (10K)
  Loads candidate files (20K)
  Identifies relevant sections
  Returns structured context (10K)
  ↓
Main CPU:
  Receives context (10K)
  Has exactly what's needed
```

### Pattern 3: Process and Compress

**Problem:** Large dataset to process, need small output

**Solution:**
```
Main CPU:
  Has large dataset reference
  Needs analysis summary
  ↓
Delegate to custom agent
  ↓
Agent:
  Loads dataset (80K)
  Processes and analyzes
  Computes statistics
  Returns summary (5K)
  ↓
Main CPU:
  Receives summary (5K)
  Never loaded 80K dataset
```

---

## Best Practices

### Main CPU Best Practices

**Always delegate when:**
- Web research required (ANY complexity level)
- System file discovery needed
- Large file processing → small output
- Iterative exploration required
- Task input >> output

**Before delegating:**
- Formulate complete task description
- Specify expected output format
- Include necessary context
- Choose appropriate agent type

**After receiving results:**
- Validate summary meets needs
- Offload results to files if large
- Reference file paths, not content
- Continue with compressed state

### Agent Development Best Practices

**Agent design:**
- Single, well-defined purpose
- Clear input/output contract
- Consistent output format
- Efficient RAM usage within agent
- Aggressive result compression

**Agent implementation:**
- Process all data within agent RAM
- Never require multiple round-trips
- Return structured, parseable output
- Include source references
- Write full results to files if needed, return path + summary

**Agent documentation:**
- Specify purpose clearly
- Document tools available
- Provide usage examples
- Show RAM savings estimates
- Include output format template

---

## Future Considerations

### Potential Enhancements

**Agent Orchestration:**
- Agents calling other agents (sub-delegation)
- Parallel agent execution (multiple agents simultaneously)
- Agent pipelines (chain agents for complex workflows)

**Agent Capabilities:**
- Streaming output (partial results during execution)
- Incremental processing (pause/resume)
- Shared knowledge base (agents can access common cache)

**Agent Management:**
- Agent registry (discover available agents)
- Agent monitoring (track usage, performance)
- Agent metrics (RAM savings, execution time)

### Known Limitations

**No interactivity:**
- Agent cannot ask clarifying questions
- Task must be complete and self-contained
- Agent makes assumptions if ambiguous

**No state persistence:**
- Agent RAM destroyed after execution
- Cannot resume partial work
- Must complete task in single execution

**Communication overhead:**
- Task description consumes main RAM
- Summary consumes main RAM
- Very small tasks may not benefit from delegation

---

## References

- I/O System: `data/architecture/hal8000-io-system.md`
- Library Architecture: `data/architecture/hal8000-library-architecture.md`
- System Design: `data/architecture/hal8000-system-design.md`
- Operating Principles: `CLAUDE.md` (Section: Sub-Agent Protocol)
- Agent Definitions: `.claude/agents/*.md`

---

**Implementation Status:** Agents Operational, Architecture Documented
**Available Agents:** 4 (research-synthesizer, hal-context-finder, system-maintenance, claude-code-validator)
**Next Steps:** Develop additional specialized agents as needs arise
