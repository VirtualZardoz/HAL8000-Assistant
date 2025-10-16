---
name: HAL-library-update
description: Update external libraries from source repositories (HAL8000 package manager)
parameters:
  - name: library-name
    description: Specific library to update (optional, defaults to all registered libraries)
    type: string
    required: false
---

# HAL-library-update

**Command Type:** Package Manager
**Category:** Library Lifecycle Management
**Created:** 2025-10-05
**Version:** 1.1

---

## Purpose

Updates external libraries from their source repositories. This is the HAL8000 **package manager** - it manages the lifecycle of external library collections by checking for updates, downloading new versions, and maintaining the library registry.

## Usage

```bash
/HAL-library-update [library-name]
```

**Parameters:**
- `library-name` (required): Name of the external library to update (must exist in registry)

**Examples:**
```bash
/HAL-library-update fabric-patterns    # Update Fabric patterns from GitHub
/HAL-library-update --list             # List all external libraries
/HAL-library-update --check-all        # Check all libraries for updates (no install)
```

## What This Command Does

1. **Reads registry** to get library source URL and current version
2. **Checks for updates** at source repository (compares commits/versions)
3. **Reports update status** (up-to-date, updates available, how many files changed)
4. **Downloads new version** if updates available (with user confirmation)
5. **Backs up old version** to `.claude/libraries/external/.[library-name].backup/`
6. **Replaces library** with new version
7. **Updates registry** with new version/date
8. **Reindexes** automatically via `/HAL-index-update`
9. **Reports results** (files added/removed/modified, new patterns discovered)

## Implementation

### Step 1: Validate Library Exists

1. Check if library exists in `.claude/libraries/external/README.md` registry
2. If not found: Error "Library '[name]' not found in registry"
3. Extract library metadata:
   - Source URL
   - Current version
   - Last updated date
   - File count

### Step 2: Check Source for Updates

**For GitHub libraries:**

1. Clone repository to temp directory (sparse checkout if applicable)
2. Get latest commit hash/date
3. Compare to current version in registry
4. Count file changes (added/removed/modified)

**Detection methods:**
- Git commit comparison (if version includes commit hash)
- File count comparison
- Timestamp comparison (last updated vs repo last commit)

### Step 3: Report Update Status

**If up-to-date:**
```
✓ fabric-patterns is up-to-date
  Current version: main-20251005
  Last updated: 2025-10-05
  Files: 292
```

**If updates available:**
```
⚡ Updates available for fabric-patterns
  Current: main-20251005 (292 files)
  Latest:  main-20251206 (305 files)
  Changes: +15 files, -2 files, ~5 modified

  Proceed with update? (y/n)
```

### Step 4: User Confirmation (if updates found)

Ask user to confirm update. If user declines, exit gracefully.

### Step 5: Backup Current Version

Before replacing:
1. Create backup directory: `.claude/libraries/external/.[library-name].backup/`
2. Copy current library to backup
3. Backup is **not indexed** (leading dot excludes it)
4. Only keep most recent backup (delete old backup if exists)

**Purpose:** Rollback capability if new version has issues

### Step 6: Download and Install New Version

1. Download new version to temp directory
2. Remove old library directory
3. Copy new version from temp to `.claude/libraries/external/[library-name]/`
4. Verify file count matches expected

### Step 7: Update Registry

Edit `.claude/libraries/external/README.md`:
- Update **Version** field (commit hash, date, or version number)
- Update **Files** count
- Update **Last Updated** date (YYYY-MM-DD)
- Update **Notes** if significant changes

### Step 8: Reindex Library

Automatically invoke:
```bash
/HAL-index-update
```

This updates `.claude/libraries/index.json` with new patterns/content.

### Step 9: Report Results

```
✅ fabric-patterns updated successfully

Changes:
  Before: 292 files (284K tokens)
  After:  305 files (298K tokens)
  Added: 15 new patterns
  Removed: 2 deprecated patterns
  Modified: 5 patterns updated

New patterns discovered:
  - analyze_quantum_paper
  - create_research_proposal
  - extract_legal_arguments
  ...

Library reindexed. Use /HAL-context-find to discover new patterns.
```

## Supported Library Sources

### GitHub Repositories

**Requirements:**
- Public repository
- Stable directory structure
- Patterns/files in consistent location

**Update detection:**
- Compare local version date to repo last commit date
- Use `git ls-remote` to check for updates without cloning
- Full clone only if updates detected

**Example registry entry:**
```markdown
### Fabric Patterns
- **Source:** https://github.com/danielmiessler/Fabric
- **Version:** main branch (2025-10-05)
- **Files:** 292 .md files (227 patterns)
- **Last Updated:** 2025-10-05
```

### Future: Other Sources

Could extend to:
- Direct URLs (ZIP files)
- Local directories (sync from file system)
- Git repositories (non-GitHub)
- Package registries

## Error Handling

**Common errors:**

1. **Library not in registry:**
   - Error: "Library 'xyz' not found. Check .claude/libraries/external/README.md"
   - Suggest: List available libraries with `--list`

2. **Source unavailable:**
   - Error: "Cannot reach source: [URL]. Check connection."
   - Suggest: Try again later or check URL in registry

3. **Download failed:**
   - Error: "Download failed at step X"
   - Action: Restore from backup automatically
   - Report: Rollback successful, library unchanged

4. **Index update failed:**
   - Warning: "Library updated but indexing failed"
   - Action: Library files are updated, but index may be stale
   - Suggest: Manually run `/HAL-index-update`

## RAM Management

**This command delegates to sub-agent (general-purpose):**

The update process involves:
- Cloning repositories
- Comparing file structures
- Reading metadata from many files
- Building index data

**Total RAM cost: ~5-10K tokens** (sub-agent summary only, not full processing context)

**Sub-agent handles:**
- All git operations
- All file comparisons
- All metadata extraction
- All error handling

**Returns to main session:**
- Clean summary of changes
- List of new/modified/removed items
- Update confirmation

## Package Manager Operations

This command is the **update** operation of HAL8000's package manager. Future expansion:

```bash
/HAL-library-install [url] [name] [category]  # Install new external library
/HAL-library-remove [name]                    # Remove external library
/HAL-library-list                             # List all libraries with status
/HAL-library-info [name]                      # Show library details
/HAL-library-search [keyword]                 # Search across all libraries
```

**Current status:** Only **update** operation implemented. Others can be added as system matures.

## When to Run

**Regular schedule:**
- Monthly for active libraries (per registry Refresh Schedule)
- Before starting major research/work (ensure latest patterns)
- When source repository announces major updates

**Triggered by:**
- User manual check
- System notices library is outdated (future: automatic check)
- User requests specific pattern not found (might be in new version)

## Integration with Library System

This command completes the library lifecycle:

```
1. Library Architecture → Design (documented)
2. Library Storage → .claude/libraries/ (directories)
3. Library Installation → HAL-library-update (this command)
4. Library Indexing → HAL-index-update (existing command)
5. Library Discovery → HAL-context-find (existing agent)
6. Library Usage → Load via discovery
```

**Package manager = installation + updates + removal**

## Command File Location

`.claude/commands/HAL-library-update.md`

## References

- Library Architecture: `data/architecture/hal8000-library-architecture.md`
- Library Registry: `.claude/libraries/external/README.md`
- Library Index: `.claude/libraries/index.json`
- Indexing Command: `.claude/commands/HAL-index-update.md`
- Discovery Agent: `.claude/agents/hal-context-finder.md`

---

**Status:** v1.0 - Package Manager Core
**Scope:** Update operation (install/remove planned for future)
**Next:** Extend to full package manager with install/remove/search operations
