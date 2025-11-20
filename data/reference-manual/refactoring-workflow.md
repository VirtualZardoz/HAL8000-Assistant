# HAL8000-Assistant Reference Manual Refactoring Workflow

**Version:** 1.0
**Created:** 2025-10-10
**Status:** Active

## Purpose

This document defines the systematic workflow for refactoring the HAL8000-Assistant Reference Manual using Gemini CLI (1M context) orchestrated by Claude Code (CPU).

---

## Overview

**Role Division:**
- **User:** Strategic decisions, approval gates, quality validation
- **CPU (Claude):** Process orchestration, prompt crafting, Gemini execution, validation checks, iteration management
- **Gemini:** Bulk refactoring execution with comprehensive context

**Key Principle:** This workflow must survive session boundaries. All state is persisted to files.

---

## State Management

### State File: `refactoring-state.json`

Location: `/mnt/d/~HAL8000-Assistant/data/reference-manual/refactoring-state.json`

Structure:
```json
{
  "workflow_version": "1.0",
  "started": "2025-10-10T16:51:00Z",
  "last_updated": "2025-10-10T17:30:00Z",
  "current_phase": "phase1",
  "current_step": "validate",
  "phases": {
    "phase1": {
      "name": "Critical Fixes",
      "status": "in_progress",
      "tasks": [
        "Unify Register Architecture",
        "Consolidate Core Concepts",
        "Standardize Callout Boxes"
      ],
      "iterations": [
        {
          "iteration": 1,
          "timestamp": "2025-10-10T17:00:00Z",
          "prompt_file": "prompts/2025-10-10-1700-phase1-critical-fixes.txt",
          "output_manual": "refactored/2025-10-10-1700-phase1-manual.html",
          "changelog": "refactored/2025-10-10-1700-phase1-changelog.md",
          "validation_report": "refactored/2025-10-10-1700-phase1-validation.md",
          "status": "completed",
          "user_approval": "approved"
        }
      ],
      "completed": false
    },
    "phase2": {
      "name": "High Priority",
      "status": "pending",
      "tasks": [
        "Implement Critical/High Priority Visuals",
        "Refactor Inline Styles",
        "Complete Document Conventions"
      ],
      "iterations": [],
      "completed": false
    },
    "phase3": {
      "name": "Enhancement",
      "status": "pending",
      "tasks": [
        "Implement Remaining Visuals",
        "Improve Semantic HTML",
        "Minor Content Pruning"
      ],
      "iterations": [],
      "completed": false
    }
  },
  "current_manual": "refactored/current-manual.html",
  "notes": []
}
```

**Critical:** CPU MUST read this file on every session start when working on refactoring.

---

## Phase Workflow

Each phase follows: **PREPARE → EXECUTE → VALIDATE → ITERATE (if needed) → FINALIZE**

### 1. PREPARE

**CPU Actions:**
1. Read `refactoring-state.json` to understand current phase
2. Read `critiques/2025-10-10-1651-comprehensive-editorial-review.md` for task details
3. Draft refactoring prompt:
   - Context: What we're fixing and why
   - Scope: Specific sections to modify
   - Instructions: Detailed changes
   - Constraints: What NOT to change
   - Output format: Request change log + rationale
   - Validation checklist: How to verify success
4. Save prompt: `prompts/YYYY-MM-DD-HHMM-phaseN-description.md`
5. Present prompt to user for approval

**User Decision:** Approve prompt or request modifications

**State Update:** None (prompt saved to disk, awaiting approval)

---

### 2. EXECUTE

**CPU Actions:**
1. Read current manual version from state: `state.current_manual` or original `index.html`
2. Execute Gemini via PowerShell:
   ```bash
   powershell.exe -Command "Get-Content 'prompt-file', 'critique-file', 'current-manual' | gemini 'Refactor according to prompt' > 'output-manual' 2>&1"
   ```
3. Save outputs:
   - `refactored/YYYY-MM-DD-HHMM-phaseN-manual.html`
   - Extract change log from Gemini output → `refactored/YYYY-MM-DD-HHMM-phaseN-changelog.md`
4. Convert encoding if needed (UTF-16 → UTF-8)
5. Update state.json:
   - Add iteration entry with files
   - Set iteration status: "completed"
   - Update `last_updated` timestamp

