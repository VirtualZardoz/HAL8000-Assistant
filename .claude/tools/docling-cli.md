# Docling CLI - Document Conversion Tool

**Category:** External Tool (Document Processing)
**Interface:** PowerShell CLI (accessible from WSL)
**Purpose:** Convert documents (PDF, DOCX, PPTX, etc.) to Markdown, JSON, HTML, or text
**Installation:** Host-installed (Python 3.13, pip)
**Path:** `C:\Users\Shahram-Dev\AppData\Local\Programs\Python\Python313\Scripts\docling.exe`
**Version:** Latest (check with `docling --version`)

---

## Overview

Docling is a powerful document processing tool that converts various document formats into clean, structured output. It's particularly valuable for ingesting external documents (PDFs, Office files, images) into the HAL8000-Assistant knowledge base.

**Architectural Position:**
```
Document (PDF/DOCX/PPTX/Image/etc)
    ↓ PowerShell CLI
Docling (OCR, table extraction, formatting)
    ↓ Markdown/JSON/HTML/Text output
HAL8000-Assistant (ingests processed content)
```

---

## Supported Formats

### Input Formats
- **PDF** - Portable Document Format
- **DOCX** - Microsoft Word documents
- **PPTX** - Microsoft PowerPoint presentations
- **HTML** - Web pages
- **Images** - PNG, JPG, etc. (with OCR)
- **AsciiDoc** - Lightweight markup
- **Markdown** - Existing markdown files
- **CSV** - Comma-separated values
- **XLSX** - Microsoft Excel spreadsheets
- **XML** - USPTO, JATS, METS-GBS variants
- **JSON** - Docling JSON format
- **Audio** - Audio files (with transcription)

### Output Formats
- **Markdown** - Clean, structured markdown (default, recommended for HAL8000-Assistant)
- **JSON** - Structured JSON with metadata
- **HTML** - HTML output (with optional page splitting)
- **Text** - Plain text extraction
- **DocTags** - Tagged document format

---

## Basic Usage Patterns

### Simple Conversion (PDF to Markdown)

```bash
powershell.exe -Command "docling input.pdf"
```

**Default behavior:**
- Converts to Markdown
- Output to current directory
- Embeds images as base64

### Specify Output Format

```bash
# Convert to JSON
powershell.exe -Command "docling input.pdf --to json"

# Convert to HTML
powershell.exe -Command "docling input.pdf --to html"

# Convert to plain text
powershell.exe -Command "docling input.pdf --to text"
```

### Specify Output Directory

```bash
# Convert and save to specific directory
powershell.exe -Command "docling input.pdf --output /output/directory"
```

### Multiple Input Files

```bash
# Convert all PDFs in directory
powershell.exe -Command "docling *.pdf"

# Convert specific files
powershell.exe -Command "docling file1.pdf file2.docx file3.pptx"
```

### Convert from URL

```bash
# Download and convert from URL
powershell.exe -Command "docling https://example.com/document.pdf"
```

---

## Advanced Features

### OCR (Optical Character Recognition)

**Enable OCR for images/scanned PDFs:**
```bash
powershell.exe -Command "docling input.pdf --ocr"
```

**Force OCR (replace existing text):**
```bash
powershell.exe -Command "docling input.pdf --force-ocr"
```

**Choose OCR engine:**
```bash
# Available: easyocr (default), ocrmac, rapidocr, tesserocr, tesseract
powershell.exe -Command "docling input.pdf --ocr --ocr-engine rapidocr"
```

**Specify OCR languages:**
```bash
powershell.exe -Command "docling input.pdf --ocr --ocr-lang en,fr,de"
```

### Image Export Modes

**Placeholder (position only, smallest output):**
```bash
powershell.exe -Command "docling input.pdf --image-export-mode placeholder"
```

**Embedded (base64 encoded, self-contained):**
```bash
powershell.exe -Command "docling input.pdf --image-export-mode embedded"
```

