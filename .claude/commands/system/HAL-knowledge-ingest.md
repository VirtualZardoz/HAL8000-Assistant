---
name: HAL-knowledge-ingest
description: Ingest knowledge and file it in the appropriate location with proper formatting
parameters:
  - name: source
    description: Content source (text, file path, or URL)
    type: string
    required: true
  - name: category_hint
    description: Optional category hint (research/architecture/library/project/tools/reference)
    type: string
    required: false
tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebFetch
  - SlashCommand
model: claude-sonnet-4-5
---

# HAL-knowledge-ingest

**Command Type:** System
**Category:** system/
**Level:** 2 - Workflow Prompt
**Created:** 2025-10-16
**Version:** 1.0

---

## Purpose

Intelligently ingest random knowledge and dispatch it to the appropriate location in the HAL8000-Assistant codebase with consistent formatting and organization.

**Problem Solved:**
- No manual decision about where to file knowledge
- Automatic classification and organization
- Consistent naming conventions
- Index updates
- Deduplication checks

---

## Usage

```bash
/HAL-knowledge-ingest "<content or path or URL>" [category_hint]
```

**Parameters:**
- `source` - (Required) One of:
  - Direct text content (in quotes)
  - Local file path to ingest
  - URL to fetch and ingest
- `category_hint` - (Optional) Force specific category: research | architecture | library | project | tools | reference

**Examples:**
```bash
/HAL-knowledge-ingest "https://example.com/article-on-caching"
/HAL-knowledge-ingest "/tmp/research-notes.md"
/HAL-knowledge-ingest "# Docker Best Practices\n\n..." architecture
```

---

## Variables/Parameters

**Input Variables:**
- `source` - string - Content, file path, or URL to ingest
- `category_hint` - string - Optional category override

**Output Variables:**
- `file_path` - string - Where the content was filed
- `category` - string - Detected/assigned category
- `related_files` - array - Related existing content found

---

## Instructions

**Multi-Step Workflow:**

### 1. **Content Acquisition**
Load the content based on source type:
- **Text**: Use content directly
- **File path**: Read file using Read tool (see Step 1.5 for document format detection)
- **URL**: Fetch using WebFetch tool with prompt: "Extract all content including title, main text, code examples, and metadata"

**Output:** Raw content ready for analysis

---

### 1.5. **Document Format Detection and Conversion** (NEW v1.1)

**If source is a file path, detect if it requires conversion:**

**Document formats requiring conversion:**
- **PDF** - `.pdf`
- **Office documents** - `.docx`, `.pptx`, `.xlsx`
- **Images with text** - `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp` (OCR needed)
- **Audio/Video** - `.mp3`, `.wav`, `.mp4`, `.avi` (transcription needed)
- **Other structured** - `.csv`, `.xml`

**Conversion Process (if document format detected):**

1. **Detect file extension:**
   ```bash
   # Check if file ends with document extension
   if [[ "$source" =~ \.(pdf|docx|pptx|xlsx|png|jpg|jpeg|gif|bmp|mp3|wav|mp4|avi|csv|xml)$ ]]
   ```

2. **Convert WSL path to Windows path:**
   ```bash
   WIN_PATH=$(wslpath -w "$source")
   OUTPUT_DIR="/tmp/docling-conversion"
   mkdir -p "$OUTPUT_DIR"
   WIN_OUTPUT=$(wslpath -w "$OUTPUT_DIR")
   ```

3. **Run docling conversion:**
   ```bash
   # Basic conversion (PDF, DOCX, PPTX, CSV, XML)
   powershell.exe -Command "docling '$WIN_PATH' --to md --output '$WIN_OUTPUT'"

   # Image with OCR
   if [[ "$source" =~ \.(png|jpg|jpeg|gif|bmp)$ ]]; then
     powershell.exe -Command "docling '$WIN_PATH' --to md --ocr --ocr-engine rapidocr --output '$WIN_OUTPUT'"
   fi

   # Audio/Video with transcription
   if [[ "$source" =~ \.(mp3|wav|mp4|avi)$ ]]; then
     powershell.exe -Command "docling '$WIN_PATH' --to md --pipeline asr --asr-model whisper_small --output '$WIN_OUTPUT'"
   fi
   ```

