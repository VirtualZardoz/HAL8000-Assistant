# HAL8000-Assistant Library Architecture

**Document Type:** Architecture Specification
**Component:** Library System
**Created:** 2025-10-05
**Status:** Active

---

## Overview

The Library System provides reusable instruction collections that the HAL8000-Assistant CPU can compose to accomplish tasks. Libraries solve the problem: **How to reuse proven solutions without reinventing them, while maintaining discoverability as the collection grows.**

Libraries are organized instruction sets stored as markdown files, indexed for discovery, and loaded on-demand to manage RAM efficiently.

---

## Design Rationale

### Problem Statement

As the HAL8000-Assistant system evolves, we will:
- Develop workflows and procedures that solve recurring problems
- Accumulate external instruction collections from other sources
- Need to discover "Do we already have a solution for X?"
- Risk RAM bloat if we load libraries speculatively

### Solution

**Library System with Hierarchical Indexing:**
1. **Store** instructions as markdown files in organized directories
2. **Index** libraries with searchable metadata
3. **Discover** via HAL-context-find without loading content
4. **Load** only what's needed for current task
5. **Compose** libraries to build complex workflows

### Key Architectural Decision: No "Program" Distinction

**Initial proposal:** Separate "libraries" (reusable) from "programs" (task-specific)

**Decision:** Drop the distinction. Everything is a library.

**Rationale:**
- **Libraries** are instruction sets (stored, reusable)
- **Programs** are just execution of library instructions (runtime behavior)
- Creating separate categories adds complexity without operational benefit
- Unix principle: Simple, not complex

**What we call "programs":**
- Ad-hoc composition of library instructions
- Specific application of general libraries
- Runtime execution, not storage category

---

## Architecture

### Library Organization

```
.claude/libraries/
├── index.json                      # Master index (searchable metadata)
│
├── internal/                       # Libraries we develop and control
│   ├── development/
│   │   ├── code-review-workflow.md
│   │   └── debugging-procedure.md
│   ├── research/
│   │   ├── literature-review.md
│   │   └── source-analysis.md
│   ├── deployment/
│   │   └── release-checklist.md
│   └── system/
│       └── maintenance-procedures.md
│
└── external/                       # External libraries (read-only)
    ├── [library-name-1]/
    │   └── [original structure preserved]
    ├── [library-name-2]/
    │   └── [different structure]
    └── README.md                   # Track sources, versions, update dates
```

### Internal vs External Libraries

#### Internal Libraries (We Control)

**Location:** `.claude/libraries/internal/`

**Characteristics:**
- We create and maintain these
- Structured with frontmatter metadata
- Organized by category (development, research, deployment, system)
- Can be modified and improved over time

**Metadata Format (Frontmatter):**
```markdown
---
title: "Code Review Workflow"
description: "Systematic code review process with quality checklist"
keywords: ["code-review", "quality", "testing", "workflow"]
category: "development"
dependencies: ["HAL-system-check"]
composable: true
last_updated: "2025-10-05"
---

# Code Review Workflow

## Instructions begin here...
```

**Why frontmatter?**
- Standard markdown convention
- Human-readable and machine-parsable
- Doesn't clutter instruction content
- Easy to extract for indexing

#### External Libraries (Read-Only Integration)

**Location:** `.claude/libraries/external/[library-name]/`

**Characteristics:**
- Imported from external sources (other repositories, collections, etc.)
- **Read-only:** Never modify these files
- Preserve original structure exactly
- May have 100+ files with varying organization
- Must support updates/refreshes

**Critical Constraints:**
- ✗ Do NOT add frontmatter to external files
- ✗ Do NOT reorganize their directory structure
- ✗ Do NOT manually curate each file
- ✓ Extract metadata via content scanning
- ✓ Store metadata in index.json (not in files)
- ✓ Support clean updates (delete old, add new, reindex)

**Example External Library:**
```
.claude/libraries/external/prompt-library-xyz/
├── category-a/
│   ├── file1.md
│   ├── file2.md
│   └── subfolder/
│       └── file3.md
├── category-b/
│   └── [225+ markdown files]
└── [original structure preserved]
```