**Referenced (PNG files, separate directory):**
```bash
powershell.exe -Command "docling input.pdf --image-export-mode referenced"
```

### Table Extraction

**Fast mode (quicker processing):**
```bash
powershell.exe -Command "docling input.pdf --table-mode fast"
```

**Accurate mode (better quality, default):**
```bash
powershell.exe -Command "docling input.pdf --table-mode accurate"
```

### Content Enrichment

**Enable code block enrichment:**
```bash
powershell.exe -Command "docling input.pdf --enrich-code"
```

**Enable formula enrichment:**
```bash
powershell.exe -Command "docling input.pdf --enrich-formula"
```

**Enable picture classification:**
```bash
powershell.exe -Command "docling input.pdf --enrich-picture-classification"
```

**Enable picture descriptions:**
```bash
powershell.exe -Command "docling input.pdf --enrich-picture-description"
```

### Pipeline Selection

**Standard pipeline (default, balanced):**
```bash
powershell.exe -Command "docling input.pdf --pipeline standard"
```

**VLM pipeline (Vision Language Model, advanced):**
```bash
powershell.exe -Command "docling input.pdf --pipeline vlm --vlm-model smoldocling"
```

**ASR pipeline (Audio Speech Recognition, for audio files):**
```bash
powershell.exe -Command "docling input.audio --pipeline asr --asr-model whisper_tiny"
```

### Performance Options

**Number of threads:**
```bash
powershell.exe -Command "docling input.pdf --num-threads 8"
```

**Page batch size:**
```bash
powershell.exe -Command "docling input.pdf --page-batch-size 8"
```

**Document timeout:**
```bash
powershell.exe -Command "docling input.pdf --document-timeout 300.0"
```

**Device selection:**
```bash
# Auto-detect (default)
powershell.exe -Command "docling input.pdf --device auto"

# Force CPU
powershell.exe -Command "docling input.pdf --device cpu"

# Use CUDA GPU
powershell.exe -Command "docling input.pdf --device cuda"
```

### Debugging and Visualization

**Verbose output:**
```bash
# Info level
powershell.exe -Command "docling input.pdf -v"

# Debug level
powershell.exe -Command "docling input.pdf -vv"
```

**Visualize PDF cells:**
```bash
powershell.exe -Command "docling input.pdf --debug-visualize-cells"
```

**Visualize OCR cells:**
```bash
powershell.exe -Command "docling input.pdf --debug-visualize-ocr"
```

**Visualize layout clusters:**
```bash
powershell.exe -Command "docling input.pdf --debug-visualize-layout-clusters"
```

**Visualize table cells:**
```bash
powershell.exe -Command "docling input.pdf --debug-visualize-table-cells"
```

---

## Integration with HAL8000-Assistant

### Pattern 1: Direct Conversion for Ingestion

**Convert document then ingest:**
```bash
# Convert PDF to Markdown
powershell.exe -Command "docling /path/to/document.pdf --output /tmp"

# Ingest the converted markdown
/HAL-knowledge-ingest "/tmp/document.md"
```

### Pattern 2: Automatic Conversion in HAL-knowledge-ingest

**HAL-knowledge-ingest automatically detects document formats:**
```bash
# Automatically converts PDF before ingesting
/HAL-knowledge-ingest "/path/to/document.pdf"

# Also works with DOCX, PPTX, images, etc.
/HAL-knowledge-ingest "/path/to/presentation.pptx"
/HAL-knowledge-ingest "/path/to/scanned-doc.jpg"
```

### Pattern 3: WSL Path Conversion

**When working with WSL paths, convert to Windows paths:**
```bash
# WSL path
WSL_PATH="/mnt/d/~HAL8000-Assistant/data/documents/input.pdf"

# Convert to Windows path
WIN_PATH=$(wslpath -w "$WSL_PATH")

# Run docling with Windows path
powershell.exe -Command "docling '$WIN_PATH' --output 'D:\~HAL8000-Assistant\data\documents\output'"
```

