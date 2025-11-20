# HAL8000-Assistant Tool Reference

**Version:** 1.0
**Created:** 2025-10-15
**Purpose:** Complete catalog of available tools for agent frontmatter specifications

---

## Overview

This reference documents all tools available in Claude Code for use in agent YAML frontmatter `tools` specifications. Use this guide when creating agents to select the appropriate tool set for the agent's purpose.

**Principle of Least Privilege:** Only include tools the agent actually needs. Tool whitelisting improves security, performance, and reliability.

---

## Standard Claude Code Tools

These tools are built into Claude Code and available without MCP servers.

### File Operations

**Read** - Read file contents
- **Use for:** Loading files, reading configurations, accessing data
- **Typical agents:** All agents that need file access
- **Example:** `- Read`

**Write** - Create or overwrite files
- **Use for:** Saving output, creating reports, generating files
- **Typical agents:** Code generation, report generation, data processing
- **Example:** `- Write`

**Edit** - Targeted file edits (find/replace)
- **Use for:** Modifying existing files without rewriting
- **Typical agents:** Code refactoring, configuration updates
- **Example:** `- Edit`

### File Search & Discovery

**Glob** - Pattern-based file matching
- **Use for:** Finding files by name patterns (*.md, **/*.py)
- **Typical agents:** File discovery, batch processing
- **Example:** `- Glob`

**Grep** - Content search in files
- **Use for:** Searching file contents, finding code patterns
- **Typical agents:** Code analysis, content discovery
- **Example:** `- Grep`

### System Operations

**Bash** - Execute shell commands
- **Use for:** Running external programs, git operations, system commands
- **Typical agents:** System maintenance, deployment, automation
- **Example:** `- Bash`
- **Caution:** Powerful tool - use sparingly and document why needed

### Web Access

**WebSearch** - Web search queries
- **Use for:** General web searches
- **Typical agents:** Research, information gathering
- **Example:** `- WebSearch`

**WebFetch** - Fetch URL content
- **Use for:** Loading specific web pages, API calls
- **Typical agents:** Research, data extraction, API integration
- **Example:** `- WebFetch`

### Task Management

**TodoWrite** - Manage task lists
- **Use for:** Creating and updating todo lists
- **Typical agents:** Rarely needed (CPU manages todos)
- **Example:** `- TodoWrite`

### Agent Delegation

**Task** - Invoke sub-agents
- **Use for:** Delegating work to other agents
- **Typical agents:** Supervisor agents, workflow coordinators
- **Example:** `- Task`

---

## MCP Server Tools

MCP tools require configured MCP servers. Format: `mcp__<server-name>__<tool-name>`

### Filesystem MCP (mcp__filesystem__)

**mcp__filesystem__read_text_file** - Read text files
- **Similar to:** Read tool (built-in may be preferred)
- **Use for:** File reading via MCP server
- **Example:** `- mcp__filesystem__read_text_file`

**mcp__filesystem__search_files** - Recursive file search
- **Use for:** Finding files in directory trees
- **Typical agents:** Context discovery, file system navigation
- **Example:** `- mcp__filesystem__search_files`

**mcp__filesystem__list_directory** - List directory contents
- **Use for:** Directory exploration, file system navigation
- **Typical agents:** Context discovery, system exploration
- **Example:** `- mcp__filesystem__list_directory`

**mcp__filesystem__get_file_info** - File metadata
- **Use for:** Getting file size, timestamps, permissions
- **Typical agents:** System analysis, metadata collection
- **Example:** `- mcp__filesystem__get_file_info`

**mcp__filesystem__write_file** - Write files
- **Similar to:** Write tool (built-in may be preferred)
- **Use for:** File creation via MCP server
- **Example:** `- mcp__filesystem__write_file`

**mcp__filesystem__edit_file** - Edit files
- **Similar to:** Edit tool (built-in may be preferred)
- **Use for:** File modification via MCP server
- **Example:** `- mcp__filesystem__edit_file`

### Omnisearch MCP (mcp__omnisearch__)

**mcp__omnisearch__web_search** - Enhanced web search
- **Providers:** Tavily, Brave, Kagi, Exa
- **Use for:** Comprehensive web research with multiple search engines
- **Typical agents:** Research agents
- **Example:** `- mcp__omnisearch__web_search`

**mcp__omnisearch__firecrawl_process** - Web content extraction
- **Modes:** Scrape, crawl, map, extract, actions
- **Use for:** Deep web content extraction and processing
- **Typical agents:** Research agents, content extraction
- **Example:** `- mcp__omnisearch__firecrawl_process`

### IDE MCP (mcp__ide__)

**mcp__ide__getDiagnostics** - Language diagnostics
- **Use for:** Getting compile errors, warnings from VS Code
- **Typical agents:** Code analysis, error detection
- **Example:** `- mcp__ide__getDiagnostics`

**mcp__ide__executeCode** - Execute code in Jupyter
- **Use for:** Running Python code in notebook kernels
- **Typical agents:** Data analysis, code testing
- **Example:** `- mcp__ide__executeCode`

---

## Common Tool Combinations

### File System Agent (Context Discovery)
```yaml
tools:
  - Read
  - Grep
  - Glob
  - mcp__filesystem__search_files
  - mcp__filesystem__list_directory
  - mcp__filesystem__get_file_info
```

**Example:** `hal-context-finder` agent

**Purpose:** Navigate and discover content in file system without heavy tool usage.

---

### Research Agent (Web Research)
```yaml
tools:
  - mcp__omnisearch__web_search
  - mcp__omnisearch__firecrawl_process
  - WebSearch
  - WebFetch
  - Read
  - Write
```

**Example:** `research-synthesizer` agent

**Purpose:** Conduct web research, extract content, synthesize findings.

**Why these tools:**
- omnisearch tools: Enhanced web search and content extraction
- WebSearch/WebFetch: Fallback web access
- Read: Load local context if needed
- Write: Save research results

---

### Code Generation Agent
```yaml
tools:
  - Read
  - Write
  - Glob
  - Grep
```

**Example:** `command-builder` agent

**Purpose:** Generate code/commands by reading templates and writing output.

**Why these tools:**
- Read: Load templates, examples, context files
- Write: Output generated code (rarely needed if returning as text)
- Glob: Discover template files
- Grep: Search for patterns in templates

**Note:** Code generation agents often don't need Write if they return generated code as text to the main session.

---

### System Maintenance Agent
```yaml
tools:
  - Read
  - Glob
  - Grep
  - Bash
  - mcp__filesystem__list_directory
  - mcp__filesystem__get_file_info
  - mcp__filesystem__search_files
```

**Example:** `system-maintenance` agent (used by HAL-system-check)

**Purpose:** Audit system structure, validate integrity, check compliance.

**Why these tools:**
- File tools: Inspect system structure
- Bash: Run validation commands
- MCP filesystem: Deep file system analysis

---

### Validation Agent (Fast and Simple)
```yaml
tools:
  - Read
  - Bash
model: haiku
```

**Purpose:** Quick validation tasks (data format, simple checks).

**Why haiku model:** Fast, cost-effective for simple validation.

**Why minimal tools:** Validation doesn't need extensive capabilities.

---

## Tool Selection Guidelines

### Start Minimal
Begin with the smallest tool set that accomplishes the task. Add tools only when needed.

**Example:**
```yaml
# Start with this
tools:
  - Read

# Add only if you discover you need them
tools:
  - Read
  - Grep  # Added: need to search file contents
```

### Avoid Redundancy
Don't include both built-in and MCP equivalents unless you have a specific reason.

**Prefer built-in tools:**
```yaml
# Good - use built-in Read
tools:
  - Read

# Redundant - both do the same thing
tools:
  - Read
  - mcp__filesystem__read_text_file
```

### Document Tool Rationale
In your agent prompt, explain why each tool is needed.

**Example in agent file:**
```markdown
---
name: my-agent
tools:
  - Read      # Load template files
  - Grep      # Search for patterns in templates
  - Write     # Output generated content
---

You need Read to load templates, Grep to find patterns, and Write to save output.
```

### Consider Security
Bash is powerful but risky. Only include if absolutely necessary and document why.

```yaml
# Needs strong justification
tools:
  - Bash  # REQUIRED: Must run git commands for version control operations
```

### Performance Implications
Each tool adds to context. Smaller tool sets = faster agent startup.

```yaml
# Heavy (slower startup)
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch

# Light (faster startup)
tools:
  - Read
  - Grep
```

---

## Model Selection Guide

### Haiku - Speed & Efficiency
**When to use:**
- Simple validation tasks
- Quick data transformations
- Fast lookups and checks
- High-volume repetitive operations

**Example:**
```yaml
tools:
  - Read
  - Bash
model: haiku
```

### Sonnet - Balanced (Default)
**When to use:**
- General research and synthesis
- Code analysis and generation
- Multi-step workflows
- Most agents (default choice)

**Example:**
```yaml
tools:
  - Read
  - Write
  - Grep
model: sonnet
```

### Opus - Maximum Capability
**When to use:**
- Complex reasoning requirements
- Novel problem-solving
- Critical decision-making
- Tasks requiring deepest understanding

**Example:**
```yaml
tools:
  - Read
  - Write
  - WebSearch
model: opus
```

---

## Verification Checklist

Before finalizing agent frontmatter:

- [ ] **Minimal tools:** Only includes tools agent actually uses
- [ ] **No redundancy:** Not mixing built-in and MCP equivalents unnecessarily
- [ ] **Appropriate model:** Haiku for simple, Sonnet for general, Opus for complex
- [ ] **Documented rationale:** Agent prompt explains why each tool is needed
- [ ] **Security considered:** Bash usage justified if included
- [ ] **Tested:** Agent verified to work with specified tool set

---

## Examples from HAL8000-Assistant

### Example 1: hal-context-finder
```yaml
---
name: hal-context-finder
description: Discovers and loads HAL8000-Assistant system context
tools:
  - Read
  - Grep
  - Glob
  - mcp__filesystem__search_files
  - mcp__filesystem__list_directory
  - mcp__filesystem__get_file_info
model: haiku
---
```

**Rationale:**
- Haiku: Fast file system navigation
- Read/Grep/Glob: Standard file operations
- MCP filesystem tools: Deep directory analysis
- No Write: Returns findings to main session
- No Bash: Pure file system operations, no shell needed

---

### Example 2: research-synthesizer
```yaml
---
name: research-synthesizer
description: Comprehensive web research specialist
tools:
  - mcp__omnisearch__web_search
  - mcp__omnisearch__firecrawl_process
  - WebSearch
  - WebFetch
  - Read
  - Write
model: sonnet
---
```

**Rationale:**
- Sonnet: Balance of capability and speed for research
- Omnisearch tools: Primary research capability
- WebSearch/WebFetch: Fallback web access
- Read: Load local context if needed
- Write: Save research output

---

### Example 3: command-builder
```yaml
---
name: command-builder
description: HAL-Script command generation specialist
tools:
  - Read
  - Glob
  - Grep
model: sonnet
---
```

**Rationale:**
- Sonnet: Code generation requires reasoning
- Read: Load template files
- Glob: Discover templates
- Grep: Search template patterns
- No Write: Returns generated command as text
- No Bash: Pure template processing

---

## Maintenance

**Update this reference when:**
- New Claude Code tools are released
- New MCP servers are integrated
- Tool behavior changes significantly
- New tool combination patterns emerge

**Version History:**
- v1.0 (2025-10-15): Initial tool reference for frontmatter system

---

**This reference enables informed tool selection for agent development, ensuring agents have exactly the capabilities they need - no more, no less.**
