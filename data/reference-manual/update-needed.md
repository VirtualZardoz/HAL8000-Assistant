# Reference Manual Update Requirements
# Post-v1.7.0 Architecture Documentation Enhancements

**Date:** 2025-10-30
**Trigger:** BIOS updates + new feature-selection-guide.md
**Priority:** Medium (documentation consistency)
**Effort:** 2-3 hours

---

## Summary

The BIOS (CLAUDE.md) and new architecture guide (`data/architecture/feature-selection-guide.md`) introduce enhanced terminology and expanded frameworks that are not reflected in the reference manual (`data/reference-manual/index.html`). The manual requires updates to maintain consistency with the system's documented architecture.

---

## Changes That Created Impacts

### 1. BIOS Updates (CLAUDE.md)
- Added "progressive disclosure" terminology to Sub-Agent Protocol
- Expanded Three-Layer Intelligence Model with trigger mechanisms and trade-offs
- Enhanced Skills vs Commands vs Agents table (5 rows → 10 rows)
- Added 5-point Decision Framework
- Added video reference (`data/videos/i-finally-cracked-claude-agent-skills/knowledge-brief.md`)

### 2. New Architecture Guide Created
- Comprehensive 467-line guide: `data/architecture/feature-selection-guide.md`
- Decision trees, comparison tables, pitfalls, composition patterns
- 100% validation of HAL8000-Assistant features
- Quick reference card
- Extension guidelines

---

## Affected Reference Manual Sections

### ✅ Sections That Are Current (No Update Needed)

**Section 16: Agent Reference (lines 9592-10573)**
- ✅ Sub-agent as virtual memory concept - **Current**
- ✅ Output volatility constraint - **Well documented**
- ✅ Return summaries not raw data - **Clear**
- ✅ Agent architecture and delegation workflow - **Accurate**
- ✅ 60-90% RAM savings explanation - **Matches BIOS**

**Good news:** Agent documentation is comprehensive and doesn't need updates.

---

### ⚠️  Sections That Need Updates

#### **1. Section 17: Skills Reference (lines 10575+)**

**Current State:**
```html
<table>
  <thead><tr><th>Aspect</th><th>Skills</th><th>Commands</th><th>Agents</th></tr></thead>
  <tbody>
    <tr><td>Invocation</td><td>Automatic (CPU decides)</td>...</tr>
    <tr><td>Purpose</td>...</tr>
    <tr><td>RAM Impact</td>...</tr>
    <tr><td>Control</td>...</tr>
    <tr><td>Example</td>...</tr>
  </tbody>
</table>
```

**Issues:**
- ❌ Only 5 rows (BIOS now has 10 rows)
- ❌ Missing: Trigger Mechanism, Context Efficiency, Context Persistence, Modularity, Best For
- ❌ No Decision Framework (5-point checklist)
- ❌ No progressive disclosure terminology
- ❌ Three-layer diagram description uses old language

**Recommended Updates:**

**A. Expand Comparison Table**
Add 5 new rows matching BIOS:
- **Trigger Mechanism**: Agent-triggered by context | User-explicit action | CPU delegates heavy work
- **Context Efficiency**: High (progressive disclosure) | Varies | N/A (isolated context)
- **Context Persistence**: Yes (main session) | Yes (main session) | ❌ No (volatility by design)
- **Modularity**: High (dedicated directories) | Medium (HAL-Script files) | Medium (agent definitions)
- **Best For**: Repeat solutions, patterns | Critical workflows, state ops | Context isolation, parallel work

**B. Add Decision Framework Section**
After the comparison table, add:

```html
<h4>Decision Framework</h4>

<p>When creating new HAL8000-Assistant capabilities, use this systematic framework:</p>

<ol>
  <li><strong>Does agent need to trigger automatically?</strong> → Skill</li>
  <li><strong>Does user need explicit control?</strong> → Command (especially for state operations)</li>
  <li><strong>Need context isolation or protect main RAM?</strong> → Agent</li>
  <li><strong>Is it a repeat solution pattern?</strong> → Skill (high modularity)</li>
  <li><strong>Is it heavy processing (>30K intermediate data)?</strong> → Agent</li>
</ol>

<div class="insight-box">
  <strong>Deep Dive:</strong> For comprehensive guidance on feature selection,
  see <a href="../architecture/feature-selection-guide.html">Feature Selection Guide</a>
  with decision trees, validation tables, and composition patterns.
</div>
```

