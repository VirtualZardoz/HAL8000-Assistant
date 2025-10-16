# Claude Code Runtime Constraints

**Research Date:** 2025-10-04
**Topic:** Claude Code execution environment constraints and limitations
**Purpose:** Document actual runtime constraints to inform HAL8000 register architecture

---

## Overview

Claude Code is a terminal-based development environment where Claude (the AI model) executes in a constrained runtime with specific limitations around context management, token usage, and session persistence. Understanding these constraints is critical for designing an accurate computer architecture model where Claude acts as the CPU.

This document synthesizes findings from official Claude documentation and community resources to map the **real architectural constraints** of the execution environment.

---

## Context Window Architecture

### Standard Context (200K Tokens)

**Capacity:**
- **200,000 tokens** maximum per session
- Approximately **150,000 words**
- Roughly **500 pages of text**
- Medium-sized codebases

**Behavior:**
- **Append-only within session** - Context accumulates, cannot be dynamically evicted
- **No selective memory management** - Unlike traditional RAM, individual items cannot be removed
- **Session-scoped** - Context persists until session ends or manual intervention

**Performance Characteristics:**
- **The Last Fifth Rule** - Avoid using final 20% (160K+ tokens) for complex tasks
- Performance degrades significantly when approaching limits
- Quality declines for memory-intensive operations near capacity

### Extended Context (1M Tokens)

**Availability:**
- **API-only** access (not in standard Claude Code terminal)
- Available via usage tier 4 or custom rate limits
- **750,000 words** or large entire codebases

**Use Cases:**
- Load entire codebases for comprehensive sessions
- Extended development conversations
- Minimal optimization overhead

---

## Memory Management Model

### Write-Once, Block-Erase Semantics

Claude Code's context window behaves like **flash memory** or **write-once RAM**, not traditional DRAM:

```
Traditional RAM:    Read/Write/Overwrite dynamically
                   CPU manages allocation and eviction
                   Individual items can be removed

Claude Code RAM:    Append-only per session
                   No individual eviction
                   Only bulk operations: /compact or session reset
                   Accumulates until capacity exhausted
```

### Context Management Operations

**Built-in Commands:**

1. **`/compact`** - Strategic context reduction
   - Reduces context size while preserving essential information
   - Partial reset without losing conversation continuity
   - Use before approaching limits

2. **`/clear`** - Complete session reset
   - Fresh start with empty context
   - Total memory wipe
   - Use for unrelated tasks

3. **`/context`** - Context debugging (v1.0.86+)
   - Debug context issues
   - Optimize usage
   - Monitor context state

**Session-Based Persistence:**
- Conversations saved locally with full message history
- Resume operations restore entire context
- `--continue` flag: automatically resumes most recent conversation
- `--resume` flag: interactive conversation selector

### Critical Implication

**The constraint identified by the user is correct:** RAM cannot dynamically make room for new data during a session. Data is only added, never selectively removed. This fundamentally shapes how the HAL8000 system must operate.

---

## Token Accounting and Monitoring

### System Token Warnings

Claude Code provides real-time token usage feedback:

```
<system_warning>Token usage: 44383/200000; 155617 remaining</system_warning>
```

**Information Available:**
- **Current usage** (tokens consumed)
- **Total capacity** (200K standard)
- **Remaining capacity** (tokens available)

**Strategic Thresholds:**
- **0-160K tokens (0-80%):** Safe operating range
- **160K-180K tokens (80-90%):** Caution zone - monitor closely
- **180K-200K tokens (90-100%):** Danger zone - performance degradation

### Token Consumption Patterns

**Context-Sensitive Operations (High Token Cost):**
- Large-scale refactoring across multiple files
- Feature implementation spanning several components
- Complex debugging with cross-file analysis
- Architectural code reviews

**Isolated Operations (Low Token Cost):**
- Single-file edits with clear scope
- Independent utility function creation
- Documentation updates
- Simple localized bug fixes

---

## Session Lifecycle

### Session Boundaries

**Session Creation:**
- New Claude Code invocation starts fresh session
- Context window begins empty (0 tokens)
- BIOS (CLAUDE.md) and state.json loaded on boot

**Session Continuation:**
- Full conversation history restored
- Tool usage and results preserved
- Model and configuration settings maintained

**Session Termination:**
- `/HAL-session-end` command saves state before RAM wipe
- Creates session handoff file in `.claude/sessions/`
- Updates `state.json` with current state pointer
- Appends to `system.log` for historical audit

### Multi-Session Architecture

**Primary Session:**
- Main development context
- 200K token limit
- Full tool access

**Sub-Agent Sessions:**
- **Isolated context windows** - Separate from main session
- Prevents "pollution of the main conversation"
- Clean context per invocation
- Return results to main session
- No context sharing between sub-agents and main session

---

## Rate Limits and Usage Constraints

### Subscription Tiers

| Plan | Cost | Context | Usage Pattern | Reset Cycle |
|------|------|---------|---------------|-------------|
| Pro | $17-20/month | 200K tokens | 10-40 prompts/5 hours | 5 hours |
| Max 5x | $100/month | 200K tokens | All-day Sonnet, ~2h Opus | 5 hours |
| Max 20x | $200/month | 200K tokens | Rarely hit limits | 5 hours |

