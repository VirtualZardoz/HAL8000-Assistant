# Reference Manual Builder - Transfer Package

**Version:** 1.0.0
**Created:** 2025-10-21
**Source:** HAL8000 System

---

## What This Package Contains

This package provides a complete **reference manual building system** that can be transferred to any Claude Code instance. It enables systematic development of comprehensive technical documentation across multiple sessions.

### Components Included

```
refman-builder-package/
├── SETUP_GUIDE.md                    # This file
├── commands/
│   └── HAL-refman.md                 # Main command for manual management
├── agents/
│   └── documentation-writer.md       # Sub-agent for content generation
└── example/
    └── reference-manual-template.html # Working example/template
```

---

## Core Capabilities

### What You Get

1. **Session-Independent Manual Development**
   - Work across multiple sessions without losing progress
   - State tracked in files (HTML metadata + state.json)
   - Any Claude instance can pick up where you left off

2. **Intelligent Context Management**
   - Main session loads only metadata (~2-3K tokens per section)
   - Sub-agent handles heavy content writing in isolated context
   - RAM savings: ~70% per section vs. direct approach

3. **Structured Workflow**
   - Clear section status tracking (draft → in_progress → complete)
   - Priority-based development queue
   - Dependency checking between sections
   - Visual placeholder management

4. **Multiple Operation Modes**
   - Status dashboard: See overall progress
   - Section development: Write specific sections
   - Auto-select next: Automatically pick next priority section
   - Export: Generate final clean manual
   - Diagram tracking: List all visual placeholders

---

## Installation Instructions

### Step 1: Set Up Directory Structure

Create the following directories in your project:

```bash
# Create command directory
mkdir -p .claude/commands/documentation

# Create agent directory
mkdir -p .claude/agents

# Create manual storage directory
mkdir -p data/reference-manual
```

### Step 2: Install Components

Copy files from this package to your project:

```bash
# Install command
cp commands/HAL-refman.md .claude/commands/documentation/

# Install agent
cp agents/documentation-writer.md .claude/agents/

# (Optional) Copy example template to study structure
cp example/reference-manual-template.html data/reference-manual/
```

### Step 3: Create Your Manual Structure

Create `data/reference-manual/index.html` with your table of contents and section metadata.

**Option A: Start from Scratch**

