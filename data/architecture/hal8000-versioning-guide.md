# HAL8000-Assistant Versioning Guide

**Version:** 1.0.0
**Created:** 2025-10-14
**Purpose:** Formal guidelines for version management in HAL8000-Assistant system

---

## Overview

HAL8000-Assistant uses **Semantic Versioning 2.0.0** adapted for computer architecture principles. This guide defines when and how to increment version numbers.

---

## Version Format: MAJOR.MINOR.PATCH

```
1.0.0
│ │ │
│ │ └─ PATCH: Bug fixes, documentation corrections
│ └─── MINOR: New features, backward-compatible additions
└───── MAJOR: Breaking architectural changes
```

---

## MAJOR Version (X.0.0)

**Trigger:** Architectural breaking changes that fundamentally alter system behavior.

### Examples of MAJOR Changes:

1. **Boot Sequence Redesign**
   - Changing BIOS initialization order
   - Removing mandatory state.json load
   - Altering session handoff mechanism

2. **Memory Model Restructuring**
   - Replacing append-only RAM with dynamic eviction
   - Changing file system organization (depth limit, directory structure)
   - Removing hierarchical indexing

3. **Operating Principles Changes**
   - Abandoning Modified von Neumann architecture
   - Removing Unix philosophy adherence
   - Eliminating assembly language mapping

4. **Register Architecture Overhaul**
   - Removing register categories
   - Changing register update protocol
   - Eliminating register-dump command

5. **State Persistence Format Changes**
   - Breaking state.json schema
   - Incompatible session file format
   - System.log structure changes

6. **Component Removal**
   - Deprecating core commands (HAL-session-end, HAL-system-check)
   - Removing essential agents (hal-context-finder)
   - Eliminating MCP integration

### MAJOR Version Checklist:

- [ ] Impact analysis: Which components break?
- [ ] Migration guide: How do users upgrade?
- [ ] Deprecation notices: Warnings in previous version
- [ ] Documentation: Update all architecture docs
- [ ] Session file: Document breaking changes
- [ ] Gap analysis: Re-evaluate vs original vision
- [ ] Testing: Verify boot sequence and core operations

---

## MINOR Version (x.Y.0)

**Trigger:** Backward-compatible feature additions that extend system capabilities.

### Examples of MINOR Changes:

1. **New Commands**
   - HAL-backup (backup system state)
   - HAL-restore (restore from backup)
   - HAL-performance (performance profiling)

2. **New Agents**
   - performance-profiler (analyze CPU performance)
   - documentation-auditor (check doc completeness)
   - test-runner (automated testing)

3. **New Tools (I/O Devices)**
   - chart-generator (data visualization)
   - pdf-processor (PDF manipulation)
   - audio-transcriber (speech-to-text)

4. **Enhanced Existing Features**
   - HAL-session-end: Add compression option
   - HAL-context-find: Add fuzzy search
   - Register architecture: Add new non-breaking registers

5. **New Integrations**
   - Additional MCP servers
   - External library collections
   - New sub-agent types

6. **System Capabilities**
   - Performance monitoring
   - Advanced indexing algorithms
   - Context prediction

### MINOR Version Checklist:

- [ ] Backward compatibility: Old sessions still work?
- [ ] Documentation: Update command/agent lists
- [ ] Session file: Document new features
- [ ] State.json: Update component counts
- [ ] Indexes: Run HAL-index-update
- [ ] Testing: Verify new features don't break existing ones

---

## PATCH Version (x.x.Z)

**Trigger:** Bug fixes, documentation corrections, performance optimizations (no behavior change).

### Examples of PATCH Changes:

1. **Bug Fixes**
   - HAL-session-end: Fix state validation counting
   - HAL-register-dump: Correct register display format
   - Boot sequence: Handle missing optional files gracefully

2. **Documentation Corrections**
   - Fix typos in CLAUDE.md
   - Correct code examples in Reference Manual
   - Update outdated file paths

3. **Performance Optimizations**
   - Faster file indexing (same results)
   - Reduced sub-agent overhead
   - Optimized grep patterns

