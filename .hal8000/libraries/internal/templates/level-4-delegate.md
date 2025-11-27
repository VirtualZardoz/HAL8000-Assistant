---
name: command-name
description: Brief description for command palette (Level 4 - sub-agent delegation)
parameters:
  - name: param1
    description: Parameter description
    type: string
    required: true
---

# [Command Name]

**Command Type:** [System | Development | Documentation | Application]
**Category:** [system/ | development/ | documentation/ | custom/]
**Level:** 4 - Delegate Prompt
**Created:** [YYYY-MM-DD]
**Version:** 1.0

---

## Purpose

[What this command does - involves delegating work to sub-agents]

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
- `delegation_params` - [Type] - [Passed to sub-agent]

**Output Variables:**
- `result_name` - [Type] - [What sub-agent returns]

---

## Instructions

**Orchestration Logic:**

1. **[Preparation Phase]**: [Setup before delegation]
   - [Prepare parameters]
   - [Validate inputs]

2. **[Delegation Phase]**: [Invoke sub-agent]
   - [See Delegation Patterns section below]

3. **[Processing Phase]**: [Handle sub-agent results]
   - [Extract relevant data]
   - [Transform or integrate]

4. **[Finalization]**: [Complete and return]
   - [Format output]
   - [Return to user]

---

## Delegation Patterns

**Sub-Agent:** [agent-name]

**When to delegate:**
- [Condition or scenario]

**Task description for agent:**
```markdown
Launch [agent-name] sub-agent with task:
  "[Specific instructions for the sub-agent]"

The sub-agent will:
- [What it does with its isolated 200K context]
- [What data it processes]
- [What it returns (<5K tokens clean summary)]

Wait for sub-agent completion.
Process returned results: [how to use output]
```

**Benefits:**
- RAM efficiency: Agent uses isolated context (60-85% token savings)
- Specialization: Agent optimized for [specific task type]
- Quality: Agent has [specific capabilities]

---

## Output Format

**What user sees:**
```
[Example output including sub-agent results]
```

---

## Error Handling

**Sub-agent failures:**
- If agent returns error: [What to do]
- If agent times out: [Fallback]
- If results invalid: [Recovery]

**Other errors:**
- [Error type]: [Detection and response]

---

## Dependencies

**Required Agents:**
- `agent-name` - [Located at .claude/agents/agent-name.md]

---

## Metadata

**Version History:**
- v1.0 (YYYY-MM-DD) - Initial implementation

**Status:** [Draft | Testing | Production]
**Template Level:** 4 - Delegate (sub-agent orchestration)
