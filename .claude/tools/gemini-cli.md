# Gemini CLI - External Agent Tool

**Category:** External Agent (Independent)
**Interface:** Bash command-line tool
**Context Window:** 1,000,000 tokens
**Installation:** Host-installed (npm global)
**Path:** `/mnt/c/Users/Shahram-Dev/AppData/Roaming/npm/gemini`
**Version:** 0.4.1

---

## Overview

Google Gemini CLI is an **external agent** - an independent AI assistant controlled via bash commands. Unlike HAL8000 sub-agents (200K context), Gemini provides a **massive 1M token context window** for extremely heavy computational tasks.

**Architectural Position:**
```
HAL8000 (Claude, 200K context)
    ↓ command
Gemini CLI (External Agent, 1M context)
    ↓ process massive workload
Returns clean summary
    ↓ result
HAL8000 (RAM += summary only, not full processing cost)
```

---

## Agent Classification

| Agent Type | Context | Control | Use Case |
|-----------|---------|---------|----------|
| **Sub-Agents** (Task tool) | 200K | Internal, isolated process | Research, context discovery, moderate tasks |
| **Gemini CLI** (Bash) | 1M | External, command interface | Massive analysis, huge codebases, heavy refactoring |

---

## When to Use Gemini CLI

### ALWAYS Delegate to Gemini When:

1. **Context Exceeds 100K Tokens**
   - Large codebase analysis (50+ files)
   - Multi-file refactoring across extensive projects
   - Processing massive documents/datasets

2. **Complex Reasoning with Huge Context**
   - Cross-referencing dozens of files
   - Architectural analysis of large systems
   - Deep dependency tracking

3. **Sub-Agents Insufficient**
   - Task needs >200K context (sub-agent limit)
   - Requires extensive exploratory analysis
   - Needs to hold entire project in working memory

### NEVER Use Gemini For:

- Simple queries answerable with current RAM
- Tasks within sub-agent capability (≤200K)
- Operations requiring HAL8000-specific tools/architecture
- Quick lookups or single-file operations

---

## Command Patterns

### Non-Interactive Mode (Preferred)

**Basic Prompt:**
```bash
gemini -p "your prompt here"
```

**With Stdin Input:**
```bash
cat large-file.txt | gemini -p "analyze this code and summarize architecture"
```

**Sandbox Mode (Isolated Execution):**
```bash
gemini -p "refactor this codebase" --sandbox
```

**YOLO Mode (Auto-approve all actions):**
```bash
gemini -p "fix all type errors" --yolo
```

**Auto-edit Mode (Auto-approve edits only):**
```bash
gemini -p "update documentation" --approval-mode auto_edit
```

### Interactive Mode

**Launch Interactive Session:**
```bash
gemini
```

**Execute Prompt Then Continue Interactively:**
```bash
gemini -i "start by analyzing the architecture"
```

---

## Usage Protocol

### Step 1: Identify Heavy Task
```
User asks for massive analysis/refactoring
    ↓
Estimate context required
    ↓
If >100K tokens → Gemini CLI
If <100K tokens → Sub-agent or direct
```

### Step 2: Prepare Command
```bash
# Pattern 1: Direct prompt
gemini -p "analyze entire src/ directory and create architectural overview"

# Pattern 2: Pipe large context
find src/ -name "*.ts" -exec cat {} \; | gemini -p "analyze this TypeScript codebase"

# Pattern 3: Sandbox for safety
gemini -p "refactor all components to use hooks" --sandbox
```

### Step 3: Capture Summary Only
```bash
# Redirect to file
gemini -p "analyze..." > temp/gemini-analysis-summary.txt

# Or capture in variable (if short)
SUMMARY=$(gemini -p "quick summary of...")
```

### Step 4: Load Summary to RAM
```
Read summary file → Load ~5K tokens (not 800K)
Report to user
Main RAM saved: 795K tokens
```

---

## RAM Efficiency Pattern

**❌ WRONG (Direct Processing):**
```
Load 50 files (800K tokens) → Analyze in HAL8000 RAM
Result: RAM = 800K + baseline
```

**✅ RIGHT (Gemini Delegation):**
```
Delegate to Gemini CLI → Process 800K tokens externally
Gemini returns 5K summary → Load only summary
Result: RAM = 5K + baseline (saves 795K!)
```

---

## Comparison: Sub-Agents vs Gemini CLI