4. **Refactoring (No Interface Change)**
   - Internal code cleanup
   - Simplify command logic
   - Improve error messages

5. **Configuration Adjustments**
   - Update MCP server settings
   - Adjust RAM zone thresholds
   - Tweak boot acknowledgment format

6. **Dependency Updates**
   - Update external library versions (compatible)
   - Patch security vulnerabilities
   - Upgrade Docker base images

### PATCH Version Checklist:

- [ ] No breaking changes: Sessions load correctly?
- [ ] No new features: Only fixes/improvements?
- [ ] Documentation: Update if behavior clarified
- [ ] Session file: Brief note on fix
- [ ] Testing: Verify fix resolves issue

---

## Dual Version Tracking

HAL8000-Assistant tracks two independent versions:

### 1. System Version (HAL8000-Assistant Core)
**Location:** `VERSION` file (root)
**Tracks:** BIOS, commands, agents, architecture, tools

**Bump triggers:**
- Command/agent additions/changes (MINOR)
- Boot sequence changes (MAJOR)
- Core bug fixes (PATCH)

### 2. Manual Version (Reference Manual)
**Location:** `.claude/state.json` → `reference_manual.version`
**Tracks:** Documentation completeness and quality

**Bump triggers:**
- New sections added (MINOR)
- Major refactoring/reorganization (MAJOR)
- Typo fixes, clarifications (PATCH)

**Current State:** Both at 1.0.0 (synchronized after initial release)

**Divergence Example:**
- System at 1.2.0 (added 2 new commands)
- Manual at 1.0.1 (fixed typos, no new content)
- Both versions track independently

---

## Component-Level Versions (Optional)

Individual components may track their own versions:

- **Tools:** `diagram-generation` tool has internal versioning
- **External Libraries:** Fabric patterns maintain source versions
- **MCP Servers:** Track server versions in registry.json

**Rule:** Component versions don't affect system version unless:
- Breaking change in tool interface → MAJOR
- New tool capability exposed to system → MINOR
- Tool bug fix improving system reliability → PATCH (optional)

---

## Pre-Release Versioning

For experimental or testing phases:

```
X.Y.Z-alpha.N    → Experimental architecture changes
X.Y.Z-beta.N     → Feature complete, testing phase
X.Y.Z-rc.N       → Release candidate (production-ready testing)
```

**Example Progression:**
```
1.1.0-alpha.1 → Testing new HAL-backup command (unstable)
1.1.0-alpha.2 → Fixed critical bugs in backup
1.1.0-beta.1  → Feature complete, testing with real sessions
1.1.0-rc.1    → Release candidate, documentation complete
1.1.0         → Production release
```

**Note:** v1.0.0 skipped pre-releases (direct to production after gap analysis)

---

## Version Lifecycle Model

```
Development → Testing → Production → Maintenance → Deprecated
```

### Lifecycle Stages:

1. **Development** (alpha)
   - Active feature development
   - Breaking changes allowed
   - No stability guarantees

2. **Testing** (beta, rc)
   - Feature freeze
   - Bug fixes only
   - Documentation completion

3. **Production** (stable)
   - Stable API
   - Bug fixes and security patches
   - New features via MINOR bumps

4. **Maintenance** (LTS)
   - Critical fixes only
   - Preparation for next MAJOR
   - Migration guides available

5. **Deprecated** (end-of-life)
   - No further updates
   - Users must upgrade
   - Historical reference only

**Current Status:** v1.0.0 is in **Production** stage

---

## Decision Matrix

| Change Type | System Version | Manual Version | Example |
|-------------|----------------|----------------|---------|
| Add HAL-backup command | 1.1.0 | No change | New command |
| Fix HAL-session-end bug | 1.0.1 | No change | Bug fix |
| Add performance-profiler agent | 1.1.0 | 1.1.0 (new section) | New agent + docs |
| Manual Phase 3 refactoring | No change | 1.1.0 | Documentation only |
| Boot sequence redesign | 2.0.0 | 2.0.0 (major rewrite) | Breaking change |
| Add diagram-generation tool | 1.1.0 | 1.1.0 (new section) | New tool |
| Fix manual typos | No change | 1.0.1 | Documentation fix |
| RAM model change (dynamic eviction) | 2.0.0 | 2.0.0 (architecture change) | Breaking change |
| Add MCP server (new) | 1.1.0 | 1.0.1 (brief mention) | Integration |
| Deprecate old command | 2.0.0 | 2.0.0 (removal documented) | Breaking change |

