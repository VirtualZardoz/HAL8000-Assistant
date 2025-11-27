---
title: [Component/System Name] Architecture
date: [YYYY-MM-DD]
type: architecture
version: [X.Y.Z]
status: draft | active | deprecated
tags: [architecture, component-name, system-area]
---

# [Component/System Name] Architecture

## Overview

### Purpose

[What is this component/system? Why does it exist?]

### Scope

**In Scope:**
- [What this covers]

**Out of Scope:**
- [What this doesn't cover]

### Key Concepts

- **[Concept 1]:** [Brief definition]
- **[Concept 2]:** [Brief definition]
- **[Concept 3]:** [Brief definition]

## Architecture Principles Applied

### Von Neumann Architecture

[How does this component/system apply Modified von Neumann principles?]

- [Principle 1] - [How it's applied]
- [Principle 2] - [How it's applied]

### Unix Philosophy

[How does this component/system follow Unix philosophy?]

- [Principle 1] - [How it's applied]
- [Principle 2] - [How it's applied]

### Assembly Principles

[How does this component/system apply assembly concepts?]

- [Principle 1] - [How it's applied]
- [Principle 2] - [How it's applied]

## System Components

### Component Diagram

```
[ASCII art or description of component relationships]

Or reference: [diagram-file.png](path/to/diagram.png)
```

### Component Catalog

#### Component 1: [Name]

- **Location:** [File path or directory]
- **Purpose:** [What it does]
- **Responsibility:** [Single responsibility]
- **Interfaces:** [How it's accessed]
- **Dependencies:** [What it depends on]

#### Component 2: [Name]

[Repeat structure]

## Design Rationale

### Why This Design

[Explain the architectural decisions]

**Key Decisions:**
1. **[Decision 1]:** [Why this approach was chosen]
2. **[Decision 2]:** [Why this approach was chosen]

### Alternatives Considered

| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| [Option 1] | [Pros] | [Cons] | [Reason] |
| [Option 2] | [Pros] | [Cons] | [Reason] |

### Trade-offs

**Performance vs. [X]:**
- [Description of trade-off]
- [Decision made]

**Simplicity vs. [Y]:**
- [Description of trade-off]
- [Decision made]

## Integration Points

### With Commands

[How does this integrate with HAL-Script commands?]

- `[command-name]` - [Integration mechanism]

### With Agents

[How does this integrate with sub-agents?]

- `[agent-name]` - [Integration mechanism]

### With Skills

[How does this integrate with Skills?]

- `[skill-name]` - [Integration mechanism]

### With External Systems

[How does this integrate with external tools/systems?]

- `[system-name]` - [Integration mechanism]

## Data Flow

### Input Data

| Data | Source | Format | Validation |
|------|--------|--------|------------|
| [Data 1] | [Where from] | [Format] | [How validated] |
| [Data 2] | [Where from] | [Format] | [How validated] |

### Processing

```
[Describe data transformation]

Input → [Step 1] → [Step 2] → [Step 3] → Output
```

### Output Data

| Data | Destination | Format | Usage |
|------|-------------|--------|-------|
| [Data 1] | [Where to] | [Format] | [How used] |
| [Data 2] | [Where to] | [Format] | [How used] |

## File System Organization

```
[Directory structure]

component-root/
├── subdir1/
│   └── file1.md
├── subdir2/
│   └── file2.py
└── README.md
```

**Depth:** [X levels] (complies with 3-level limit)

**Naming Conventions:**
- [Convention 1]
- [Convention 2]

## State Management

### Volatile State (RAM)

[What state is kept in context/RAM?]

- [State item 1] - [Why volatile]
- [State item 2] - [Why volatile]

### Persistent State (File System)

[What state is persisted to files?]

- [State item 1] - [Location, format]
- [State item 2] - [Location, format]

### State Transitions

[How does state change?]

```
State A → [Event] → State B → [Event] → State C
```

## Error Handling

### Error Categories

| Category | Severity | Handling Strategy |
|----------|----------|-------------------|
| [Error type 1] | [Critical/High/Low] | [How handled] |
| [Error type 2] | [Critical/High/Low] | [How handled] |

### Recovery Mechanisms

- **[Error scenario 1]:** [Recovery approach]
- **[Error scenario 2]:** [Recovery approach]

## Performance Characteristics

### Resource Usage

- **RAM Impact:** [Token cost, memory footprint]
- **Processing Time:** [Expected execution time]
- **File I/O:** [Read/write operations]

### Scalability

[How does this scale? What are the limits?]

### Optimization Strategies

- [Strategy 1]
- [Strategy 2]

## Security & Safety

### Access Control

[Who/what can access this component?]

### Tool Permissions

[Which tools are allowed? Why?]

```yaml
allowed-tools:
  - Read
  - Write
  - [etc.]
```

### Safety Mechanisms

- [Safety mechanism 1]
- [Safety mechanism 2]

## Testing & Validation

### Test Strategy

[How is this component tested?]

### Validation Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Known Limitations

- [Limitation 1]
- [Limitation 2]

## Future Considerations

### Potential Enhancements

- [Enhancement 1] - [Priority: High/Medium/Low]
- [Enhancement 2] - [Priority: High/Medium/Low]

### Known Issues

- [Issue 1] - [Impact, workaround]
- [Issue 2] - [Impact, workaround]

### Evolution Path

[How might this architecture evolve?]

## Related Documentation

- [Architecture doc 1](path/to/doc.md)
- [Design decision 1](path/to/decision.md)
- [Component spec 1](path/to/spec.md)

## References

- [Research doc 1](path/to/research.md)
- [External reference 1](url)
- [Standard/principle](reference)

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | YYYY-MM-DD | Initial architecture | [Author] |
| 1.1.0 | YYYY-MM-DD | Added [feature] | [Author] |

---

**Architecture Status:** [Active / Deprecated]
**Last Reviewed:** [YYYY-MM-DD]
**Next Review:** [YYYY-MM-DD or trigger event]