**C. Update Three-Layer Model Description**

Change from:
```
Skills - "I detect patterns and suggest"
Commands - "You control critical operations"
Agents - "I offload heavy work"
```

To:
```
Skills (Proactive) - Agent-triggered, context-efficient, modular
Commands (Explicit) - User-triggered, state operations, critical workflows
Agents (Delegated) - Context isolation, heavy processing, no persistence
```

**D. Add Progressive Disclosure Terminology**

After Skills introduction, add:

```html
<h4>Progressive Disclosure Pattern</h4>

<p>Skills implement a three-level progressive disclosure pattern for context efficiency:</p>

<ol>
  <li><strong>Level 1 (Metadata):</strong> Always loaded - skill name, description, trigger conditions (lightweight)</li>
  <li><strong>Level 2 (Instructions):</strong> Loaded when skill triggered - SKILL.md content</li>
  <li><strong>Level 3 (Resources):</strong> Loaded only when referenced - forms, schemas, scripts</li>
</ol>

<p>This prevents "context window explosion" where all capabilities load into RAM upfront
(like MCP servers), instead loading only what's needed when it's needed.</p>
```

---

#### **2. Section 15: Command Reference (lines 7608+)**

**Current State:**
- Commands documented with overview and specifications
- No comparison to Skills/Agents beyond basic differences

**Issues:**
- ❌ No cross-reference to decision framework
- ❌ No explanation of when Commands are preferred over Skills

**Recommended Updates:**

**A. Add "When to Use Commands" Section**

After Command System Overview:

```html
<h4>When to Use Commands vs. Skills</h4>

<p>Use Commands when:</p>
<ul>
  <li><strong>User should explicitly control triggering</strong> - Critical workflows requiring confirmation</li>
  <li><strong>State operations</strong> - Modifying system state (session-end, index updates)</li>
  <li><strong>Part of user workflow routine</strong> - Operations users invoke regularly</li>
  <li><strong>Context persistence required</strong> - Results must remain in main session</li>
</ul>

<p>Use Skills when agent should trigger automatically based on context detection.</p>

<p>See <a href="../architecture/feature-selection-guide.html">Feature Selection Guide</a>
for detailed comparison.</p>
```

---

#### **3. Section 11: User Guide - Using Skills/Commands/Agents (lines 5049+)**

**Current State:**
- Has "Running Commands" (11.1)
- Has "Using Agents" (11.3)
- Likely has basic skills usage

**Issues:**
- ❌ No unified decision framework reference
- ❌ May not explain when to use each type

**Recommended Updates:**

**A. Add Cross-Reference Section**

After Skills/Commands/Agents sections:

```html
<h3>11.4 Choosing the Right Feature Type</h3>

<p>HAL8000-Assistant provides three extensibility layers, each serving distinct purposes:</p>

<table>
  <thead>
    <tr><th>Feature Type</th><th>Use When</th><th>Example</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Skills</strong></td>
      <td>Agent should trigger automatically</td>
      <td>Context-awareness detects missing files</td>
    </tr>
    <tr>
      <td><strong>Commands</strong></td>
      <td>User needs explicit control</td>
      <td><code>/HAL-session-end</code> before RAM wipe</td>
    </tr>
    <tr>
      <td><strong>Agents</strong></td>
      <td>Need context isolation</td>
      <td>research-synthesizer for web research</td>
    </tr>
  </tbody>
</table>

<p><strong>Quick Decision:</strong></p>
<ol>
  <li>Agent triggers automatically? → Skill</li>
  <li>User triggers explicitly? → Command</li>
  <li>Context isolation needed? → Agent</li>
</ol>

<p>For comprehensive guidance, see <a href="../architecture/feature-selection-guide.html">
Feature Selection Guide</a>.</p>
```

---

#### **4. Section 8: Architecture Principles (Sub-Agent Protocol)**

