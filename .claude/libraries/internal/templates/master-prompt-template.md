---
name: command-name
description: Brief description of what this command does (one sentence for command palette)
parameters:
  - name: argument1
    description: Description of what this parameter does
    type: string
    required: true
  - name: argument2
    description: Optional parameter description
    type: string
    required: false
---

# [Command Name]

**Command Type:** [System | Development | Documentation | Application]
**Category:** [system/ | development/ | documentation/ | custom/]
**Created:** [YYYY-MM-DD]
**Version:** 1.0

---

## Purpose

[Single sentence describing what this command does and why it exists]

[Optional: 1-2 paragraphs providing context, use cases, and value proposition]

---

## Usage

```bash
/command-name [arguments]
```

**Parameters:**
- `argument1` - [Description of what this parameter does]
- `argument2` - [Optional: Description, default value]

**Examples:**
```bash
/command-name "simple example"
/command-name --option "value" "complex example"
```

---

## Variables/Parameters

**Input Variables** (data passed to this command):
- `variable_name` - [Type: string/number/boolean] - [Purpose and constraints]
- `another_variable` - [Type] - [Description]

**Configuration** (settings that affect behavior):
- `setting_name` - [Default value] - [What it controls]
- `option_name` - [Values: A|B|C] - [Impact of each choice]

**Output Variables** (data returned or produced):
- `result_name` - [Type] - [What gets returned]
- `status_code` - [Type] - [Success/failure indicators]

**Example Variable Usage:**
```markdown
Input: search_path = "/mnt/d/~HAL8000/data/"
Config: recursive = true, depth_limit = 3
Output: file_list = [array of matching files]
```

---

## Instructions

**Core Logic** (the main work this command performs):

[Step-by-step description of what happens when this command executes]

1. **[Phase Name]**: [What happens in this phase]
   - [Specific action or operation]
   - [Specific action or operation]
   - [Expected outcome]

2. **[Next Phase]**: [What happens next]
   - [Specific action or operation]
   - [Conditions or branches]
   - [Expected outcome]

3. **[Final Phase]**: [Completion and output]
   - [What gets produced]
   - [What gets returned to user]
   - [State changes or side effects]

**Execution Flow:**
```
Start
  ↓
[Validate inputs]
  ↓
[Process data] → [Handle errors?] → [Retry or abort]
  ↓
[Generate output]
  ↓
[Return results]
  ↓
End
```

---

## Delegation Patterns

**Sub-Agent Invocation** (when this command delegates work):

**When to delegate:**
- [Condition or scenario requiring delegation]
- [Another scenario]

**Which agent to use:**
- **[agent-name]** - Use when: [specific criteria]
- **[another-agent]** - Use when: [different criteria]

**Delegation structure:**
```markdown
Launch [agent-name] sub-agent with task:
  "[Specific instructions for the sub-agent]"

The sub-agent will:
- [What it does with isolated 200K context]
- [What data it processes]
- [What it returns (clean summary, <5K tokens)]

Wait for sub-agent completion.
Process returned results: [how to use agent output]
```

**Agent coordination** (multiple agents):
```markdown
Parallel delegation:
1. Launch agent-A for task-X
2. Launch agent-B for task-Y
3. Wait for both completions
4. Combine results from both agents
5. Proceed with integrated data
```

**Benefits of delegation:**
- RAM efficiency: Agent uses isolated context (60-85% token savings)
- Specialization: Agent optimized for specific task
- Parallelism: Multiple agents work concurrently

---

## Workflow Integration

**How this command fits into larger workflows:**

**Prerequisites** (what should happen before this command):
- [Command or state that should exist first]
- [Data or files that need to be ready]

