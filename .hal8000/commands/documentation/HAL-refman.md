---
name: HAL-refman
description: Manage HAL8000-Assistant Reference Manual development across multiple sessions with intelligent context loading
parameters:
  - name: command
    description: Command to execute (section-id, next, status, export, diagrams, complete)
    type: string
    required: false
  - name: section-id
    description: Specific section ID to work on (required for 'complete' command)
    type: string
    required: false
---

# HAL-refman Command

**Purpose:** Manage HAL8000-Assistant Reference Manual development across multiple sessions with intelligent context loading.

**Usage:**
```bash
/HAL-refman [section-id]
/HAL-refman next
/HAL-refman status
/HAL-refman export
/HAL-refman diagrams
```

---

## Command Behavior

### Mode 1: Status Dashboard (No Arguments)
When invoked without arguments or with "status":

**Action:**
1. Load `data/reference-manual/index.html`
2. Parse all section metadata attributes
3. Display progress dashboard
4. Suggest next priority section

**Output Format:**
```
📖 HAL8000-Assistant Reference Manual - Development Status

Progress:
├─ Total Sections: [N]
├─ Complete: [N] ✅
├─ In Progress: [N] 🔄
├─ Draft: [N] 📝
└─ Estimated Completion: [X]%

Current Section: [section-name or None]
Last Updated: [timestamp from state.json]

Next Priority Sections:
1. [section-id] - [title] (Priority: 1, Est: XK tokens)
2. [section-id] - [title] (Priority: 2, Est: XK tokens)

💡 Recommended: /HAL-refman next
    or: /HAL-refman [section-id]
```

---

### Mode 2: Section Development (With Section ID)
When invoked with a section ID:

**Action:**
1. Load `data/reference-manual/index.html` (parse metadata only, minimal RAM)
2. Locate section by ID attribute
3. Parse section metadata:
   - `data-status`: current status
   - `data-sources`: required source files
   - `data-estimated-tokens`: context budget
   - `data-dependencies`: prerequisite sections
4. Check dependencies (warn if incomplete)
5. Extract hidden writing guidelines from `.meta-guidance` div
6. **Launch documentation-writer sub-agent** via Task tool with prompt:
   ```
   Write [doc_type] documentation for HAL8000-Assistant Reference Manual.

   Section: [section-title]
   Section ID: [section-id]

   Sources to read: [comma-separated file paths from data-sources]

   Format: html

   Guidelines:
   [paste complete .meta-guidance content]

   Return complete <section> HTML block with:
   - Section opening tag with all data-* attributes (data-status="complete", etc.)
   - <h2> with section title
   - <div class="meta-guidance"> (copy from input)
   - <div class="content"> with layered documentation
   - All visual placeholders using standard format
   - Section closing tag

   Use layered structure: overview (all audiences) → concepts (users+devs) → technical (devs only)
   Create diagram placeholders per VISUALS list in guidelines.
   ```
7. **Receive complete section HTML** from agent
8. **Replace section in index.html** with returned HTML
9. Update state.json: `reference_manual.completed++`, clear `in_progress`
10. Display completion status

**Output Format:**
```
📝 HAL-refman: Working on [Section Title]

Section ID: [section-id]
Status: DRAFT → IN_PROGRESS
Priority: [N]

Context Strategy:
├─ Main session: Lightweight (parse metadata only)
├─ Sub-agent: documentation-writer (isolated 200K context)
└─ RAM optimization: ~95% savings vs. direct approach

Writing Guidelines:
├─ Target: [brief description]
├─ Audience: [all three / specific]
├─ Key Points: [bullet list]
├─ Tone: [guidance]
└─ Visuals: [placeholder list]

Dependencies:
├─ [dependency-section] ✅ Complete
└─ [dependency-section] ⚠️ Incomplete (consider completing first)

🚀 Launching documentation-writer agent...
   (This will take a moment - agent has isolated 200K context)

[Agent completes work]

✅ Section complete and integrated!
   Progress: [N]/31 sections ([X]%)

💡 Next: /HAL-refman next
```

**Context Loading Strategy (Reduce and Delegate):**
- Main session: Only load `data/reference-manual/index.html` for metadata parsing (~2K tokens)
- Sub-agent: Loads all source files in isolated 200K context
- Integration: Replace section HTML with agent output (~1K tokens)
- **Total main session cost: ~3K tokens per section** (vs. ~10K direct approach)
- **RAM savings: ~70% per section, enables completing all 31 sections in one session**

---

### Mode 3: Auto-Select Next (Keyword: "next")
When invoked with "next":

**Action:**
1. Parse all sections
2. Filter: status="draft" AND priority is lowest number
3. Select first match
4. Execute Mode 2 with that section-id

**Fallback:**
- If no draft sections: Check for "in_progress" sections, offer to resume
- If all complete: Display congratulations, suggest "export"

---

### Mode 4: Export Final Document (Keyword: "export")
When invoked with "export":

**Action:**
1. Load `data/reference-manual/index.html`
2. Check: All sections status="complete"?
3. If incomplete: Display list of remaining sections, abort
4. If complete:
   - Strip all `data-*` attributes
   - Remove all `.meta-guidance` divs
   - Validate all internal links
   - Generate `data/reference-manual/HAL8000-Assistant-Reference-Manual-v[version].html`
   - Update state.json: `reference_manual.status = "complete"`