**Refresh Workflow:**
1. Delete old library directory
2. Add new version to `.claude/libraries/external/`
3. Run `/HAL-index-update`
4. Index regenerates automatically from content
5. No manual curation needed

---

## Library Index System

### Index Purpose

**Enable discovery without loading:**
- "Do we have instructions for X?"
- "Which library covers topic Y?"
- "What's the RAM cost of loading library Z?"

**Solve the discoverability problem at scale:**
- 10 libraries: Easy to remember
- 100 libraries: Need search
- 1,000+ libraries: Need structured index

### Index Schema

**File:** `.claude/libraries/index.json`

**Structure:**
```json
{
  "version": "1.0",
  "libraries": [
    {
      "path": ".claude/libraries/internal/development/code-review.md",
      "source": "internal",
      "title": "Code Review Workflow",
      "description": "Systematic code review process with quality checklist",
      "keywords": ["code-review", "quality", "testing", "workflow"],
      "category": "development",
      "dependencies": ["HAL-system-check"],
      "composable": true,
      "metadata_source": "frontmatter",
      "size_estimate_tokens": 1200,
      "last_updated": "2025-10-05"
    },
    {
      "path": ".claude/libraries/external/library-xyz/debugging/async-debug.md",
      "source": "external:library-xyz",
      "title": "Async Debugging Techniques",
      "description": "Extracted from first paragraph...",
      "keywords": ["debugging", "async", "promises"],
      "category": "development",
      "metadata_source": "content-scan",
      "size_estimate_tokens": 800,
      "last_scanned": "2025-10-05T10:30:00Z"
    }
  ],
  "sources": {
    "internal": {
      "path": ".claude/libraries/internal",
      "file_count": 12,
      "categories": ["development", "research", "deployment", "system"]
    },
    "external:library-xyz": {
      "path": ".claude/libraries/external/library-xyz",
      "file_count": 225,
      "version": "1.0.0",
      "source_url": "https://github.com/example/library-xyz",
      "last_updated": "2025-10-04",
      "index_strategy": "content-scan"
    }
  },
  "statistics": {
    "total_libraries": 237,
    "total_estimated_tokens": 189400,
    "last_indexed": "2025-10-05T10:30:00Z"
  }
}
```

### Metadata Extraction Strategies

#### Strategy 1: Frontmatter Parsing (Internal Libraries)

**Process:**
1. Read markdown file
2. Parse YAML frontmatter between `---` delimiters
3. Extract all metadata fields directly
4. Add to index with `metadata_source: "frontmatter"`

**Accuracy:** High (explicit metadata)

#### Strategy 2: Content Scanning (External Libraries)

**Process:**
1. Read markdown file
2. Extract metadata from content:
   - **Title:** First H1 heading (`# Title`)
   - **Description:** First paragraph after title
   - **Keywords:** Extract from H2/H3 headings, filename
   - **Category:** Infer from directory path
3. Estimate token count (word count × 1.3)
4. Add to index with `metadata_source: "content-scan"`

**Accuracy:** Moderate (heuristic-based)

**Trade-off:** Enables indexing without file modification

---

## Index Maintenance

### HAL-index-update Command

**Command:** `/HAL-index-update [path]`

**Default behavior:** Update both filesystem index AND library index

**Library indexing process:**

1. **Scan internal libraries** (`.claude/libraries/internal/`):
   - Find all `.md` files via Glob
   - Parse frontmatter from each file
   - Extract metadata fields
   - Add to index with `metadata_source: "frontmatter"`

2. **Scan external libraries** (`.claude/libraries/external/`):
   - For each subdirectory (each external library):
   - Recursively find all `.md` files
   - For each file:
     - Extract title from first H1
     - Extract description from first paragraph
     - Extract keywords from headings and filename
     - Estimate token count
   - Add to index with `metadata_source: "content-scan"`
   - Track library-level metadata (file count, last scanned)

3. **Generate index.json**:
   - Merge all entries
   - Calculate statistics
   - Write to `.claude/libraries/index.json`

4. **Report summary**:
   - Internal libraries indexed: X
   - External libraries: Y (Z total files)
   - Total searchable entries: N
   - Estimated total tokens: M

