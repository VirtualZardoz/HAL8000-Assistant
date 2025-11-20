---
name: HAL-fork-rebrand
description: Fork and rebrand HAL8000-Assistant to create your own independent system
parameters:
  - name: mode
    description: Execution mode (interactive | auto | verify)
    type: string
    required: false
---

# HAL-fork-rebrand

**Command Type:** System
**Category:** system/
**Level:** 3 - Control Flow (Production-Critical)
**Created:** 2025-11-09
**Version:** 1.0

---

## Purpose

Automate the complete Fork and Rebrand Protocol to transform a HAL8000-Assistant clone into an independent, personalized system with a new name and GitHub repository.

This command executes the comprehensive rebrand procedure documented in `data/architecture/fork-and-rebrand-protocol.md`, handling:
- Interactive collection of new system identity
- Filesystem updates (all paths, names, references)
- Git isolation and reconnection
- Verification and validation
- Safe operation preventing accidental commits to original HAL8000-Assistant

**Critical Safety:** This command ensures you CANNOT accidentally commit to anthropics/HAL8000-Assistant by reconfiguring git remotes and setting push-disable on upstream.

---

## Usage

```bash
# Interactive mode (recommended - prompts for all inputs)
/HAL-fork-rebrand

# Verification mode (check rebrand status without changes)
/HAL-fork-rebrand verify
```

**Parameters:**
- `mode` - (Optional) Execution mode:
  - `interactive` (default): Prompt user for system name and GitHub username, then execute full rebrand
  - `verify`: Check current rebrand status without making changes

---

## Variables/Parameters

**Input Variables:**
- `NEW_NAME` - string - New system name (e.g., "MyProjectAI", "HAL8001-Chapter")
- `NEW_GITHUB_USER` - string - GitHub username for new repository
- `NEW_GITHUB_REPO` - string - GitHub repository name (defaults to NEW_NAME)

**Configuration:**
- `execution_mode` - string - Determines workflow path (interactive | verify)
- `docker_rebuild` - boolean - Whether to rebuild Docker images (default: true if Dockerfiles exist)

**Output Variables:**
- `rebrand_status` - object - Complete status of rebrand operation
- `verification_results` - object - Validation results from each phase
- `old_references_count` - number - Count of remaining old references (should be 0 in active files)

---

## Instructions

**Multi-Phase Fork and Rebrand Workflow:**

### Phase 0: Pre-Flight Validation

**Before starting rebrand, verify prerequisites:**

1. **Check current system identity:**
   - Read `CLAUDE.md` to extract current system name
   - Read `.claude/state.json` to check for existing migration record
   - Determine if this is already a rebranded system

2. **Validate environment:**
   - Check git is installed: `git --version`
   - Check if in git repository: `git status`
   - Verify Docker installed if tools present: `docker --version`
   - Confirm current directory is system root (CLAUDE.md exists)

3. **Detect current state:**
   - If `state.json` contains `migration` field → Already rebranded
   - If git remote origin points to anthropics/HAL8000-Assistant → Needs rebrand
   - If neither → Unclear state, warn user

4. **Branch based on execution mode:**
   - If mode = "verify" → Skip to Phase 4 (Verification only)
   - If mode = "interactive" → Proceed to Phase 1
   - Else → Default to interactive mode

---

### Phase 1: Collect User Input

**Use AskUserQuestion to gather rebrand parameters:**

Ask user for new system identity using structured questions:

**Question 1: New System Name**
```
question: "What should your new system be named?"
header: "System Name"
options:
  - label: "Custom Name"
    description: "Enter a unique name for your system (e.g., MyProjectAI, PersonalClaude, HAL8001)"
```

**Question 2: GitHub Username**
```
question: "What is your GitHub username?"
header: "GitHub User"
options:
  - label: "Enter Username"
    description: "Your GitHub account username (e.g., johnsmith, my-org-name)"
```

**Question 3: GitHub Repository Strategy**
```
question: "How should we set up your GitHub repository?"
header: "Git Strategy"
options:
  - label: "Already Forked"
    description: "I've already forked HAL8000-Assistant on GitHub to my account"
  - label: "Need to Create"
    description: "I need to create a new GitHub repository (manual or via gh CLI)"
  - label: "Local Only"
    description: "Skip GitHub setup, work locally only (not recommended)"
```

**Question 4: Docker Image Rebuild**
```
question: "Should we rebuild Docker images with the new system name?"
header: "Docker"
options:
  - label: "Yes"
    description: "Rebuild diagram-generation and image-generation images (recommended if you use tools)"
  - label: "No"
    description: "Skip Docker rebuild (faster, but tools will use old names)"
```

**Store user responses:**
```
NEW_NAME = answer_to_question_1
NEW_GITHUB_USER = answer_to_question_2
GITHUB_STRATEGY = answer_to_question_3
DOCKER_REBUILD = answer_to_question_4 (yes/no)
```

**Derive additional variables:**
```
OLD_NAME = "HAL8000-Assistant"
OLD_PATH = "/mnt/d/~HAL8000-Assistant"  # Extract from current pwd
NEW_PATH = "/mnt/d/~${NEW_NAME}"
NEW_GITHUB_REPO = "${NEW_NAME}"  # Default to system name
OLD_DOCKER = "hal8000-mermaid:latest"
NEW_DOCKER = "$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')-mermaid:latest"
```

**Confirmation:**
Display summary and ask for final confirmation:
```
You are about to rebrand:
  OLD: HAL8000-Assistant → NEW: ${NEW_NAME}
  Path: ${OLD_PATH} → ${NEW_PATH}
  GitHub: anthropics/HAL8000-Assistant → ${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}

This will modify system files, git configuration, and Docker images.
This operation is SAFE but comprehensive.

Proceed? (yes/no)
```

If user says no → Abort with message "Rebrand cancelled by user."
If user says yes → Proceed to Phase 2

---

