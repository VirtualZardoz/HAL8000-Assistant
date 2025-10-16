# Internal Libraries

This directory contains reusable instruction collections that we develop and maintain for the HAL8000 system.

## Purpose

Internal libraries provide proven workflows, procedures, and patterns that we create and refine over time. These are our "playbooks" for recurring tasks.

## Organization

Libraries are organized by category:

- **development/** - Software development workflows (code review, debugging, testing, etc.)
- **research/** - Research procedures (literature review, source analysis, etc.)
- **deployment/** - Deployment and release workflows
- **system/** - System maintenance and management procedures

## Creating a New Library

### 1. Choose the Right Category

Place the library in the appropriate category directory based on its primary purpose.

### 2. Use Frontmatter Metadata

All internal libraries must include frontmatter metadata for indexing:

```markdown
---
title: "Descriptive Library Title"
description: "Brief description of what this library does (1-2 sentences)"
keywords: ["keyword1", "keyword2", "keyword3"]
category: "development"
dependencies: ["other-library-name"]  # Optional: libraries this one references
composable: true  # Can this be chained with other libraries?
last_updated: "2025-10-05"
---

# Library Title

## Purpose

What this library accomplishes...

## Steps

1. First step
2. Second step
...
```

### 3. Naming Conventions

- Use lowercase with hyphens: `code-review-workflow.md`
- Be descriptive: `async-debugging-procedure.md` not `debug.md`
- One library per file

### 4. Content Guidelines

- **Single responsibility:** Each library should focus on one workflow/procedure
- **Clear steps:** Numbered steps or clear sections
- **Composable:** Reference other libraries when appropriate
- **Testable:** Include success criteria or validation steps
- **Maintainable:** Update `last_updated` when modified

### 5. Index the Library

After creating a new library:
```bash
/HAL-index-update
```

This will scan the library, extract frontmatter, and add it to `.claude/libraries/index.json`.

## Using Libraries

### Discovery

Find libraries by keyword:
```bash
/HAL-context-find "code review"
```

This searches the library index and returns matching libraries with descriptions and token estimates.

### Loading

Libraries are loaded into RAM on-demand using the Read tool. Check RAM budget before loading.

### Composition

Libraries can reference and chain other libraries:
```markdown
## Steps

1. Run Code Review (see: code-review-workflow.md)
2. Execute Tests (see: test-suite-execution.md)
3. Deploy (see: deployment-checklist.md)
```

## Maintenance

### When to Update

- After refining a workflow
- When adding new steps
- When dependencies change
- Periodically review and improve

### Versioning

- Update `last_updated` field in frontmatter
- Consider adding version in title for major changes
- Document significant changes in library content

### Archiving

If a library is no longer relevant:
- Move to archive subdirectory (e.g., `development/archive/`)
- Or delete and rely on git history
- Run `/HAL-index-update` to update index

## Best Practices

1. **Start simple:** Create library after using a workflow 2-3 times successfully
2. **Iterate:** Refine based on actual use
3. **Document rationale:** Include "why" not just "what"
4. **Link related libraries:** Build a knowledge graph
5. **Keep it current:** Review and update periodically

## See Also

- Library Architecture: `data/architecture/hal8000-library-architecture.md`
- HAL-index-update Command: `.claude/commands/HAL-index-update.md`
- External Libraries: `.claude/libraries/external/README.md`
