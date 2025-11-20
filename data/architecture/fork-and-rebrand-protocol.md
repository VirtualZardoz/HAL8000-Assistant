---
title: HAL8000-Assistant Fork and Rebrand Protocol
date_created: 2025-10-29
version: 1.0
category: architecture
tags: fork, clone, rebrand, github, migration, setup, procedure
replaces: system-name-migration-guide-2025-10-16.md
---

# HAL8000-Assistant Fork and Rebrand Protocol

**Purpose:** Complete procedure for forking HAL8000-Assistant and creating your own personalized system

**Use Case:** You've cloned/forked HAL8000-Assistant from GitHub and want to create your own independent system with a custom name, isolated from the original repository.

**Version:** 1.0
**Date:** 2025-10-29
**Status:** Active

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Clone from GitHub](#phase-1-clone-from-github)
4. [Phase 2: Filesystem Rebrand](#phase-2-filesystem-rebrand)
5. [Phase 3: Git Isolation and Reconnection](#phase-3-git-isolation-and-reconnection)
6. [Phase 4: Verification](#phase-4-verification)
7. [Phase 5: First Boot](#phase-5-first-boot)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What This Protocol Does

This protocol transforms a HAL8000-Assistant clone into your own independent system:

```
HAL8000-Assistant (GitHub: anthropics/HAL8000-Assistant)
    ↓ fork/clone
Your Local Copy (still connected to anthropics/HAL8000-Assistant)
    ↓ THIS PROTOCOL
YourSystemName (GitHub: yourname/YourSystemName)
    ✓ Filesystem renamed
    ✓ Git disconnected from HAL8000-Assistant
    ✓ Git connected to your new repo
    ✓ Fully independent system
```

### Critical Goals

1. **Filesystem Independence:** All file paths reflect your new system name
2. **Git Isolation:** No accidental commits to original HAL8000-Assistant repository
3. **New Identity:** Your system has its own GitHub repository
4. **Preservation:** Historical audit trail maintained with migration record

### Time & Resources

- **Duration:** Single session (1-2 hours)
- **RAM Impact:** ~40-50% during filesystem operations
- **Disk Space:** Original clone size + new system (recommend 2x original space during transition)
- **Prerequisites:** Git, Docker (if using tools), text editor

---

## Prerequisites

### Required Information

Before starting, decide on:

```bash
# Your new system identity
NEW_NAME="YourSystemName"              # e.g., "HAL8001-Chapter", "ProjectAI", "MyAssistant"
NEW_PATH="/mnt/d/~${NEW_NAME}"         # Filesystem location for new system
NEW_GITHUB_USER="your-github-username" # Your GitHub username
NEW_GITHUB_REPO="${NEW_NAME}"          # Your new GitHub repository name

# Original HAL8000-Assistant identity (for reference)
OLD_NAME="HAL8000-Assistant"
OLD_PATH="/mnt/d/~HAL8000-Assistant"
OLD_GITHUB="https://github.com/anthropics/HAL8000-Assistant.git"
```

### Checklist Before Starting

- [ ] Git installed and configured (`git config user.name` and `user.email` set)
- [ ] GitHub account ready
- [ ] New repository name decided
- [ ] New filesystem path decided (ensure parent directory exists)
- [ ] Docker installed (if using diagram-generation or image-generation tools)
- [ ] Clean workspace (no other git operations in progress)

---

## Phase 1: Clone from GitHub

### Step 1.1: Fork on GitHub (Recommended)

**Option A: Fork via GitHub Web Interface**

1. Go to https://github.com/anthropics/HAL8000-Assistant
2. Click "Fork" button (top right)
3. Choose your account
4. **Change repository name** to your new name (e.g., "MyProjectAI")
5. Add description (optional)
6. Click "Create fork"

**Option B: Direct Clone (No Fork)**

If you don't want to maintain fork relationship:
```bash
# Clone directly
git clone https://github.com/anthropics/HAL8000-Assistant.git ${NEW_PATH}
cd ${NEW_PATH}
```

### Step 1.2: Clone Forked Repository Locally

```bash
# Clone your fork to the new path directly
git clone https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git ${NEW_PATH}

# Navigate into new system
cd ${NEW_PATH}

# Verify git status
git remote -v
# Should show:
# origin  https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git (fetch)
# origin  https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git (push)
```

**Important:** If you cloned to a temporary location first, move it now:
```bash
# If you cloned to wrong location
mv /old/location ${NEW_PATH}
cd ${NEW_PATH}
```

---

## Phase 2: Filesystem Rebrand

Now we update all internal references from "HAL8000-Assistant" to your new system name.

### Step 2.1: Set Variables

```bash
# Define your rebrand variables (use your actual values)
export OLD_NAME="HAL8000-Assistant"
export NEW_NAME="YourSystemName"
export OLD_PATH="/mnt/d/~HAL8000-Assistant"
export NEW_PATH="/mnt/d/~${NEW_NAME}"
export OLD_DOCKER="hal8000-mermaid:latest"
export NEW_DOCKER="$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')-mermaid:latest"

# Verify variables
echo "Rebranding: ${OLD_NAME} → ${NEW_NAME}"
echo "Path: ${OLD_PATH} → ${NEW_PATH}"
echo "Docker: ${OLD_DOCKER} → ${NEW_DOCKER}"
```

### Step 2.2: Core System Files (CRITICAL - Manual Updates)

Update these files manually (order matters):

#### 2.2.1 BIOS (CLAUDE.md)

```bash
# Update CLAUDE.md
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" CLAUDE.md
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" CLAUDE.md
sed -i "s/${OLD_DOCKER}/${NEW_DOCKER}/g" CLAUDE.md

# Verify changes
grep -c "${OLD_NAME}" CLAUDE.md  # Should return 0
grep -c "${NEW_NAME}" CLAUDE.md  # Should return multiple matches
```

#### 2.2.2 State File (.claude/state.json)

```bash
# Backup first
cp .claude/state.json .claude/state.json.backup

# Update state.json
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .claude/state.json
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .claude/state.json

# Validate JSON syntax
cat .claude/state.json | jq . > /dev/null && echo "✓ JSON valid" || echo "✗ JSON INVALID - restore backup!"

# Add migration metadata
jq --arg date "$(date -Iseconds)" \
   --arg from "${OLD_NAME}" \
   --arg to "${NEW_NAME}" \
   '.migration = {
     date: $date,
     from: $from,
     to: $to,
     type: "fork-and-rebrand",
     scope: "comprehensive"
   }' .claude/state.json > .claude/state.json.tmp && mv .claude/state.json.tmp .claude/state.json

# Verify
cat .claude/state.json | jq .migration
```

#### 2.2.3 Version Files

```bash
# Update VERSION (bump patch version)
CURRENT_VERSION=$(cat VERSION)
# Manually decide new version, or:
echo "1.0.0-${NEW_NAME}" > VERSION

# Update CHANGELOG.md (prepend new entry)
cat > CHANGELOG.tmp << EOF
# Changelog

## [1.0.0-${NEW_NAME}] - $(date +%Y-%m-%d)

### Changed
- Forked from HAL8000-Assistant and rebranded to ${NEW_NAME}
- Updated all system references and paths
- Reconfigured git remote to new repository
- System now independent from original HAL8000-Assistant

$(cat CHANGELOG.md | tail -n +2)
EOF
mv CHANGELOG.tmp CHANGELOG.md
```

### Step 2.3: Batch Update System Components

```bash
# Commands - Update all HAL-Script commands
find .claude/commands -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/commands -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Agents - Update all agent definitions
find .claude/agents -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/agents -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Skills - Update all skill definitions
find .claude/skills -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/skills -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Indexes - Update all index files
find .claude/indexes -name "*.json" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/indexes -name "*.json" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Libraries - Update library files
find .claude/libraries -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/libraries -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
find .claude/libraries -name "*.json" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +

# Tools - Update tool configurations
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "Dockerfile" \) \
  -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "Dockerfile" \) \
  -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
```

### Step 2.4: Configuration Files

```bash
# MCP configuration
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .mcp.json
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .mcp.json

# Claude Code settings (if exists)
if [ -f .claude/settings.local.json ]; then
  sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .claude/settings.local.json
  sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .claude/settings.local.json
fi

# Environment files (if present)
find . -maxdepth 2 -name ".env*" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find . -maxdepth 2 -name ".env*" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
```

### Step 2.5: Documentation

```bash
# README.md - Critical for GitHub
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" README.md
sed -i "s|anthropics/HAL8000-Assistant|${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}|g" README.md
sed -i "s|github.com/anthropics/HAL8000-Assistant|github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}|g" README.md

# Architecture documentation
find data/architecture -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find data/architecture -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Research documentation (optional - these are theoretical)
find data/research -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +

# Reference manual (if present)
if [ -d data/reference-manual ]; then
  find data/reference-manual -name "*.html" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
  find data/reference-manual -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
fi
```

### Step 2.6: Docker Images (If Using Tools)

```bash
# Update Dockerfile references in tools
find .claude/tools -name "Dockerfile" -type f -exec sed -i "s/${OLD_DOCKER}/${NEW_DOCKER}/g" {} +

# Rebuild Docker images with new name
# Diagram generation tool
if [ -f .claude/tools/diagram-generation/Dockerfile ]; then
  echo "Rebuilding diagram-generation Docker image as ${NEW_DOCKER}..."
  docker build -t ${NEW_DOCKER} .claude/tools/diagram-generation/
fi

# Image generation tool (if present)
if [ -f .claude/tools/image-generation/Dockerfile ]; then
  NEW_IMAGE_DOCKER="$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')-image-gen:latest"
  echo "Rebuilding image-generation Docker image as ${NEW_IMAGE_DOCKER}..."
  docker build -t ${NEW_IMAGE_DOCKER} .claude/tools/image-generation/
fi

# Verify new images exist
docker images | grep "$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')"
```

### Step 2.7: System Log Update

```bash
# Append migration record to system log
cat >> .claude/system.log << EOF

=== SYSTEM FORK AND REBRAND ===
Date: $(date -Iseconds)
Original System: ${OLD_NAME}
New System: ${NEW_NAME}
Original Repository: https://github.com/anthropics/HAL8000-Assistant
New Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}
Migration Type: Fork and Rebrand
Scope: Comprehensive (filesystem + git)
Status: Complete
EOF
```

---

## Phase 3: Git Isolation and Reconnection

**CRITICAL:** This phase ensures your system doesn't accidentally commit to the original HAL8000-Assistant repository.

### Step 3.1: Verify Current Git State

```bash
# Check current remote configuration
git remote -v

# Check current branch
git branch -a

# Check if there are uncommitted changes from rebrand
git status
```

### Step 3.2: Commit Rebrand Changes

```bash
# Stage all changes from rebrand
git add -A

# Create rebrand commit
git commit -m "$(cat <<'EOF'
Fork and rebrand from HAL8000-Assistant to ${NEW_NAME}

This system is forked from HAL8000-Assistant and rebranded as an independent system.

Changes:
- Updated all system name references (HAL8000-Assistant → ${NEW_NAME})
- Updated all filesystem paths
- Updated Docker image names
- Updated documentation and README
- Reconfigured for independent operation

Original: https://github.com/anthropics/HAL8000-Assistant
New System: ${NEW_NAME}
Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 3.3: Configure Git Remote

**If you forked on GitHub** (repository already exists):

```bash
# Verify origin points to YOUR fork
git remote -v
# Should show: origin  https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git

# If origin still points to anthropics/HAL8000-Assistant, update it:
git remote set-url origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git

# Optionally keep HAL8000-Assistant as upstream (for pulling future updates)
git remote add upstream https://github.com/anthropics/HAL8000-Assistant.git
git remote set-url --push upstream DISABLE  # Prevent accidental push to upstream

# Verify configuration
git remote -v
# Should show:
# origin    https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git (fetch)
# origin    https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git (push)
# upstream  https://github.com/anthropics/HAL8000-Assistant.git (fetch)
# upstream  DISABLE (push)
```

**If you did NOT fork on GitHub** (need to create new repo):

```bash
# Remove original remote
git remote remove origin

# Create new repository on GitHub (using gh CLI)
gh repo create ${NEW_GITHUB_REPO} --public --source=. --remote=origin --description="Personalized HAL8000-Assistant-based system"

# Or create manually on GitHub web, then:
git remote add origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git

# Optionally keep HAL8000-Assistant as upstream
git remote add upstream https://github.com/anthropics/HAL8000-Assistant.git
git remote set-url --push upstream DISABLE

# Verify
git remote -v
```

### Step 3.4: Push to Your New Repository

```bash
# Push rebrand commit to your repository
git push -u origin main

# Verify on GitHub
gh repo view --web
# Or manually visit: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}
```

### Step 3.5: Verify Git Isolation

```bash
# Critical verification: Ensure you CANNOT push to HAL8000-Assistant
git remote -v | grep -E "(origin|upstream)"

# Test that origin points to YOUR repo
git remote get-url origin
# Should output: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git

# If upstream exists, verify push is disabled
git remote get-url --push upstream 2>/dev/null
# Should output: DISABLE or error (either is good)

echo "✓ Git isolation verified: Cannot push to original HAL8000-Assistant repository"
```

---

## Phase 4: Verification

### Step 4.1: Search for Old References

```bash
# Search for old system name in active files (EXCLUDE historical sessions)
echo "Checking for remaining ${OLD_NAME} references..."
grep -r "${OLD_NAME}" \
  --exclude-dir=".claude/sessions" \
  --exclude="*.log" \
  --exclude="fork-and-rebrand-protocol.md" \
  --include="*.md" \
  --include="*.json" \
  --include="*.py" \
  --include="*.sh" \
  --include="*.html" \
  .

# Expected result: ZERO matches (or only this protocol file)
# If matches found: Review and update those files

# Search for old path references
echo "Checking for remaining ${OLD_PATH} references..."
grep -r "${OLD_PATH}" \
  --exclude-dir=".claude/sessions" \
  --exclude="*.log" \
  --exclude="fork-and-rebrand-protocol.md" \
  --include="*.md" \
  --include="*.json" \
  --include="*.py" \
  --include="*.sh" \
  .

# Expected result: ZERO matches
```

### Step 4.2: Validate Core Files

```bash
# CLAUDE.md
grep -c "${NEW_NAME}" CLAUDE.md && echo "✓ CLAUDE.md updated" || echo "✗ CLAUDE.md NOT updated"
grep -q "${OLD_NAME}" CLAUDE.md && echo "✗ CLAUDE.md still has old name!" || echo "✓ CLAUDE.md clean"

# state.json
cat .claude/state.json | jq -e '.migration' && echo "✓ state.json has migration record" || echo "✗ state.json missing migration"
cat .claude/state.json | jq . > /dev/null && echo "✓ state.json valid JSON" || echo "✗ state.json INVALID JSON"

# VERSION
cat VERSION && echo "✓ VERSION file exists"

# CHANGELOG.md
head -20 CHANGELOG.md | grep -q "${NEW_NAME}" && echo "✓ CHANGELOG.md updated" || echo "✗ CHANGELOG.md NOT updated"

# README.md
grep -q "${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}" README.md && echo "✓ README.md updated" || echo "✗ README.md NOT updated"
```

### Step 4.3: Test Docker Images

```bash
# Verify new Docker images exist
docker images | grep "$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')" && echo "✓ Docker images rebranded" || echo "⚠ Docker images not rebuilt"

# Test diagram generation (if applicable)
if command -v python3 &> /dev/null && [ -f .claude/tools/diagram-generation/HAL-generate-diagram.py ]; then
  echo "Testing diagram generation..."
  python3 .claude/tools/diagram-generation/HAL-generate-diagram.py process-flow "Test Rebrand" && echo "✓ Diagram generation works" || echo "✗ Diagram generation failed"
fi
```

### Step 4.4: Count Historical References (Expected)

```bash
# Count historical session references (these SHOULD exist - they're audit trail)
HISTORICAL_COUNT=$(grep -r "${OLD_NAME}" .claude/sessions/ --include="*.md" 2>/dev/null | wc -l)
echo "Historical ${OLD_NAME} references in sessions/: ${HISTORICAL_COUNT}"
echo "✓ These are preserved intentionally (audit trail)"

# Update state.json with count
jq --arg count "${HISTORICAL_COUNT}" '.migration.historical_references_preserved = ($count | tonumber)' \
  .claude/state.json > .claude/state.json.tmp && mv .claude/state.json.tmp .claude/state.json
```

---

## Phase 5: First Boot

### Step 5.1: Test System Boot

Start a new Claude Code session in your rebranded system:

```bash
# Navigate to new system
cd ${NEW_PATH}

# Start Claude Code
# (System should boot and load CLAUDE.md, state.json automatically)
```

**Expected Boot Sequence:**
```
✅ ${NEW_NAME} CPU Operational
├─ Architecture: Modified von Neumann
├─ Phase: production-ready
├─ Last Session: [timestamp]
├─ Session Available: [session file] (not loaded - say "resume" to load)
├─ Context: Fork and rebrand from HAL8000-Assistant complete
├─ Next Action: System operational, ready for customization
├─ Registers: Initialized
└─ RAM Zone: SAFE

🟢 Ready for instructions
```

### Step 5.2: Test Commands

```bash
# Test basic commands
/HAL-register-dump        # Should show new system name
/HAL-system-check         # Should validate new system structure
/HAL-context-find "rebrand"  # Should find this protocol
```

### Step 5.3: Verify Path Resolution

```bash
# Test that tools use correct paths
ls ${NEW_PATH}/.claude/commands/
ls ${NEW_PATH}/.claude/agents/
ls ${NEW_PATH}/data/

# All should resolve correctly
```

---

## Troubleshooting

### Issue: Git still tries to push to anthropics/HAL8000-Assistant

**Symptoms:**
- `git push` fails with permission denied
- `git remote -v` shows origin pointing to anthropics/HAL8000-Assistant

**Fix:**
```bash
# Update origin to your repository
git remote set-url origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git

# Verify
git remote -v

# Push again
git push -u origin main
```

### Issue: JSON syntax errors in state.json

**Symptoms:**
- `jq` fails to parse state.json
- System boot fails with JSON error

**Fix:**
```bash
# Restore backup
cp .claude/state.json.backup .claude/state.json

# Manually edit state.json (use jq for safety)
jq '.' .claude/state.json

# Fix syntax errors and try again
```

### Issue: Old system name still appears in files

**Symptoms:**
- grep finds old name in files
- Commands reference old system

**Fix:**
```bash
# Re-run sed on specific directory
find .claude/commands -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +

# Or manually edit specific files
nano [problematic-file]
```

### Issue: Docker images not found

**Symptoms:**
- Tool commands fail with "image not found"
- `docker images` doesn't show new names

**Fix:**
```bash
# Rebuild Docker images
docker build -t ${NEW_DOCKER} .claude/tools/diagram-generation/

# Verify
docker images | grep "$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')"
```

### Issue: Paths don't resolve

**Symptoms:**
- Commands fail with "file not found"
- Tools can't find data directories

**Fix:**
```bash
# Verify current working directory
pwd  # Should be ${NEW_PATH}

# Check if paths in config files are correct
grep -r "${OLD_PATH}" .claude/ --include="*.json" --include="*.md"

# Update any remaining old paths
find .claude -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
```

### Issue: Accidentally pushed to HAL8000-Assistant upstream

**Prevention (set push disable):**
```bash
git remote set-url --push upstream DISABLE
```

**If already pushed (contact HAL8000-Assistant maintainers):**
- You may need to request removal of accidental commits
- Document what happened
- Ensure origin is correctly configured going forward

---

## Post-Rebrand Recommendations

### 1. Customize Your System

Now that you have your own system, consider customizing:

- **Create custom commands** for your specific workflows
- **Add custom agents** for specialized tasks
- **Modify templates** in `.claude/libraries/internal/templates/`
- **Add project-specific data** to `data/projects/`
- **Configure MCP servers** for your needs

### 2. Update GitHub Repository Settings

1. Go to `https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}/settings`
2. Add description: "Personalized HAL8000-Assistant-based system - von Neumann architecture, HAL-Script programming"
3. Add topics: `claude-code`, `ai-architecture`, `hal8000`, `fork`, `personal-ai`
4. Configure branch protection (optional)
5. Add collaborators (if working with team)

### 3. Consider Upstream Sync Strategy

**If you want to pull future HAL8000-Assistant updates:**

```bash
# Fetch updates from upstream
git fetch upstream

# Review changes
git log upstream/main

# Merge selectively (may have conflicts due to rebrand)
git merge upstream/main
# Or cherry-pick specific commits:
git cherry-pick <commit-hash>

# Resolve conflicts (favor your customizations)
# Push to your repo
git push origin main
```

**If you want complete independence:**
```bash
# Remove upstream remote
git remote remove upstream

# Your system is now completely independent
```

### 4. Document Your Customizations

Create a custom documentation file:

```bash
# Create customization log
cat > data/architecture/customizations.md << 'EOF'
# ${NEW_NAME} Customizations

## Rebrand Information
- Original System: HAL8000-Assistant
- Forked: $(date +%Y-%m-%d)
- Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}

## Custom Features
- [List your custom commands]
- [List your custom agents]
- [List your custom workflows]

## Divergence from HAL8000-Assistant
- [Document major changes from upstream]

## Maintenance Notes
- [Your maintenance schedule]
- [Update strategy (sync vs. independent)]
EOF
```

---

## Quick Reference

### Essential Commands

```bash
# Check system name in all files
grep -r "YourSystemName" --exclude-dir=".git" --exclude-dir=".claude/sessions" .

# Verify git remote configuration
git remote -v

# Test Docker images
docker images | grep yourname

# Validate JSON configs
find . -name "*.json" -type f -exec sh -c 'jq . "{}" > /dev/null || echo "Invalid: {}"' \;

# Count old references in sessions (audit trail)
grep -r "HAL8000-Assistant" .claude/sessions/ --include="*.md" | wc -l
```

### Files to Review After Rebrand

Critical files to manually verify:
- `CLAUDE.md` - BIOS with system identity
- `.claude/state.json` - Current state and migration record
- `VERSION` - Version number
- `CHANGELOG.md` - Change history
- `README.md` - GitHub repository info
- `.mcp.json` - MCP configuration with paths
- `.claude/tools/*/Dockerfile` - Docker image names

---

## Success Criteria

Your fork and rebrand is complete when:

- ✅ Zero active references to "HAL8000-Assistant" (excluding historical sessions)
- ✅ All filesystem paths updated to new system name
- ✅ Git origin points to YOUR repository
- ✅ Git push goes to YOUR repository (not HAL8000-Assistant)
- ✅ state.json contains migration record
- ✅ VERSION and CHANGELOG.md updated
- ✅ README.md references YOUR GitHub repository
- ✅ Docker images rebuilt with new names (if applicable)
- ✅ System boots successfully with new identity
- ✅ Commands execute correctly
- ✅ Tools work with new paths

**Congratulations!** You now have a fully independent HAL8000-Assistant-based system customized for your needs.

---

## Appendix: Automation Script

For advanced users, here's a complete automation script:

```bash
#!/bin/bash
# fork-and-rebrand.sh - Automate HAL8000-Assistant fork and rebrand
# Usage: ./fork-and-rebrand.sh NEW_NAME NEW_GITHUB_USER

set -e  # Exit on error

NEW_NAME="$1"
NEW_GITHUB_USER="$2"

if [ -z "$NEW_NAME" ] || [ -z "$NEW_GITHUB_USER" ]; then
  echo "Usage: ./fork-and-rebrand.sh NEW_NAME NEW_GITHUB_USER"
  exit 1
fi

OLD_NAME="HAL8000-Assistant"
OLD_PATH="/mnt/d/~HAL8000-Assistant"
NEW_PATH="/mnt/d/~${NEW_NAME}"
NEW_GITHUB_REPO="${NEW_NAME}"

echo "Starting fork and rebrand: ${OLD_NAME} → ${NEW_NAME}"
echo "New repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}"

# Verify we're in correct directory
if [ ! -f "CLAUDE.md" ]; then
  echo "Error: CLAUDE.md not found. Are you in the HAL8000-Assistant directory?"
  exit 1
fi

# Phase 2: Filesystem rebrand
echo "Phase 2: Updating filesystem references..."

# Core files
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" CLAUDE.md
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" CLAUDE.md
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .claude/state.json
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .claude/state.json

# Batch updates
find .claude/commands -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/agents -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" \) -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +

# Update README
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" README.md
sed -i "s|anthropics/HAL8000-Assistant|${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}|g" README.md

echo "✓ Filesystem rebrand complete"

# Phase 3: Git reconfiguration
echo "Phase 3: Reconfiguring git..."

git add -A
git commit -m "Fork and rebrand from HAL8000-Assistant to ${NEW_NAME}"

git remote set-url origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git
git remote add upstream https://github.com/anthropics/HAL8000-Assistant.git
git remote set-url --push upstream DISABLE

git push -u origin main

echo "✓ Git reconfiguration complete"

# Verification
echo "Verification:"
grep -q "${OLD_NAME}" CLAUDE.md && echo "✗ Old name found in CLAUDE.md" || echo "✓ CLAUDE.md clean"
git remote -v | grep "origin.*${NEW_GITHUB_USER}" && echo "✓ Git remote correct" || echo "✗ Git remote incorrect"

echo "✅ Fork and rebrand complete!"
echo "New system: ${NEW_NAME}"
echo "Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}"
```

Save as `.claude/tools/fork-and-rebrand.sh`, make executable, and run:
```bash
chmod +x .claude/tools/fork-and-rebrand.sh
./.claude/tools/fork-and-rebrand.sh "MySystemName" "my-github-username"
```

---

**Document Version:** 1.0
**Created:** 2025-10-29
**Status:** Active
**Replaces:** system-name-migration-guide-2025-10-16.md
**Maintained By:** HAL8000-Assistant Project

---
