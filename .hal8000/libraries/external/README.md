# External Libraries

This directory contains external library collections imported from other sources. These libraries are **read-only** - we do not modify their files or structure.

## Purpose

External libraries provide proven workflows, instructions, and patterns developed by other sources. They are indexed via content scanning (not frontmatter) to avoid modifying the original files.

## Management

### Adding a New External Library

1. Place the library directory in `.claude/libraries/external/[library-name]/`
2. Preserve the original directory structure (do not reorganize)
3. Add entry below to track source and version
4. Run `/HAL-index-update` to index the library

### Updating an External Library

1. Delete the old library directory
2. Add the new version
3. Update the entry below with new version/date
4. Run `/HAL-index-update` to reindex

## External Library Registry

List of external libraries currently in the system:

---

### Fabric Patterns
- **Source:** https://github.com/danielmiessler/Fabric
- **Version:** main branch (2025-10-05)
- **Files:** 292 .md files (227 patterns)
- **Last Updated:** 2025-10-05
- **Description:** Crowdsourced AI prompt patterns for various cognitive, creative, analytical, and professional tasks. Each pattern contains system prompts and user templates for specific use cases.
- **Refresh Schedule:** Monthly (check for new patterns)
- **Notes:** Each pattern directory contains system.md (system prompt) and user.md (user template). Patterns cover analysis, creation, extraction, coding, and specialized tasks.

---

## Notes

- External libraries are indexed automatically during `/HAL-index-update`
- Metadata is extracted via content scanning (H1 titles, first paragraphs, headings)
- All metadata is stored in `.claude/libraries/index.json` (not in the library files)
- To find libraries: Use `/HAL-context-find [keyword]`

## See Also

- Library Architecture: `data/architecture/hal8000-library-architecture.md`
- HAL-index-update Command: `.claude/commands/HAL-index-update.md`
