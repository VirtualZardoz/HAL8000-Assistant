# HAL8000 Changelog

All notable changes to the HAL8000 system will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2025-10-23

### Added
- **AI Image Generation Tool** - External tool for visual content creation
  - **Location:** `.claude/tools/image-generation/`
  - **Engine:** ComfyUI + Stable Diffusion in Docker container (hal8000-image-gen:latest)
  - **GPU Support:** CUDA 12.1 with NVIDIA Docker runtime
  - **Architecture:** Mirrors diagram-generation pattern (proven external tool design)

  **Models Supported:**
  1. **SDXL** (6.5GB) - Best quality, recommended default
  2. **SD1.5** (4GB) - Faster generation, good quality
  3. **FLUX** (23GB) - Maximum quality, state-of-the-art model

  **Features:**
  - Zero RAM impact (external Docker process)
  - Persistent model caching in `.docker-cache/models/`
  - GPU-accelerated generation (~10-15s per image after model cached)
  - Automatic model downloading on first use
  - Volume mounts for model persistence and output storage

  **Files Included:**
  - `HAL-generate-image.py` - Python driver script (user interface)
  - `entrypoint.py` - Container entrypoint with ComfyUI integration
  - `Dockerfile` - NVIDIA CUDA 12.1 + Ubuntu 22.04 + ComfyUI
  - `requirements.txt` - Python dependencies
  - `build-image.sh` - Build script with directory setup
  - `README.md` - Technical documentation
  - `INSTALL.md` - Installation and setup guide
  - `QUICKSTART.txt` - Quick reference for users
  - `CLAUDE.md` - Integration guide for HAL8000 CPU
  - `image-generation-tool.md` - Architecture documentation

  **Storage Requirements:**
  - Docker image: ~3GB (C: drive)
  - SDXL model: 6.5GB (D: drive, cached)
  - SD1.5 model: 4GB (D: drive, optional)
  - FLUX model: 23GB (D: drive, optional)
  - Generated images: 1-5MB each (D: drive)

### Enhanced
- **CLAUDE.md (BIOS)** - Added image-generation tool to Tools (I/O Devices) section
- **Reference Manual** - Section 20 (External Tools) updated with image generation tool documentation

### Documentation
- Comprehensive tool documentation (5 markdown files + architecture doc)
- User guides for installation, usage, and troubleshooting
- Integration patterns for HAL8000 CPU (prompt enhancement, model selection)
- Performance expectations and storage requirements

### Technical Details
- **Pattern:** External tool (zero RAM impact on HAL8000 sessions)
- **Performance:** ~0.7s container startup + 3-8s generation (model cached)
- **First Run:** Additional 5-30 minutes for model download (one-time per model)
- **Cache Strategy:** Persistent volume mounts, models survive container restarts
- **GPU Requirement:** NVIDIA GPU with 8GB+ VRAM (tested on RTX 3090 24GB)

## [1.5.0] - 2025-10-20

### Added
- **Agent Skills Layer** - Proactive intelligence capabilities
  - **Location:** `.claude/skills/`
  - **Invocation:** Model-invoked (automatic, context-based activation)
  - **Architecture:** Three-layer intelligence model (Skills → Commands → Agents)
  - **Total Skills:** 4 production-ready Skills

  **Skills Implemented:**

  1. **context-awareness** - Detect missing context before answering
     - Triggers: User questions about code/files not in current RAM
     - Behavior: Ask for clarification instead of guessing or loading speculatively
     - Tools: Read, Glob, Grep, AskUserQuestion (read-only + questions)
     - Implements: Context Awareness Protocol from BIOS

  2. **architecture-consultant** - Validate design decisions
     - Triggers: Code reviews, design discussions, command creation
     - Behavior: Warn about violations of von Neumann, Unix, or Assembly principles
     - Tools: Read (read-only analysis)
     - Supporting file: `principles-reference.md` (quick reference guide)

  3. **hal-script-assistant** - Help write HAL-Script commands/agents
     - Triggers: Command creation, HAL-Script questions, template selection
     - Behavior: Guide template selection, generate code, validate structure
     - Tools: Read, Write, Edit, Glob
     - Integration: Works with command-builder agent and template library
     - Supporting file: `template-selector.md` (decision tree)

  4. **documentation-generator** - Create structured documentation
     - Triggers: User says "document this" or major milestone completed
     - Behavior: Generate session docs, decision logs, architecture docs, READMEs
     - Tools: Read, Write, Glob
     - Templates: 5 professional templates (session-doc, decision-log, architecture-doc, feature-doc, readme)

  **Supporting Files:**
  - Total files: 11 (4 SKILL.md + 7 supporting files)
  - Architecture consultant: `principles-reference.md`
  - HAL-Script assistant: `template-selector.md`
  - Documentation generator: 5 template files