---

## Version Bump Process

### Step 1: Determine Version Change
- Review change type (MAJOR/MINOR/PATCH)
- Consult decision matrix
- Check both system and manual impact

### Step 2: Update VERSION File
```bash
# Root directory
echo "1.1.0" > VERSION
```

### Step 3: Update state.json
```json
{
  "variables": {
    "version": "1.1.0"
  },
  "reference_manual": {
    "version": "1.0.0"  # Update if manual changed
  }
}
```

### Step 4: Update CHANGELOG.md
```markdown
## [1.1.0] - 2025-10-XX

### Added
- HAL-backup command for state preservation
- performance-profiler agent for CPU analysis

### Changed
- Enhanced HAL-context-find with fuzzy search

Session: .claude/sessions/2025-10-XX-HHMM-v1-1-0-release.md
```

### Step 5: Create Session File
Document the version bump:
```markdown
# Session: 2025-10-XX HHMM - v1.1.0 Release

## Context
Version bump from 1.0.0 to 1.1.0 due to...

## Changes
- [List all changes]

## Rationale
- [Why this version number]
```

### Step 6: Update Documentation
- Reference Manual (if needed)
- Architecture docs (if structural changes)
- Command/agent indexes

### Step 7: Run System Check
```bash
/HAL-system-check
/HAL-index-update
```

### Step 8: Session End
```bash
/HAL-session-end "v1.1.0 release preparation"
```

---

## Version Validation

Before declaring a new version:

### Pre-Release Checklist:

- [ ] VERSION file updated
- [ ] state.json updated (both versions if applicable)
- [ ] CHANGELOG.md entry complete
- [ ] Session file created
- [ ] Documentation updated
- [ ] HAL-system-check passes
- [ ] HAL-CC-check passes (external validation)
- [ ] Indexes updated (HAL-index-update)
- [ ] Boot sequence verified (test new session)
- [ ] No regressions (existing features work)

### MAJOR Version Additional Checks:

- [ ] Migration guide created
- [ ] Breaking changes documented
- [ ] Deprecation warnings added (in previous version)
- [ ] Gap analysis re-run
- [ ] Architecture docs revised

---

## Examples from HAL8000-Assistant History

### v1.0.0 (2025-10-04) - Production Release
**Type:** MAJOR
**Rationale:** First production-ready release with all core components
**Changes:** Initial system architecture complete
**Session:** `.claude/sessions/2025-10-04-1612-v1-0-0-production-release.md`

### Hypothetical v1.0.1 - Bug Fix
**Type:** PATCH
**Rationale:** Fix state validation counting in HAL-session-end
**Changes:** Corrected agents_available count logic
**Impact:** System only (no manual change)

### Hypothetical v1.1.0 - Feature Addition
**Type:** MINOR
**Rationale:** Added HAL-backup and HAL-restore commands
**Changes:** New backup/restore capability, manual section added
**Impact:** Both system (1.1.0) and manual (1.1.0)

### Hypothetical v2.0.0 - Architecture Redesign
**Type:** MAJOR
**Rationale:** Replaced append-only RAM with dynamic eviction
**Changes:** Complete memory management overhaul
**Impact:** Breaking change, migration required

---

## Summary

**Current Version:** 1.0.0
**Current Phase:** Production
**Next Likely:** 1.1.0 (new features) or 1.0.1 (bug fixes)

**Key Principles:**
1. Semantic Versioning 2.0.0 adapted for architecture
2. Dual version tracking (system vs manual)
3. Pre-release stages for major changes
4. Comprehensive documentation for every bump
5. Validation before declaring new version

**Questions?**
- See `CHANGELOG.md` for historical changes
- See `.claude/sessions/` for version bump sessions
- Run `/HAL-system-check` to verify current version consistency