Create a minimal HTML skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your Reference Manual</title>
    <style>
        /* Add your CSS here */
        .meta-guidance { display: none; }
        .diagram-placeholder { border: 2px dashed #ccc; padding: 20px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Your Reference Manual</h1>

    <!-- Add sections with metadata (see Section Metadata Schema below) -->

</body>
</html>
```

**Option B: Use the Template**

Study `example/reference-manual-template.html` to see a complete working example with:
- Proper section metadata structure
- Writing guidelines format
- Visual placeholder patterns
- Multiple section examples

### Step 4: Configure State Tracking

Add this to your `.claude/state.json`:

```json
{
  "reference_manual": {
    "version": "1.0.0",
    "file": "data/reference-manual/index.html",
    "total_sections": 0,
    "completed": 0,
    "status": "in_development"
  }
}
```

### Step 5: Verify Installation

Run the command in Claude Code:

```bash
/HAL-refman status
```

You should see a status dashboard showing your sections.

---

## Section Metadata Schema

Each section in your `index.html` must follow this structure:

```html
<section id="unique-section-id"
         data-status="draft"
         data-priority="1"
         data-sources="file1.md,file2.md"
         data-estimated-tokens="8000"
         data-dependencies="">

  <h2>Section Title</h2>

  <!-- Hidden metadata for the command (NOT visible in final export) -->
  <div class="meta-guidance" style="display:none;">
    TARGET: What this section explains
    AUDIENCE: Who reads this (e.g., "All three layers" or "Developers only")
    KEY_POINTS: Point 1, Point 2, Point 3
    TONE: Writing style (e.g., "Technical but accessible")
    STRUCTURE: Organization approach (e.g., "Layered: overview → concepts → technical")
    VISUALS: [DIAGRAM: Architecture overview], [DIAGRAM: Data flow]
  </div>

  <div class="content">
    <!-- Actual section content will go here -->
    <!-- Initially empty for draft sections -->
  </div>
</section>
```

### Metadata Field Reference

| Field | Values | Purpose |
|-------|--------|---------|
| `id` | Unique string | Section identifier (used in commands and cross-references) |
| `data-status` | `draft` \| `in_progress` \| `complete` | Current development status |
| `data-priority` | `1-5` | Development priority (1 = highest) |
| `data-sources` | Comma-separated paths | Files to read for content |
| `data-estimated-tokens` | Number | Estimated token cost for sources |
| `data-dependencies` | Comma-separated section IDs | Prerequisite sections (or empty) |

### Writing Guidelines Format

The `.meta-guidance` div contains instructions for the documentation-writer agent:

- **TARGET:** What concept/topic this section covers
- **AUDIENCE:** Who will read this (executives, users, developers, or "all three")
- **KEY_POINTS:** Essential topics to cover (comma-separated)
- **TONE:** Writing style (formal, instructional, conversational, etc.)
- **STRUCTURE:** Content organization (layered, sequential, reference-style, etc.)
- **VISUALS:** List of diagram placeholders to create (e.g., `[DIAGRAM: Title]`)

---

## Usage Guide

### Basic Workflow

**1. Check Status**
```bash
/HAL-refman status
```
Shows progress dashboard with completion stats and next priority sections.

**2. Work on Next Priority Section**
```bash
/HAL-refman next
```
Automatically selects and develops the highest-priority draft section.

**3. Work on Specific Section**
```bash
/HAL-refman architecture-overview
```
Develops a specific section by its ID.

**4. Track Visual Placeholders**
```bash
/HAL-refman diagrams
```
Lists all diagram placeholders that need to be created.

**5. Export Final Manual**
```bash
/HAL-refman export
```
Generates clean final version with metadata and guidelines stripped.

### Development Process

**Typical Session Flow:**

1. Start session → Load BIOS/state
2. Run `/HAL-refman status` to see progress
3. Run `/HAL-refman next` to work on next section
4. Command launches documentation-writer agent (isolated context)
5. Agent reads sources, writes content, returns complete HTML
6. Command integrates content into manual
7. Repeat steps 3-6 for multiple sections
8. End session with `/HAL-session-end` (if using HAL8000 system)

**Multi-Session Development:**

The system is designed for work across many sessions:

- Section status persists in HTML metadata
- State tracked in `state.json`
- Any fresh Claude instance can continue work
- No context carryover needed between sessions

---

## How It Works (Technical Overview)

### Context Optimization Architecture

The system uses a **"Reduce and Delegate"** pattern:

```
Main Session (Limited RAM)
  ↓
  Loads: index.html metadata only (~2K tokens)
  ↓
  Launches: documentation-writer agent
  ↓
Sub-Agent (Isolated 200K Context)
  ↓
  Loads: All source files
  Writes: Complete section content
  Returns: Clean HTML block (~1K tokens)
  ↓
Main Session
  ↓
  Integrates: Returned HTML into manual
  Updates: state.json
  Total Cost: ~3K tokens per section
```

**RAM Savings:** ~70% vs. loading sources directly in main session

### Command Processing Flow

When you run `/HAL-refman [section-id]`:

1. **Parse Arguments:** Determine operation mode
2. **Load Manual:** Read `index.html`, parse section metadata
3. **Extract Guidelines:** Get `.meta-guidance` content
4. **Check Dependencies:** Warn if prerequisite sections incomplete
5. **Launch Agent:** Invoke documentation-writer with:
   - Source file list
   - Writing guidelines
   - Output format requirements
6. **Receive Content:** Agent returns complete `<section>` HTML
7. **Integrate:** Replace section in `index.html`
8. **Update State:** Increment completion counter, update status
9. **Report:** Show progress and suggest next action

### Sub-Agent Operation

The documentation-writer agent:

- Operates in **isolated context** (separate from main session)
- Loads **only sources specified** in section metadata
- Writes **complete formatted content** following guidelines
- Returns **clean output** (HTML or Markdown)
- **Context is discarded** after completion

This prevents source files from polluting main session RAM.

---

## Customization

### Adapting for Your Project

**1. Modify Section Structure**

Edit the HTML template to match your needs:
- Add/remove sections
- Change priority order
- Adjust metadata fields
- Customize CSS styling

**2. Add Custom Guidelines**

Tailor `.meta-guidance` content for your documentation style:
- Different tone requirements
- Specific formatting standards
- Custom visual placeholder formats
- Domain-specific terminology

**3. Extend the Command**

The HAL-refman command can be modified:
- Add new operation modes
- Change status dashboard format
- Customize export process
- Add validation rules

**4. Use Different Formats**

While the example uses HTML, you can adapt for:
- Markdown (change format parameter)
- reStructuredText
- AsciiDoc
- Any text-based format

---

## Troubleshooting

### Command Not Found

**Symptom:** `/HAL-refman` shows "command not found"

**Solution:**
- Verify file location: `.claude/commands/documentation/HAL-refman.md`
- Check file naming (must start with `/` when invoked, but file has no `/`)
- Ensure YAML frontmatter is present with `name: HAL-refman`

### Agent Not Working

**Symptom:** Section development fails, agent doesn't launch

**Solution:**
- Verify agent file exists: `.claude/agents/documentation-writer.md`
- Check Task tool is available in your Claude Code instance
- Verify source files specified in metadata exist

### Sections Not Updating

**Symptom:** Content doesn't integrate into manual

**Solution:**
- Check section ID matches between command invocation and HTML
- Ensure `data-status` attribute exists
- Verify HTML is well-formed (closing tags, proper nesting)

### State Not Persisting

**Symptom:** Progress lost between sessions

**Solution:**
- Verify `.claude/state.json` exists and is writable
- Check JSON syntax is valid
- Ensure `reference_manual` section exists in state file

---

## Advanced Features

### Dependency Chains

Sections can depend on others:

```html
<section id="advanced-features"
         data-dependencies="basic-concepts,core-architecture">
```

The command will warn if dependencies aren't complete before working on this section.

### Token Budget Management

Set `data-estimated-tokens` to track context costs:

```html
<section id="large-section"
         data-estimated-tokens="15000">
```

This helps plan session work (avoid exceeding context limits).

### Multi-Audience Layering

Use guidelines to create layered documentation:

```
AUDIENCE: All three (executives, users, developers)
STRUCTURE: Layered: overview → concepts → technical details
```

The agent will structure content with progressive depth:
1. High-level overview (all audiences)
2. Conceptual explanation (users + developers)
3. Technical deep-dive (developers only)

### Visual Placeholder Tracking

The command tracks all diagram placeholders:

```bash
/HAL-refman diagrams
```

Shows all `[DIAGRAM: ...]` entries across all sections, helping you plan visual development separately.

---

## Integration with Other Systems

### HAL8000 Integration

If you're using the full HAL8000 system:

- Command is already installed
- Agent is already available
- State tracking is integrated
- Session continuity protocol works automatically

### Standalone Usage

This package works standalone without HAL8000:

- No dependency on HAL8000 architecture
- Works with any `.claude/state.json` format
- Can be adapted to any directory structure
- Portable across projects

### Custom Workflow Integration

The command can be invoked from:

- Other slash commands (composition)
- User typing directly
- Automated workflows
- External scripts (if state is managed externally)

---

## Examples

### Example 1: Simple Manual with 3 Sections

**Setup:**

```html
<section id="introduction" data-status="draft" data-priority="1" data-sources="README.md">
  <h2>Introduction</h2>
  <div class="meta-guidance" style="display:none;">
    TARGET: Project overview and goals
    AUDIENCE: All users
    KEY_POINTS: What it does, why it exists, who should use it
    TONE: Welcoming and clear
    STRUCTURE: Sequential: problem → solution → benefits
    VISUALS: None
  </div>
  <div class="content"></div>
</section>

<section id="getting-started" data-status="draft" data-priority="2" data-sources="docs/setup.md">
  <h2>Getting Started</h2>
  <div class="meta-guidance" style="display:none;">
    TARGET: Installation and first steps
    AUDIENCE: New users
    KEY_POINTS: Installation, configuration, first example
    TONE: Instructional, step-by-step
    STRUCTURE: Sequential tutorial
    VISUALS: [DIAGRAM: Installation flow]
  </div>
  <div class="content"></div>
</section>

<section id="api-reference" data-status="draft" data-priority="3"
         data-sources="src/api.js:100-500" data-dependencies="getting-started">
  <h2>API Reference</h2>
  <div class="meta-guidance" style="display:none;">
    TARGET: Complete API documentation
    AUDIENCE: Developers
    KEY_POINTS: Methods, parameters, return values, examples
    TONE: Technical reference
    STRUCTURE: Alphabetical reference format
    VISUALS: None
  </div>
  <div class="content"></div>
</section>
```

**Workflow:**

```bash
/HAL-refman next          # Writes introduction
/HAL-refman next          # Writes getting-started
/HAL-refman next          # Writes api-reference
/HAL-refman export        # Generate final manual
```

### Example 2: Large Manual with Priorities

**Setup:**

25 sections with varied priorities:
- Priority 1: Core concepts (5 sections)
- Priority 2: Feature documentation (10 sections)
- Priority 3: Advanced topics (7 sections)
- Priority 4: Appendices (3 sections)

**Workflow:**

```bash
# Session 1: Core concepts
/HAL-refman status        # See all 25 sections, 0 complete
/HAL-refman next          # Priority 1 section 1
/HAL-refman next          # Priority 1 section 2
/HAL-refman next          # Priority 1 section 3
# ... work until RAM caution zone
# End session

# Session 2: Continue
/HAL-refman status        # See 3/25 complete
/HAL-refman next          # Continues with remaining Priority 1
# ... work until RAM caution zone
# End session

# Session 3-5: Continue pattern
# ...

# Final session
/HAL-refman status        # See 25/25 complete
/HAL-refman diagrams      # List all placeholders
# Create diagrams separately
# Integrate diagrams into HTML
/HAL-refman export        # Generate final clean manual
```

---

## Performance Characteristics

### RAM Usage

**Per Section Development:**
- Main session: ~3K tokens (metadata + integration)
- Sub-agent: ~10-20K tokens (sources + writing, isolated)
- Total main session impact: ~3K tokens (70% savings)

**Full Manual Development (25 sections):**
- Traditional approach: 250K+ tokens (impossible in one session)
- This system: ~75K tokens (fits comfortably in one session)

### Time Estimates

- Status check: <1 second
- Section development: 30-60 seconds (depends on source size)
- Export: 2-5 seconds (validation + cleanup)
- Diagram listing: <1 second

### Scalability

**Tested With:**
- 32 sections (HAL8000 Reference Manual v1.2.0)
- 75,000 words total content
- 21 visual placeholders
- Multiple development sessions
- Full completion in production

**Theoretical Limits:**
- Up to ~60 sections per session (at 3K tokens each)
- No limit across multiple sessions
- Constrained only by HTML file size (reasonable until ~10MB)

---

## Best Practices

### Section Organization

1. **Start with core concepts** (Priority 1)
2. **Build foundation before advanced topics** (use dependencies)
3. **Group related sections** (easier to manage)
4. **Estimate tokens conservatively** (better to underestimate)

### Writing Guidelines

1. **Be specific in KEY_POINTS** (guides agent focus)
2. **Define AUDIENCE clearly** (affects complexity level)
3. **Specify VISUALS upfront** (plan diagram work separately)
4. **Use consistent TONE** (maintains manual coherence)

### Development Workflow

1. **Check status before starting** (know current state)
2. **Use `next` for batch work** (efficient priority-based flow)
3. **Use specific section-id for revisions** (targeted updates)
4. **Export only when 100% complete** (avoid incomplete exports)

### Session Management

1. **Monitor RAM usage** (stop before danger zone)
2. **Save state before ending session** (persistence)
3. **Document session progress** (external notes help)
4. **Plan diagram work separately** (visual development is different workflow)

---

## Frequently Asked Questions

### Can I use this without HAL8000?

**Yes.** This package is standalone. You only need:
- Claude Code
- `.claude/commands/` directory
- `.claude/agents/` directory
- `.claude/state.json` (simple JSON file)

### Can I modify the command?

**Yes.** The command is open for customization:
- Edit operation modes
- Change output formats
- Add new features
- Adapt to your workflow

### Does this work with Markdown?

**Yes.** Change `format: html` to `format: markdown` in guidelines and adapt the section structure. The agent supports both.

### How do I create the diagrams?

The system creates **placeholders only**. You create actual diagrams separately using:
- Draw.io
- SVG editors
- Mermaid (if you have diagram generation tools)
- Any visual design tool

Then integrate them into the HTML by replacing placeholder elements.

### Can multiple people work on the same manual?

**Yes, with coordination:**
- Manual is file-based (supports version control)
- Section status prevents conflicts (claim sections via status)
- State can be merged (standard JSON merge)
- Best practice: One person per section at a time

### What if a section needs major revision?

1. Change `data-status="complete"` back to `data-status="draft"`
2. Update `.meta-guidance` if needed
3. Run `/HAL-refman [section-id]` again
4. Agent rewrites the section
5. Status returns to "complete" after integration

---

## Version History

**v1.0.0** (2025-10-21)
- Initial transfer package
- HAL-refman command v1.0.0
- documentation-writer agent v1.0.0
- Complete example template included
- Tested with 32-section manual in production

---

## Credits

**Developed by:** HAL8000 System (https://github.com/VirtualZardoz/HAL8000)
**Architecture:** Modified von Neumann + Unix Philosophy
**Inspired by:** Technical documentation best practices, context optimization patterns

---

## Support

For issues, questions, or contributions:

1. Check this guide's Troubleshooting section
2. Review example template structure
3. Study command and agent files for implementation details
4. Verify all installation steps completed

---

## License

This package is part of the HAL8000 system. Check the main repository for license information.

---

**You now have everything needed to build comprehensive reference manuals with intelligent context management. Happy documenting!**