4. **Update source to converted file:**
   ```bash
   # Docling creates output with same base name + .md extension
   BASENAME=$(basename "$source" | sed 's/\.[^.]*$/.md/')
   CONVERTED_FILE="$OUTPUT_DIR/$BASENAME"
   source="$CONVERTED_FILE"
   ```

5. **Preserve original source in metadata:**
   - Store original file path for metadata footer
   - Note that content was converted via docling

**Error Handling:**
- If docling conversion fails:
  - Report error to user with docling output
  - Ask if user wants to: retry with different options, skip conversion, or cancel
  - Do not proceed with ingestion if conversion failed

**Output:** Source now points to converted Markdown file, ready for content analysis

**Tool Reference:** See `.claude/tools/docling-cli.md` for full docling documentation

---

### 2. **Content Analysis and Classification**

Analyze the content to extract:
- **Title**: Extract or generate from first heading or content
- **Content Type**: Detect document structure and purpose
- **Topics**: Identify main topics and keywords
- **Category**: Classify into one of the target categories

**Classification Logic:**

**Research** (`data/research/`):
- Contains theoretical explanations, academic concepts
- Has sections like Abstract, Introduction, Background, Conclusion
- Deep dive into a specific topic
- References to papers, research, fundamental concepts
- Keywords: "theory", "fundamental", "concept", "history of", "how X works"

**Architecture** (`data/architecture/`):
- System design documents, technical specifications
- Architecture Decision Records (ADRs)
- Design patterns, system diagrams
- Contains "Architecture", "Design", "System", "Specification"
- Keywords: "design", "architecture", "decision", "specification", "structure"

**Library** (`.claude/libraries/internal/`):
- Reusable code patterns, templates, utilities
- How-to guides for common tasks
- Code examples with explanations
- API references, usage patterns
- Keywords: "pattern", "template", "reusable", "utility", "helper"

**Tools** (`data/tools/` or `.claude/tools/`):
- Tool documentation, usage guides
- Installation instructions, configuration
- Command references, CLI guides
- Keywords: "install", "setup", "command", "tool", "utility"

**Reference** (`data/reference/`):
- Quick reference materials, cheat sheets
- Tables, condensed information
- Lookup guides, syntax references
- Keywords: "reference", "cheat sheet", "quick guide", "syntax"

**Project** (`data/projects/`):
- Project-specific documentation
- Implementation notes for specific projects
- Project plans, status updates
- Keywords: project names, "implementation", "status", "plan"