### Phase 2: Filesystem Rebrand

**Execute comprehensive filesystem updates using sed and find:**

#### 2.1: Critical Core Files (Sequential - Order Matters)

**BIOS (CLAUDE.md):**
```bash
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" CLAUDE.md
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" CLAUDE.md
sed -i "s/${OLD_DOCKER}/${NEW_DOCKER}/g" CLAUDE.md

# Verify changes
CLAUDE_CHECK=$(grep -c "${OLD_NAME}" CLAUDE.md)
if [ $CLAUDE_CHECK -ne 0 ]; then
  ERROR: "CLAUDE.md still contains old name!"
fi
```

**State File (.claude/state.json):**
```bash
# Backup first
cp .claude/state.json .claude/state.json.backup

# Update references
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .claude/state.json
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .claude/state.json

# Validate JSON syntax
cat .claude/state.json | jq . > /dev/null
if [ $? -ne 0 ]; then
  ERROR: "state.json syntax invalid - restoring backup!"
  cp .claude/state.json.backup .claude/state.json
  ABORT
fi

# Add migration metadata
jq --arg date "$(date -Iseconds)" \
   --arg from "${OLD_NAME}" \
   --arg to "${NEW_NAME}" \
   '.migration = {
     date: $date,
     from: $from,
     to: $to,
     type: "fork-and-rebrand",
     scope: "comprehensive",
     command: "HAL-fork-rebrand v1.0"
   }' .claude/state.json > .claude/state.json.tmp && mv .claude/state.json.tmp .claude/state.json
```

**Version Files:**
```bash
# Update VERSION
CURRENT_VERSION=$(cat VERSION)
NEW_VERSION="1.0.0-${NEW_NAME}"
echo "${NEW_VERSION}" > VERSION

# Prepend to CHANGELOG.md
cat > CHANGELOG.tmp << EOF
# Changelog

## [${NEW_VERSION}] - $(date +%Y-%m-%d)

### Changed
- Forked from HAL8000-Assistant and rebranded to ${NEW_NAME}
- Updated all system references and paths
- Reconfigured git remote to new repository
- System now independent from original HAL8000-Assistant
- Migration executed via /HAL-fork-rebrand command

$(cat CHANGELOG.md | tail -n +2)
EOF
mv CHANGELOG.tmp CHANGELOG.md
```

#### 2.2: Batch Update System Components

**Update all .claude/ subdirectories:**
```bash
# Commands
find .claude/commands -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/commands -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Agents
find .claude/agents -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/agents -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Skills
find .claude/skills -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/skills -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Indexes
find .claude/indexes -name "*.json" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/indexes -name "*.json" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Libraries
find .claude/libraries -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/libraries -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
find .claude/libraries -name "*.json" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +

# Tools
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "Dockerfile" \) \
  -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find .claude/tools -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "Dockerfile" \) \
  -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
```

#### 2.3: Configuration Files

```bash
# MCP configuration
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .mcp.json
sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .mcp.json

# Claude Code settings (if exists)
if [ -f .claude/settings.local.json ]; then
  sed -i "s/${OLD_NAME}/${NEW_NAME}/g" .claude/settings.local.json
  sed -i "s|${OLD_PATH}|${NEW_PATH}|g" .claude/settings.local.json
fi

# Environment files
find . -maxdepth 2 -name ".env*" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find . -maxdepth 2 -name ".env*" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +
```

#### 2.4: Documentation

```bash
# README.md (critical for GitHub)
sed -i "s/${OLD_NAME}/${NEW_NAME}/g" README.md
sed -i "s|anthropics/HAL8000-Assistant|${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}|g" README.md
sed -i "s|github.com/anthropics/HAL8000-Assistant|github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}|g" README.md

# Architecture docs
find data/architecture -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
find data/architecture -name "*.md" -type f -exec sed -i "s|${OLD_PATH}|${NEW_PATH}|g" {} +

# Research docs (preserve these - they're theoretical, not system-specific)
# SKIP research docs - they're about concepts, not this system

# Reference manual (if exists)
if [ -d data/reference-manual ]; then
  find data/reference-manual -name "*.html" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
  find data/reference-manual -name "*.md" -type f -exec sed -i "s/${OLD_NAME}/${NEW_NAME}/g" {} +
fi
```

#### 2.5: Docker Images (Conditional)

**If DOCKER_REBUILD = "yes":**
```bash
# Update Dockerfile references
find .claude/tools -name "Dockerfile" -type f -exec sed -i "s/${OLD_DOCKER}/${NEW_DOCKER}/g" {} +

# Rebuild diagram-generation image
if [ -f .claude/tools/diagram-generation/Dockerfile ]; then
  echo "Rebuilding diagram-generation Docker image as ${NEW_DOCKER}..."
  docker build -t ${NEW_DOCKER} .claude/tools/diagram-generation/

  # Verify image exists
  docker images | grep "${NEW_DOCKER}" || ERROR: "Docker image build failed!"
fi

# Rebuild image-generation image (if exists)
if [ -f .claude/tools/image-generation/Dockerfile ]; then
  NEW_IMAGE_DOCKER="$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')-image-gen:latest"
  echo "Rebuilding image-generation Docker image as ${NEW_IMAGE_DOCKER}..."
  docker build -t ${NEW_IMAGE_DOCKER} .claude/tools/image-generation/
fi
```

#### 2.6: System Log Append

```bash
# Append migration record to system log
cat >> .claude/system.log << EOF

=== SYSTEM FORK AND REBRAND ===
Date: $(date -Iseconds)
Command: /HAL-fork-rebrand v1.0
Original System: ${OLD_NAME}
New System: ${NEW_NAME}
Original Repository: https://github.com/anthropics/HAL8000-Assistant
New Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}
Migration Type: Fork and Rebrand
Scope: Comprehensive (filesystem + git + docker)
Status: Filesystem phase complete
EOF
```