### Pattern 4: Bulk Conversion

**Convert multiple documents in batch:**
```bash
# Create conversion script
cat > /tmp/convert-docs.sh <<'EOF'
#!/bin/bash
INPUT_DIR="/mnt/d/~HAL8000-Assistant/data/documents/input"
OUTPUT_DIR="/mnt/d/~HAL8000-Assistant/data/documents/converted"

for file in "$INPUT_DIR"/*.pdf; do
  WIN_INPUT=$(wslpath -w "$file")
  WIN_OUTPUT=$(wslpath -w "$OUTPUT_DIR")
  powershell.exe -Command "docling '$WIN_INPUT' --output '$WIN_OUTPUT'"
done
EOF

chmod +x /tmp/convert-docs.sh
/tmp/convert-docs.sh
```

---

## Common Use Cases

### Use Case 1: Research Paper Ingestion

```bash
# Convert academic PDF with formulas and tables
powershell.exe -Command "docling research-paper.pdf \
  --enrich-formula \
  --table-mode accurate \
  --image-export-mode referenced \
  --output /tmp"

# Ingest into HAL8000-Assistant
/HAL-knowledge-ingest "/tmp/research-paper.md" research
```

### Use Case 2: Technical Documentation

```bash
# Convert technical manual with code examples
powershell.exe -Command "docling manual.pdf \
  --enrich-code \
  --table-mode accurate \
  --to md \
  --output /tmp"

/HAL-knowledge-ingest "/tmp/manual.md" reference
```

### Use Case 3: Scanned Documents (OCR)

```bash
# Convert scanned PDF with OCR
powershell.exe -Command "docling scanned-doc.pdf \
  --ocr \
  --ocr-engine rapidocr \
  --ocr-lang en \
  --output /tmp"

/HAL-knowledge-ingest "/tmp/scanned-doc.md"
```

### Use Case 4: Presentation Slides

```bash
# Convert PowerPoint to Markdown
powershell.exe -Command "docling presentation.pptx \
  --image-export-mode embedded \
  --output /tmp"

/HAL-knowledge-ingest "/tmp/presentation.md" architecture
```

### Use Case 5: Image with Text (OCR)

```bash
# Extract text from image
powershell.exe -Command "docling screenshot.png \
  --ocr \
  --ocr-engine easyocr \
  --to md \
  --output /tmp"

/HAL-knowledge-ingest "/tmp/screenshot.md"
```

### Use Case 6: Audio Transcription

```bash
# Transcribe audio file
powershell.exe -Command "docling meeting-recording.mp3 \
  --pipeline asr \
  --asr-model whisper_small \
  --to md \
  --output /tmp"

/HAL-knowledge-ingest "/tmp/meeting-recording.md" project
```

---

## Best Practices

### 1. Choose Appropriate Output Format

**For HAL8000-Assistant ingestion:**
- **Markdown** (default) - Recommended, clean, preserves structure
- JSON - For structured data extraction and processing
- Text - For simple text content without formatting

### 2. Image Handling

**For small documents (< 10 images):**
- Use `--image-export-mode embedded` for self-contained output

**For large documents (> 10 images):**
- Use `--image-export-mode referenced` to keep file sizes manageable
- Images exported as separate PNG files

**For minimal output:**
- Use `--image-export-mode placeholder` if images not needed

### 3. OCR Considerations

**When to use OCR:**
- Scanned documents (no selectable text)
- Images containing text
- PDFs with poor text extraction

**OCR engine selection:**
- `easyocr` - Default, good balance of speed and accuracy
- `rapidocr` - Faster, good for large batches
- `tesseract` - Highest accuracy, slower

### 4. Performance Optimization

**For fast processing:**
```bash
--table-mode fast
--num-threads 8
--page-batch-size 8
--device cuda  # If GPU available
```

**For quality output:**
```bash
--table-mode accurate
--enrich-formula
--enrich-code
--ocr  # If needed
```

### 5. Path Handling in WSL