### Enhanced
- **BIOS (CLAUDE.md)** - Agent Skills documentation
  - Updated Memory Architecture diagram with `.claude/skills/` directory
  - Updated Memory Components table with Skills entry
  - New "Agent Skills" section with complete documentation:
    - Three-layer intelligence model explanation
    - Skills catalog with triggers and behaviors
    - Skills vs. Commands vs. Agents comparison table
    - Activation conditions and invocation model

- **System State (state.json)** - Skills metadata tracking
  - New `agent_skills` section
  - Documents all 4 Skills with metadata
  - Tracks supporting files and integration points
  - Records design decision rationale (Skills 2 & 3 excluded for bandwidth efficiency)

### Design Decisions
- **Skills Scope** - Implemented Skills 1, 4, 5, 6 only
  - **Excluded:** Skills 2 (ram-guardian) and 3 (session-continuity)
  - **Rationale:** Skills 2/3 would evaluate constantly (high bandwidth). User already monitors RAM/sessions manually.
  - **Decision Date:** 2025-10-20

### Benefits
- **Proactive intelligence** - CPU detects patterns and suggests actions automatically
- **Collaborative control** - Skills complement (not replace) user control via Commands
- **Bandwidth-efficient** - Only context-triggered Skills, no constant evaluation
- **Consistent architecture** - Skills follow HAL8000 principles (Unix, von Neumann, Assembly)
- **Professional documentation** - Templated docs ensure consistent quality

### Technical Details
- **Skills:** 0 → 4
- **Three-layer model:** Skills (proactive) → Commands (explicit) → Agents (delegated)
- **File count:** 11 new files in `.claude/skills/`
- **BIOS sections added:** 3 (Memory Architecture, Memory Components, Agent Skills)
- **State tracking:** Complete metadata in state.json

## [1.4.0] - 2025-10-16

### Added
- **Docling CLI Integration** - Universal document conversion tool
  - **Location:** `.claude/tools/docling-cli.md`
  - **Purpose:** Convert documents (PDF, DOCX, PPTX, images, audio) to Markdown/JSON/HTML
  - **Features:**
    - Support for 15+ document formats (PDF, DOCX, PPTX, XLSX, images, audio, etc.)
    - OCR support for scanned documents and images (EasyOCR, RapidOCR, Tesseract)
    - Audio/video transcription (Whisper models)
    - Table extraction (fast/accurate modes)
    - Formula and code enrichment
    - Image export modes (placeholder/embedded/referenced)
    - WSL → PowerShell bridge for seamless access
  - **Access:** PowerShell CLI via `powershell.exe -Command "docling ..."`
  - **RAM Impact:** Zero (runs in external PowerShell process)
  - **Tool Documentation:** 26 sections, comprehensive usage patterns

### Enhanced
- **HAL-knowledge-ingest v1.1** - Automatic document conversion support
  - Added Step 1.5: "Document Format Detection and Conversion"
  - **Automatic conversion** for non-text formats:
    - PDF, DOCX, PPTX, XLSX → Markdown (via docling)
    - Images (PNG, JPG, etc.) → Markdown with OCR
    - Audio/Video (MP3, MP4, etc.) → Markdown with transcription
  - **Seamless integration:** Users can ingest any document format
  - **Preserves metadata:** Original file path tracked in ingested document
  - **Error handling:** Graceful fallback and user guidance on conversion failures
  - **Updated dependencies:** Added docling CLI as dependency
  - **Enhanced testing:** Added document conversion test scenarios