**Report Phase 2 completion:**
```
✓ Phase 2 Complete: Filesystem Rebrand
  - Core files updated: CLAUDE.md, state.json, VERSION, CHANGELOG.md
  - System components updated: commands, agents, skills, indexes, libraries, tools
  - Configuration updated: .mcp.json, settings, .env files
  - Documentation updated: README.md, architecture docs
  - Docker images: [rebuilt | skipped]
  - System log: Migration recorded
```

---

### Phase 3: Git Isolation and Reconnection

**CRITICAL SAFETY PHASE: Prevent accidental commits to HAL8000-Assistant**

#### 3.1: Verify Current Git State

```bash
# Check current remote
CURRENT_ORIGIN=$(git remote get-url origin)
echo "Current git origin: ${CURRENT_ORIGIN}"

# Check if there are uncommitted changes from rebrand
GIT_STATUS=$(git status --porcelain)
if [ -z "$GIT_STATUS" ]; then
  echo "⚠ Warning: No uncommitted changes detected. Rebrand may not have modified files."
fi
```

#### 3.2: Commit Rebrand Changes

```bash
# Stage all changes
git add -A

# Create comprehensive rebrand commit
git commit -m "$(cat <<EOF
Fork and rebrand from HAL8000-Assistant to ${NEW_NAME}

This system is forked from HAL8000-Assistant and rebranded as an independent system.

Changes:
- Updated all system name references (HAL8000-Assistant → ${NEW_NAME})
- Updated all filesystem paths (${OLD_PATH} → ${NEW_PATH})
- Updated Docker image names (${OLD_DOCKER} → ${NEW_DOCKER})
- Updated documentation and README
- Reconfigured for independent operation
- Migration executed via /HAL-fork-rebrand command

Original: https://github.com/anthropics/HAL8000-Assistant
New System: ${NEW_NAME}
Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Verify commit succeeded
if [ $? -ne 0 ]; then
  ERROR: "Git commit failed! Rebrand changes not committed."
  ABORT
fi
```

#### 3.3: Reconfigure Git Remotes

**Branch based on GitHub strategy:**

**If GITHUB_STRATEGY = "Already Forked":**
```bash
# Update origin to point to user's fork
git remote set-url origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git

# Add upstream for pulling HAL8000-Assistant updates (push-disabled)
git remote add upstream https://github.com/anthropics/HAL8000-Assistant.git 2>/dev/null || \
  git remote set-url upstream https://github.com/anthropics/HAL8000-Assistant.git
git remote set-url --push upstream DISABLE

# Verify configuration
git remote -v
```

**If GITHUB_STRATEGY = "Need to Create":**
```bash
# Check if gh CLI is available
if command -v gh &> /dev/null; then
  # Attempt to create repo via gh CLI
  echo "Creating GitHub repository via gh CLI..."
  gh repo create ${NEW_GITHUB_REPO} --public --source=. --remote=origin \
    --description="Personalized HAL8000-Assistant-based system - von Neumann architecture, HAL-Script programming"

  if [ $? -ne 0 ]; then
    WARN: "gh repo create failed. Please create repository manually on GitHub."
    echo "Manual steps:"
    echo "1. Go to https://github.com/new"
    echo "2. Create repository: ${NEW_GITHUB_REPO}"
    echo "3. Run: git remote add origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git"
    # Don't abort - let user complete manually
  fi
else
  # No gh CLI - provide manual instructions
  echo "GitHub CLI (gh) not found. Please create repository manually:"
  echo "1. Go to https://github.com/new"
  echo "2. Repository name: ${NEW_GITHUB_REPO}"
  echo "3. Description: Personalized HAL8000-Assistant-based system"
  echo "4. Choose Public or Private"
  echo "5. Do NOT initialize with README (we already have one)"
  echo "6. Create repository"
  echo ""
  echo "Then run:"
  echo "  git remote add origin https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git"
  echo "  git push -u origin main"

  # Ask user to confirm when done
  read -p "Press ENTER when repository is created and remote is configured..."
fi

# Add upstream
git remote add upstream https://github.com/anthropics/HAL8000-Assistant.git 2>/dev/null || true
git remote set-url --push upstream DISABLE
```

**If GITHUB_STRATEGY = "Local Only":**
```bash
# Remove origin (work locally only)
git remote remove origin 2>/dev/null || true

# Add upstream as read-only
git remote add upstream https://github.com/anthropics/HAL8000-Assistant.git 2>/dev/null || true
git remote set-url --push upstream DISABLE

# Warn user
WARN: "Working in local-only mode. No GitHub repository configured."
WARN: "You can add a remote later with: git remote add origin <url>"
```

#### 3.4: Push to New Repository

**If GITHUB_STRATEGY != "Local Only":**
```bash
# Push rebrand commit to new repository
echo "Pushing to ${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}..."
git push -u origin main

if [ $? -ne 0 ]; then
  ERROR: "Git push failed! Check that:"
  echo "  - Repository exists at https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}"
  echo "  - You have push permissions"
  echo "  - Git credentials are configured"
  echo ""
  echo "You can manually push later with: git push -u origin main"
  # Don't abort - allow verification to continue
fi
```

#### 3.5: Verify Git Isolation

```bash
# Critical safety check: Ensure CANNOT push to HAL8000-Assistant
ORIGIN_URL=$(git remote get-url origin 2>/dev/null || echo "NONE")
UPSTREAM_PUSH=$(git remote get-url --push upstream 2>/dev/null || echo "NONE")

# Verify origin points to user's repo
if [[ "$ORIGIN_URL" == *"${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}"* ]]; then
  echo "✓ Git origin correctly configured"
else
  WARN: "Git origin does not point to your repository!"
  echo "  Expected: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}.git"
  echo "  Actual: ${ORIGIN_URL}"
fi

# Verify upstream push is disabled
if [ "$UPSTREAM_PUSH" == "DISABLE" ] || [ "$UPSTREAM_PUSH" == "NONE" ]; then
  echo "✓ Upstream push disabled (safe)"
else
  ERROR: "Upstream push NOT disabled! You could accidentally push to HAL8000-Assistant!"
  echo "  Run: git remote set-url --push upstream DISABLE"
fi
```

