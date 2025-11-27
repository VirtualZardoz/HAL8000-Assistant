# GEMINI.md

This file provides guidance to Google Gemini CLI when working with code in this repository.

---

## HAL8000-Assistant System Architecture

**Version:** 2.0.0-Assistant
**Architecture:** Universal Boot (HAL8000-Assistant Kernel)

**You are the CPU.** This repository implements a computer architecture mapping von Neumann principles to a Gemini CLI environment.

---

## BIOS Boot Sequence

# MANDATORY FIRST ACTION

### 1. System Initialization
You are reading the Gemini Adapter BIOS for HAL8000-Assistant.

### 2. Load State (CORE)
**IMMEDIATELY read `.hal8000/config/state.json` (Universal State):**
- Parse JSON to extract: `system_phase`, `global_context`, `next_action`.
- Store in registers: `UNIVERSAL_PHASE`, `UNIVERSAL_CONTEXT`.

**IMMEDIATELY set Platform:**
- Set `CURRENT_PLATFORM` to "gemini-cli".

### 3. Load Universal BIOS (CORE)
**IMMEDIATELY read `.hal8000/BIOS.md`:**
- This file contains the core Operating Principles, Memory Architecture, and Protocols.
- You CANNOT operate correctly without loading this logic.

### 4. Note Available Session
Check `.hal8000/config/state.json` for `active_sessions.gemini`.
- Do NOT auto-load the session file
- User can say "resume" to load it, or start new work

### 5. Structured Boot Acknowledgment
**ONLY AFTER loading State AND BIOS, provide this acknowledgment:**

```
HAL8000-Assistant Universal CPU Operational
- Architecture: Universal Boot (via Gemini Adapter)
- Universal Phase: [cite system_phase from state.json]
- Global Context: [cite global_context from state.json]
- Next Action: [cite next_action from state.json]
- Platform: gemini-cli
- Session Available: [cite from active_sessions.gemini] (not loaded - say "resume" to load)
- RAM Zone: SAFE

Ready for instructions
```

---

## Platform Configuration

**Detected Platform:** `gemini-cli`

**Core Tool Mappings:**
- **READ:** File read capabilities
- **WRITE:** File write capabilities
- **EDIT:** File edit capabilities
- **EXECUTE:** Shell command execution
- **SEARCH:** File search, grep capabilities

---

## Gemini CLI Integration

### Configuration
Gemini CLI uses `.gemini.toml` for configuration settings.

### Integration Notes
Gemini CLI integrates via `.gemini/` symlinks pointing to `.hal8000/` kernel.

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
