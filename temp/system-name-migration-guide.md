# System Name Migration Guide

**For:** HAL8000-based system clones requiring name changes
**Version:** 1.0
**Date:** 2025-10-16
**Based on:** HAL8000 → HAL8001-Chapter migration (2025-10-15)

---

## Overview

This guide provides a comprehensive procedure for migrating your HAL8000-based system to a new name. The migration process updates all system references, paths, Docker images, and configuration while preserving historical records for audit purposes.

**Migration Scope:** Complete system-wide rename affecting ~500+ references across ~200+ files

**Time Required:** Single session (~1-2 hours depending on system size)

**RAM Impact:** Moderate (expect ~40-50% RAM usage during migration)

---

## Pre-Migration Checklist

Before starting, verify:

- [ ] **Clean state:** No uncommitted work or pending operations
- [ ] **Session saved:** Run `/HAL-session-end` to save current work
- [ ] **Backup:** Create filesystem backup (optional but recommended)
- [ ] **Docker images:** Note any custom Docker images requiring rename
- [ ] **External dependencies:** Identify any external systems referencing old name
- [ ] **New name chosen:** Decide on exact new system name (e.g., HAL8001-Chapter, HAL8000-Production, etc.)

---

## Migration Variables

Define these variables before starting:

```bash
OLD_NAME="HAL8000"                        # Your current system name
NEW_NAME="HAL8001-Chapter"                # Your new system name
OLD_PATH="/mnt/d/~HAL8000"                # Current base path
NEW_PATH="/mnt/d/~HAL8001-Chapter"        # New base path
OLD_DOCKER="hal8000-mermaid:latest"       # Current Docker image name
NEW_DOCKER="hal8001-chapter-mermaid:latest"  # New Docker image name
```

---

## Migration Procedure

### Phase 1: Core System Files (CRITICAL - Do First)

**Update order matters - follow sequence exactly:**

1. **BIOS (CLAUDE.md)**
   - Replace all `OLD_NAME` references with `NEW_NAME`
   - Update all `OLD_PATH` references with `NEW_PATH`
   - Update Docker image references
   - **Verification:** Search for old name - should find ZERO matches

2. **State File (.claude/state.json)**
   - Update `system_name` variable
   - Update `base_path` variable
   - Update `docker_image` variable
   - Add migration metadata to track change
   - **Verification:** Validate JSON syntax

3. **Version Files**
   - Update `VERSION` (bump minor or patch as appropriate)
   - Add migration entry to `CHANGELOG.md`

### Phase 2: Batch Update System Components

**Use sed for efficient batch processing:**

```bash
# Commands - Update all HAL-Script commands
find .claude/commands -name "*.md" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find .claude/commands -name "*.md" -type f -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +

# Agents - Update all agent definitions
find .claude/agents -name "*.md" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find .claude/agents -name "*.md" -type f -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +

# Indexes - Update all index files
find .claude/indexes -name "*.json" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find .claude/indexes -name "*.json" -type f -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +

# Libraries - Update library files
find .claude/libraries -name "*.md" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find .claude/libraries -name "*.md" -type f -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +
find .claude/libraries -name "*.json" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +

# Tools - Update tool configurations
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "Dockerfile" \) -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "Dockerfile" \) -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +
```

### Phase 3: Configuration Files

```bash
# MCP configuration
sed -i 's/OLD_NAME/NEW_NAME/g' .mcp.json
sed -i 's|OLD_PATH|NEW_PATH|g' .mcp.json

# Claude Code settings
sed -i 's/OLD_NAME/NEW_NAME/g' .claude/settings.local.json
sed -i 's|OLD_PATH|NEW_PATH|g' .claude/settings.local.json

# Environment files (if present)
find . -maxdepth 2 -name ".env*" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find . -maxdepth 2 -name ".env*" -type f -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +
```

### Phase 4: Documentation

```bash
# Architecture documentation
find data/architecture -name "*.md" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find data/architecture -name "*.md" -type f -exec sed -i 's|OLD_PATH|NEW_PATH|g' {} +

# Research documentation
find data/research -name "*.md" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +

# Reference manual (if present)
find data/reference-manual -name "*.html" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
find data/reference-manual -name "*.md" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +

# Any other data directories
find data -name "*.md" -o -name "*.html" -type f -exec sed -i 's/OLD_NAME/NEW_NAME/g' {} +
```

### Phase 5: System Log Update

```bash
# Append migration record to system log (DO NOT batch replace - log is historical)
echo "" >> .claude/system.log
echo "=== SYSTEM MIGRATION ===" >> .claude/system.log
echo "Date: $(date -Iseconds)" >> .claude/system.log
echo "From: OLD_NAME" >> .claude/system.log
echo "To: NEW_NAME" >> .claude/system.log
echo "Scope: Comprehensive system-wide rename" >> .claude/system.log
echo "Status: Complete" >> .claude/system.log
```

### Phase 6: Docker Images (If Applicable)

If your system uses Docker images:

```bash
# Update Dockerfile references
find . -name "Dockerfile" -type f -exec sed -i 's/OLD_DOCKER/NEW_DOCKER/g' {} +

# Rebuild Docker images with new name
docker build -t NEW_DOCKER .claude/tools/diagram-generation/

# Optionally remove old image
docker rmi OLD_DOCKER
```

---

## Historical Records Policy

