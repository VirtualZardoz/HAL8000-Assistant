---
name: HAL-index-update
description: Update hierarchical file system and library indexes for efficient discovery
parameters:
  - name: path
    description: Specific directory to index (optional, defaults to all monitored directories)
    type: string
    required: false
---

# HAL-index-update

**Command Type:** System Maintenance
**Category:** File System and Library Management
**Created:** 2025-10-04
**Updated:** 2025-10-15 (v2.2 - Added YAML frontmatter)

---

## Purpose

Updates both the hierarchical file system indexes and the library index with metadata about files in the HAL8000-Assistant system. Uses a **master index** pointing to **per-directory indexes** for infinite scalability. This enables efficient discovery of relevant files and libraries without loading the entire file system into RAM.

## Usage

```bash
/HAL-index-update [path]
```

**Parameters:**
- `path` (optional): Directory to index (default: entire system from root)

**Examples:**
```bash
/HAL-index-update                    # Index entire system (all directories)
/HAL-index-update data/research      # Index only research directory
/HAL-index-update .claude/commands   # Index only commands directory
```

## Hierarchical Index Structure

```
.claude/indexes/
├── master.json           # Lightweight master index (~500 tokens for 100 dirs)
├── research.json         # data/research/ files
├── architecture.json     # data/architecture/ files
├── commands.json         # .claude/commands/ files
├── sessions.json         # .claude/sessions/ files
└── [project-name].json   # Future: per-project indexes
```

**Scalability:**
- Master index: ~10 tokens per directory (stays tiny)
- Directory index: ~2K tokens per directory
- 1,000 directories = 10K master + 2K per dir loaded
- Load master first, then only the directory indexes you need

## Implementation

### Step 1: Identify Target Directories

If no path specified:
- Index all major directories (data/research/, data/architecture/, .claude/commands/, etc.)
- Create/update directory index for each

If path specified:
- Index only that directory
- Update its directory index file

### Step 2: Discover Files per Directory

Use Glob to find all files in target directory:
```
Glob patterns:
- **/*.md (all markdown files)
- **/*.json (all JSON files)
- **/*.js, **/*.ts, etc. (code files if applicable)
```

### Step 3: Extract Metadata

For each file, extract:
- **Type:** system, research, architecture-spec, command, session, data, project
- **Category:** Infer from path and file name
- **Topics:** Extract from:
  - File name (keywords)
  - First 200 chars (headers, metadata)
  - Do NOT load entire file
- **Summary:** First sentence or metadata description
- **Size estimate:** Token count estimate (chars × 0.25 rough estimate)

### Step 4: Update Directory Index

Create/update `.claude/indexes/[directory-name].json`:
- File entries with metadata
- Directory statistics (file count, total tokens, categories)
- Timestamp of index update

### Step 5: Update Master Index

Update `.claude/indexes/master.json`:
- Add/update directory entry pointing to directory index
- Update directory statistics (file count, topics, tokens)
- Update timestamp

### Step 6: Report Results

Output summary:
```
Hierarchical index updated
- Directories indexed: 4
- Total files indexed: 25
- Directory indexes updated: architecture.json, research.json, commands.json, sessions.json
- Master index: updated
- Total estimated tokens: 39,800
```

## Library Indexing

In addition to filesystem indexing, this command also indexes the library system.

### Step 7: Index Libraries

**Target directories:**
- `.claude/libraries/internal/` - Libraries we develop
- `.claude/libraries/external/` - External libraries (read-only)

**Dual-mode indexing:**

#### Mode 1: Frontmatter Parsing (Internal Libraries)

For files in `.claude/libraries/internal/`:
1. Find all `.md` files via Glob
2. Read frontmatter (between `---` delimiters)
3. Extract metadata:
   - title
   - description
   - keywords
   - category
   - dependencies
   - composable
   - last_updated
4. Estimate token count
5. Add to library index with `metadata_source: "frontmatter"`

#### Mode 2: Content Scanning (External Libraries)

For files in `.claude/libraries/external/`:
1. For each subdirectory (each external library):
2. Recursively find all `.md` files
3. For each file:
   - Extract title from first H1 heading
   - Extract description from first paragraph
   - Extract keywords from H2/H3 headings and filename
   - Infer category from directory path
   - Estimate token count (word count × 1.3)
4. Add to library index with `metadata_source: "content-scan"`
5. Track library-level metadata (file count, last scanned)

### Step 8: Update Library Index

Create/update `.claude/libraries/index.json`:
- Library entries with metadata
- Source tracking (internal vs external)
- Statistics (total libraries, total tokens)
- Timestamp

**Library Index Structure:**
```json
{
  "version": "1.0",
  "libraries": [
    {
      "path": ".claude/libraries/internal/development/code-review.md",
      "source": "internal",
      "title": "Code Review Workflow",
      "description": "...",
      "keywords": ["code-review", "quality"],
      "category": "development",
      "metadata_source": "frontmatter",
      "size_estimate_tokens": 1200
    },
    {
      "path": ".claude/libraries/external/lib-xyz/file.md",
      "source": "external:lib-xyz",
      "title": "Extracted from H1",
      "description": "...",
      "keywords": ["extracted"],
      "metadata_source": "content-scan",
      "size_estimate_tokens": 800
    }
  ],
  "sources": {
    "internal": {
      "file_count": 12
    },
    "external:lib-xyz": {
      "file_count": 225,
      "last_updated": "2025-10-04"
    }
  },
  "statistics": {
    "total_libraries": 237,
    "total_estimated_tokens": 189400
  }
}
```

