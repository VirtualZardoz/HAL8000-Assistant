---
name: HAL-context-find
description: Find and load system context without consuming main session RAM
---

# HAL Context Find Command

This command launches the `hal-context-finder` specialized agent to discover and load HAL8000-Assistant system context efficiently. It preserves main session RAM by delegating navigation and file loading to an isolated sub-agent context.

## Usage

```bash
/HAL-context-find [query]
```

**Arguments:**
- `query` (required): What context you're looking for (e.g., "register architecture", "HAL-session-end command", "von Neumann research")

## What This Command Does

1. **Launches Specialized Agent**
   - Spawns `hal-context-finder` sub-agent with fresh 200K RAM
   - Passes user query to agent
   - Agent operates in isolated context

2. **Efficient Navigation**
   - Agent classifies query type (Architecture, Command, Research, Session, Data)
   - Uses built-in directory priority mappings for smart targeting
   - Targets most likely 2-3 directories before expanding scope
   - Uses token-efficient search patterns

3. **Complete Content Loading**
   - Agent reads complete files (not just paths)
   - Packages content with clear source attribution
   - Includes related context when relevant
   - Returns structured summary to main session

4. **RAM Preservation**
   - Main session RAM += summary only (not full navigation cost)
   - Typically saves 60-80% tokens vs direct loading
   - Agent context is automatically garbage collected after completion

## Implementation

### Execution Logic

When `/HAL-context-find [query]` is invoked:

**Command:** Launch `hal-context-finder` sub-agent with the user's query as input.

The sub-agent will:
1. Classify query type and prioritize search directories using built-in mappings
2. Navigate file system efficiently using targeted searches
3. Load complete file contents (not summaries)
4. Package results with structured format:
   - Context Content (complete files)
   - File Locations (exact paths)
   - Summary (relevance assessment)
   - Related Context (additional relevant files)
5. Return clean summary to main session

### Expected Output

Agent returns structured response:

```markdown
## Context Content
[Complete file contents with clear source headers]

## File Locations
- /mnt/d/~HAL8000-Assistant/path/to/file1.md
- /mnt/d/~HAL8000-Assistant/path/to/file2.md

## Summary
Found [N] relevant files for query "[query]".
[Brief relevance assessment]

## Related Context
- path/to/related-file1.md - [Brief description]
- path/to/related-file2.md - [Brief description]
```

Main session receives only this structured summary, not the full navigation cost.

## Query Examples

### Architecture Queries
```bash
/HAL-context-find register architecture
/HAL-context-find system design specification
/HAL-context-find operating principles
```

Agent targets: `.claude/architecture/`, `data/architecture/`

### Command Queries
```bash
/HAL-context-find HAL-session-end command
/HAL-context-find available commands
/HAL-context-find how to use HAL-system-check
```

Agent targets: `.claude/commands/`

### Research Queries
```bash
/HAL-context-find von Neumann architecture
/HAL-context-find Unix philosophy
/HAL-context-find assembly language principles
```

Agent targets: `data/research/`

### Session Queries
```bash
/HAL-context-find last session
/HAL-context-find previous work
/HAL-context-find current system state
```

Agent targets: `.claude/sessions/`, `.claude/state.json`

### Agent Queries
```bash
/HAL-context-find research-synthesizer agent
/HAL-context-find available agents
```

Agent targets: `.claude/agents/`

## Token Economics

**Without hal-context-finder (direct loading):**
```
Main Session RAM before: 30K
+ Navigate directories: +10K
+ Read multiple files: +15K
+ Filter and summarize: +5K
= Main Session RAM after: 60K
Cost: 30K tokens
```

**With hal-context-finder (delegated):**
```
Main Session RAM before: 30K
+ Launch agent: +1K (command overhead)
+ Receive summary: +4K (structured results)
= Main Session RAM after: 35K
Cost: 5K tokens
Agent used: ~30K in isolated context (auto-collected)
Savings: 30K tokens (85%)
```

## Architecture Alignment

This command implements HAL8000-Assistant architecture principles:

**Von Neumann:**
- Sub-agent as virtual memory extension (isolated address space)
- Stored-program concept (agent definition is data that executes)
- Self-modifying capability (can discover and load other commands)

**Unix Philosophy:**
- Does one thing well (context discovery and loading)
- Delegates specialized work (to sub-agent)
- Composable (works with any query type)
- Text-based I/O (structured markdown output)
- Reduces context through delegation

**Assembly Principles:**
- Explicit control (manual invocation, no auto-loading)
- Low-level visibility (shows exact file paths)
- Direct memory access (agent reads from filesystem)
- Efficient resource usage (minimal main RAM consumption)

**Sub-Agent Protocol:**
- Extends total RAM capacity through process isolation
- Agent has fresh 200K context, returns only summary
- Pattern: input (query) >> output (summary)
- Main session RAM += result only, not processing cost

## Related Components

- **Agent Definition:** `.claude/agents/hal-context-finder.md`
- **System Indexes:** `.claude/indexes/master.json` (system inventory)
- **BIOS:** `CLAUDE.md` (defines sub-agent protocol)
- **State:** `.claude/state.json` (referenced for session queries)

## When to Use

**ALWAYS use this command for:**
- Loading architecture documentation
- Discovering command definitions
- Accessing research files
- Exploring session history
- Finding agent definitions
- Any context-heavy navigation task

**DON'T use this command for:**
- Files you already know the exact path to (use Read directly)
- Single small files (<2K tokens)
- Current session state (already in RAM)

## Notes

- Agent operates in isolated 200K context (separate from main session)
- Agent context is garbage collected automatically after completion
- Structure map enables smart navigation (load it first for efficiency)
- Typical token savings: 60-85% vs direct loading
- Agent returns complete file contents, not excerpts
- Multiple related files can be loaded in single agent invocation
