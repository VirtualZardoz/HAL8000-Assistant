---
name: command-name
description: Brief description for command palette (Level 7 - production-critical system)
parameters:
  - name: param1
    description: Parameter description
    type: string
    required: false
---

# [Command Name]

**Command Type:** System
**Category:** system/
**Level:** 7 - System Prompt (Production-Critical)
**Created:** [YYYY-MM-DD]
**Version:** 1.0

---

## Purpose

[What this core system command does - production-critical functionality]

[Detailed context about why this is essential to system operation]

---

## Usage

```bash
/command-name [arguments]
```

**Parameters:**
- `argument1` - [Detailed description with constraints]
- `argument2` - [Optional: Description, default, validation rules]

**Examples:**
```bash
/command-name "simple case"
/command-name --advanced "complex case"
```

---

## Variables/Parameters

**Input Variables:**
- `variable_name` - [Type: specific] - [Purpose, constraints, validation]

**Configuration:**
- `setting_name` - [Default: X] - [What it controls, impact]

**Output Variables:**
- `result_name` - [Type] - [What gets returned, format]

---

## Instructions

**Core System Logic:**

### Phase 1: [Initialization]
**Purpose:** [Why this phase exists]

1. [Step 1]: [Detailed action]
   - Validation: [What gets checked]
   - Error check: [What happens if invalid]

2. [Step 2]: [Next action]
   - Logic: [Why this is done]
   - State change: [What gets modified]

### Phase 2: [Processing]
**Purpose:** [Why this phase exists]

[Detailed step-by-step logic with rationale]

### Phase 3: [Verification]
**Purpose:** [Ensure correctness]

[Postcondition checks and validation]

### Phase 4: [Finalization]
**Purpose:** [Complete operation]

[Final steps and cleanup]

---

## Delegation Patterns

**If applicable:** [Sub-agent usage]

**Agent:** [agent-name]
**Task:** [Detailed delegation logic]

---

## Workflow Integration

**Prerequisites:**
- [What must exist before running]
- [Required state]

**Dependents:**
- [What relies on this command]
- [Integration points]

**Common Patterns:**
[Show how this integrates into workflows]

---

## Output Format

**Terminal Output:**
```
[Detailed output specification with all variations]
```

**File Output:**
- Path: [specific path]
- Format: [exact format]
- Structure: [detailed schema]

**Return Values:**
- Success: [exact format]
- Failure: [exact format with error codes]

---

## Error Handling

**Comprehensive error coverage:**

### Error Type 1: [Name]
- **Detection:** [How identified]
- **Action:** [System response]
- **User message:** `"[Exact message]"`
- **Recovery:** [Automatic steps]
- **User action:** [What user should do]
- **Impact:** [Severity and consequences]

### Error Type 2: [Name]
[Same detailed structure]

### Validation Strategy:
**Pre-execution:**
- [Check 1]
- [Check 2]

**During execution:**
- [Monitor 1]
- [Monitor 2]

**Post-execution:**
- [Verify 1]
- [Verify 2]

---

## Examples

### Example 1: Standard Usage
[Detailed example with context]

### Example 2: Edge Case
[Complex scenario]

### Example 3: Integration Pattern
[How it works in larger workflow]

---

## Dependencies

**Required Files:**
- `path/to/file` - [Detailed why needed]

**Required Commands:**
- `/other-command` - [Integration point]

**Required Agents:**
- `agent-name` - [When invoked]

**System Requirements:**
- RAM: [Minimum, typical, maximum]
- State: [Required state.json fields]
- Phase: [System phase requirements]

---

## Performance Considerations

**RAM Usage:**
- Estimated cost: [~XK tokens]
- Peak usage: [highest point]
- RAM zone impact: [transition details]
- Optimization: [How to reduce if needed]

**Execution Time:**
- Typical: [duration]
- Worst case: [duration]
- Factors affecting: [what impacts speed]

**Resource Efficiency:**
- [Any delegation or parallelism]
- [Caching strategies]
- [Optimization techniques]

---

## Testing & Validation

**Test Suite:**

### Test 1: Happy Path
- Input: [specific test input]
- Expected: [exact expected output]
- Validation: [how to verify]

### Test 2: Edge Case
- Input: [edge case]
- Expected: [how handled]
- Validation: [verification]

### Test 3: Error Case
- Input: [invalid input]
- Expected: [error response]
- Validation: [error handling check]

### Test 4: Integration
- Setup: [prerequisite state]
- Execution: [in workflow context]
- Validation: [end-to-end verification]

**Validation Checklist:**
- [ ] Input validation working
- [ ] Core logic correct
- [ ] Output format exact
- [ ] Error handling comprehensive
- [ ] Integration verified
- [ ] Performance acceptable
- [ ] Documentation accurate

---

## Notes

**Design Decisions:**
- [Why this architecture]
- [Alternatives considered]
- [Trade-offs made]
- [Future considerations]

**Known Limitations:**
- [Limitation 1 and rationale]
- [Limitation 2 and workaround]

**Future Enhancements:**
- [Potential improvement 1]
- [Potential improvement 2]

**Security Considerations:**
- [Any security-relevant aspects]

**Maintenance:**
- [Regular maintenance needs]
- [What to check periodically]

---

## Related Documentation

- `data/architecture/[relevant-spec].md` - [Purpose]
- `.claude/commands/[related-command].md` - [Connection]
- `CLAUDE.md` - [BIOS integration]

---

## Metadata

**Version History:**
- v1.0 (YYYY-MM-DD) - Initial implementation
  - [Key features]
  - [Rationale]

**Maintainer:** [Name]
**Last Updated:** [YYYY-MM-DD]
**Status:** Production
**Criticality:** High (core system functionality)

**Integration Points:**
- BIOS: [If referenced in CLAUDE.md]
- State: [If tracked in state.json]
- Index: [If cataloged]

**Audit Trail:**
- Created: [session file reference]
- Modified: [session file references]
- Validated: [test session references]

---

**Template Version:** 1.0
**Template Level:** 7 - System (production-critical, comprehensive documentation)
**Usage:** Use for core infrastructure commands requiring highest reliability
