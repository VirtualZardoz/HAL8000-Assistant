---
name: Documentation Generator
description: Generate professional documentation for sessions, decisions, architecture, and code. Use when user asks to "document this", "create docs", "write up", after completing major work, or when explicit documentation is needed. Activate on requests for session summaries, decision logs, architecture docs, or README files.
allowed-tools: Read, Write, Glob
---

# Documentation Generator

This Skill generates structured documentation for HAL8000 work sessions, architectural decisions, and system components.

## Purpose

Create consistent, well-formatted documentation that captures decisions, context, and outcomes for future reference and team collaboration.

## When to Activate

**Explicit Triggers:**
- User says: "document this", "create docs", "write this up"
- User requests: "session summary", "decision log", "architecture doc"
- User asks: "can you document..." or "write documentation for..."

**Implicit Triggers:**
- Major milestone completed (new feature, system change)
- Complex decision made requiring rationale capture
- Research completed needing synthesis
- Architecture changes requiring documentation

**Do NOT activate for:**
- Code comments (use inline commenting instead)
- Minor edits or trivial changes
- Temporary notes (unless user specifically requests)

## Documentation Types

### 1. Session Documentation
**Purpose:** Capture work session for continuity
**Location:** `data/sessions/summaries/`
**Template:** `templates/session-doc-template.md`

**Contains:**
- Session metadata (date, duration, participants)
- Objectives
- Work performed
- Decisions made
- Outcomes/deliverables
- Next actions

### 2. Decision Logs
**Purpose:** Record architectural/design decisions with rationale
**Location:** `data/architecture/decisions/`
**Template:** `templates/decision-log-template.md`

**Contains:**
- Decision title and date
- Context/background
- Options considered
- Decision made
- Rationale
- Consequences
- Status (proposed, accepted, deprecated, superseded)

### 3. Architecture Documentation
**Purpose:** Document system design and structure
**Location:** `data/architecture/`
**Template:** `templates/architecture-doc-template.md`

**Contains:**
- Component overview
- Architecture principles applied
- Design rationale
- Integration points
- Trade-offs
- Diagrams (if applicable)

### 4. Feature Documentation
**Purpose:** Document new features or significant changes
**Location:** `data/projects/[project-name]/`
**Template:** `templates/feature-doc-template.md`

**Contains:**
- Feature description
- Use cases
- Implementation details
- API/interface documentation
- Examples
- Testing notes

### 5. README Files
**Purpose:** Project/component overviews
**Location:** Project/component root directories
**Template:** `templates/readme-template.md`

**Contains:**
- What it is
- Why it exists
- How to use it
- Examples
- Related components

## Documentation Workflow

### Step 1: Determine Documentation Type

Ask user (or infer from context):
- What kind of documentation needed?
- Where should it be stored?
- What level of detail required?

### Step 2: Gather Context

**For Session Docs:**
- Review current session context
- Identify key accomplishments
- Note decisions made
- List deliverables

**For Decision Logs:**
- Understand the decision
- Identify options considered
- Capture rationale
- Note consequences

**For Architecture Docs:**
- Load relevant system files
- Understand component structure
- Identify principles applied
- Note integration points

**For Feature Docs:**
- Review implementation
- Identify use cases
- Document API/interface
- Create examples

### Step 3: Select and Populate Template

1. Choose appropriate template from `templates/`
2. Copy template structure
3. Fill in sections with gathered context
4. Remove inapplicable sections (keep only relevant parts)
5. Format for readability

### Step 4: Generate Documentation

1. Create file in appropriate location
2. Use descriptive filename:
   - Session: `YYYY-MM-DD-HHMM-brief-description.md`
   - Decision: `YYYY-MM-DD-decision-title.md`
   - Architecture: `component-name-architecture.md`
   - Feature: `feature-name.md`
   - README: `README.md`
3. Write content using template structure
4. Ensure markdown formatting is correct

### Step 5: Validate and Report

1. Check documentation completeness
2. Verify all template sections addressed
3. Ensure readability and clarity
4. Report to user:
   - File location
   - Documentation type
   - Summary of content
   - Word count / size

## Documentation Standards