**CRITICAL: Do NOT update session files in `.claude/sessions/`**

**Rationale:**
- Session files are historical records reflecting work done under original name
- Changing them destroys audit trail and context continuity
- Session references to old name are intentional and correct

**Exception:** Active session file (current work) should be updated if migration happens mid-session

---

## Verification Procedure

After migration, verify completeness:

### 1. Active References Check

```bash
# Search for old name in active system files (EXCLUDE sessions/)
grep -r "OLD_NAME" \
  --exclude-dir=".claude/sessions" \
  --exclude="*.log" \
  --include="*.md" \
  --include="*.json" \
  --include="*.py" \
  --include="*.sh" \
  --include="*.html" \
  .

# Expected result: ZERO matches (or only comments/strings explaining migration)
```

### 2. Path References Check

```bash
# Search for old path in active system files
grep -r "OLD_PATH" \
  --exclude-dir=".claude/sessions" \
  --exclude="*.log" \
  --include="*.md" \
  --include="*.json" \
  --include="*.py" \
  --include="*.sh" \
  .

# Expected result: ZERO matches
```

### 3. Core File Validation

Manually verify these critical files:
- [ ] `CLAUDE.md` - No old name references
- [ ] `.claude/state.json` - Valid JSON, new name in variables
- [ ] `VERSION` - Version bumped appropriately
- [ ] `CHANGELOG.md` - Migration documented
- [ ] `.mcp.json` - Paths updated
- [ ] Docker files - Image names updated

### 4. Count Session References (Expected)

```bash
# Count historical session references (these SHOULD exist)
grep -r "OLD_NAME" .claude/sessions/ --include="*.md" | wc -l

# This number is your audit trail - document it in state.json
```

---

## Post-Migration Tasks

### 1. Update State Metadata

Add migration record to `.claude/state.json`:

```json
"migration": {
  "date": "2025-XX-XX",
  "from": "OLD_NAME",
  "to": "NEW_NAME",
  "scope": "comprehensive",
  "active_references_remaining": 0,
  "historical_references_preserved": XXX,
  "verification_complete": true
}
```

### 2. Create Migration Session File

Run `/HAL-session-end "system-name-migration"` to document the migration work.

### 3. Test Critical Functions

Verify system functionality:
- [ ] Boot sequence works (new session loads state.json correctly)
- [ ] Commands execute (test 2-3 commands)
- [ ] Agents can be invoked
- [ ] Docker tools work (if rebuilt)
- [ ] File paths resolve correctly

### 4. Update External Dependencies

If applicable, update:
- External scripts referencing system
- Documentation outside repository
- CI/CD pipelines
- Backup systems

---

## Migration Statistics (Reference)

From HAL8000 → HAL8001-Chapter migration:

| Metric | Count |
|--------|-------|
| Files processed | ~200+ |
| References updated | ~500+ |
| Active references remaining | 0 |
| Historical references preserved | 242 |
| Commands updated | 10 |
| Agents updated | 5 |
| RAM usage during migration | 48.8% |
| Time to complete | 1 session |

---

## Troubleshooting

### Issue: JSON syntax errors after sed replacement

**Cause:** sed replaced string inside JSON syntax
**Fix:** Manually review and fix JSON files, validate with `jq` or JSON validator

### Issue: Paths not resolving

**Cause:** Missed path references or incorrect replacement
**Fix:** Run verification grep again, check for escaped paths or unusual formats

### Issue: Docker image not found

**Cause:** Image not rebuilt or old image name cached
**Fix:** Rebuild with `docker build -t NEW_DOCKER <path>`, verify with `docker images`

### Issue: Commands failing with "file not found"

**Cause:** Hardcoded paths in command scripts
**Fix:** Check command files for absolute paths, ensure all updated

---

## Best Practices

1. **Work methodically** - Follow phases in order, don't skip verification
2. **Use batch operations** - sed/find are faster and more reliable than manual edits
3. **Preserve history** - Never modify session files or system log entries
4. **Test incrementally** - Verify each phase before moving to next
5. **Document thoroughly** - Update state.json and CHANGELOG.md completely
6. **Save session** - Run `/HAL-session-end` before AND after migration

---

## Quick Reference Commands

**Search for old references:**
```bash
grep -r "OLD_NAME" --exclude-dir=".claude/sessions" --exclude="*.log" .
```

**Count session references (audit trail):**
```bash
grep -r "OLD_NAME" .claude/sessions/ --include="*.md" | wc -l
```

**Validate JSON files:**
```bash
find . -name "*.json" -type f -exec sh -c 'jq . "{}" > /dev/null' \;
```

**Rebuild Docker image:**
```bash
docker build -t NEW_DOCKER .claude/tools/diagram-generation/
```

---

## Conclusion

System name migration is a comprehensive but straightforward process when executed methodically. The key is complete coverage of all references while preserving historical audit trails.

**Migration Success Criteria:**
✅ Zero active references to old name (excluding sessions/)
✅ All paths updated to new base path
✅ Core files verified and functional
✅ state.json updated with migration metadata
✅ Version and changelog updated
✅ Docker images rebuilt (if applicable)
✅ System boots and operates normally

After successful migration, your system will be fully operational under the new name with complete historical continuity preserved.

---

**Document Version:** 1.0
**Last Updated:** 2025-10-16
**Maintained By:** HAL8001-Chapter System