**Override:** If `category_hint` provided, use that category (validate it's a valid category).

---

### 3. **Deduplication Check**

Search for similar existing content:
- Use Grep to search for key terms from the title across relevant directories
- Check file names for similar slugs
- Report any related files found

**If similar content exists:**
- Report to user: "Similar content found: [paths]"
- Ask: "Proceed with filing, merge with existing, or cancel?"
- Wait for user confirmation

---

### 4. **Determine Target Location and Filename**

Based on category, determine:

**Research:**
- Location: `data/research/`
- Get next number: Use Glob tool with pattern `[0-9]*.md` in path `data/research/` to find all numbered files. Extract the leading number from each filename (e.g., "07-redis.md" → 7), find the maximum, then increment by 1 and pad to 2 digits.
- Filename: `[NN]-[slug].md` (e.g., `07-redis-internals.md`)

**Architecture:**
- Location: `data/architecture/`
- Filename: `[slug]-[YYYY-MM-DD].md` (e.g., `session-continuity-design-2025-10-16.md`)

**Library:**
- Location: `.claude/libraries/internal/`
- Determine subcategory (patterns, utilities, templates, guides)
- Filename: `[subcategory]/[slug].md` (e.g., `patterns/error-handling.md`)

**Tools:**
- Location: `data/tools/` (documentation) or `.claude/tools/[tool-name]/` (tool files)
- Filename: `[tool-name]-[topic].md` (e.g., `docker-best-practices.md`)

**Reference:**
- Location: `data/reference/`
- Filename: `[topic]-reference.md` (e.g., `bash-reference.md`)

**Project:**
- Location: `data/projects/[project-name]/`
- Detect or ask for project name
- Filename: `[topic].md` (e.g., `implementation-notes.md`)

**Slug generation:**
- Extract from title
- Lowercase, replace spaces with hyphens
- Remove special characters
- Max 50 characters

---

### 5. **Format Content with Metadata**

Prepare final file content with standardized frontmatter:

```markdown
---
title: [Extracted Title]
date_ingested: [YYYY-MM-DD]
source: [original source - URL, file path, or "direct input"]
category: [assigned category]
tags: [comma-separated keywords]
---

# [Title]

[Original content with any formatting cleanup]

---

**Metadata:**
- Ingested: [YYYY-MM-DD HH:MM:SS]
- Source: [source]
- Classification: [category] ([confidence: high/medium])
- Related: [list of related file paths if found]
```

**Content cleanup:**
- Preserve all original content
- Fix obvious formatting issues (extra newlines, broken lists)
- Ensure single H1 heading at top
- Add metadata footer

---

### 6. **Write File**

Write the formatted content to the determined location using Write tool.

**Directory creation:**
- If target directory doesn't exist, create it using Bash `mkdir -p`

**File verification:**
- After writing, use Read tool to verify file was written correctly
- Check file size is non-zero

---

### 7. **Update Indexes**

Update the file system indexes:
```bash
/HAL-index-update [directory path]
```

**Directories to update:**
- The specific directory where file was written
- Master index if needed

---

### 8. **Report Results**

Provide structured output to user:

```
✅ Knowledge Ingested Successfully

📁 Filed as: [full file path]
📂 Category: [category]
🏷️  Tags: [tags]
📊 Size: [file size]

🔗 Related Content:
  - [path 1]
  - [path 2]

💡 Next Actions:
  - Review filed content: [command to view]
  - Find related: /HAL-context-find "[topic]"
  - Update if needed: [edit command]
```

---

## Error Handling

**Invalid source:**
- Cannot read file: Report error, ask user to verify path
- Cannot fetch URL: Report error, check URL validity
- Empty content: Reject, ask for valid content

**Classification uncertainty:**
- If confidence is low (content doesn't clearly match any category):
  - Report ambiguity to user
  - Suggest 2-3 possible categories
  - Ask user to provide category_hint
  - Proceed only after confirmation

**Duplicate content:**
- If very similar content found:
  - Show user the existing files
  - Ask: file as new, merge, or cancel
  - Proceed only after confirmation

**Write failures:**
- Directory creation fails: Report error, check permissions
- File write fails: Report error, suggest alternative location
- Index update fails: Report warning, file still saved

---

## Output Format

**Success:**
```
✅ Knowledge Ingested Successfully

📁 Filed as: data/research/08-distributed-consensus.md
📂 Category: research
🏷️  Tags: distributed-systems, consensus, raft, paxos
📊 Size: 15.2 KB

🔗 Related Content:
  - data/research/03-distributed-systems-fundamentals.md
  - data/architecture/replication-strategy-2025-10-10.md

💡 Next Actions:
  - Review: Read data/research/08-distributed-consensus.md
  - Find related: /HAL-context-find "consensus"
```

**Classification uncertainty:**
```
⚠️  Classification Uncertain

Analyzed content could fit multiple categories:
1. research (confidence: 40%) - Contains theoretical explanations
2. architecture (confidence: 35%) - Has design patterns
3. library (confidence: 25%) - Includes code examples

Please specify category:
/HAL-knowledge-ingest "<source>" [research|architecture|library]
```

**Duplicate found:**
```
⚠️  Similar Content Detected

Found existing files:
  - data/research/05-caching-strategies.md (similarity: high)
  - data/architecture/cache-design-2025-09-15.md (similarity: medium)

Options:
1. File as new document (recommended if content is distinct)
2. Review existing files first
3. Cancel ingestion

Proceed? [y/n]
```

---

## Metadata

**Version History:**
- v1.0 (2025-10-16) - Initial implementation
- v1.1 (2025-10-16) - Added automatic document conversion via docling CLI (PDF, DOCX, PPTX, images with OCR, audio transcription)

**Status:** Production
**Template Level:** 2 - Workflow (sequential multi-step)

**Dependencies:**
- File system write access
- Index update command (/HAL-index-update)
- Web fetch capability (for URL sources)
- Docling CLI (for document conversion, see `.claude/tools/docling-cli.md`)

**Testing:**
- Test with direct text content
- Test with local file path (markdown/text files)
- Test with URL
- Test with PDF document conversion
- Test with DOCX/PPTX conversion
- Test with image OCR conversion
- Test with audio transcription
- Test category hint override
- Test deduplication detection
- Verify index updates
