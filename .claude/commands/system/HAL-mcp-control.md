---
name: HAL-mcp-control
description: Dynamic MCP server control for RAM optimization
parameters:
  - name: action
    description: Action to perform (status, enable, disable)
    type: string
    required: true
  - name: server_name
    description: MCP server name (required for enable/disable)
    type: string
    required: false
---

# HAL MCP Control Command

**Purpose:** Selectively enable/disable MCP servers to optimize RAM usage by loading only what's needed for current session.

**Architecture:** MCP servers are Extended I/O interfaces (tools). Each enabled server costs ~500-1000 tokens on session boot. This command provides dynamic control.

---

## 📋 INSTRUCTIONS

Execute the Python script with provided arguments:

> **🔧 EXECUTION:** `python3 ".claude/tools/mcp/control.py" $1 $2`

---

## Usage

### Check Status
```bash
/HAL-mcp-control status
```
Shows all available MCP servers, their current state (enabled/disabled), dependencies, and RAM cost.

### Enable Server
```bash
/HAL-mcp-control enable <server_name>
```
Examples:
- `/HAL-mcp-control enable replicate` - Enable Replicate AI models
- `/HAL-mcp-control enable context7` - Enable Context7 vector database

**What happens:**
1. Validates server exists in registry
2. Checks required API keys in .env files
3. Adds server to `.claude/settings.local.json` (enabledMcpjsonServers)
4. Adds server definition to `.mcp.json`
5. Sets `enableAllProjectMcpServers: false` for selective control
6. Prompts for session restart

### Disable Server
```bash
/HAL-mcp-control disable <server_name>
```
Examples:
- `/HAL-mcp-control disable filesystem` - Disable filesystem MCP (falls back to Read/Grep/Glob)
- `/HAL-mcp-control disable replicate` - Disable Replicate when not doing AI work

**What happens:**
1. Warns if disabling required server
2. Removes from enabledMcpjsonServers array
3. Removes definition from .mcp.json
4. Prompts for session restart

**Note:** Disabling required servers (like `omnisearch`) may break agents that depend on them.

---

## Available Servers

Server registry maintained in `.claude/tools/mcp/registry.json`. Current servers:

### omnisearch (Required)
- **Purpose:** Multi-provider web search + content extraction
- **API Keys:** BRAVE_API_KEY, FIRECRAWL_API_KEY (in `.env`)
- **Used By:** research-synthesizer, claude-code-validator agents
- **Tools:** mcp__omnisearch__web_search, mcp__omnisearch__firecrawl_process

### filesystem (Optional)
- **Purpose:** Enhanced file operations
- **API Keys:** None
- **Used By:** hal-context-finder, system-maintenance (graceful fallback)
- **Fallback:** Read, Grep, Glob work at 100% functionality

### replicate (Optional)
- **Purpose:** AI/ML model access
- **API Keys:** REPLICATE_API_TOKEN (in `.env`)
- **Use Cases:** Image generation, ML inference, model testing

### context7 (Optional)
- **Purpose:** Vector database for semantic context
- **API Keys:** CONTEXT7_API_KEY (in `.env`)
- **Use Cases:** Embeddings, semantic search, context storage

---

## Configuration Files

### Server Registry
**Location:** `.claude/tools/mcp/registry.json`
**Purpose:** Defines all available MCP servers (type, command, env requirements, description)
**Maintenance:** Add new servers here as they become available

### Settings
**Location:** `.claude/settings.local.json`
**Managed Keys:**
- `enableAllProjectMcpServers`: false (enables selective control)
- `enabledMcpjsonServers`: ["omnisearch", "filesystem", ...]

### MCP Configuration
**Location:** `.mcp.json` (HAL root)
**Content:** Server definitions (command, args, env vars) for enabled servers

### Environment Files
**Pattern:** `.env.<server_name>` in HAL root
**Purpose:** API keys and configuration for each server
**Security:** Not checked into git (add to .gitignore)

---

## Workflow Examples

### Research Session
```bash
# Start: Enable only omnisearch (required for research-synthesizer)
/HAL-mcp-control enable omnisearch
# Restart session
# Do research work
# End: omnisearch stays enabled (required)
```

### AI/ML Session
```bash
# Start: Enable replicate for model access
/HAL-mcp-control enable replicate
# Restart session
# Work with AI models
# End: Disable to free RAM for next session
/HAL-mcp-control disable replicate
# Restart session
```

### Vector Database Work
```bash
# Start: Enable context7
/HAL-mcp-control enable context7
# Restart session
# Work with embeddings
# End: Disable when done
/HAL-mcp-control disable context7
```

---

## RAM Optimization Strategy

**Default Configuration:**
- omnisearch: ✓ ENABLED (required)
- filesystem: ✓ ENABLED (useful, low cost)
- replicate: ✗ DISABLED (enable when needed)
- context7: ✗ DISABLED (enable when needed)

**Estimated Boot Cost:**
- 2 servers enabled: ~1000-2000 tokens
- 4 servers enabled: ~2000-4000 tokens

**Best Practice:**
1. Keep required servers enabled (omnisearch)
2. Keep low-cost optional servers enabled (filesystem)
3. Enable/disable specialized servers per session (replicate, context7)
4. Check status before major work: `/HAL-mcp-control status`

---

## Troubleshooting

### Server won't enable
**Cause:** Missing API keys
**Solution:** Check `.env.<server_name>` file, add required keys, try again

### Changes not applying
**Cause:** Session restart needed
**Solution:** After enable/disable, restart Claude Code session

### Required server disabled
**Cause:** Accidentally disabled omnisearch
**Solution:** `/HAL-mcp-control enable omnisearch` and restart

### Invalid server name
**Cause:** Typo or server not in registry
**Solution:** Run `/HAL-mcp-control status` to see available servers

---

## Related Documentation

- **MCP Requirements:** `.claude/tools/mcp/requirements.md` - Installation, configuration, troubleshooting
- **Server Registry:** `.claude/tools/mcp/registry.json` - Server definitions
- **I/O System:** `data/architecture/hal8000-io-system.md` - MCP as Extended I/O layer

---

**Principle:** Unix philosophy - do one thing well. This command manages MCP loading. Agent definitions specify which MCPs they need. Separation of concerns.

**Architecture:** MCPs are tools (Extended I/O). Command modifies OS configuration (settings files). Clean, transparent, controllable.