### Step 9: Report Library Indexing

Include in output summary:
```
Library index updated
- Internal libraries: 12
- External libraries: 225 (from 1 source)
- Total libraries indexed: 237
- Library index: .claude/libraries/index.json
```

## RAM Management

**If indexing >20 files (filesystem) OR >50 libraries:**
- Delegate to sub-agent (general-purpose or system-maintenance)
- Sub-agent scans files, builds indexes
- Returns summary only
- Main RAM impact: ~500 tokens (not thousands)

**If indexing ≤20 files AND ≤50 libraries:**
- Process directly
- Use Glob (no content loading)
- Extract metadata from file names/paths
- Read first 200 chars or frontmatter only if needed

## Index Structure

### Master Index (.claude/indexes/master.json)

```json
{
  "version": "2.0-hierarchical",
  "last_updated": "2025-10-04T15:15:00Z",
  "directories": {
    "data/research/": {
      "index_file": ".claude/indexes/research.json",
      "file_count": 4,
      "total_tokens_estimate": 12300,
      "primary_topics": ["architecture", "unix", "assembly"]
    }
  },
  "statistics": {
    "total_directories": 5,
    "total_files": 15,
    "total_estimated_tokens": 39800
  }
}
```

### Directory Index (.claude/indexes/research.json)

```json
{
  "version": "2.0-hierarchical",
  "directory": "data/research/",
  "files": {
    "data/research/01-von-neumann-architecture.md": {
      "type": "research",
      "category": "architecture-theory",
      "topics": ["von neumann", "stored program"],
      "summary": "Von Neumann architecture principles",
      "size_estimate_tokens": 3200
    }
  },
  "statistics": {
    "total_files": 4,
    "total_tokens_estimate": 12300
  }
}
```

## When to Run

**Automatic triggers:**
- After creating multiple new files (3+)
- After major refactoring
- Before starting context-heavy work (ensure index is current)

**Manual triggers:**
- User requests index update
- Switching to new project phase
- After session resume (if files changed externally)

## Integration with Discovery System

The hierarchical index enables **Layer 3: Metadata Discovery** in the I/O System with infinite scalability:

1. **Load master index** (~500 tokens for 100 directories)
2. **Identify relevant directories** by primary topics
3. **Load directory index** (~2K tokens per directory)
4. **Search directory index** by topic/keyword (in RAM, no I/O)
5. **Identify relevant files** with size estimates
6. **Calculate RAM cost** before loading
7. **Load selectively** based on RAM budget

**Total RAM cost for discovery: ~2.5K tokens (master + one directory), regardless of total file system size**

## Example Usage

### Scenario: Find files about "buses" (small scale)

**Hierarchical index approach:**
```
1. Load .claude/indexes/master.json (~500 tokens)
2. Search directories for "buses" topic
3. Find: data/architecture/ has "buses" in primary_topics
4. Load .claude/indexes/architecture.json (~2K tokens)
5. Search for "bus" in topics
6. Find: hal8000-bus-architecture.md (3500 tokens)
7. Decide: Load or not based on RAM budget
Total RAM: 2.5K (master + directory index) or 6K (+ file)
```

### Scenario: Find files about "quantum computing" (large scale - 1000 directories)

**Hierarchical index approach:**
```
1. Load .claude/indexes/master.json (~10K tokens for 1000 dirs)
2. Search 1000 directory entries for "quantum" topic
3. Find: projects/quantum-research/ matches
4. Load .claude/indexes/quantum-research.json (~2K tokens)
5. Search 50 files in that directory
6. Find relevant files
Total RAM: 12K (master + directory) vs 500K+ (loading all files to search)
```

### Scenario: Estimate RAM cost for loading all research docs

**Hierarchical index approach:**
```
1. Load .claude/indexes/master.json (~500 tokens)
2. Check directories["data/research/"].total_tokens_estimate
3. See: 12,300 tokens
4. Decide: Can RAM handle 12K? (yes/no)
Total RAM: 500 tokens (just master index)
```

## Command File Location

`.claude/commands/HAL-index-update.md`

## References

- I/O System: `data/architecture/hal8000-io-system.md`
- Library Architecture: `data/architecture/hal8000-library-architecture.md`
- Operating Principles: `CLAUDE.md` (Resource Management Protocol)
- Master Index: `.claude/indexes/master.json`
- Directory Indexes: `.claude/indexes/*.json`
- Library Index: `.claude/libraries/index.json`

---

**Status:** v2.1 - File System + Library Indexing - Ready for use
**Scalability:** Infinite (hierarchical for filesystem, flat for libraries, both can scale)
**Next:** Can be invoked via `/HAL-index-update` slash command