**State Update:**
```json
{
  "phases": {
    "phase1": {
      "iterations": [
        {
          "iteration": 1,
          "timestamp": "2025-10-10T17:00:00Z",
          "prompt_file": "...",
          "output_manual": "...",
          "changelog": "...",
          "status": "completed",
          "user_approval": "pending"
        }
      ]
    }
  },
  "current_step": "validate"
}
```

---

### 3. VALIDATE

**CPU Actions:**
1. Read change log
2. Sample-check refactored manual:
   - Verify tasks from checklist
   - Check for unintended changes
   - Validate HTML structure
   - Spot-check cross-references
3. Generate validation report: `refactored/YYYY-MM-DD-HHMM-phaseN-validation.md`
   - ✅ Completed tasks
   - ⚠️ Issues found
   - 📊 Change statistics
   - 🔍 Specific examples
4. Present report to user

**User Decision:** Approve output, request corrections, or reject

**State Update:**
```json
{
  "phases": {
    "phase1": {
      "iterations": [
        {
          "iteration": 1,
          "validation_report": "refactored/2025-10-10-1700-phase1-validation.md",
          "user_approval": "pending"
        }
      ]
    }
  },
  "current_step": "awaiting_approval"
}
```

---

### 4. ITERATE (conditional)

**Triggered by:** User requests corrections

**CPU Actions:**
1. Create correction prompt based on user feedback
2. Save: `prompts/YYYY-MM-DD-HHMM-phaseN-corrections-vN.md`
3. Execute Gemini with correction prompt + current iteration output
4. Save new iteration outputs
5. Return to VALIDATE step

**State Update:** Add new iteration entry, increment iteration number

---

### 5. FINALIZE

**Triggered by:** User approves phase output

**CPU Actions:**
1. Promote approved manual to current:
   ```bash
   cp refactored/YYYY-MM-DD-HHMM-phaseN-manual.html \
      refactored/current-manual.html
   ```
2. Update state.json:
   - Mark iteration: `"user_approval": "approved"`
   - Mark phase: `"completed": true`
   - Update `current_manual` path
   - Advance `current_phase` to next phase
   - Set `current_step`: "prepare"

**State Update:**
```json
{
  "current_phase": "phase2",
  "current_step": "prepare",
  "phases": {
    "phase1": {
      "status": "completed",
      "completed": true,
      "iterations": [
        {
          "iteration": 1,
          "user_approval": "approved"
        }
      ]
    },
    "phase2": {
      "status": "in_progress"
    }
  },
  "current_manual": "refactored/2025-10-10-1700-phase1-manual.html"
}
```

---

## Session Recovery Protocol

**When CPU starts new session:**

1. Check if working on refactoring (user context or explicit request)
2. Read `/mnt/d/~HAL8000-Assistant/data/reference-manual/refactoring-state.json`
3. Report current state:
   ```
   📋 Refactoring Status
   ├─ Current Phase: phase1 (Critical Fixes)
   ├─ Current Step: awaiting_approval
   ├─ Last Iteration: 2025-10-10-1700
   ├─ Status: User approval pending for Phase 1
   └─ Next Action: [based on current_step]
   ```
4. Resume workflow at `current_step`:
   - `prepare`: Draft next prompt
   - `execute`: Execute pending prompt
   - `validate`: Generate validation report
   - `awaiting_approval`: Wait for user decision
   - `iterate`: Process correction request

---

## File Organization

```
data/reference-manual/
├── index.html                          # Original (never touched)
├── refactoring-workflow.md             # This file (workflow definition)
├── refactoring-state.json              # Current state (critical for recovery)
├── prompts/
│   ├── 2025-10-10-1651-comprehensive-editorial-review.md
│   ├── YYYY-MM-DD-HHMM-phase1-critical-fixes.md
│   ├── YYYY-MM-DD-HHMM-phase1-corrections-v2.md
│   ├── YYYY-MM-DD-HHMM-phase2-high-priority.md
│   └── YYYY-MM-DD-HHMM-phase3-enhancements.md
├── critiques/
│   └── 2025-10-10-1651-comprehensive-editorial-review.md
├── refactored/
│   ├── YYYY-MM-DD-HHMM-phase1-manual.html
│   ├── YYYY-MM-DD-HHMM-phase1-changelog.md
│   ├── YYYY-MM-DD-HHMM-phase1-validation.md
│   ├── YYYY-MM-DD-HHMM-phase2-manual.html
│   ├── YYYY-MM-DD-HHMM-phase2-changelog.md
│   ├── YYYY-MM-DD-HHMM-phase2-validation.md
│   ├── YYYY-MM-DD-HHMM-phase3-manual.html
│   ├── YYYY-MM-DD-HHMM-phase3-changelog.md
│   ├── YYYY-MM-DD-HHMM-phase3-validation.md
│   └── current-manual.html              # Latest approved version
└── final/
    └── index.html                       # Final published version (after all phases)
```

