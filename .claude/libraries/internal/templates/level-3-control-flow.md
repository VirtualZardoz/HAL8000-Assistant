---
name: command-name
description: Brief description for command palette (Level 3 - conditional logic/loops)
parameters:
  - name: param1
    description: Parameter description
    type: string
    required: true
---

# [Command Name]

**Command Type:** [System | Development | Documentation | Application]
**Category:** [system/ | development/ | documentation/ | custom/]
**Level:** 3 - Control Flow Prompt
**Created:** [YYYY-MM-DD]
**Version:** 1.0

---

## Purpose

[What this command does - includes conditional logic or loops]

---

## Usage

```bash
/command-name [arguments]
```

**Parameters:**
- `argument1` - [Description]
- `argument2` - [Optional: Description]

---

## Variables/Parameters

**Input Variables:**
- `variable_name` - [Type] - [Purpose]
- `condition_var` - [Type] - [Controls branching]

**Configuration:**
- `setting_name` - [Default] - [What it controls]

**Output Variables:**
- `result_name` - [Type] - [What gets returned]

---

## Instructions

**Workflow with Control Flow:**

1. **[Initial Phase]**: [Setup]
   - [Action]

2. **[Conditional Branch]**:
   - If [condition A]:
     - [Action for A]
   - Else if [condition B]:
     - [Action for B]
   - Else:
     - [Default action]

3. **[Loop Phase]** (if applicable):
   - For each [item] in [collection]:
     - [Process item]
     - [Check condition]
     - [Continue or break]

4. **[Finalization]**: [Complete]
   - [Final action]
   - [Return results]

---

## Output Format

**What user sees:**
```
[Example output with different outcomes based on conditions]
```

---

## Error Handling

**Error Type: [Specific Error]**
- **Detection:** [How to identify]
- **Action:** [What command does]
- **User message:** `"[Error message]"`
- **Recovery:** [How to handle]

---

## Metadata

**Version History:**
- v1.0 (YYYY-MM-DD) - Initial implementation

**Status:** [Draft | Testing | Production]
**Template Level:** 3 - Control Flow (conditionals and loops)