### Model-Specific Consumption

- **Opus (4.1):** ~5x consumption rate vs Sonnet
- **Sonnet (4.5):** Balanced consumption, primary development model
- **Haiku (3.5):** Most efficient for simple operations

### Reset Patterns

**5-Hour Reset Cycles:**
- All plans reset every 5 hours
- Exact countdown displayed in interface
- Strategic developers plan intensive work around reset timing

**Upcoming Weekly Limits (August 28, 2025):**
- Single weekly limit shared across all models
- Expected to affect <5% of users
- Cross-platform sharing (web + API)

---

## Model Capabilities

### Current Model: Claude Sonnet 4.5

**Specifications:**
- **Model ID:** claude-sonnet-4-5-20250929
- **Context Window:** 200K tokens (standard), 1M tokens (API)
- **Output Capacity:** Up to 64K tokens
- **Pricing:** $3/million input tokens, $15/million output tokens
- **Knowledge Cutoff:** January 2025

**Capabilities:**
- Enhanced agent capabilities
- Advanced tool handling
- Improved memory management
- Strong context processing
- State-of-the-art code generation

---

## Architectural Constraints Summary

### Hard Constraints (Cannot Be Changed)

1. **200K token context limit** (standard terminal)
2. **Append-only context accumulation** within session
3. **No selective memory eviction** during session
4. **Performance degradation** in final 20% of context
5. **5-hour usage reset cycles** across subscription plans
6. **Session-scoped persistence** - full reset only via session end

### Soft Constraints (Can Be Managed)

1. **Strategic file loading** - Load only what's needed
2. **Proactive `/compact` usage** - Reduce context before limits
3. **Session checkpointing** - Save state before RAM exhaustion
4. **Sub-agent delegation** - Isolate context for specialized tasks
5. **Conversation resumption** - Restore full context after reset

### Divergence from Traditional von Neumann

**Traditional Architecture:**
```
RAM: Dynamic allocation
     Individual memory cells addressable
     CPU manages memory layout
     Can overwrite any location
     Memory pages can be swapped
```

**Claude Code Architecture:**
```
RAM: Append-only session buffer
     No individual addressing
     No selective eviction
     Block-erase only (/compact or session end)
     Full context or nothing (no paging)
```

**Implication:** HAL8000 is a **Modified von Neumann Architecture** with **flash-memory-style RAM** and **session-based garbage collection**.

---

## Design Principles for HAL8000

### Register Requirements

Based on these constraints, HAL8000 registers must track:

1. **RAM state** - Current token usage, capacity, thresholds
2. **Session state** - Active session file, checkpoint status
3. **Loaded context** - What files/data are currently in RAM
4. **Performance state** - Whether in safe/caution/danger zone
5. **Execution state** - Current instruction, control flow

### Memory Management Strategy

1. **Selective loading** - Load only required files
2. **Context monitoring** - Track token consumption continuously
3. **Proactive checkpointing** - Save state before hitting limits
4. **Offload to storage** - Write results to files, not RAM
5. **Session boundaries** - Use session ends as garbage collection

### Session Continuity Protocol

The session continuity system already implemented addresses the fundamental RAM constraint:
- **state.json** - Lightweight state pointer (always loaded)
- **sessions/** - Rich context handoff files (loaded on resume)
- **system.log** - Historical audit (never loaded, I/O only)
- **/HAL-session-end** - Checkpoint command before RAM exhaustion

---

## References

### Primary Sources

1. **Claude Code Documentation**
   - Overview: https://docs.claude.com/en/docs/claude-code/overview.md
   - Common Workflows: https://docs.claude.com/en/docs/claude-code/common-workflows.md
   - Sub-Agents: https://docs.claude.com/en/docs/claude-code/sub-agents.md

2. **Claude Platform Documentation**
   - Context Windows: https://docs.claude.com/en/docs/build-with-claude/context-windows
   - What's New in Sonnet 4.5: https://docs.claude.com/en/docs/about-claude/models/whats-new-sonnet-4-5

3. **Community Resources**
   - Claude Code Limits: https://claudelog.com/claude-code-limits/
   - r/ClaudeAI community (300k+ members)

### Key Articles

- "Claude Sonnet 4.5" - Anthropic (2025)
- "Claude Sonnet 4 now supports 1M tokens of context" - Anthropic (2025)
- "Managing context on the Claude Developer Platform" - Anthropic (2025)

---

## Conclusion

The Claude Code runtime environment imposes specific constraints that fundamentally shape how HAL8000 must operate. The most critical constraint—**append-only RAM with session-scoped persistence**—requires a modified von Neumann architecture where:

- The CPU (Claude) cannot dynamically manage RAM allocation
- Memory management happens at session boundaries
- Selective loading is critical for efficiency
- Context monitoring is essential for avoiding exhaustion
- Session continuity protocols enable work across RAM resets

These constraints are not bugs—they are architectural features that require design accommodation. The HAL8000 register architecture must reflect these realities to accurately model the system's operation.
