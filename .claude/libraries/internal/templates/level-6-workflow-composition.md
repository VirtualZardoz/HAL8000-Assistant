---
name: command-name
description: Brief description for command palette (Level 6 - command composition)
parameters:
  - name: param1
    description: Parameter description
    type: string
    required: true
---

# [Command Name]

**Command Type:** [System | Development | Documentation | Application]
**Category:** [system/ | development/ | documentation/ | custom/]
**Level:** 6 - Workflow Composition Prompt
**Created:** [YYYY-MM-DD]
**Version:** 1.0

---

## Purpose

[What this application-level workflow does - composes multiple commands and agents]

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

**Configuration:**
- `workflow_mode` - [Options] - [Controls execution path]

**Output Variables:**
- `workflow_results` - [Type] - [End-to-end results]

---

## Instructions

**End-to-End Workflow Orchestration:**

### Phase 1: [Preparation]
[Setup and validation]

### Phase 2: [Command A Execution]
Execute: `/command-A [params]`
- [What command A does]
- [What it produces]
- [Hand-off to next phase]

### Phase 3: [Agent Delegation]
Launch: [agent-name] sub-agent
- [What agent processes]
- [What agent returns]
- [Integration with workflow]

### Phase 4: [Command B Execution]
Execute: `/command-B [params from A and agent]`
- [What command B does]
- [How it uses previous results]
- [What it produces]

### Phase 5: [Finalization]
Execute: `/command-C [final params]`
- [Final processing]
- [Output generation]
- [State updates]

---

## Delegation Patterns

**Agents used in workflow:**

**Agent: [agent-name]**
- **When:** [At which phase]
- **Task:** [What it does]
- **Output:** [What it returns]

---

## Workflow Integration

**Command composition:**

```
/command-A "prepare"
    ↓ [produces dataset]
agent-X "process dataset"
    ↓ [returns analysis]
/command-B "refine" [using analysis]
    ↓ [produces output]
/command-C "finalize" [using output]
    ↓ [complete]
```

**Data flow:**
- Command A → Agent X: [data type]
- Agent X → Command B: [data type]
- Command B → Command C: [data type]

**Error propagation:**
- If any step fails: [abort or continue?]
- Rollback strategy: [if applicable]

---

## Output Format

**Final workflow output:**
```
[Application Name] - Complete

Phase 1: [Status] ✓
  - [Results summary]

Phase 2: [Status] ✓
  - [Results summary]

Phase 3: [Status] ✓
  - [Results summary]

Final Results:
  - [Key outcome 1]
  - [Key outcome 2]

[Detailed output or file references]
```

---

## Error Handling

**Phase-level error handling:**

**Phase 1 failure:**
- Detection: [How to know it failed]
- Action: [Abort or retry]
- Recovery: [What to do]

**Phase 2 failure:**
- Detection: [How to know it failed]
- Action: [Can continue without it?]
- Recovery: [What to do]

**Workflow-level validation:**
- Before each phase: [Validate preconditions]
- After each phase: [Verify postconditions]
- At end: [Complete workflow validation]

---

## Examples

### Example 1: Complete Workflow
**Scenario:** [End-to-end use case]

**Execution:**
```bash
/command-name "full-workflow"
```

**What happens:**
1. [Phase 1 details]
2. [Phase 2 details]
3. [Phase 3 details]
4. [Final outcome]

---

## Dependencies

**Required Commands:**
- `/command-A` - [Purpose in workflow]
- `/command-B` - [Purpose in workflow]
- `/command-C` - [Purpose in workflow]

**Required Agents:**
- `agent-name` - [Purpose in workflow]

---

## Performance Considerations

**RAM Usage:**
- Workflow accumulates context across phases
- Consider checkpointing between major phases
- Estimated peak RAM: [%]

**Execution Time:**
- Full workflow: [estimated duration]
- Can be broken into parts if needed

---

## Metadata

**Version History:**
- v1.0 (YYYY-MM-DD) - Initial implementation

**Status:** [Draft | Testing | Production]
**Template Level:** 6 - Workflow Composition (end-to-end application)