**Dependents** (what typically happens after this command):
- [Command that uses this command's output]
- [Next step in workflow]

**Common Patterns:**

**Pattern 1: Sequential Workflow**
```bash
/command-A "prepare data"
/command-B "process data"    # <-- This command
/command-C "finalize output"
```

**Pattern 2: Conditional Workflow**
```bash
/command-check-status
# If status is X:
  /this-command "action-A"
# If status is Y:
  /different-command "action-B"
```

**Pattern 3: Composition with Other Commands**
```markdown
This command can be composed with:
- /command-X - [How they work together]
- /command-Y - [Integration pattern]
- /command-Z - [Data flow between them]
```

**Workflow diagram:**
```
[Previous Command]
        ↓
   [This Command] ←→ [Optional: Parallel Command]
        ↓
[Next Command]
```

---

## Output Format

**Output Structure** (what this command returns):

**Terminal Output** (what user sees):
```
[Command Name] Results
────────────────────────
Status: [Success/Warning/Error]
Items processed: [N]
Time elapsed: [X seconds]

[Main output content here]
  - Item 1
  - Item 2
  - Item 3

Summary: [Brief description of results]
```

**File Output** (if command creates files):
- **File path:** `/path/to/output/file.md`
- **Format:** [Markdown | JSON | Plain text]
- **Structure:**
  ```
  [Example of file contents]
  ```

**Return Values** (for programmatic use):
- **Success:** `{ status: "success", data: [...] }`
- **Failure:** `{ status: "error", error_code: "...", message: "..." }`

**Output Examples:**

**Example 1: Success case**
```
[Show what successful output looks like]
```

**Example 2: Partial success (warnings)**
```
[Show output with warnings]
```

**Example 3: Failure case**
```
[Show error output]
```

---

## Error Handling

**Error Detection:**
- [Error type 1] - How to detect it
- [Error type 2] - Symptoms or indicators
- [Error type 3] - When it occurs

**Error Responses:**

**Error Type: [Specific Error]**
- **Detection:** [How to identify this error]
- **Action:** [What the command does when this happens]
- **User message:** `"[Exact error message shown to user]"`
- **Recovery:** [Automatic recovery steps, if any]
- **User action:** [What user should do to fix]

**Error Type: [Another Error]**
- **Detection:** [...]
- **Action:** [...]
- **User message:** `"[...]"`
- **Recovery:** [...]
- **User action:** [...]

**Graceful Degradation:**
```markdown
If critical error:
  - Report specific error details
  - Suggest recovery action
  - Abort operation (no partial state)

If non-critical error:
  - Warn user about issue
  - Continue with degraded functionality
  - Log issue for later review
```

**Validation Patterns:**
```markdown
Before execution:
1. Validate all input parameters
2. Check preconditions (files exist, RAM available, etc.)
3. If validation fails: report specific issue, abort early

After execution:
1. Verify postconditions (output produced, state correct)
2. If verification fails: rollback if possible, report error
3. Confirm successful completion
```

---

## Examples

### Example 1: Basic Usage
**Scenario:** [Simple, common use case]

**Command:**
```bash
/command-name "basic input"
```

**What happens:**
1. [Step-by-step description]
2. [What the command does]
3. [What output is produced]

**Output:**
```
[Show the actual output]
```

---

### Example 2: Advanced Usage
**Scenario:** [Complex use case with options]

**Command:**
```bash
/command-name --option "value" --flag "advanced input"
```

**What happens:**
1. [Step-by-step description]
2. [How options change behavior]
3. [What output is produced]

**Output:**
```
[Show the actual output]
```

---

### Example 3: Integration with Workflow
**Scenario:** [This command as part of larger workflow]

**Workflow:**
```bash
# Step 1: Preparation
/command-A "prepare"

# Step 2: This command
/command-name "process"

# Step 3: Finalization
/command-C "finalize"
```

**What happens:**
1. [How commands work together]
2. [Data flow between commands]
3. [Final outcome]

---

## Dependencies

**Required Files:**
- `path/to/file.md` - [Why this is needed]
- `path/to/config.json` - [What this provides]

**Required Commands:**
- `/other-command` - [When this is needed]

**Required Agents:**
- `agent-name` - [When agent is invoked]

**Required Tools:**
- Bash, Read, Write - [Which tools are used]
- MCP servers: [omnisearch, filesystem, etc.]

**System Requirements:**
- RAM: [Minimum tokens needed]
- State: [Required state.json fields]
- Phase: [production-ready, development, etc.]

---

## Performance Considerations

**RAM Usage:**
- Estimated token cost: [~XK tokens]
- RAM zone impact: [SAFE→SAFE | SAFE→CAUTION | etc.]
- Mitigation: [If high usage, how to optimize]

**Execution Time:**
- Typical duration: [seconds | minutes]
- Long-running: [If yes, progress indicators?]
- Optimization: [How to make faster]

**Resource Efficiency:**
- Sub-agent usage: [If delegating, token savings]
- Parallel operations: [If using parallelism]
- Caching: [If results cached]

---

## Testing & Validation

**Test Cases:**

**Test 1: Happy path**
- Input: [Test input]
- Expected output: [What should happen]
- Validation: [How to verify success]

**Test 2: Edge case**
- Input: [Edge case input]
- Expected output: [How it should handle]
- Validation: [How to verify]

**Test 3: Error case**
- Input: [Invalid input]
- Expected output: [Error message]
- Validation: [Proper error handling]

**Validation Checklist:**
- [ ] Input validation working
- [ ] Core logic executes correctly
- [ ] Output format correct
- [ ] Error handling robust
- [ ] Integration with other commands works
- [ ] Documentation accurate

---

## Notes

**Design Decisions:**
- [Why this approach was chosen]
- [Alternatives considered and rejected]
- [Trade-offs made]

**Known Limitations:**
- [Limitation 1 and why it exists]
- [Limitation 2 and potential workaround]

**Future Enhancements:**
- [Potential improvement 1]
- [Potential improvement 2]

**Related Documentation:**
- `path/to/related/doc.md` - [Relevance]
- `path/to/architecture/spec.md` - [Context]

---

## Metadata

**Version History:**
- v1.0 (YYYY-MM-DD) - Initial implementation

**Maintainer:** [Your name or "System"]
**Last Updated:** [YYYY-MM-DD]
**Status:** [Draft | Testing | Production | Deprecated]

**Integration Points:**
- BIOS: [If referenced in CLAUDE.md]
- State: [If tracked in state.json]
- Index: [If cataloged in indexes]

---

**Template Version:** 1.0
**Template Type:** Master (all possible sections)
**Usage:** Copy and remove unused sections for your specific command
