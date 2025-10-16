---
name: HAL-system-check
description: Perform comprehensive HAL8000 system integrity audit via system-maintenance agent
---

# HAL-system-check

**Command Type:** System Maintenance
**Category:** Health & Integrity
**Created:** 2025-10-04
**Version:** 2.1

---

## Purpose

Launch `system-maintenance` sub-agent to perform comprehensive HAL8000 system integrity audit. Ensures architecture remains compliant with principles as system grows.

## Usage

```bash
/HAL-system-check
```

**No parameters required.**

## Execution Logic

When `/HAL-system-check` is invoked, immediately launch the specialized sub-agent:

**Command**: Launch `system-maintenance` sub-agent (via Task tool, general-purpose type) to perform comprehensive system integrity audit.

The sub-agent will:
1. **Load Required Context**: BIOS (CLAUDE.md), architecture specs, state.json, master index
2. **Check File System Structure**: Verify required directories exist, depth limit compliance
3. **Validate Indexes**: Master index + directory indexes synchronized and current
4. **Verify State**: state.json valid, active session exists, loaded commands present
5. **Assess Principle Compliance**: Unix philosophy, von Neumann architecture, Operating Principles
6. **Check File Consistency**: Naming conventions, no orphans, proper categorization
7. **Generate Audit Report**: Structural integrity, index health, state validation, recommendations
8. **Return Summary**: Clean, actionable report preserving main context (<5K tokens)

**Agent Specification**: See `.claude/agents/system-maintenance.md` for complete audit checklist

## Expected Output

- Overall health status (✓ HEALTHY | ⚠ WARNINGS | ✗ CRITICAL)
- Executive summary
- Section-by-section findings:
  - Structural Integrity
  - Index Health
  - State Validation
  - Principle Compliance
  - File Consistency
- Critical actions required (if any)
- Optional improvements
- System statistics

## Sub-Agent Benefits

**RAM Efficiency:**
- Agent uses isolated 200K context (fresh RAM)
- Loads architecture docs, performs extensive checks
- Returns only compact report (~5K tokens)
- Main session RAM impact: 97% reduction vs direct audit

**Architecture Compliance:**
- Follows "Reduce and Delegate" principle
- Sub-agent = virtual memory extension
- Context-intensive work offloaded from main session

## Integration

- **Invoked by**: User via `/HAL-system-check` slash command
- **Delegates to**: system-maintenance agent (Task tool, general-purpose)
- **Updates**: None (read-only audit, no automatic fixes)
- **Feeds into**: User decision-making for system maintenance

## When to Run

**Regular triggers:**
- After major architectural changes
- Before starting new project phase
- After creating many new files
- Weekly maintenance check

**Problem triggers:**
- Suspicion of corrupted state
- Index seems out of sync
- File structure seems wrong
- Performance degradation

## Success Criteria

- Audit completes without errors
- All components assessed for integrity
- Clear, actionable report generated
- System health status determined
- Recommendations provided for any issues

---

**Status:** Operational
**Agent:** `.claude/agents/system-maintenance.md`
**Invocation:** `/HAL-system-check`