**RAM Management:**
- For large libraries (100+ files): Delegate to sub-agent
- Process external libraries in batches
- Write index incrementally

**Frequency:**
- Run when adding new libraries
- Run after updating external libraries
- Run periodically to catch changes
- Can be automated as part of system maintenance

---

## Package Manager

### Overview

The HAL8000-Assistant package manager handles the complete lifecycle of external libraries through dedicated commands. This is essential OS infrastructure - every operating system has package management (apt, yum, npm, pip, cargo).

**Package manager operations:**
- **Update:** `/HAL-library-update [library-name]` (implemented)
- **Install:** `/HAL-library-install [url] [name]` (planned)
- **Remove:** `/HAL-library-remove [library-name]` (planned)
- **List:** `/HAL-library-list` (planned)
- **Info:** `/HAL-library-info [library-name]` (planned)

### HAL-library-update Command

**Purpose:** Updates external libraries from source repositories

**Command:** `/HAL-library-update [library-name]`

**Workflow:**

1. **Validate:** Check library exists in `.claude/libraries/external/README.md` registry
2. **Check Updates:** Connect to source repository (GitHub, etc.)
   - Compare current version to latest version
   - Count file changes (added/removed/modified)
3. **Report:** Show update status and changes
4. **Confirm:** Ask user permission to proceed
5. **Backup:** Copy current version to `.claude/libraries/external/.[library-name].backup/`
6. **Download:** Fetch new version from source
7. **Replace:** Remove old library, install new version
8. **Update Registry:** Edit README.md with new version/date/file count
9. **Reindex:** Automatically run `/HAL-index-update` to update metadata
10. **Report Results:** Show what changed (files added/removed, new patterns discovered)

**RAM Management:**
- Delegates to sub-agent (general-purpose) for heavy operations
- Main session RAM cost: ~5-10K tokens (summary only)
- Sub-agent handles: git operations, file comparisons, metadata extraction

**Example:**
```bash
/HAL-library-update fabric-patterns

⚡ Updates available for fabric-patterns
  Current: main-20251005 (292 files)
  Latest:  main-20251206 (305 files)
  Changes: +15 files, -2 files, ~5 modified

  Proceed with update? (y/n)

✅ fabric-patterns updated successfully
  Added: 15 new patterns
  Removed: 2 deprecated patterns
  Library reindexed. Use /HAL-context-find to discover new patterns.
```

**Update Schedule:**
- Per library registry entry (typically monthly/quarterly)
- Before major projects (ensure latest patterns available)
- When specific pattern not found (may be in new version)

**See:** `.claude/commands/HAL-library-update.md`

### Future Package Manager Operations

**Installation:**
```bash
/HAL-library-install https://github.com/user/library-name library-name
```
- Clone repository
- Place in external libraries
- Add registry entry
- Index automatically

**Removal:**
```bash
/HAL-library-remove library-name
```
- Remove library directory
- Update registry
- Reindex to remove from index.json

**Registry Management:**
```bash
/HAL-library-list              # Show all libraries with versions
/HAL-library-info fabric-patterns  # Show detailed library information
```

### Package Manager Philosophy

**Unix Principle: "Do one thing well"**
- Each command handles one operation
- Composable: Can script multiple operations
- Simple interface: Natural language parameters

**Reduce and Delegate:**
- Heavy operations (git, file ops) delegated to sub-agent
- Main session stays lightweight
- Returns clean summaries only

**Reliability:**
- Backups before updates (rollback capability)
- Validation before operations (check library exists)
- Error handling with automatic rollback on failure

---

## Library Discovery

### Discovery Mechanism

**Primary tool:** `/HAL-context-find [query]`

**Process:**
1. Load `.claude/libraries/index.json` (~2-5K tokens)
2. Search index for keywords/topics
3. Return matching libraries with:
   - Title and description
   - Path and source
   - Token size estimate
   - Dependencies
4. User/CPU decides which to load
5. Load selected library files into RAM

**Benefits:**
- Discover across 100+ libraries without loading them
- Estimate RAM cost before loading
- Find related libraries by keyword
- Identify dependencies