---

## Phase Definitions

### Phase 1: Critical Fixes
**Status:** Pending
**Priority:** Must complete before Phase 2
**Tasks:**
1. **Unify Register Architecture**
   - Establish Section 8 as single source of truth
   - Remove register definitions from Sections 1, 4, 7
   - Add cross-references to Section 8
2. **Consolidate Core Concepts**
   - Sub-agents/Virtual Memory: One authoritative section
   - RAM as Context/Performance Zones: One authoritative section
   - Von Neumann/Unix/Assembly: Section 3 as single source
   - All other mentions become summaries + links
3. **Standardize Callout Boxes**
   - Define CSS classes: `.callout-info`, `.callout-warning`, `.callout-technical`, `.callout-summary`
   - Replace all custom boxes (`.overview`, `.technical`, `.note`, etc.) with standard set
   - Update CSS stylesheet

**Validation Checklist:**
- [ ] Register definitions removed from Sections 1, 4, 7
- [ ] Section 8 register architecture intact
- [ ] All register mentions link to Section 8
- [ ] Sub-agent concept has one primary explanation
- [ ] RAM zones have one primary explanation
- [ ] Three philosophies refer to Section 3 only
- [ ] CSS defines standard callout classes
- [ ] All old callout classes replaced
- [ ] No broken HTML tags
- [ ] Table of contents accurate

### Phase 2: High Priority
**Status:** Pending
**Priority:** After Phase 1
**Tasks:**
1. **Implement Critical/High Priority Visuals**
   - Create placeholders or embedded diagrams for high-priority visuals from critique
2. **Refactor Inline Styles**
   - Remove all `style="..."` attributes
   - Create CSS classes in stylesheet
3. **Complete Document Conventions**
   - Update Section 4 with all UI patterns
   - Replace emoji symbols with accessible alternatives

**Validation Checklist:**
- [ ] High-priority visual placeholders added
- [ ] No inline styles remain
- [ ] All styles moved to CSS classes
- [ ] Section 4 documents all conventions
- [ ] No emojis in Symbolic Conventions table

### Phase 3: Enhancement
**Status:** Pending
**Priority:** After Phase 2
**Tasks:**
1. **Implement Remaining Visuals**
   - Add medium/low priority diagrams
2. **Improve Semantic HTML**
   - Use `<header>`, `<aside>`, `<article>` appropriately
3. **Minor Content Pruning**
   - Trim remaining minor redundancies

**Validation Checklist:**
- [ ] All visual enhancements complete
- [ ] Semantic HTML improved
- [ ] Content is concise and non-redundant

---

## Commands for CPU

### Check Status
```bash
cat data/reference-manual/refactoring-state.json | grep -E '"current_phase"|"current_step"|"status"'
```

### Resume Workflow
1. Read `refactoring-state.json`
2. Identify `current_phase` and `current_step`
3. Execute appropriate action

### Update State
Use `jq` or manual edit to update state.json after each step.

---

## User Commands

### Check Progress
"What's the refactoring status?"

### Approve Current Step
"Approved, proceed" or "Approve Phase N"

### Request Corrections
"Phase N needs corrections: [specific issues]"

### Skip Iteration
"Reject Phase N iteration, start fresh"

---

## Notes

- **All state in files:** Workflow survives RAM wipes
- **Incremental progress:** Each phase builds on previous
- **Full history:** Never delete intermediate versions
- **Transparent:** Change logs explain every modification
- **User control:** CPU cannot proceed without approval at key gates

---

**End of Workflow Definition**
