---
name: Architecture Consultant
description: Validate design decisions against HAL8000-Assistant's architectural principles (von Neumann, Unix philosophy, Assembly concepts). Use when reviewing code, making design decisions, creating new components, or when architectural violations are detected. Activate during code reviews, command creation, or system modifications.
allowed-tools: Read
---

# Architecture Consultant

This Skill validates HAL8000-Assistant design decisions against the system's architectural foundations: Modified von Neumann Architecture, Unix Philosophy, and Assembly Language Principles.

## Purpose

Proactively detect and warn about architectural violations to maintain system coherence and principle compliance.

## When to Activate

**Triggers:**
- Creating new commands or agents
- Modifying system structure or organization
- Design discussions about new features
- Code reviews
- User asks "should I..." or "how should I..." about system design
- Detecting potential violations in proposed changes

## Architecture Principles Reference

### Modified von Neumann Architecture

**Core Tenets:**
1. **Append-only RAM** - Context accumulates, no dynamic eviction within session
2. **Session boundaries = garbage collection** - Only way to reclaim RAM
3. **Selective loading mandatory** - Every file load is permanent commitment
4. **State persists via file system** - Not in volatile RAM

**Violations to Watch For:**
- ❌ Assuming RAM can be freed during session
- ❌ Loading files "just in case" (speculative loading)
- ❌ Storing critical state only in RAM
- ❌ Ignoring token cost of operations

### Unix Philosophy

**Core Tenets:**
1. **Do one thing well** - Single responsibility per component
2. **Build once, reuse always** - Create reusable patterns
3. **Compose via interfaces** - File I/O is universal interface
4. **Delegate specialized work** - Pipe to external programs
5. **Simple, not complex** - Max 3-level depth, minimal abstractions
6. **Text streams** - Plain text files, human-readable

**Violations to Watch For:**
- ❌ Single component doing multiple unrelated things
- ❌ Directory depth exceeding 3 levels (except external libraries)
- ❌ Binary/opaque file formats for system data
- ❌ Duplicating functionality across components
- ❌ Complex abstractions when simple will do
- ❌ Not delegating to specialized tools/agents

### Assembly Language Principles

**Core Tenets:**
1. **Explicit control** - No hidden operations
2. **Register awareness** - Track CPU state continuously
3. **Sequential execution** - Fetch-decode-execute unless control flow changes
4. **One-to-one mapping** - Commands map directly to operations
5. **Low-level visibility** - System state inspectable at all times

**Violations to Watch For:**
- ❌ Hidden state changes
- ❌ Unclear control flow
- ❌ Commands with vague/ambiguous mappings
- ❌ Opaque system state

## Response Protocol

When architectural issue detected:

### 1. Identify Violation

State which principle is violated and why:
```
⚠️ Architecture Warning: [Principle] violation detected

Issue: [Specific problem]
Principle: [Which tenet violated]
```

### 2. Explain Impact

Describe consequences:
```
Impact:
- [Immediate consequence]
- [Long-term consequence]
- [System coherence issue]
```

### 3. Suggest Solution

Offer architecturally-sound alternatives:
```
Recommended approach:
- [Solution aligned with principles]
- [Why this maintains coherence]
```

### 4. Provide Context

Reference relevant architecture docs if needed:
```
See: [relevant doc in data/architecture/ or data/research/]
```

## Examples

### Example 1: Unix Philosophy Violation

**Scenario:** User wants to add research, context-finding, AND maintenance to one agent

**Response:**
```
⚠️ Architecture Warning: Unix Philosophy violation

Issue: Proposed agent combines three distinct responsibilities
(research, context-finding, maintenance) in one component.

Principle: "Do one thing well" - Each component should have single purpose

Impact:
- Harder to maintain and test
- Violates existing agent separation pattern
- Increases complexity unnecessarily

Recommended approach:
- Keep existing specialized agents (research-synthesizer,
  hal-context-finder, system-maintenance)
- Create coordinator agent if needed to orchestrate them
- Follows Unix: "Compose via interfaces"

See: data/research/02-unix-philosophy.md
```

### Example 2: Depth Limit Violation

**Scenario:** User creates `.claude/commands/system/utilities/helpers/file-ops/`

**Response:**
```
⚠️ Architecture Warning: Depth limit exceeded

Issue: Proposed path has 5 levels of depth
(.claude/commands/system/utilities/helpers/file-ops/)

Principle: Unix Philosophy - "Simple, not complex" (max 3 levels)

Impact:
- Violates HAL8000-Assistant structural standard
- Makes navigation harder
- Increases cognitive overhead

Recommended approach:
- Flatten to: .claude/commands/system/ (level 2)
- OR: .claude/commands/utilities/ if distinct category needed
- Group by function, not nested hierarchy

Exception: External libraries (.claude/libraries/external/) exempt
```

### Example 3: RAM Management Violation

**Scenario:** Code loads entire directory speculatively

**Response:**
```
⚠️ Architecture Warning: Modified von Neumann violation

Issue: Loading all files in directory without specific need

Principle: "Selective loading mandatory" - Every file load is permanent

Impact:
- Wastes limited RAM on unused content
- May push session into DANGER zone prematurely
- Violates Resource Management Protocol

Recommended approach:
- Ask user which specific files needed
- Use Grep to search for specific content first
- Load only confirmed-necessary files
- Follow Context Awareness Protocol

See: CLAUDE.md - Resource Management Protocol
```

### Example 4: Good Design (Positive Reinforcement)

**Scenario:** User creates focused single-purpose command

**Response:**
```
✅ Architecture: Well-designed

Design: New command has single clear responsibility, uses existing
agents for delegation, follows template structure.

Principles followed:
- Unix: "Do one thing well"
- Unix: "Delegate specialized work"
- Assembly: "One-to-one mapping" (clear command-to-operation)

This maintains system coherence. Proceed!
```

## Integration with HAL8000-Assistant Architecture

**References (loaded on-demand):**
- CLAUDE.md (BIOS - always in context)
- data/research/01-von-neumann-architecture.md
- data/research/02-unix-philosophy.md
- data/research/03-assembly-language-principles.md
- data/architecture/hal8000-system-design.md

**Works with:**
- command-builder agent (validates generated commands)
- system-maintenance agent (audits existing structure)

For detailed principles, see [principles-reference.md](principles-reference.md).
