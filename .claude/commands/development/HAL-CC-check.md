---
name: HAL-CC-check
description: Validate HAL8000-Assistant commands and agents for Claude Code compatibility via claude-code-validator agent
parameters:
  - name: file_path
    description: Optional specific file path to validate (defaults to all commands/agents)
    type: string
    required: false
---

# Command: HAL-CC-check

## Purpose

Validates HAL8000-Assistant commands and agents for compatibility with the current Claude Code environment by invoking the `claude-code-validator` agent.

## Syntax

```bash
/HAL-CC-check
```

No parameters required.

## Description

This command verifies that all HAL8000-Assistant CPU-level components (commands and agents) are compatible with the external Claude Code architecture. It detects:

- Deprecated tools that need replacement
- Invalid tool references
- API changes requiring updates
- New capabilities available for optimization

**Use Cases:**
- After Anthropic releases Claude Code updates
- Before major HAL8000-Assistant development sessions
- When commands/agents behave unexpectedly
- Periodic maintenance (quarterly recommended)

## Implementation

```markdown
# HAL-CC-check Implementation

## Step 1: Announce Check
Inform user that Claude Code compatibility check is starting.

## Step 2: Invoke Validator Agent
Use Task tool to launch claude-code-validator agent with this prompt:

"Validate all HAL8000-Assistant commands and agents for Claude Code compatibility.

Tasks:
1. Fetch current Claude Code documentation from docs.claude.com (start with claude_code_docs_map.md)
2. Extract available tools, deprecated features, and API changes
3. Read and analyze all files in .claude/commands/
4. Read and analyze all files in .claude/agents/
5. Identify tool usage issues (deprecated, invalid, changed APIs)
6. Generate structured compatibility report

Return complete report in markdown format with:
- Summary (total checked, issues found, overall status)
- Tool availability inventory
- Per-component analysis (commands and agents)
- Prioritized recommendations
- Documentation references

Focus on actionable findings - what needs updating and why."

## Step 3: Present Results
Display the agent's compatibility report to the user.

## Step 4: Summarize Status
Provide concise summary:
- Overall compatibility status (COMPATIBLE | WARNINGS | INCOMPATIBLE)
- Critical issues requiring immediate attention
- Recommended next actions

## Error Handling
If validator agent fails:
- Report failure to user
- Suggest manual verification at docs.claude.com
- Note that validation couldn't be completed
```

## Execution Pattern

```bash
/HAL-CC-check
↓
Task tool → claude-code-validator agent
↓ (isolated 200K context)
Agent fetches docs, validates components
↓
Returns compatibility report
↓
Display results to user
```

## Design Notes

**Why Separate from HAL-system-check:**
- Different validation target: External interface vs internal structure
- Different data source: Web documentation vs local filesystem
- Different failure response: Update our code vs fix our structure
- Composable: Can run independently or together

**Agent Delegation:**
- Documentation fetching is context-heavy (10-50K tokens)
- Validation logic complex (parsing, cross-referencing)
- Isolated execution keeps main session RAM clean
- Agent returns only final report (~2-5K tokens)

**Token Efficiency:**
- Direct implementation: ~50K tokens (fetch docs, load all commands/agents)
- Agent delegation: ~5K tokens (report only)
- Savings: ~90% RAM reduction

## Related Commands

- **HAL-system-check** - Validates internal HAL8000-Assistant structure and principles
- **HAL-register-dump** - Shows current CPU state
- **HAL-session-end** - Saves state before RAM wipe

## Related Agents

- **claude-code-validator** - Performs the validation (invoked by this command)
- **hal-system-check** - Validates internal structure

## Architecture Alignment

- **Von Neumann:** CPU instruction validation against external architecture
- **Unix:** Do one thing well (external compatibility only)
- **Assembly:** Verify opcodes match CPU capabilities

## Notes

- Run this check after Anthropic announces Claude Code updates
- Consider running before major development sessions
- Compatibility report helps maintain long-term system health
- Complements (doesn't replace) internal system validation