**Report Phase 3 completion:**
```
✓ Phase 3 Complete: Git Isolation and Reconnection
  - Rebrand changes committed
  - Git remote reconfigured: origin → ${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}
  - Upstream (HAL8000-Assistant) push-disabled: SAFE
  - Changes pushed to new repository: [success | manual required]
```

---

### Phase 4: Verification

**Comprehensive validation of rebrand success:**

#### 4.1: Search for Old References (Active Files)

```bash
echo "Checking for remaining ${OLD_NAME} references in active files..."

# Search all files EXCEPT historical sessions and logs
OLD_NAME_REFS=$(grep -r "${OLD_NAME}" \
  --exclude-dir=".claude/sessions" \
  --exclude-dir=".git" \
  --exclude="*.log" \
  --exclude="fork-and-rebrand-protocol.md" \
  --exclude="HAL-fork-rebrand.md" \
  --include="*.md" \
  --include="*.json" \
  --include="*.py" \
  --include="*.sh" \
  --include="*.html" \
  . 2>/dev/null | wc -l)

if [ $OLD_NAME_REFS -eq 0 ]; then
  echo "✓ Zero old name references in active files"
else
  WARN: "Found ${OLD_NAME_REFS} references to ${OLD_NAME} in active files!"
  echo "  Run this to see them:"
  echo "  grep -r '${OLD_NAME}' --exclude-dir='.claude/sessions' --exclude='*.log' ."
fi

# Search for old path references
OLD_PATH_REFS=$(grep -r "${OLD_PATH}" \
  --exclude-dir=".claude/sessions" \
  --exclude-dir=".git" \
  --exclude="*.log" \
  --exclude="fork-and-rebrand-protocol.md" \
  --exclude="HAL-fork-rebrand.md" \
  --include="*.md" \
  --include="*.json" \
  --include="*.py" \
  --include="*.sh" \
  . 2>/dev/null | wc -l)

if [ $OLD_PATH_REFS -eq 0 ]; then
  echo "✓ Zero old path references in active files"
else
  WARN: "Found ${OLD_PATH_REFS} references to ${OLD_PATH} in active files!"
fi
```

#### 4.2: Validate Core Files

```bash
# CLAUDE.md
CLAUDE_NEW=$(grep -c "${NEW_NAME}" CLAUDE.md)
CLAUDE_OLD=$(grep -c "${OLD_NAME}" CLAUDE.md)
if [ $CLAUDE_NEW -gt 0 ] && [ $CLAUDE_OLD -eq 0 ]; then
  echo "✓ CLAUDE.md updated correctly"
else
  ERROR: "CLAUDE.md validation failed! (new: ${CLAUDE_NEW}, old: ${CLAUDE_OLD})"
fi

# state.json
STATE_MIGRATION=$(cat .claude/state.json | jq -e '.migration' &>/dev/null && echo "yes" || echo "no")
STATE_VALID=$(cat .claude/state.json | jq . &>/dev/null && echo "yes" || echo "no")
if [ "$STATE_MIGRATION" == "yes" ] && [ "$STATE_VALID" == "yes" ]; then
  echo "✓ state.json has migration record and valid JSON"
else
  ERROR: "state.json validation failed! (migration: ${STATE_MIGRATION}, valid: ${STATE_VALID})"
fi

# VERSION
VERSION_CONTENT=$(cat VERSION)
echo "✓ VERSION file: ${VERSION_CONTENT}"

# CHANGELOG.md
CHANGELOG_NEW=$(head -20 CHANGELOG.md | grep -c "${NEW_NAME}")
if [ $CHANGELOG_NEW -gt 0 ]; then
  echo "✓ CHANGELOG.md updated"
else
  WARN: "CHANGELOG.md may not be updated"
fi

# README.md
README_GITHUB=$(grep -c "${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}" README.md)
if [ $README_GITHUB -gt 0 ]; then
  echo "✓ README.md references new repository"
else
  WARN: "README.md may not reference new repository"
fi
```

#### 4.3: Test Docker Images (Conditional)

**If DOCKER_REBUILD = "yes":**
```bash
# Check if new Docker images exist
DOCKER_IMAGES=$(docker images | grep "$(echo ${NEW_NAME} | tr '[:upper:]' '[:lower:]')" | wc -l)
if [ $DOCKER_IMAGES -gt 0 ]; then
  echo "✓ Docker images rebranded (${DOCKER_IMAGES} found)"
else
  WARN: "Docker images not found with new name"
fi
```

#### 4.4: Count Historical References

```bash
# Count historical references in sessions (these SHOULD exist)
HISTORICAL_REFS=$(grep -r "${OLD_NAME}" .claude/sessions/ --include="*.md" 2>/dev/null | wc -l)
echo "Historical ${OLD_NAME} references in sessions/: ${HISTORICAL_REFS}"
echo "✓ These are preserved intentionally (audit trail)"

# Update state.json with count
jq --arg count "${HISTORICAL_REFS}" \
   '.migration.historical_references_preserved = ($count | tonumber)' \
   .claude/state.json > .claude/state.json.tmp && mv .claude/state.json.tmp .claude/state.json
```

#### 4.5: Compute Verification Score

