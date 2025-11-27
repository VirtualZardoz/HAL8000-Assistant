---
name: command-name
description: Brief description for command palette (Level 5 - multi-agent coordination)
parameters:
  - name: param1
    description: Parameter description
    type: string
    required: true
---

# [Command Name]

**Command Type:** [System | Development | Documentation | Application]
**Category:** [system/ | development/ | documentation/ | custom/]
**Level:** 5 - Supervisor Prompt
**Created:** [YYYY-MM-DD]
**Version:** 1.0

---

## Purpose

[What this command does - coordinates multiple sub-agents]

---

## Usage

```bash
/command-name [arguments]
```

**Parameters:**
- `argument1` - [Description]

---

## Variables/Parameters

**Input Variables:**
- `variable_name` - [Type] - [Purpose]
- `agent_A_params` - [Type] - [Passed to agent A]
- `agent_B_params` - [Type] - [Passed to agent B]

**Output Variables:**
- `integrated_results` - [Type] - [Combined from multiple agents]

---

## Instructions

**Multi-Agent Coordination:**

1. **[Preparation Phase]**: [Setup]
   - [Prepare parameters for all agents]
   - [Determine execution strategy: parallel or sequential]

2. **[Agent Coordination Phase]**: [Orchestrate multiple agents]
   - [See Delegation Patterns section below]

3. **[Integration Phase]**: [Combine agent results]
   - [Merge data from agent A and agent B]
   - [Resolve conflicts or dependencies]
   - [Synthesize unified output]

4. **[Finalization]**: [Complete and return]
   - [Format integrated results]
   - [Return to user]

---

## Delegation Patterns

**Multi-Agent Orchestration:**

### Agent A: [agent-name-A]
**Purpose:** [What agent A does]
**Task:**
```markdown
Launch [agent-name-A] sub-agent with task:
  "[Instructions for agent A]"

Agent A will: [specific work]
Returns: [what A provides]
```

### Agent B: [agent-name-B]
**Purpose:** [What agent B does]
**Task:**
```markdown
Launch [agent-name-B] sub-agent with task:
  "[Instructions for agent B]"

Agent B will: [specific work]
Returns: [what B provides]
```

### Coordination Strategy:

**Parallel execution:**
```markdown
Launch both agents simultaneously (single message, multiple Task calls):
1. Launch agent-A with task-X
2. Launch agent-B with task-Y
3. Wait for both completions
4. Integrate results from both agents
```

**Sequential execution:**
```markdown
1. Launch agent-A first
2. Wait for completion
3. Use agent-A results to inform agent-B task
4. Launch agent-B
5. Wait for completion
6. Combine both results
```

---

## Workflow Integration

**Agent coordination patterns:**
- [How agents depend on each other]
- [Data flow between agents]
- [Error propagation and handling]

---

## Output Format

**What user sees:**
```
[Integrated output from multiple agents]

Agent A Results:
  - [Summary]

Agent B Results:
  - [Summary]

Integrated Analysis:
  - [Combined insights]
```

---

## Error Handling

**Multi-agent error scenarios:**
- If agent-A fails: [Response and recovery]
- If agent-B fails: [Response and recovery]
- If both fail: [Fallback strategy]
- If results incompatible: [Resolution approach]

---

## Dependencies

**Required Agents:**
- `agent-name-A` - [Purpose]
- `agent-name-B` - [Purpose]

---

## Performance Considerations

**RAM Usage:**
- Multiple agents = multiple isolated contexts
- Main session only receives summaries
- Estimated token savings: [X%]

**Execution Time:**
- Parallel: [faster but resource-intensive]
- Sequential: [slower but more controlled]

---

## Metadata

**Version History:**
- v1.0 (YYYY-MM-DD) - Initial implementation

**Status:** [Draft | Testing | Production]
**Template Level:** 5 - Supervisor (multi-agent coordination)