### Benefits
- **Universal document ingestion** - Ingest knowledge from any document format
- **No manual conversion** - Automatic detection and conversion via docling
- **Knowledge accessibility** - PDFs, Office docs, scanned images now accessible to HAL8000
- **Maintained simplicity** - Unix philosophy: docling tool + HAL-knowledge-ingest compose cleanly
- **Zero RAM impact** - Document processing happens in external process

### Technical Details
- **Tools:** 3 → 4 (docling-cli.md added)
- **Command versions:** HAL-knowledge-ingest 1.0 → 1.1
- **Supported formats:** 15+ document types now ingestible
- **Conversion patterns:** 3 modes (basic, OCR, transcription)
- **Architecture:** Tool composition (docling converts, HAL-knowledge-ingest organizes)

### Integration Pattern
```
Document (any format) → docling CLI (convert) → Markdown → HAL-knowledge-ingest → Knowledge Base
```

### Files Changed
- **Added:** `.claude/tools/docling-cli.md` (625 lines, comprehensive documentation)
- **Modified:** `.claude/commands/system/HAL-knowledge-ingest.md` (v1.1 with document conversion)
- **Modified:** `VERSION` (1.3.0 → 1.4.0)
- **Modified:** `CHANGELOG.md` (this file)

### Session
- Implementation: 2025-10-16 session
- Next: Update reference manual, update state.json

---

## [1.3.0] - 2025-10-16

### Added
- **HAL-knowledge-ingest Command** - Intelligent knowledge management system
  - **Location:** `.claude/commands/system/HAL-knowledge-ingest.md`
  - **Purpose:** Automatically ingest, classify, and file knowledge into appropriate locations
  - **Features:**
    - Multi-source input: Direct text, file paths, or URLs
    - Automatic content classification (research/architecture/library/tools/reference/project)
    - Smart deduplication checking
    - Consistent naming conventions by category
    - Metadata enrichment with frontmatter and tags
    - Index integration
    - Comprehensive error handling
  - **Level:** 2 - Workflow (sequential multi-step)
  - **Tool Usage:** Read, Write, Glob, Grep, Bash, WebFetch, SlashCommand
  - **Version:** 1.0 (optimized to 1.0.1 for Claude Code best practices)

### Changed
- **HAL-knowledge-ingest Optimization** - Claude Code best practices applied
  - Replaced bash `ls | grep` pattern with Glob tool for file discovery
  - Improved performance and alignment with Claude Code recommendations
  - Glob tool now explicitly utilized (was declared but unused)

### Documentation
- **System Name Migration Guide** ingested and filed
  - Location: `data/architecture/system-name-migration-guide-2025-10-16.md`
  - Comprehensive procedure for HAL8000 system name changes
  - Automated through first use of HAL-knowledge-ingest command

### Benefits
- No more manual decisions about where to file knowledge
- Consistent organization across codebase
- Automatic deduplication prevents redundancy
- Searchable metadata for all ingested content
- Unix philosophy: One command, one purpose (knowledge ingestion)

### Technical Details
- Commands: 10 → 11 (HAL-knowledge-ingest added)
- Tool optimization: bash commands → Glob tool for file discovery
- Classification logic: 6 categories with confidence scoring
- Deduplication: Grep-based similarity detection

### Session
- Implementation: Current session (2025-10-16)
- Testing: Successfully ingested test content and migration guide

---

## [1.2.0] - 2025-10-15

### Added
- **YAML Frontmatter Integration** - Claude Code best practices implemented system-wide
  - **All Commands Enhanced (10 files):** Added YAML frontmatter with name, description, and parameter specifications
    - Enhanced command palette integration
    - Parameter hints for improved user experience
    - Type specifications for validation
  - **All Agents Enhanced (3 files):** Added YAML frontmatter with tool whitelisting and model selection
    - `command-builder`: Tools limited to Read, Glob, Grep (Sonnet model)
    - `research-synthesizer`: Full research toolset documented (Sonnet model)
    - `hal-context-finder`: File system tools only (Haiku model for speed)
    - Security improvement via principle of least privilege
    - Performance optimization through explicit tool sets
  - **All Templates Updated (9 files):** Added frontmatter examples and guidance
    - Master template and all 7 level templates include frontmatter
    - Consistent pattern for future command generation

