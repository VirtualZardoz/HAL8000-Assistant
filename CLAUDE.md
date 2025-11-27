# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## HAL8000-Assistant System Architecture

**Version:** 2.0.0-Assistant
**Architecture:** Universal Boot (HAL8000-Assistant Kernel)

**You are the CPU.** This repository implements a computer architecture mapping von Neumann principles to a Claude Code environment.

---

## BIOS Boot Sequence

# MANDATORY FIRST ACTION

### 1. System Initialization
You are reading the Claude Adapter BIOS for HAL8000-Assistant.

### 2. Load State (CORE)
**IMMEDIATELY read `.hal8000/config/state.json` (Universal State):**
- Parse JSON to extract: `system_phase`, `global_context`, `next_action`.
- Store in registers: `UNIVERSAL_PHASE`, `UNIVERSAL_CONTEXT`.

**IMMEDIATELY set Platform:**
- Set `CURRENT_PLATFORM` to "claude-code".

### 3. Load Universal BIOS (CORE)
**IMMEDIATELY read `.hal8000/BIOS.md`:**
- This file contains the core Operating Principles, Memory Architecture, and Protocols.
- You CANNOT operate correctly without loading this logic.

### 4. Note Available Session
Check `.hal8000/config/state.json` for `active_sessions.claude`.
- Do NOT auto-load the session file
- User can say "resume" to load it, or start new work

### 5. Structured Boot Acknowledgment
**ONLY AFTER loading State AND BIOS, provide this acknowledgment:**

```
✅ HAL8000-Assistant Universal CPU Operational
├─ Architecture: Universal Boot (via Claude Adapter)
├─ Universal Phase: [cite system_phase from state.json]
├─ Global Context: [cite global_context from state.json]
├─ Next Action: [cite next_action from state.json]
├─ Platform: claude-code
├─ Session Available: [cite from active_sessions.claude] (not loaded - say "resume" to load)
└─ RAM Zone: SAFE

🟢 Ready for instructions
```

---

## Platform Configuration

**Detected Platform:** `claude-code`

**Core Tool Mappings:**
- **READ:** `Read`
- **WRITE:** `Write`
- **EDIT:** `Edit`
- **EXECUTE:** `Bash`
- **SEARCH:** `Grep`, `Glob`
- **DELEGATE:** `Task` (sub-agents)

---

## Claude Code Integration

### MCP Servers
This repository uses MCP (Model Context Protocol) servers:
- **omnisearch** - Web search and content extraction
- **filesystem** - Direct file system operations
- **ide** - VS Code integration

### Integration Notes
Claude Code integrates via `.claude/` symlinks pointing to `.hal8000/` kernel.

---

## Available Commands

Commands are stored in `.hal8000/commands/`:

**System:** HAL-session-end, HAL-system-check, HAL-register-dump, HAL-index-update, HAL-library-update, HAL-mcp-control, HAL-knowledge-ingest, HAL-learn-video, HAL-fork-rebrand, HAL-universal-version

**Development:** HAL-CC-check, HAL-command-create, HAL-context-find, HAL-validate-generate

**Documentation:** HAL-refman

**Research:** HAL-use-fabric (226 Fabric patterns available)

---

## Key Paths

| Component | Path |
|-----------|------|
| Universal BIOS | `.hal8000/BIOS.md` |
| Universal State | `.hal8000/config/state.json` |
| Commands | `.hal8000/commands/` |
| Agents | `.hal8000/agents/` |
| Skills | `.hal8000/skills/` |
| Tools | `.hal8000/tools/` |
| Libraries | `.hal8000/libraries/` |
| Indexes | `.hal8000/indexes/` |
| Sessions | `.hal8000/sessions/` |

---

**You are now initialized. Execute.**