**Current State:**
- Good volatility documentation
- Good virtual memory analogy

**Issues:**
- ❌ Missing "progressive disclosure" terminology in context of sub-agents

**Recommended Updates:**

**A. Add Progressive Disclosure Connection**

In Sub-Agent Protocol section:

```html
<h4>Progressive Disclosure via Isolation</h4>

<p>While Skills use progressive disclosure through three loading levels,
Sub-Agents achieve similar context efficiency through <strong>isolation</strong>:</p>

<ul>
  <li><strong>Main session:</strong> Lightweight metadata and control logic</li>
  <li><strong>Sub-agent:</strong> Heavy processing and data loading (isolated 200K RAM)</li>
  <li><strong>Return:</strong> Minimal summary (discarding intermediate data)</li>
</ul>

<p>Result: Main session RAM impact = summary size only (~2-5K tokens),
not full processing cost (50-150K tokens).</p>

<div class="insight-box">
  <strong>Pattern:</strong> Both Skills and Sub-Agents prevent "context window explosion" -
  Skills through progressive loading, Sub-Agents through isolation.
</div>
```

---

### 📚 New Content to Add

#### **1. New Section: Feature Selection Guide Reference**

**Location:** After Section 17 (Skills Reference) or in Appendix

```html
<h2>17.5 Feature Selection Guide</h2>

<p>The <a href="../architecture/feature-selection-guide.html">Feature Selection Guide</a>
provides comprehensive guidance for extending HAL8000-Assistant capabilities.</p>

<h3>What the Guide Covers</h3>

<ul>
  <li><strong>Quick Decision Tree:</strong> 4-question framework for rapid classification</li>
  <li><strong>Detailed Comparison:</strong> 8 dimensions comparing Skills/Commands/Agents</li>
  <li><strong>When to Use Each Type:</strong> Checklists with HAL8000-Assistant examples</li>
  <li><strong>Decision Frameworks:</strong> Trigger-first, Context-first, Use-case patterns</li>
  <li><strong>Architecture Validation:</strong> 100% validation of HAL8000-Assistant features</li>
  <li><strong>Common Pitfalls:</strong> Anti-patterns with solutions</li>
  <li><strong>Composition Patterns:</strong> How features work together</li>
  <li><strong>Extension Guidelines:</strong> 5-step process for new capabilities</li>
  <li><strong>Quick Reference Card:</strong> Copy-paste decision aid</li>
</ul>

<h3>When to Consult the Guide</h3>

<ul>
  <li>Creating new Skills, Commands, or Agents</li>
  <li>Unsure which feature type to use</li>
  <li>Reviewing feature selection decisions</li>
  <li>Understanding composition patterns</li>
  <li>Validating architecture compliance</li>
</ul>

<div class="reference-box">
  <strong>📖 External Resource:</strong>
  <a href="../architecture/feature-selection-guide.html">View Feature Selection Guide</a>
</div>
```

---

#### **2. Add to Appendix: Architecture Validation**

```html
<h2>Appendix C: Architecture Validation</h2>

<h3>Feature Classification Validation</h3>

<p>HAL8000-Assistant's features have been validated against Claude Code community best practices
(see <code>data/videos/i-finally-cracked-claude-agent-skills/knowledge-brief.md</code>).</p>

<h4>Validation Results</h4>

<table>
  <thead>
    <tr><th>Feature Category</th><th>Count</th><th>Validation</th></tr>
  </thead>
  <tbody>
    <tr><td>Skills</td><td>5</td><td>✅ 100% correctly classified</td></tr>
    <tr><td>Commands</td><td>13</td><td>✅ 100% correctly classified</td></tr>
    <tr><td>Sub-Agents</td><td>5</td><td>✅ 100% correctly classified</td></tr>
  </tbody>
</table>

<p><strong>Validation Framework:</strong> Trigger mechanism, context efficiency,
persistence requirements, modularity level, use case patterns.</p>

<p><strong>Reference:</strong> See Feature Selection Guide for complete validation tables
and decision criteria.</p>
```

---

## Priority Recommendations

### High Priority (Core Documentation Consistency)

