---
title: [Feature Name]
date: [YYYY-MM-DD]
type: feature-doc
version: [X.Y.Z]
status: planned | in-development | completed | deprecated
tags: [feature, component, area]
---

# Feature: [Feature Name]

## Overview

### What It Is

[One-paragraph description of the feature]

### Why It Exists

[The problem this feature solves or value it provides]

### Status

- **Current Status:** [planned | in-development | completed | deprecated]
- **Version Introduced:** [X.Y.Z]
- **Version Completed:** [X.Y.Z] (if completed)

## Use Cases

### Primary Use Case

**Scenario:** [Describe the main use case]

**User Goal:** [What the user wants to accomplish]

**How Feature Helps:** [How this feature enables the goal]

### Secondary Use Cases

1. **[Use case 2]:** [Description]
2. **[Use case 3]:** [Description]

### Anti-Use Cases

**Not intended for:**
- [What this feature should NOT be used for]
- [Scenarios where alternative approach is better]

## User Guide

### How to Use

**Step 1:** [First step]
```bash
# Example command or code
```

**Step 2:** [Second step]
```bash
# Example command or code
```

**Step 3:** [Third step]
```bash
# Example command or code
```

### Quick Start Example

```language
# Complete minimal example showing the feature in action
```

**Expected Output:**
```
[What you should see]
```

### Advanced Usage

#### Feature Option 1

[Description of advanced option]

```language
# Example code
```

#### Feature Option 2

[Description of another advanced option]

```language
# Example code
```

## Implementation Details

### Architecture

[How is this feature implemented? High-level architecture]

**Components involved:**
- [Component 1] - [Role]
- [Component 2] - [Role]

### File Locations

```
[Directory structure for this feature]

feature-root/
├── component1.md
├── component2.py
└── tests/
    └── test_feature.py
```

### Dependencies

**Internal Dependencies:**
- [Component/module 1]
- [Component/module 2]

**External Dependencies:**
- [Library/tool 1] (version)
- [Library/tool 2] (version)

### Configuration

[Any configuration required for this feature]

```yaml
# Example configuration
feature_enabled: true
feature_option: value
```

## API / Interface Documentation

### Commands

#### Command: `/feature-command`

**Description:** [What this command does]

**Arguments:**
- `arg1` (required) - [Description]
- `arg2` (optional, default: `value`) - [Description]

**Usage:**
```bash
/feature-command arg1 [arg2]
```

**Example:**
```bash
/feature-command "example value"
```

**Returns:**
```
[Expected output format]
```

### Functions / Methods

#### Function: `featureFunction(param1, param2)`

**Description:** [What this function does]

**Parameters:**
- `param1` (type) - [Description]
- `param2` (type, optional) - [Description]

**Returns:** `type` - [Description of return value]

**Example:**
```language
result = featureFunction("value1", "value2")
```

**Exceptions:**
- `ErrorType` - [When this error occurs]

## Examples

### Example 1: [Common Scenario]

**Goal:** [What we're trying to accomplish]

**Code:**
```language
# Complete working example
```

**Explanation:**
[Step-by-step explanation of what's happening]

**Output:**
```
[Expected output]
```

### Example 2: [Another Scenario]

[Repeat structure]

### Example 3: [Edge Case]

[Repeat structure]

## Integration

### With Existing Features

**Integrates with [Feature A]:**
[How they work together]

**Integrates with [Feature B]:**
[How they work together]

### With External Tools

**Works with [Tool 1]:**
[Integration details]

## Performance

### Resource Usage

- **RAM Impact:** [Token cost, memory usage]
- **Processing Time:** [Expected execution time]
- **File I/O:** [Read/write operations]

### Performance Tips

- [Tip 1 for optimal performance]
- [Tip 2 for optimal performance]

### Benchmarks

| Operation | Time | Memory |
|-----------|------|--------|
| [Operation 1] | [Xms] | [Xkb] |
| [Operation 2] | [Xms] | [Xkb] |

## Testing

### How to Test

**Manual Testing:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Automated Testing:**
```bash
# Command to run tests
```

### Test Cases

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| [Case 1] | [Input] | [Output] | ✅ Pass |
| [Case 2] | [Input] | [Output] | ✅ Pass |

### Known Issues

- [Issue 1] - [Workaround or status]
- [Issue 2] - [Workaround or status]

## Troubleshooting

### Common Problems

#### Problem: [Error message or symptom]

**Cause:** [Why this happens]

**Solution:**
```bash
# Commands or steps to fix
```

#### Problem: [Another issue]

[Repeat structure]

### Debug Mode

[How to enable debug/verbose output for this feature]

```bash
# Example debug command
```

## Migration Guide

### From Previous Version

**Breaking Changes:**
- [Change 1] - [How to adapt]
- [Change 2] - [How to adapt]

**Deprecated Features:**
- [Old feature] → Use [new feature] instead

**Migration Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

### From Alternative Approach

**If you were using [old approach]:**

Before:
```language
# Old code
```

After:
```language
# New code using this feature
```

## Best Practices

### Do's

✅ [Best practice 1]
✅ [Best practice 2]
✅ [Best practice 3]

### Don'ts

❌ [Anti-pattern 1]
❌ [Anti-pattern 2]
❌ [Anti-pattern 3]

### Patterns

**Pattern: [Name]**

When to use: [Scenario]

Implementation:
```language
# Example code
```

## Security & Safety

### Security Considerations

- [Security consideration 1]
- [Security consideration 2]

### Safety Mechanisms

- [Safety mechanism 1]
- [Safety mechanism 2]

### Permissions Required

[What permissions/tools are needed]

## Future Enhancements

### Planned Improvements

- [ ] [Enhancement 1] - [Target version]
- [ ] [Enhancement 2] - [Target version]

### Ideas Under Consideration

- [Idea 1]
- [Idea 2]

## Related Documentation

- [Related feature 1](path/to/doc.md)
- [Architecture doc](path/to/architecture.md)
- [API reference](path/to/api.md)

## References

- [Specification](url)
- [Original proposal](path/to/proposal.md)
- [External documentation](url)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
| 1.1.0 | YYYY-MM-DD | Added [feature] |
| 1.2.0 | YYYY-MM-DD | Fixed [issue], improved [aspect] |

---

**Feedback:** [How to provide feedback on this feature]
**Support:** [Where to get help]