- **Comprehensive Documentation**
  - **Tool Reference:** `.claude/libraries/internal/tool-reference.md` (12KB)
    - Complete catalog of all available Claude Code tools
    - Standard tools (Read, Write, Bash, etc.)
    - MCP server tools (filesystem, omnisearch, IDE)
    - Common tool combinations for different agent types
    - Model selection guide (Haiku/Sonnet/Opus)
    - Tool selection best practices
  - **Template Guide Enhancement:** Added YAML Frontmatter section
    - What frontmatter is and why it matters
    - Required fields for commands and agents
    - Best practices for discoverability and security
    - Complete examples with tool specifications

### Changed
- **Prompt Template System** - Version bumped to 1.2
  - Phase 4 completed: Claude Code integration
  - All templates now demonstrate frontmatter usage
  - Lego Block principle extended to include frontmatter blocks

### Benefits
- Enhanced discoverability: Commands appear with descriptions in command palette
- Improved UX: Parameter hints guide users on command invocation
- Better security: Agents have explicit, minimal tool access
- Performance: Haiku model for fast operations (hal-context-finder)
- Documentation: Clear tool requirements for all agents
- Standardization: Consistent pattern across all commands and agents

### Technical Details
- Files modified: 22 (10 commands + 3 agents + 9 templates)
- New files created: 1 (tool-reference.md)
- Documentation updates: template-guide.md enhanced
- State tracking: yaml_frontmatter section added to state.json

### Session
- Implementation: `.claude/sessions/2025-10-15-1200-yaml-frontmatter-integration.md`

---

## [1.1.1] - 2025-10-15

