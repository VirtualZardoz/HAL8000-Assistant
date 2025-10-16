# MCP Server Requirements

This document lists the MCP (Model Context Protocol) servers required and recommended for HAL8000 operation.

## Overview

HAL8000 uses MCP servers to extend Claude Code capabilities beyond built-in tools. MCP servers provide specialized functionality for web research, file operations, AI/ML models, and vector databases.

**Dynamic Control:** Use `/HAL-mcp-control` command to selectively enable/disable servers per session, optimizing RAM usage (~500-1000 tokens per server).

**Architecture:** MCPs are "Extended I/O" - external tools that provide specialized capabilities. See `data/architecture/hal8000-io-system.md` for details.

## Required MCP Servers

### omnisearch

**Purpose:** Enhanced web search and content extraction
**Status:** ✓ Configured
**Used By:**
- `research-synthesizer` agent
- `claude-code-validator` agent

**Capabilities:**
- `mcp__omnisearch__web_search` - Multi-provider web search (Brave, Tavily, Kagi, Exa)
- `mcp__omnisearch__firecrawl_process` - Deep web content extraction and processing

**Configuration:**
- File: `.env`
- Required API keys:
  - Brave Search API key
  - Firecrawl API key
- Launch script: `run-omnisearch.sh`

**Without this server:**
- Web research capabilities degraded
- Claude Code validator cannot fetch documentation
- Falls back to built-in WebSearch/WebFetch (limited functionality)

---

## Optional MCP Servers

### filesystem

**Purpose:** Enhanced file system operations
**Status:** ⚠️ Optional (not required)
**Used By:**
- `hal-context-finder` agent (graceful fallback)
- `system-maintenance` agent (graceful fallback)

**Capabilities:**
- `mcp__filesystem__search_files` - Advanced file search
- `mcp__filesystem__list_directory` - Directory listing with metadata
- `mcp__filesystem__get_file_info` - Detailed file information
- `mcp__filesystem__read_file` - File reading
- `mcp__filesystem__write_file` - File writing
- `mcp__filesystem__edit_file` - File editing

**Configuration:**
- Standard MCP filesystem server
- Configure in Claude Code settings or via CLI

**Without this server:**
- hal-context-finder falls back to Read, Grep, Glob (works fine)
- system-maintenance falls back to Bash, Read, Glob (works fine)
- Functionality: 100% (no degradation)
- Performance: Slightly slower file operations

**Recommendation:** Install for enhanced file operations, but not critical for system operation.

### replicate

**Purpose:** AI/ML model access via Replicate API
**Status:** ⚠️ Optional (enable when needed)
**Used By:** None (available for user tasks)

**Capabilities:**
- AI model inference (text, image, code)
- Image generation and manipulation
- Access to latest ML models without local installation

