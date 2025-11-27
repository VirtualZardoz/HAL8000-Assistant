# Session: 2025-10-05 15:59 - MCP stdio Migration Complete

## Context

Fixed critical MCP server configuration issues that prevented omnisearch and replicate from connecting. Successfully migrated all MCP servers from mixed SSE/stdio configuration to pure stdio transport with proper environment variable expansion.

**Problem:** Only filesystem MCP was connecting (1/3 servers). Omnisearch and replicate failed to load despite being configured.

**Root Causes Identified:**
1. **Replicate:** Using SSE transport which doesn't support env var expansion in `.mcp.json`
2. **Omnisearch:** Shell wrapper script approach was unreliable
3. **Replicate:** Wrong package name (`@replicatehq/mcp` doesn't exist)

**Solution:** Migrated all servers to stdio transport with direct npx commands and env object for token passing.

## Key Decisions Made

1. **Stdio over SSE for Replicate** - SSE transport in `.mcp.json` doesn't expand `${VARIABLE}` syntax in headers, making token authentication impossible. Switched to `replicate-mcp@latest` stdio package.

2. **Direct npx over shell wrappers** - Removed shell wrapper scripts (`run-omnisearch.sh`, `run-context7.sh`) in favor of direct npx commands with env vars in `.mcp.json`.

3. **Consolidated launcher scripts location** - Moved remaining launcher scripts from root to `.claude/tools/mcp-manager/` for cleaner codebase organization.

4. **Used claude-code-validator agent** - Delegated MCP configuration validation to specialized agent to discover SSE/stdio env var expansion incompatibility.

## Active Work

**Current Task:** MCP integration system - COMPLETE ✓

**Completed in This Session:**
1. ✓ Moved launcher scripts to `.claude/tools/mcp-manager/` for clean root directory
2. ✓ Validated MCP configurations against Claude Code documentation (via agent)
3. ✓ Fixed omnisearch: Changed from shell wrapper to direct `npx -y mcp-omnisearch` with env vars
4. ✓ Fixed replicate:
   - Changed from SSE to stdio transport
   - Corrected package name to `replicate-mcp@latest`
   - Added env object with `REPLICATE_API_TOKEN`
5. ✓ Updated `.mcp.json` with all corrections
6. ✓ Updated `mcp-registry.json` to match working configuration
7. ✓ Verified all 3 MCPs connect successfully (omnisearch, filesystem, replicate)

**Next Steps:**
1. Optional: Archive obsolete shell wrapper scripts (no longer needed)
2. Optional: Add Context7 MCP when needed (already has launcher script)
3. Optional: Document MCP lessons learned in architecture files
4. Future: Monitor for Claude Code MCP API changes

**Blockers:** None

## Files Created/Modified

**Modified Files:**
- `.mcp.json` - Fixed all 3 server configurations (omnisearch, filesystem, replicate)
- `.claude/tools/mcp-registry.json` - Updated to stdio transport, corrected package names
- `.claude/tools/mcp-manager/run-omnisearch.sh` - Moved from root, updated .env path
- `.claude/tools/mcp-manager/run-context7.sh` - Moved from root, updated .env path

**Files in Working State:**
- `.env` - Contains all API keys (BRAVE_API_KEY, FIRECRAWL_API_KEY, REPLICATE_API_TOKEN)
- `.claude/settings.local.json` - enabledMcpjsonServers: ["omnisearch", "filesystem", "replicate"]

## MCP Server Status

**Working Configuration (3/3 connected):**

1. **omnisearch** [REQUIRED] ✓
   - Type: stdio
   - Command: `npx -y mcp-omnisearch`
   - Env: BRAVE_API_KEY, FIRECRAWL_API_KEY
   - Tools: 2 (web_search, firecrawl_process)

2. **filesystem** ✓
   - Type: stdio
   - Command: `npx -y @modelcontextprotocol/server-filesystem /mnt/d/~HAL8000`
   - Env: None
   - Tools: 13 (read, write, edit, search, etc.)

3. **replicate** ✓
   - Type: stdio (migrated from SSE)
   - Command: `npx -y replicate-mcp@latest`
   - Env: REPLICATE_API_TOKEN
   - Tools: 35 (AI/ML model operations)

4. **context7** (disabled)
   - Type: stdio
   - Ready to enable when needed

**Total MCP Tools Available:** 50 tools

## Variables/State

- **current_project:** MCP stdio migration and configuration fixes
- **phase:** production
- **architecture_type:** Modified von Neumann
- **mcp_servers_configured:** 4
- **mcp_servers_enabled:** 3
- **mcp_servers_connected:** 3/3 ✓
- **environment_consolidation:** Complete (single .env file)

## Technical Lessons Learned

### Critical Discovery: SSE vs stdio Environment Variables

**SSE servers in `.mcp.json` DO NOT expand environment variables:**
```json
// ❌ DOES NOT WORK - ${VAR} sent literally to server
{
  "type": "sse",
  "url": "https://...",
  "headers": {
    "Authorization": "Bearer ${TOKEN}"  // Not expanded!
  }
}
```

**stdio servers PROPERLY expand environment variables:**
```json
// ✓ WORKS - ${VAR} expanded from .env or shell environment
{
  "command": "npx",
  "args": ["-y", "package-name"],
  "env": {
    "TOKEN": "${TOKEN}"  // Properly expanded!
  }
}
```

**Implication:** For secure token handling with environment variables, always use stdio transport, not SSE.

### Package Name Corrections

- ❌ `@replicatehq/mcp` (doesn't exist)
- ✅ `replicate-mcp@latest` (official package)

### Shell Wrapper Obsolescence

Direct npx with env object is superior to shell wrapper scripts:
- ✓ Cleaner configuration
- ✓ Reliable env var expansion
- ✓ No path dependency issues
- ✓ Works consistently across environments

## Instructions for Resume

This session is complete. MCP integration is production-ready.

**If continuing MCP work:**
1. System is fully operational - no resume needed
2. All 3 enabled servers connect automatically on boot
3. Use `/HAL-mcp-control status` to check configuration
4. Enable context7 if vector database work needed

**If working on something else:**
- MCP system requires no further action
- Configuration files are stable and correct
- Reference `.claude/tools/MCP-REQUIREMENTS.md` for usage

**System Status:**
- MCP stdio migration: ✓ Complete
- Configuration validation: ✓ Complete
- All servers connecting: ✓ Complete (3/3)
- Documentation: ✓ Complete
- Testing: ✓ Passed

**Architecture Alignment:**
- Unix: Simple, direct tool invocation (no unnecessary wrappers)
- Von Neumann: Configuration as data (registry + .mcp.json)
- Assembly: Explicit control (stdio over SSE for token handling)