### Markdown Formatting
- Use `#` for headers (hierarchy: H1 → H2 → H3)
- Code blocks with language specification: ` ```python `
- Lists: `-` for bullets, `1.` for numbered
- **Bold** for emphasis, *italic* for terms
- Tables for structured data
- Links: `[text](url)` or `[text](relative-path.md)`

### File Naming Conventions
- All lowercase
- Hyphens for spaces: `my-document.md`
- Timestamps where relevant: `YYYY-MM-DD-description.md`
- Descriptive, not cryptic: `session-skills-integration.md` not `s1.md`

### Content Guidelines
- **Clear and concise** - Remove unnecessary words
- **Structured** - Use headers and sections
- **Scannable** - Bullets, short paragraphs, tables
- **Complete** - Answer who/what/when/where/why/how
- **Objective** - State facts, note opinions clearly
- **Future-proof** - Write for someone reading months later

### Frontmatter (Optional)
For important documents, add YAML frontmatter:

```yaml
---
title: Document Title
date: 2025-10-20
author: HAL8000 CPU + User
type: session-doc | decision-log | architecture | feature | readme
status: draft | final | deprecated
tags: [tag1, tag2, tag3]
---
```

## Examples

### Example 1: Session Documentation Request

**User:** "Document today's work on the Skills integration"

**Response:**
```
I'll create a session document for the Skills integration work.

[Gathers context from current session]
[Uses session-doc-template.md]
[Creates file: data/sessions/summaries/2025-10-20-1430-skills-integration.md]

✅ Session documentation created

Location: data/sessions/summaries/2025-10-20-1430-skills-integration.md
Type: Session Documentation
Summary: Documented integration of 4 new Skills (context-awareness,
         architecture-consultant, hal-script-assistant,
         documentation-generator) into HAL8000 architecture.
Size: ~1,200 words

Captured:
- Skills architecture design
- Implementation details for 4 Skills
- Supporting files created
- Integration with existing system
- Next actions (BIOS update, state.json update, testing)
```

### Example 2: Decision Log Request

**User:** "Document the decision to not include RAM monitoring and session-continuity Skills"

**Response:**
```
I'll create a decision log for the Skills scope decision.

[Creates file: data/architecture/decisions/2025-10-20-skills-scope-decision.md]

✅ Decision log created

Location: data/architecture/decisions/2025-10-20-skills-scope-decision.md
Type: Decision Log
Decision: Exclude RAM monitoring and session-continuity Skills from initial Skills integration

Summary:
- Context: Skills 2 (ram-guardian) and 3 (session-continuity) identified as high-bandwidth
- Options: Include all 6 Skills vs. prioritize low-bandwidth Skills
- Decision: Implement Skills 1, 4, 5, 6 only (context-aware, architecture, HAL-Script, docs)
- Rationale: User already monitors RAM/sessions; Skills would evaluate constantly
- Consequence: More efficient resource usage, user maintains control

Status: Accepted
```

### Example 3: Architecture Documentation

**User:** "Can you create architecture documentation for the Skills system?"

**Response:**
```
I'll document the Skills architecture integration into HAL8000.

[Gathers context from Skills implementation]
[Uses architecture-doc-template.md]
[Creates file: data/architecture/skills-system-architecture.md]

✅ Architecture documentation created

Location: data/architecture/skills-system-architecture.md
Type: Architecture Documentation
Summary: Complete architecture for Skills layer integration, including
         three-layer intelligence model, Skills catalog, integration
         points, and design principles.
Size: ~2,500 words

Sections:
- Overview (Three-Layer Intelligence Model)
- Skills Architecture
- Individual Skill Designs
- Integration with Commands/Agents
- Tool Permissions Model
- Architecture Principles Applied
- Future Considerations
```

## Template Usage

See supporting files:
- [templates/session-doc-template.md](templates/session-doc-template.md)
- [templates/decision-log-template.md](templates/decision-log-template.md)
- [templates/architecture-doc-template.md](templates/architecture-doc-template.md)
- [templates/feature-doc-template.md](templates/feature-doc-template.md)
- [templates/readme-template.md](templates/readme-template.md)

Templates are starting points - adapt as needed for specific use cases.

## Best Practices

### 1. Write for Future You
Document as if you'll forget everything in 6 months (you will).

### 2. Capture Context
Don't just state what was done - explain WHY decisions were made.

### 3. Be Specific
"Updated command" → "Added YAML frontmatter to 10 commands for Claude Code integration"

### 4. Use Examples
Show concrete examples, not just abstract descriptions.

### 5. Link Related Docs
Connect related documentation for easy navigation.

### 6. Keep Updated
Mark outdated docs as deprecated, update with changes.

### 7. Separate Facts from Opinions
"This approach is faster (benchmark: 0.7s vs 2.1s)" vs "This seems better"

## Integration with HAL8000

**Works with:**
- Session continuity protocol (capture session state)
- Architecture principles (document design decisions)
- HAL-Script commands (document command creation)
- Version control (track documentation in git)

**Complements:**
- `/HAL-session-end` (creates session files, this documents work)
- architecture-consultant Skill (validates design, this captures rationale)
- hal-script-assistant Skill (creates commands, this documents them)

**Storage locations:**
- Session docs: `data/sessions/summaries/`
- Decisions: `data/architecture/decisions/`
- Architecture: `data/architecture/`
- Projects: `data/projects/[project-name]/`
- READMEs: Component directories