**Example:**
```
User: "I need to debug an async issue"

CPU: /HAL-context-find "async debugging"

Result:
- Async Debugging Techniques (external:library-xyz, 800 tokens)
- Debugging Workflow (internal, 1200 tokens)
- Promise Error Handling (external:library-xyz, 600 tokens)

Total RAM to load all: 2600 tokens

CPU: Loads "Async Debugging Techniques" (most relevant)
```

### Search Strategy

**By keyword:**
```
/HAL-context-find "code review"
→ Returns libraries with "code-review" in keywords
```

**By topic:**
```
/HAL-context-find "deployment"
→ Returns libraries in deployment category
```

**By source:**
```
/HAL-context-find "external:library-xyz"
→ Returns all libraries from that source
```

---

## Library Composition

### Composability

Libraries can reference and chain other libraries:

**Example - Deployment Workflow:**
```markdown
---
title: "Production Deployment Workflow"
dependencies: ["code-review-workflow", "test-suite-execution", "rollback-procedure"]
composable: true
---

# Production Deployment Workflow

## Steps

1. Execute Code Review Workflow (see: code-review-workflow.md)
2. Run Test Suite (see: test-suite-execution.md)
3. Deploy to staging
4. Smoke test
5. Deploy to production
6. Monitor (if issues, see: rollback-procedure.md)
```

**Benefits:**
- Reuse existing workflows
- Build complex procedures from simple components
- Maintain single source of truth
- Update component libraries, all dependent workflows inherit improvements

### Dependency Tracking

**In frontmatter:**
```yaml
dependencies: ["library-1", "library-2"]
```

**In index:**
```json
"dependencies": ["library-1", "library-2"]
```

**Usage:**
- When loading library, check dependencies
- Optionally load dependencies automatically
- Or notify user of required dependencies

---

## Integration with Existing Architecture

### Relationship to HAL Commands

**HAL Commands** (`.claude/commands/HAL-*.md`):
- **Purpose:** System-level operations (maintenance, navigation, health)
- **Operate ON:** The system itself
- **Examples:** HAL-session-end, HAL-register-dump, HAL-system-check
- **Callable:** Via `/command-name` (SlashCommand tool)

**Libraries** (`.claude/libraries/`):
- **Purpose:** Task-level instructions (workflows, patterns, procedures)
- **Operate ON:** External tasks and objectives
- **Examples:** code-review-workflow, debugging-procedure, deployment-checklist
- **Callable:** Loaded into RAM and executed by CPU

**Clear separation:**
- Commands = System operations layer
- Libraries = Task instruction layer

### Relationship to I/O System

Libraries use the I/O system for discovery:

**Discovery flow:**
1. `/HAL-context-find "keyword"` (SlashCommand I/O)
2. hal-context-finder agent searches index (Execution I/O - Task tool)
3. Agent uses File I/O (Read) to load index and search
4. Returns summary to main CPU (Standard I/O - stdout)
5. CPU loads selected library (File I/O - Read)

**Integration:** Libraries discovered via Search I/O (Layer 3 - Metadata Discovery), loaded via File I/O

See: `data/architecture/hal8000-io-system.md`

### Relationship to Agents

**Agents as co-processors** can:
- Build libraries (research-synthesizer creates research workflows)
- Index libraries (system-maintenance agent updates index)
- Search libraries (hal-context-finder discovers relevant libraries)

**Agents vs Libraries:**
- **Agents:** Separate computational units (own CPU + RAM)
- **Libraries:** Instruction sets for main CPU

See: `data/architecture/hal8000-agent-architecture.md`

### Relationship to Session Continuity

**Before session end:**
- Note which libraries were loaded (track in session file)
- Don't save library content (too large)
- Save library references: "Used code-review-workflow.md"

**On session resume:**
- Read library references
- Reload same libraries if needed for continuation
- Or discover new libraries for new task

See: `CLAUDE.md` (Section: Session Continuity Protocol)

---

## Usage Guidelines

### When to Create a New Library

**Create internal library when:**
- Workflow will be reused (not one-off task)
- Procedure is proven and tested
- Instructions are generalizable
- Future tasks will benefit from having this pattern