**Configuration:**
- Type: SSE (Server-Sent Events)
- URL: `https://mcp.replicate.com/sse`
- File: `.env`
- Required API keys:
  - Replicate API token (from https://replicate.com/account/api-tokens)

**Use Cases:**
- Image generation (Stable Diffusion, DALL-E, etc.)
- Model testing and experimentation
- AI-powered content creation

**Recommendation:** Enable only when doing AI/ML work to save RAM (~500 tokens).

### context7

**Purpose:** Upstash Context7 vector database for semantic context management
**Status:** ⚠️ Optional (enable when needed)
**Used By:** None (available for user tasks)

**Capabilities:**
- Vector embeddings storage and retrieval
- Semantic search across contexts
- Persistent context management across sessions

**Configuration:**
- Type: stdio
- Command: `run-context7.sh`
- File: `.env`
- Required API keys:
  - Context7 API key (from https://upstash.com)

**Use Cases:**
- Building semantic search features
- Storing and retrieving context embeddings
- Long-term context persistence

**Recommendation:** Enable only when doing vector/embedding work to save RAM (~500 tokens).

---

## Dynamic Control

**HAL8000 provides dynamic MCP server management to optimize RAM usage.**

### Quick Start

Check current status:
```bash
/HAL-mcp-control status
```

Enable a server:
```bash
/HAL-mcp-control enable replicate
# Restart session
```

Disable a server:
```bash
/HAL-mcp-control disable replicate
# Restart session
```

**How it works:**
- Modifies `.claude/settings.local.json` (enabledMcpjsonServers array)
- Updates `.mcp.json` (server definitions)
- Sets `enableAllProjectMcpServers: false` for selective control
- Requires session restart to apply changes

**Strategy:**
- Keep required servers enabled: `omnisearch`
- Keep low-cost servers enabled: `filesystem`
- Enable/disable specialized servers per session: `replicate`, `context7`

See `.claude/commands/HAL-mcp-control.md` for complete documentation.

---

## Installation

### omnisearch (Required)

1. Configure API keys in `.env`:
   ```bash
   BRAVE_API_KEY=your_key_here
   FIRECRAWL_API_KEY=your_key_here
   ```

2. Launch server:
   ```bash
   ./run-omnisearch.sh
   ```

3. Verify in Claude Code:
   - MCP servers panel should show "omnisearch" connected
   - Test: Run `/HAL-CC-check` to verify web fetch capabilities

### filesystem (Optional)

Enable via control command:
```bash
/HAL-mcp-control enable filesystem
```

Or manually add to `.mcp.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/mnt/d/~HAL8000"]
    }
  }
}
```

Restart session and verify in MCP servers panel.

### replicate (Optional)

1. Configure API key in `.env`:
   ```bash
   REPLICATE_API_TOKEN=your_token_here
   ```

2. Enable server:
   ```bash
   /HAL-mcp-control enable replicate
   ```

3. Restart session

4. Verify: MCP servers panel should show "replicate" connected

### context7 (Optional)

1. Configure API key in `.env`:
   ```bash
   CONTEXT7_API_KEY=your_key_here
   ```

2. Enable server:
   ```bash
   /HAL-mcp-control enable context7
   ```

3. Restart session

4. Verify: MCP servers panel should show "context7" connected

**Note:** A `.env.template` file is provided in HAL root. Copy it to `.env` and update with your actual API keys.

---

## Verification

### Check MCP Status
```bash
/HAL-mcp-control status
```

Shows:
- All available servers
- Current status (enabled/disabled)
- Required servers and dependencies
- Estimated RAM cost

### Check Agent Compatibility
```bash
/HAL-CC-check
```

Validates:
- Which MCP servers are configured
- Which agents depend on MCP tools
- Fallback behavior if servers unavailable

---

## Troubleshooting

**omnisearch not connecting:**
- Check `.env` has valid API keys
- Verify `run-omnisearch.sh` is executable
- Check MCP server logs for errors

**filesystem not connecting:**
- Verify MCP configuration in Claude Code settings
- Check path permissions for `/mnt/d/~HAL8000`
- Ensure `@modelcontextprotocol/server-filesystem` package is available

**Agents failing:**
- Check `/HAL-CC-check` output for specific issues
- Review agent logs for tool availability errors
- Verify fallback tools (Read, Grep, Glob, Bash) are working

**Server won't enable:**
- Check API keys in corresponding `.env` file
- Ensure `.env` file exists in HAL root
- Verify API key is valid (not placeholder text)

**Changes not applying:**
- Restart Claude Code session after enable/disable
- Check `.claude/settings.local.json` for `enableAllProjectMcpServers: false`
- Verify `.mcp.json` contains/lacks server definition as expected

---

## Architecture Notes

**Design Philosophy:**
- Required MCP: Core functionality depends on it
- Optional MCP: Enhances performance but has graceful fallback
- No hard dependencies: System operates in degraded mode without optional MCPs

**Unix Principle:**
- MCP servers are "external programs" (pipe to specialized tools)
- Agents compose MCP tools with built-in tools
- Clean separation: MCP failure doesn't crash system

**RAM Optimization:**
- Each MCP server costs ~500-1000 tokens on session boot
- Selective loading reduces base RAM footprint
- Enable only what you need for current session
- Default: omnisearch + filesystem (~1000-2000 tokens)
- All enabled: 4 servers (~2000-4000 tokens)

**Maintenance:**
- Run `/HAL-CC-check` quarterly or after Claude Code updates
- Review `/HAL-mcp-control status` before major sessions
- Update API keys as needed
- Add new servers to `.claude/tools/mcp-registry.json`

---

## Server Registry

All available MCP servers are defined in `.claude/tools/mcp-registry.json`. This registry includes:
- Server type (stdio, sse)
- Command/URL configuration
- Environment variable requirements
- Description and use cases
- Agent dependencies

To add a new server, update the registry and it becomes available to `/HAL-mcp-control`.

---

## Related Documentation

- **HAL MCP Control:** `.claude/commands/HAL-mcp-control.md` - Complete command documentation
- **Server Registry:** `.claude/tools/mcp-registry.json` - All available servers
- **I/O Architecture:** `data/architecture/hal8000-io-system.md` - MCP as Extended I/O
- Claude Code MCP docs: https://docs.claude.com/en/docs/claude-code/mcp
- Replicate API: https://replicate.com/docs
- Context7/Upstash: https://upstash.com/docs/vector/overall/getstarted

---

**Last Updated:** 2025-10-05
**Validated Against:** Claude Code current release (September 2025)
**Servers Configured:** omnisearch (required), filesystem, replicate, context7