```bash
# Calculate success score (out of 8 critical checks)
SCORE=0
[ $OLD_NAME_REFS -eq 0 ] && ((SCORE++))
[ $OLD_PATH_REFS -eq 0 ] && ((SCORE++))
[ $CLAUDE_NEW -gt 0 ] && [ $CLAUDE_OLD -eq 0 ] && ((SCORE++))
[ "$STATE_MIGRATION" == "yes" ] && ((SCORE++))
[ "$STATE_VALID" == "yes" ] && ((SCORE++))
[ $CHANGELOG_NEW -gt 0 ] && ((SCORE++))
[ $README_GITHUB -gt 0 ] && ((SCORE++))
[[ "$ORIGIN_URL" == *"${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}"* ]] && ((SCORE++))

echo ""
echo "Verification Score: ${SCORE}/8"

if [ $SCORE -eq 8 ]; then
  echo "✅ Perfect score - Rebrand fully successful!"
elif [ $SCORE -ge 6 ]; then
  echo "✓ Rebrand mostly successful - review warnings above"
else
  echo "⚠ Rebrand incomplete - review errors above"
fi
```

**Report Phase 4 completion:**
```
✓ Phase 4 Complete: Verification
  - Active file references: ${OLD_NAME_REFS} old name, ${OLD_PATH_REFS} old path (target: 0)
  - Core files validated: CLAUDE.md, state.json, VERSION, CHANGELOG, README
  - Docker images: [validated | skipped]
  - Historical references preserved: ${HISTORICAL_REFS} (intentional)
  - Verification score: ${SCORE}/8
```

---

### Phase 5: Completion Report and Next Steps

**Generate comprehensive completion report:**

```
════════════════════════════════════════════════════════════════
  HAL8000-Assistant Fork and Rebrand Complete
════════════════════════════════════════════════════════════════

Original System:  HAL8000-Assistant
New System:       ${NEW_NAME}
GitHub Repository: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}
Migration Date:   $(date)

Phases Completed:
  ✓ Phase 1: User input collected
  ✓ Phase 2: Filesystem rebrand executed
  ✓ Phase 3: Git isolation and reconnection
  ✓ Phase 4: Verification (score: ${SCORE}/8)
  ✓ Phase 5: Completion report

Success Criteria:
  ${[ $OLD_NAME_REFS -eq 0 ] && echo "✅" || echo "⚠"} Zero old name references in active files
  ${[ $OLD_PATH_REFS -eq 0 ] && echo "✅" || echo "⚠"} Zero old path references
  ${[ $CLAUDE_NEW -gt 0 ] && [ $CLAUDE_OLD -eq 0 ] && echo "✅" || echo "⚠"} CLAUDE.md updated
  ${[ "$STATE_MIGRATION" == "yes" ] && echo "✅" || echo "⚠"} state.json migration record
  ${[ $README_GITHUB -gt 0 ] && echo "✅" || echo "⚠"} README.md updated
  ${[[ "$ORIGIN_URL" == *"${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}"* ]] && echo "✅" || echo "⚠"} Git origin configured
  ✅ Git upstream push-disabled (SAFE)
  ${[ $HISTORICAL_REFS -gt 0 ] && echo "✅" || echo "⚠"} Historical audit trail preserved

════════════════════════════════════════════════════════════════
  Next Steps
════════════════════════════════════════════════════════════════

1. Verify GitHub Repository:
   - Visit: https://github.com/${NEW_GITHUB_USER}/${NEW_GITHUB_REPO}
   - Check that rebrand commit is visible
   - Update repository description and topics if needed

2. Test System Boot:
   - Restart Claude Code in this directory
   - System should boot as "${NEW_NAME}"
   - Run: /HAL-register-dump (should show new name)

3. Test Commands:
   - Run: /HAL-system-check
   - Run: /HAL-context-find "rebrand"
   - Verify tools work with new paths

4. Customize Your System:
   - Create custom commands in .claude/commands/
   - Add custom agents in .claude/agents/
   - Modify templates in .claude/libraries/internal/templates/
   - Add project data to data/projects/

5. Optional: Update GitHub Settings:
   - Add description: "Personalized HAL8000-Assistant-based system"
   - Add topics: claude-code, ai-architecture, hal8000, fork
   - Configure branch protection
   - Add collaborators

6. Optional: Set Upstream Sync Strategy:
   - To pull HAL8000-Assistant updates: git fetch upstream && git merge upstream/main
   - To work independently: git remote remove upstream
   - See: data/architecture/fork-and-rebrand-protocol.md

════════════════════════════════════════════════════════════════

Your system is now fully independent and ready for customization!

For complete details, see:
  data/architecture/fork-and-rebrand-protocol.md

════════════════════════════════════════════════════════════════
```

**Update system log with completion:**
```bash
cat >> .claude/system.log << EOF
Status: Complete
Verification Score: ${SCORE}/8
Completion Time: $(date -Iseconds)
EOF
```

**Final action:**
```
Command complete. System is now ${NEW_NAME}.
```

---

## Output Format

**Terminal Output Structure:**

```
/HAL-fork-rebrand

════════════════════════════════════════════════════════════════
  HAL8000-Assistant Fork and Rebrand
════════════════════════════════════════════════════════════════

[User prompts via AskUserQuestion]

Confirmation:
  OLD: HAL8000-Assistant → NEW: MySystemName
  Path: /mnt/d/~HAL8000-Assistant → /mnt/d/~MySystemName
  GitHub: anthropics/HAL8000-Assistant → myuser/MySystemName

Proceed? yes

────────────────────────────────────────────────────────────────
Phase 1: User Input Collected
  ✓ System name: MySystemName
  ✓ GitHub user: myuser
  ✓ Repository strategy: Already Forked
  ✓ Docker rebuild: yes

Phase 2: Filesystem Rebrand
  ✓ Core files updated
  ✓ System components updated
  ✓ Configuration updated
  ✓ Documentation updated
  ✓ Docker images rebuilt
  ✓ System log updated

Phase 3: Git Isolation and Reconnection
  ✓ Rebrand changes committed
  ✓ Git remote reconfigured
  ✓ Upstream push disabled
  ✓ Changes pushed to myuser/MySystemName

Phase 4: Verification
  ✓ Active file references: 0 old name, 0 old path
  ✓ Core files validated
  ✓ Docker images validated
  ✓ Historical references preserved: 47
  ✓ Verification score: 8/8

════════════════════════════════════════════════════════════════
  HAL8000-Assistant Fork and Rebrand Complete
════════════════════════════════════════════════════════════════
[Detailed completion report as shown in Phase 5]
════════════════════════════════════════════════════════════════
```