**Don't create library when:**
- Task is unique to specific context
- Procedure is still experimental
- Instructions are highly specific (not reusable)

### When to Import External Library

**Import when:**
- External library provides proven workflows
- Collection is large enough to justify indexing overhead
- Source is trustworthy and well-maintained
- Updates/refreshes are expected

**Track in `.claude/libraries/external/README.md`:**
```markdown
# External Libraries

## library-xyz
- **Source:** https://github.com/example/library-xyz
- **Version:** 1.0.0
- **Files:** 225
- **Last Updated:** 2025-10-04
- **Description:** Comprehensive prompt library for software development
- **Refresh:** Quarterly (check for updates)
```

### Library Organization Best Practices

**Internal libraries:**
- Use clear category names (development, research, deployment, system)
- Name files descriptively: `code-review-workflow.md` not `cr.md`
- Always include frontmatter metadata
- Keep files focused (single workflow/procedure per file)
- Document dependencies explicitly

**External libraries:**
- Preserve original structure (don't reorganize)
- Document source and version in README
- Set refresh schedule
- Track in version control as submodule if possible

---

## RAM Management

### Discovery Without Loading

**Pattern:**
```
1. Load index.json (2-5K tokens)
2. Search for relevant libraries
3. Review size estimates
4. Load only what's needed
```

**Never:**
```
❌ Load all libraries "just to see what we have"
❌ Keep library content in RAM after use (offload to session notes)
❌ Load dependencies speculatively (load only when needed)
```

### Size Estimation

**Index includes token estimates:**
- Estimate before loading
- Calculate: Current RAM + Library Size
- Check if result exceeds safe zone (80%)
- If too large: load subset or defer to next session

**Example:**
```
Current RAM: 75K (75%)
Library size estimate: 12K
Projected RAM: 87K (87%) → CAUTION zone

Decision: Load now with caution, or checkpoint first
```

---

## Future Considerations

### Potential Enhancements

**Smart Composition:**
- Auto-detect when multiple libraries can be chained
- Suggest workflow combinations
- Build dependency graphs

**Version Control:**
- Track library versions (especially external)
- Maintain changelog for internal libraries
- Support rollback to previous versions

**Categorization:**
- Auto-categorize external libraries via content analysis
- Tag-based organization (multi-category support)
- Hierarchical categories (development/frontend, development/backend)

**Collaborative Libraries:**
- Share internal libraries with other HAL8000-Assistant instances
- Community library repository
- Import/export library collections

### Known Limitations

**External library metadata:**
- Content scanning is heuristic (less accurate than frontmatter)
- May miss nuanced categorization
- Requires periodic reindexing as content changes

**Index scalability:**
- Current design: Single index.json
- At 1,000+ libraries: Consider hierarchical indexing (like filesystem index)
- Potential: Master index → category indexes → library indexes

**Dependency resolution:**
- Currently manual (user checks dependencies)
- No automatic dependency loading
- No circular dependency detection

---

## References

- I/O System: `data/architecture/hal8000-io-system.md`
- Agent Architecture: `data/architecture/hal8000-agent-architecture.md`
- System Design: `data/architecture/hal8000-system-design.md`
- HAL-index-update: `.claude/commands/HAL-index-update.md`
- HAL-library-update: `.claude/commands/HAL-library-update.md`
- HAL-context-find: `.claude/commands/HAL-context-find.md`

---

**Implementation Status:** Core Complete, Production Ready

**Completed:**
1. ✓ Directory structure created (`.claude/libraries/internal/` and `external/`)
2. ✓ HAL-index-update extended to v2.1 with library indexing
3. ✓ First external library imported (Fabric Patterns - 227 patterns, 292 files)
4. ✓ Library index generated (`.claude/libraries/index.json`)
5. ✓ Package manager implemented (`/HAL-library-update`)
6. ✓ Registry system established (`.claude/libraries/external/README.md`)

**Next Steps:**
1. Create first internal library as example (e.g., code review workflow)
2. Extend package manager with install/remove operations
3. Test library discovery via `/HAL-context-find`
4. Build library composition examples (chained workflows)