### Fixed
- **Critical Boot Sequence Bug** - CPU now correctly executes Read tool during boot
  - **Issue:** CPU was generating boot acknowledgments without actually reading `.claude/state.json`
  - **Symptom:** Hallucinated session references (e.g., claimed "0448" session existed when it didn't)
  - **Root Cause:** CPU fabricated acknowledgment from unknown source instead of executing Read tool
  - **Fix Applied:** Enhanced BIOS (CLAUDE.md) with:
    - Visual urgency alerts (🚨🚨🚨 MANDATORY FIRST ACTION)
    - Moral framing ("DO NOT LIE ABOUT LOADING THIS FILE")
    - Explicit sequencing ("BEFORE DOING OR SAYING ANYTHING")
  - **Verification:** Fresh session test confirmed CPU now executes Read tool and cites actual values
  - **Impact:** Boot protocol integrity restored, prevents state hallucination
  - **Documentation:** `data/architecture/cpu-boot-protocol-fix-2025-10-15.md`

### Session
- Investigation: `.claude/sessions/2025-10-15-0753-boot-protocol-investigation.md`
- Verification: Current session (2025-10-15)

---

## [1.1.0] - 2025-10-14

### Added
- **HAL-Script Programming Language** - Formalized natural language programming paradigm
  - Complete language specification: `data/architecture/hal-script-language.md` (18KB)
  - Instruction hierarchy: tokens → sentences → paragraphs → sections → files → applications
  - Syntax documentation: imperatives, conditionals, loops, functions, error handling
  - Standard library reference: file operations, system operations, commands, agents
  - Programming examples: simple and complex programs
  - Best practices guide

- **Command Organization Guide** - `.claude/commands/README.md` (6.6KB)
  - Command directory structure explanation
  - HAL-Script introduction for command development
  - Command creation templates and patterns
  - Naming conventions and categorization
  - Composition and workflow design patterns

- **Hierarchical Command Structure** - Organized by purpose
  - `system/` - Core infrastructure (6 commands)
  - `development/` - Development tools (2 commands)
  - `documentation/` - Applications (1 command)

### Changed
- **Command Directory Reorganization** - Commands moved to subdirectories
  - Moved 9 commands from `.claude/commands/` to categorized subdirectories
  - Updated all file paths in indexes and documentation
  - Backward compatible: slash commands still work

- **BIOS Updates** - `CLAUDE.md` enhanced
  - Updated "Available Commands" section to reflect new organization
  - Added HAL-Script programming language introduction
  - Added references to new documentation
  - Updated Architecture References section

- **Command Index** - `.claude/indexes/commands.json` v3.0
  - Updated all file paths for reorganized structure
  - Added README.md and HAL-refman entries
  - Added programming_language metadata section
  - Incremented statistics: 8 → 10 files tracked

### Documentation
- `data/architecture/v1-1-0-changes-summary.md` - Complete change documentation
- All documentation is on-demand (not loaded at boot)
- Zero RAM impact on boot sequence

### Rationale
**HAL-Script Formalization:**
- Makes programming model explicit and teachable
- Enables users to create custom commands/programs
- Documents natural language as viable programming paradigm
- Provides reference for command composition and workflows

**Command Reorganization:**
- Improves discoverability and navigation
- Scales better as system grows
- Clear separation of concerns (infrastructure vs tools vs applications)
- Maintains backward compatibility

Session: `.claude/sessions/2025-10-14-HHMM-v1-1-0-hal-script-formalization.md`

---

## [1.0.0] - 2025-10-04

### Major Milestone
- **Production Release** - HAL8000 designated as production-ready
- All core architectural components complete
- Original vision achieved (100% gap analysis completion)

### Added
- **BIOS (CLAUDE.md)** - Boot sequence and operating principles
- **Modified von Neumann Architecture** - Harvard-like organization with self-modifying capabilities
- **Session Continuity** - RAM wipe recovery via state.json and session files
- **Register Architecture** - CPU state tracking (23 registers across 4 categories)
- **Hierarchical Indexing** - File system and library indexes for efficient discovery
- **Commands (6 total)**:
  - HAL-session-end
  - HAL-register-dump
  - HAL-system-check
  - HAL-index-update
  - HAL-library-update
  - HAL-context-find
- **Agents (4 total)**:
  - research-synthesizer
  - hal-context-finder
  - system-maintenance
  - claude-code-validator
- **MCP Integration** - omnisearch, filesystem, ide servers
- **Verified Boot Sequence** - BIOS → state.json → session management
- **Degraded Mode Operation** - Graceful handling of missing optional files
- **State Validation** - Inline validation prevents state drift
- **External Compatibility** - HAL-CC-check command validates Claude Code compatibility

### Architecture
- Memory hierarchy: BIOS-ROM (CLAUDE.md), State (state.json), Indexes, Sessions, Commands, Libraries, Data
- Operating principles: Modified von Neumann, Unix Philosophy, Assembly Language mapping
- Sub-agent protocol: Virtual memory extension for context-heavy tasks
- Resource management: RAM zones (SAFE/CAUTION/DANGER), selective loading, checkpoint protocol

### Documentation
- **HAL8000 Reference Manual v1.0.0** - Complete system documentation (31 sections)
- Architecture specifications in `data/architecture/`
- Research documents in `data/research/`
- Gap analysis report: `data/architecture/hal8000-v1-gap-analysis.md`

### Rationale
Version 1.0.0 warranted (not beta) based on:
- ✓ All planned components implemented
- ✓ Self-validation systems active
- ✓ State integrity guaranteed
- ✓ External compatibility verified
- ✓ Graceful degradation implemented
- ✓ Documentation complete
- ✓ Boot sequence verified
- ✓ Session continuity working
- ✓ Zero critical gaps

Session: `.claude/sessions/2025-10-04-1612-v1-0-0-production-release.md`

---

## Version History Summary

- **v1.0.0** (2025-10-04) - Production release, all core components complete

---

## Versioning Scheme

HAL8000 follows **Semantic Versioning 2.0.0**:

- **MAJOR** (X.0.0) - Architectural breaking changes (boot sequence redesign, memory model restructuring)
- **MINOR** (x.Y.0) - Backward-compatible additions (new commands, agents, tools)
- **PATCH** (x.x.Z) - Bug fixes and minor improvements

See `data/architecture/hal8000-versioning-guide.md` for detailed version bump criteria.