**Always convert WSL paths to Windows paths:**
```bash
# Good
WIN_PATH=$(wslpath -w "/mnt/d/file.pdf")
powershell.exe -Command "docling '$WIN_PATH'"

# Bad (won't work)
powershell.exe -Command "docling /mnt/d/file.pdf"
```

---

## Error Handling

### Common Errors

**File not found:**
```
ERROR: Cannot find file: /path/to/file.pdf
```
- **Cause:** Path not accessible from PowerShell
- **Fix:** Convert WSL path to Windows path with `wslpath -w`

**Unsupported format:**
```
ERROR: Unsupported input format
```
- **Cause:** File format not supported by docling
- **Fix:** Check supported formats list, convert file first

**OCR engine not available:**
```
ERROR: OCR engine 'tesseract' not found
```
- **Cause:** OCR engine not installed
- **Fix:** Use default `easyocr` or install missing engine

**Timeout:**
```
ERROR: Document processing timeout
```
- **Cause:** Large document exceeds default timeout
- **Fix:** Increase timeout with `--document-timeout 600.0`

### Recovery Strategies

**If conversion fails:**
1. Try with `--verbose -v` to see detailed errors
2. Simplify options (remove enrichments, use fast mode)
3. Try different pipeline: `--pipeline standard` vs `--pipeline vlm`
4. Check if file is corrupted (open manually)

**If output is poor quality:**
1. Enable OCR: `--ocr --ocr-engine rapidocr`
2. Use accurate table mode: `--table-mode accurate`
3. Enable enrichments: `--enrich-formula --enrich-code`
4. Try VLM pipeline: `--pipeline vlm`

---

## RAM Efficiency

**Docling runs in PowerShell (outside HAL8000-Assistant context):**
- ✅ **Zero RAM impact** on HAL8000-Assistant session
- ✅ Processing happens in separate process
- ✅ Only converted output loaded into HAL8000-Assistant RAM

**Comparison:**

| Method | RAM Impact |
|--------|-----------|
| Read PDF directly | Not possible (binary file) |
| Docling → Load Markdown | ~5-20K tokens (only converted text) |
| Manual copy-paste | ~5-20K tokens (but manual work) |

---

## Tool Discovery

Docling CLI is discoverable via:
1. **Tool index:** `.claude/indexes/tools.json`
2. **Direct path:** `.claude/tools/docling-cli.md` (this file)
3. **Context finder:** `/HAL-context-find docling` loads this doc

---

## Version & Maintenance

**Check version:**
```bash
powershell.exe -Command "docling --version"
```

**Update docling:**
```bash
powershell.exe -Command "pip install --upgrade docling"
```

**Check installed OCR engines:**
```bash
powershell.exe -Command "docling --logo"
```

**Show external plugins:**
```bash
powershell.exe -Command "docling --show-external-plugins --allow-external-plugins"
```

---

## Related Documentation

- **HAL-knowledge-ingest:** `.claude/commands/system/HAL-knowledge-ingest.md` - Automatic document ingestion
- **Gemini CLI:** `.claude/tools/gemini-cli.md` - External AI agent for heavy analysis
- **Docker CLI:** `.claude/tools/docker-cli.md` - Containerized tool execution

---

## Summary

Docling CLI enables HAL8000-Assistant to process documents in any format:
- **Universal converter** - PDF, DOCX, PPTX, images, audio → Markdown/JSON
- **OCR support** - Extract text from scanned documents and images
- **Advanced features** - Table extraction, formula enrichment, code highlighting
- **Zero RAM impact** - Runs in external PowerShell process
- **Seamless integration** - Works with HAL-knowledge-ingest for automatic ingestion

**Integration Pattern:**
```
Document (any format) → Docling CLI (convert) → Markdown → HAL-knowledge-ingest → Knowledge Base
```

This extends HAL8000-Assistant's ability to ingest knowledge from any document source, making the entire world of PDFs, Office documents, and images accessible to the system.