1. **Update Section 17: Skills Reference comparison table** (5 rows → 10 rows)
2. **Add Decision Framework to Section 17** (5-point checklist)
3. **Add progressive disclosure terminology to Skills section**

### Medium Priority (Enhanced Guidance)

4. **Add "When to Use Commands" section to Command Reference**
5. **Add Feature Selection Guide reference section**
6. **Update Three-Layer Model descriptions with new language**

### Low Priority (Nice to Have)

7. **Add cross-reference in User Guide (Section 11)**
8. **Add progressive disclosure connection in Sub-Agent Protocol**
9. **Add Architecture Validation appendix**

---

## Implementation Strategy

### Option 1: Incremental Updates (Recommended)
**Approach:** Update sections one at a time, test each change
**Effort:** 2-3 hours total, can be spread across sessions
**Risk:** Low (changes are localized)

**Steps:**
1. Session 1: Update Skills Reference table + Decision Framework (1 hour)
2. Session 2: Add Feature Selection Guide references (30 min)
3. Session 3: Update Three-Layer Model descriptions (30 min)
4. Session 4: Add cross-references and validation (1 hour)

### Option 2: Comprehensive Rewrite
**Approach:** Update all sections in single session
**Effort:** 2-3 hours continuous
**Risk:** Medium (large diff, potential for inconsistencies)

### Option 3: Next Version Cycle (v1.8.0)
**Approach:** Bundle with next major reference manual update
**Effort:** Include in larger documentation overhaul
**Risk:** Low (planned maintenance window)

---

## Files to Update

### Primary Target
- `data/reference-manual/index.html` (13,000+ lines)

### Sections to Modify
- Lines ~10575-10850: Section 17 (Skills Reference)
- Lines ~7608-9590: Section 15 (Command Reference)
- Lines ~5049-5300: Section 11 (User Guide)
- Lines ~4480+: Sub-Agent Protocol sections

### New Sections to Add
- 17.5: Feature Selection Guide Reference (new)
- Appendix C: Architecture Validation (new)

---

## Impact Assessment

### If Updates Are NOT Done

**Risks:**
- ❌ Reference manual diverges from BIOS (authoritative source)
- ❌ Users may use outdated decision criteria
- ❌ New feature-selection-guide.md not discoverable from manual
- ❌ Progressive disclosure terminology inconsistent

**Severity:** Medium (documentation inconsistency, not functional bug)

### If Updates ARE Done

**Benefits:**
- ✅ Reference manual aligned with BIOS and industry best practices
- ✅ Users have comprehensive decision framework
- ✅ Feature selection guidance is discoverable
- ✅ Terminology consistent across all documentation

**Effort:** 2-3 hours (manageable in single session or spread across multiple)

---

## Recommended Next Actions

### Immediate (Current Session)
1. ✅ Document impacts (this file)
2. ✅ Commit this impact assessment with BIOS/guide changes

### Next Session (When Ready for Manual Update)
1. Start with High Priority updates (Skills Reference table + Decision Framework)
2. Test manual loads correctly after changes
3. Validate all internal links work
4. Run `/HAL-refman validate` if available

### Long-Term
1. Add to CHANGELOG.md: v1.7.1 - Documentation enhancement
2. Consider automating consistency checks (BIOS vs Manual)
3. Schedule periodic validation reviews

---

## References

### Source Files
- BIOS: `CLAUDE.md` (lines 164-185, 675-757)
- Feature Selection Guide: `data/architecture/feature-selection-guide.md` (467 lines, 21KB)
- Video Knowledge: `data/videos/i-finally-cracked-claude-agent-skills/knowledge-brief.md`

### Reference Manual Sections Affected
- Section 17: Skills Reference (lines 10575+)
- Section 15: Command Reference (lines 7608+)
- Section 16: Agent Reference (lines 9592+) - Already good
- Section 11: User Guide (lines 5049+)
- Section 8: Architecture Principles (Sub-Agent Protocol)

---

**Status:** Impact assessment complete
**Recommendation:** Proceed with incremental updates (Option 1) starting with High Priority items
**Effort Estimate:** 2-3 hours total, can be spread across multiple sessions
**Priority:** Medium (documentation consistency, not critical system function)