| Feature | Sub-Agents (Task tool) | Gemini CLI |
|---------|----------------------|------------|
| Context Window | 200K tokens | 1M tokens |
| Control | Internal (HAL8000 spawns) | External (bash command) |
| Isolation | Process-level | Independent agent |
| Tools | HAL8000 tools (Read, Grep, etc.) | Gemini-specific tools |
| Best For | Research, discovery, moderate tasks | Massive analysis, huge codebases |
| Invocation | `Task` tool | `Bash` tool (`gemini` command) |

---

## Example Use Cases

### Use Case 1: Analyze Large Codebase
```bash
# Task: Analyze 100-file codebase, create architecture doc
gemini -p "Analyze all TypeScript files in src/, create comprehensive \
architecture document covering: components, data flow, dependencies, \
patterns used. Output markdown." --sandbox > data/architecture/codebase-analysis.md
```

### Use Case 2: Multi-File Refactoring
```bash
# Task: Refactor 50+ components
gemini -p "Refactor all React class components to functional components \
with hooks. Maintain all functionality. Test thoroughly." --yolo
```

### Use Case 3: Cross-Reference Analysis
```bash
# Task: Find all usages of API across massive codebase
find . -name "*.ts" -o -name "*.tsx" | xargs cat | \
gemini -p "Identify all API calls, document endpoints used, \
create API usage map with file locations."
```

### Use Case 4: Heavy Documentation Generation
```bash
# Task: Generate docs from 200+ files
gemini -p "Generate comprehensive API documentation for entire codebase. \
Include: function signatures, parameters, return types, examples, \
cross-references." > docs/api-reference.md
```

---

## Advanced Features

### MCP Support
```bash
# Manage MCP servers
gemini mcp
```

### Extensions
```bash
# List extensions
gemini -l

# Use specific extensions
gemini -e extension1,extension2
```

### Sandbox with Custom Image
```bash
# Use specific Docker sandbox image
gemini -p "task" --sandbox --sandbox-image "custom-image:tag"
```

### Include Additional Directories
```bash
# Include extra workspace directories
gemini --include-directories /path/to/dir1,/path/to/dir2
```

---

## Integration with HAL8000

### Proactive Usage

I (HAL8000 CPU) will **proactively suggest** Gemini CLI when:
- User request implies >100K context needed
- Task involves entire codebase analysis
- Multi-file refactoring across many files
- Sub-agent capacity insufficient

**Example Proactive Suggestion:**
```
User: "Analyze the entire backend architecture and suggest improvements"
HAL8000: "This task requires analyzing extensive files (~500K tokens).
I'll delegate to Gemini CLI (1M context) for comprehensive analysis,
then load the summary. Proceeding..."
```

### Tool Discovery

Gemini CLI is discoverable via:
1. **Tool index:** `.claude/indexes/tools.json`
2. **Direct path:** `.claude/tools/gemini-cli.md` (this file)
3. **File system search:** Indexed for keyword discovery
4. **Context finder:** `/HAL-context-find gemini` loads this doc

---

## Credentials & Configuration

**API Key:** Configured in Gemini CLI settings (host installation)
**Config Location:** User's home directory (Gemini CLI manages)
**No HAL8000 Setup Required:** Tool is pre-configured on host

---

## Error Handling

**If Gemini CLI fails:**
1. Check host installation: `gemini --version`
2. Verify API credentials: `gemini -p "test"`
3. Fallback to sub-agents if context permits (≤200K)
4. Report error to user with diagnostic info

**Common Issues:**
- Timeout: Increase with `timeout` parameter in Bash tool
- API limits: Check Gemini API quota
- Sandbox failures: Verify Docker availability

---

## Version & Maintenance

**Current Version:** 0.4.1
**Update Check:** `npm list -g @google/generative-ai-cli`
**Upgrade:** `npm update -g @google/generative-ai-cli`

**Docker Image (Fallback):**
- Image: `us-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.4.1`
- Size: 1.26GB
- Use if host tool unavailable

---

## Summary

Gemini CLI is HAL8000's **heavy-lifting external agent**:
- **1M token context** for massive tasks
- **Independent processing** saves HAL8000 RAM
- **Command-line interface** via bash
- **Proactively used** for tasks >100K tokens
- **Returns summaries** not raw processing dumps

**Delegation Pattern:**
```
Heavy Task → Gemini CLI (1M context) → Clean Summary → HAL8000 RAM
```

This extends HAL8000's total computational capacity beyond the 200K RAM limit while maintaining efficient resource usage.