**Output Format:**
```
📦 Exporting HAL8000-Assistant Reference Manual

Validation:
├─ All sections complete: ✅
├─ Internal links valid: ✅
├─ Diagrams integrated: [N/N] ✅
└─ Metadata stripped: ✅

Generated: data/reference-manual/HAL8000-Assistant-Reference-Manual-v1.0.0.html
Size: [X]KB

🎉 Reference manual export complete!
```

---

### Mode 5: List Visual Placeholders (Keyword: "diagrams")
When invoked with "diagrams":

**Action:**
1. Load `data/reference-manual/index.html`
2. Extract all elements with class="diagram-placeholder"
3. Parse `data-diagram-id` attributes
4. List all placeholders with descriptions

**Output Format:**
```
🎨 Visual Placeholders in Reference Manual

Total: [N] diagrams pending

[Section: System Architecture]
├─ arch-overview: Architecture Overview
│   └─ Block diagram showing CPU/RAM/Storage
├─ data-flow: Data Flow Diagram
│   └─ Sequence diagram of fetch-decode-execute

[Section: Memory Architecture]
├─ memory-hierarchy: Memory Hierarchy
│   └─ Layered diagram of BIOS/RAM/Storage

💡 Develop diagrams separately, then integrate with:
   - SVG inline or <img> tag
   - Replace placeholder <figure> elements
```

---

### Mode 6: Mark Section Complete (Keyword: "complete [section-id]")
When invoked with "complete [section-id]":

**Action:**
1. Load `data/reference-manual/index.html`
2. Locate section by ID
3. Update `data-status="complete"`
4. Update state.json: clear `in_progress`, increment `completed` counter
5. Save document
6. Display status dashboard

**Output Format:**
```
✅ Section Complete: [Section Title]

Updated Status:
├─ [section-id]: COMPLETE
├─ Total Complete: [N]/[Total]
└─ Progress: [X]%

Next Priority Section: [section-id] - [title]

💡 Continue: /HAL-refman next
```

---

## Section Metadata Schema

Each section in `reference-manual.html` must have:

```html
<section id="unique-section-id"
         data-status="draft|in_progress|complete"
         data-priority="1-5"
         data-sources="file1.md,file2.md:Section Title"
         data-estimated-tokens="8000"
         data-dependencies="other-section-id,another-section-id">

  <h2>Section Title</h2>

  <!-- Hidden metadata for command -->
  <div class="meta-guidance" style="display:none;">
    TARGET: [What this section explains]
    AUDIENCE: [All three / Specific audiences]
    KEY_POINTS: [Comma-separated key points]
    TONE: [Writing style guidance]
    VISUALS: [List of diagram placeholders]
  </div>

  <div class="content">
    <!-- Actual section content -->
  </div>
</section>
```

---

## State Tracking

The command updates `.claude/state.json`:

```json
{
  "reference_manual": {
    "version": "1.0.0",
    "file": "data/reference-manual/index.html",
    "total_sections": 25,
    "completed": 3,
    "in_progress": "architecture",
    "last_updated": "2025-10-08T12:00:00Z",
    "status": "in_development|complete"
  }
}
```

---

## Error Handling

**Missing reference-manual.html:**
```
❌ Error: Reference manual not found
Expected: data/reference-manual/index.html

Create skeleton first:
1. Define complete TOC
2. Add section metadata
3. Run: /HAL-refman status
```

**Invalid section ID:**
```
❌ Error: Section not found: [section-id]

Available sections:
- what-is-hal8000
- system-architecture
- [...]

Use: /HAL-refman status (to see all sections)
```

**Dependency not met:**
```
⚠️  Warning: Dependencies incomplete

Section [section-id] depends on:
├─ [dependency-1] ❌ DRAFT
└─ [dependency-2] ✅ COMPLETE

Recommendation:
- Complete dependencies first for logical flow
- Or proceed anyway (you can handle it)

Continue? [The command doesn't block, just warns]
```

---

## Design Principles

**Unix Philosophy:**
- Single command, one purpose (manage reference manual)
- Smart defaults (no args = show status)
- Composable (outputs suggest next commands)
- Text-based (HTML is text)

**Context Optimization:**
- Load only what's needed for current section
- Respect token budgets in metadata
- Offload completed work to storage

**Session Independence:**
- Any fresh Claude instance can run command
- All state in files (HTML + state.json)
- No hidden assumptions

---

## Execution Instruction

**CPU: When this command is invoked:**

1. **Parse arguments:** Determine mode based on input
2. **Load master document:** Always load `data/reference-manual/index.html` first
3. **Execute mode logic:** Follow mode-specific action steps above
4. **Update state:** Modify state.json as needed
5. **Display output:** Use format templates above
6. **Suggest next action:** Always guide user on what to do next

**Content Development Guidelines:**

When writing section content:
- **Visuals:** Use placeholder format for all diagrams/images (never attempt to generate actual images)
- **Placeholder Format:**
  ```html
  <figure class="diagram-placeholder" data-diagram-id="unique-id">
      <div class="placeholder-box">
          [DIAGRAM: Description]
          Description: Detailed explanation of what the diagram shows
          Type: Block diagram / Flowchart / Sequence diagram / etc.
          Tools: Draw.io or SVG
      </div>
  </figure>
  ```
- Check `.meta-guidance` VISUALS field for list of required placeholders
- Create one placeholder per visual mentioned
- Diagrams will be developed separately and integrated later

**Remember:** This command is your copilot for reference manual development. Trust the metadata in the HTML, load only what's specified, maintain session independence.

---

**Command Version:** 1.0.0
**Created:** 2025-10-08
**Status:** Active