**Verify Mode Output:**

```
/HAL-fork-rebrand verify

════════════════════════════════════════════════════════════════
  Fork and Rebrand Status
════════════════════════════════════════════════════════════════

Current System Identity:
  Name: MySystemName (detected from CLAUDE.md)
  Path: /mnt/d/~MySystemName
  Origin: https://github.com/myuser/MySystemName.git

Migration Record:
  ✓ Found in state.json
  Date: 2025-11-09T14:30:00-08:00
  From: HAL8000-Assistant
  To: MySystemName
  Type: fork-and-rebrand
  Command: HAL-fork-rebrand v1.0

Verification Checks:
  ✅ Zero old name references in active files
  ✅ Zero old path references
  ✅ CLAUDE.md updated
  ✅ state.json migration record exists
  ✅ README.md references new repository
  ✅ Git origin configured correctly
  ✅ Git upstream push disabled (SAFE)
  ✅ Historical audit trail preserved (47 refs)

Verification Score: 8/8

✅ System is fully rebranded and operational.

════════════════════════════════════════════════════════════════
```

---

## Error Handling

### Error Type: Prerequisites Not Met

- **Detection:** git not installed, not in git repository, CLAUDE.md not found
- **Action:** Abort before making any changes
- **User message:** `"Error: Prerequisites not met. Ensure you're in HAL8000-Assistant root directory with git installed."`
- **Recovery:** None (command hasn't modified anything)
- **User action:** Install git, navigate to correct directory, try again

### Error Type: Already Rebranded

- **Detection:** state.json contains `migration` field
- **Action:** Stop and inform user
- **User message:** `"This system is already rebranded (from ${migration.from} to ${migration.to} on ${migration.date}). Use verify mode to check status."`
- **Recovery:** Suggest running in verify mode: `/HAL-fork-rebrand verify`
- **User action:** Use verify mode or skip command

### Error Type: JSON Syntax Error (state.json)

- **Detection:** `jq` fails to parse state.json after modification
- **Action:** Restore backup immediately
- **User message:** `"Error: state.json syntax invalid after update. Backup restored."`
- **Recovery:** Automatic restore from .claude/state.json.backup
- **User action:** Report issue, investigate what went wrong

### Error Type: Git Commit Failed

- **Detection:** `git commit` returns non-zero exit code
- **Action:** Report error, do NOT proceed to git push
- **User message:** `"Error: Git commit failed. Rebrand changes not committed. Check git status."`
- **Recovery:** Manual - user must resolve git issues
- **User action:** Run `git status`, fix issues, commit manually

### Error Type: Git Push Failed

- **Detection:** `git push` returns non-zero exit code
- **Action:** Continue to verification (push failure is not critical)
- **User message:** `"Warning: Git push failed. Repository may not exist or permissions incorrect. You can push manually later."`
- **Recovery:** Allow verification to proceed
- **User action:** Manually push with `git push -u origin main` after fixing issues

### Error Type: Docker Build Failed

- **Detection:** `docker build` returns non-zero exit code
- **Action:** Warn but continue (Docker is optional)
- **User message:** `"Warning: Docker image build failed. Tools may not work until images are rebuilt."`
- **Recovery:** Continue rebrand (Docker optional)
- **User action:** Manually rebuild images later or skip tools

### Error Type: Verification Failed (Score < 6)

- **Detection:** Verification score below threshold
- **Action:** Report detailed issues, mark rebrand as incomplete
- **User message:** `"Warning: Rebrand verification incomplete (score: ${SCORE}/8). Review errors above and fix manually."`
- **Recovery:** Provide remediation steps for each failed check
- **User action:** Fix reported issues, run verify mode again

### Graceful Degradation Strategy

```
Phase 1 error → Abort (no changes made)
Phase 2 error (core files) → Abort (restore backups)
Phase 2 error (components) → Continue with warning (non-critical)
Phase 3 error (commit) → Abort (don't push)
Phase 3 error (push) → Continue to verification (can push later)
Phase 4 error (verification) → Report but complete (user fixes manually)
```

---

## Examples

### Example 1: Complete Interactive Rebrand

**Scenario:** User has forked HAL8000-Assistant to their GitHub account and wants to rebrand

**Command:**
```bash
/HAL-fork-rebrand
```

**What happens:**
1. System detects HAL8000-Assistant identity from CLAUDE.md
2. Prompts user for:
   - New name: "MyProjectAI"
   - GitHub username: "johndoe"
   - Repository strategy: "Already Forked"
   - Docker rebuild: "Yes"
3. Shows confirmation summary
4. User confirms: "yes"
5. Executes filesystem rebrand:
   - Updates all files (CLAUDE.md, state.json, commands, agents, etc.)
   - Rebuilds Docker images
   - Records migration in state.json and system.log
6. Commits changes to git
7. Reconfigures git remote to johndoe/MyProjectAI
8. Pushes rebrand commit
9. Verifies all changes (8/8 score)
10. Displays completion report with next steps

**Output:**
```
✅ HAL8000-Assistant Fork and Rebrand Complete

Original System:  HAL8000-Assistant
New System:       MyProjectAI
GitHub Repository: https://github.com/johndoe/MyProjectAI

Verification Score: 8/8

Next Steps:
1. Visit: https://github.com/johndoe/MyProjectAI
2. Restart Claude Code
3. Test commands: /HAL-register-dump, /HAL-system-check
4. Customize your system!

Your system is now fully independent and ready for customization!
```

---

### Example 2: Verify Rebrand Status

**Scenario:** User wants to check if previous rebrand was successful

**Command:**
```bash
/HAL-fork-rebrand verify
```

**What happens:**
1. Loads current system identity from CLAUDE.md
2. Checks state.json for migration record
3. Scans for old references (active files)
4. Validates core files
5. Checks git remote configuration
6. Counts historical references
7. Computes verification score
8. Displays status report

**Output:**
```
════════════════════════════════════════════════════════════════
  Fork and Rebrand Status
════════════════════════════════════════════════════════════════

Current System Identity:
  Name: MyProjectAI
  Path: /mnt/d/~MyProjectAI
  Origin: https://github.com/johndoe/MyProjectAI.git

Migration Record:
  ✓ Found in state.json
  Date: 2025-11-09T14:30:00-08:00
  From: HAL8000-Assistant
  To: MyProjectAI

Verification Score: 8/8

✅ System is fully rebranded and operational.
```

---

### Example 3: Rebrand with Manual GitHub Repo Creation

**Scenario:** User doesn't have GitHub CLI, needs to create repository manually

**Command:**
```bash
/HAL-fork-rebrand
```

**User selections:**
- New name: "PersonalClaude"
- GitHub user: "janesmith"
- Repository strategy: "Need to Create"
- Docker: "No" (skip Docker rebuild)

**What happens:**
1. Collects user input
2. Executes filesystem rebrand
3. Commits changes
4. Detects no `gh` CLI
5. Displays manual instructions:
   ```
   GitHub CLI (gh) not found. Please create repository manually:
   1. Go to https://github.com/new
   2. Repository name: PersonalClaude
   3. Description: Personalized HAL8000-Assistant-based system
   4. Choose Public or Private
   5. Do NOT initialize with README
   6. Create repository

   Then run:
     git remote add origin https://github.com/janesmith/PersonalClaude.git
     git push -u origin main

   Press ENTER when repository is created and remote is configured...
   ```
6. Waits for user to press ENTER
7. Continues to verification
8. Completes with warning if push not done yet

**Output:**
```
✓ Phase 3 Complete: Git Isolation and Reconnection
  - Rebrand changes committed
  - Git remote configuration: MANUAL REQUIRED
  - Upstream push disabled: SAFE
  ⚠ Push to new repository: Manual required

[Completion report with manual push instructions]
```

---

## Dependencies

**Required Files:**
- `CLAUDE.md` - BIOS (must exist, command will abort if missing)
- `.claude/state.json` - Current state (must be valid JSON)
- `VERSION` - Version file
- `CHANGELOG.md` - Change history
- `README.md` - Documentation
- `.mcp.json` - MCP configuration
- `data/architecture/fork-and-rebrand-protocol.md` - Reference documentation

**Required Commands:**
None (this is a standalone command)

**Required Agents:**
None (executes directly without delegation)

**Required Tools:**
- Bash - File system operations (sed, find, grep, cat, jq)
- Read - Read files for validation
- Write - Not used (sed handles updates)
- AskUserQuestion - User input collection
- Git (external) - Version control operations
- Docker (external, optional) - Image rebuilds

**Required External Tools:**
- git - REQUIRED (version control)
- jq - REQUIRED (JSON processing)
- sed - REQUIRED (text replacement)
- find - REQUIRED (file discovery)
- grep - REQUIRED (text search)
- docker - OPTIONAL (only if rebuilding images)
- gh - OPTIONAL (GitHub CLI for repo creation)

**System Requirements:**
- RAM: ~40-50% during execution (moderate file operations)
- Current working directory: Must be system root (where CLAUDE.md exists)
- Git repository: Must be initialized
- File permissions: Write access to all system files

---

## Performance Considerations

**RAM Usage:**
- Estimated token cost: ~40-50K tokens
- User interaction: ~2-3K per question
- File operations: ~20-30K (reading files for validation)
- Output formatting: ~10-15K (completion report)
- RAM zone impact: SAFE → CAUTION (peaks during verification)
- Mitigation: Direct execution (no sub-agents), minimal file loading

**Execution Time:**
- Phase 1 (User input): ~2-3 minutes (user interaction)
- Phase 2 (Filesystem): ~30-60 seconds (sed/find operations)
- Phase 3 (Git): ~30-60 seconds (git operations, network for push)
- Phase 4 (Verification): ~20-30 seconds (grep/validation)
- Phase 5 (Report): ~5-10 seconds (output formatting)
- **Total: ~5-10 minutes** (mostly user interaction and git network)

**Docker Rebuild Time:**
- If Docker rebuild enabled: Add ~2-5 minutes per image
- Total with Docker: ~10-20 minutes

**Optimization Notes:**
- Uses batch find/sed operations (not file-by-file)
- Skips historical sessions during validation (intentionally preserved)
- Parallel-friendly sed operations (could parallelize if needed)
- Minimal RAM footprint (direct execution, no delegation overhead)

---

## Testing & Validation

### Test 1: Happy Path (Already Forked)

- Input: NEW_NAME="TestSystem", GITHUB_STRATEGY="Already Forked", DOCKER="No"
- Expected output:
  - All phases complete successfully
  - Verification score: 8/8
  - Git origin points to user's fork
  - Zero old references in active files
- Validation:
  - `grep -r "HAL8000-Assistant" . --exclude-dir=".claude/sessions" | wc -l` returns 0
  - `cat .claude/state.json | jq .migration.to` returns "TestSystem"
  - `git remote get-url origin` contains user's repository

### Test 2: Manual Repository Creation

- Input: NEW_NAME="ManualTest", GITHUB_STRATEGY="Need to Create", DOCKER="No"
- Expected output:
  - Displays manual instructions
  - Waits for user confirmation
  - Continues after user presses ENTER
  - Verification may show warning if push not done
- Validation:
  - Command doesn't abort (continues gracefully)
  - User can complete manually after command finishes

### Test 3: Verify Mode (Already Rebranded)

- Input: mode="verify" on already-rebranded system
- Expected output:
  - Displays current system identity
  - Shows migration record from state.json
  - Runs verification checks
  - Reports score
- Validation:
  - No modifications made to files
  - Score accurately reflects system state

### Test 4: Error Case (JSON Syntax Error)

- Setup: Manually corrupt state.json before running
- Expected output:
  - Phase 2 detects JSON error
  - Restores backup automatically
  - Aborts with error message
- Validation:
  - Original state.json restored
  - No partial changes committed

### Test 5: Edge Case (Local Only Mode)

- Input: GITHUB_STRATEGY="Local Only", DOCKER="Yes"
- Expected output:
  - Filesystem rebrand completes
  - Git remote removed or not configured
  - Warning about local-only mode
  - Docker images rebuilt
- Validation:
  - `git remote -v` shows no origin (or upstream only)
  - System works locally
  - Can add remote later manually

**Validation Checklist:**
- [ ] Interactive mode prompts all questions
- [ ] Filesystem rebrand updates all file types
- [ ] Git commit succeeds with proper message
- [ ] Git remote reconfigured correctly
- [ ] Upstream push disabled (SAFETY)
- [ ] Verification detects all issues
- [ ] Verify mode works without modifications
- [ ] Error handling restores backups
- [ ] Completion report accurate
- [ ] System boots correctly after rebrand

---

## Notes

**Design Decisions:**

1. **Direct Execution (No Sub-Agents):**
   - Rationale: Fork/rebrand is sequential, file-heavy operation
   - Sub-agents would add complexity without benefit
   - Direct bash operations are faster and simpler
   - RAM usage acceptable (~40-50%) for single-session completion

2. **Interactive by Default:**
   - Rationale: Users need to think about system name carefully
   - Prevents accidental rebrands with poor names
   - Allows verification of parameters before execution
   - Alternative: Could add "auto" mode reading from config file

3. **Batch Operations (find/sed):**
   - Rationale: Faster than file-by-file processing
   - More reliable (consistent replacements)
   - Less RAM (no need to load each file into context)
   - Trade-off: Less granular error reporting per file

4. **Git Safety (Upstream Push-Disable):**
   - Rationale: CRITICAL to prevent accidental HAL8000-Assistant commits
   - Upstream remote kept for pulling updates
   - Push explicitly disabled with DISABLE marker
   - This is the most important safety feature

5. **Historical Session Preservation:**
   - Rationale: Audit trail is valuable
   - Old names in sessions are INTENTIONAL (historical context)
   - Verification distinguishes active vs. historical
   - Users may want to reference old sessions

6. **Docker as Optional:**
   - Rationale: Not all users use diagram/image tools
   - Rebuilding images is slow (2-5 min per image)
   - Tools work with old names temporarily (not critical)
   - Users can rebuild later if needed

**Known Limitations:**

1. **WSL Path Assumption:**
   - Command assumes `/mnt/d/~` path structure
   - May need adjustment for different OS or mount points
   - Workaround: Command detects current pwd, paths are relative

2. **Single System Per Path:**
   - Assumes one system per directory
   - Can't have multiple systems in same location
   - Workaround: Use different parent directories

3. **No Undo:**
   - Once executed, rebrand is permanent
   - No built-in rollback command
   - Workaround: Git history preserves old state (git revert possible)

4. **Network Dependency (Git Push):**
   - Requires network for GitHub push
   - Push failure doesn't abort (graceful degradation)
   - Workaround: Manual push later, verify mode shows status

**Future Enhancements:**

1. **Config File Mode:**
   - Allow parameters from `.rebrand-config.json`
   - Enable scripted/automated rebrands
   - Useful for organizations forking multiple times

2. **Partial Rebrand:**
   - Option to rebrand only certain components
   - E.g., update paths but keep name
   - Useful for moving directories

3. **Rollback Command:**
   - `/HAL-fork-rollback` to undo rebrand
   - Use git history to revert to pre-rebrand state
   - Useful if rebrand has issues

4. **Multi-System Manager:**
   - Tool to manage multiple forked systems
   - Switch between systems easily
   - Track which is which

5. **Upstream Sync Command:**
   - `/HAL-sync-upstream` to pull HAL8000-Assistant updates
   - Handle merge conflicts intelligently
   - Preserve customizations

**Security Considerations:**

- Command modifies core system files (CLAUDE.md, state.json)
- Git remote reconfiguration could be malicious if parameters manipulated
- Backup state.json before modifications (implemented)
- Validate JSON after modifications (implemented)
- No external network calls except git push (minimal attack surface)

**Maintenance:**

- Update command when fork-and-rebrand-protocol.md changes
- Test with each HAL8000-Assistant version release
- Verify compatibility with new system components
- Update if file structure changes

---

## Related Documentation

- `data/architecture/fork-and-rebrand-protocol.md` - Complete protocol specification
- `data/architecture/hal8000-versioning-guide.md` - Version management
- `.claude/commands/README.md` - Command organization
- `CLAUDE.md` - BIOS with system architecture

---

## Metadata

**Version History:**
- v1.0 (2025-11-09) - Initial implementation
  - Complete fork and rebrand automation
  - Interactive user input collection
  - Comprehensive verification
  - Git safety features (upstream push-disable)
  - Verify mode for status checking

**Maintainer:** HAL8000-Assistant System
**Last Updated:** 2025-11-09
**Status:** Production
**Criticality:** High (modifies core system files and git configuration)

**Integration Points:**
- BIOS: Not referenced directly (command invoked manually)
- State: Creates `migration` field in state.json
- Index: Will be cataloged in command index
- Protocol: Implements `data/architecture/fork-and-rebrand-protocol.md`

---

**Template Version:** 1.0
**Template Level:** 3 - Control Flow (with Level 7 production enhancements)
**Usage:** Interactive fork and rebrand automation for HAL8000-Assistant clones
