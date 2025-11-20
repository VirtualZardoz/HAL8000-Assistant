#!/usr/bin/env python3
"""
HAL8000-Assistant MCP Control - Dynamic MCP server management for RAM optimization

Manages selective loading of MCP servers via .claude/settings.local.json and .mcp.json
"""

import json
import os
import sys

def get_absolute_paths():
    """Get absolute paths for configuration files"""
    # Script is in .claude/tools/mcp/, HAL root is 3 levels up
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hal_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

    registry_path = os.path.join(script_dir, "registry.json")
    settings_path = os.path.join(hal_root, ".claude", "settings.local.json")
    mcp_config_path = os.path.join(hal_root, ".mcp.json")

    return hal_root, registry_path, settings_path, mcp_config_path

def safe_file_operation(file_path, operation, data=None):
    """Safe file operations with error handling"""
    try:
        if operation == "read":
            with open(file_path, 'r') as f:
                return json.load(f)
        elif operation == "write":
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
    except FileNotFoundError:
        return f"ERROR: File not found: {file_path}"
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON in {file_path}: {str(e)}"
    except PermissionError:
        return f"ERROR: Permission denied: {file_path}"
    except Exception as e:
        return f"ERROR: Unexpected error with {file_path}: {str(e)}"

def load_env_file(hal_root):
    """Load environment variables from .env file"""
    env_path = os.path.join(hal_root, ".env")
    env_vars = {}

    if os.path.exists(env_path):
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        except Exception as e:
            print(f"WARNING: Could not load .env file: {e}")

    return env_vars

def validate_environment():
    """Validate script is in expected location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    expected_suffix = os.path.join(".claude", "tools", "mcp")

    if not script_dir.endswith(expected_suffix):
        return f"ERROR: Script not in expected location.\nFound: {script_dir}\nExpected to end with: {expected_suffix}"

    return None

def load_registry(registry_path):
    """Load MCP server registry"""
    registry = safe_file_operation(registry_path, "read")
    if isinstance(registry, str) and registry.startswith("ERROR"):
        return None, registry

    if "servers" not in registry:
        return None, f"ERROR: Invalid registry format - missing 'servers' key"

    return registry["servers"], None

def build_mcp_config(server_name, server_def, hal_root):
    """Build .mcp.json configuration for a server"""
    config = {}

    if server_def["type"] == "stdio":
        config["command"] = server_def["command"]
        config["args"] = server_def.get("args", [])

        # Load environment variables from .env if server requires them
        if server_def.get("env_vars"):
            env_vars = load_env_file(hal_root)
            # Only include the vars this server needs
            server_env_vars = {k: f"${{{k}}}" for k in server_def["env_vars"] if k in env_vars}
            if server_env_vars:
                config["env"] = server_env_vars

    elif server_def["type"] == "sse":
        config["url"] = server_def["url"]

        # Load environment variables from .env if server requires them
        if server_def.get("env_vars"):
            env_vars = load_env_file(hal_root)
            # Only include the vars this server needs
            server_env_vars = {k: f"${{{k}}}" for k in server_def["env_vars"] if k in env_vars}
            if server_env_vars:
                config["env"] = server_env_vars

    return config

def check_required_env_vars(hal_root, server_def):
    """Check if required environment variables are available"""
    required_vars = server_def.get("env_vars", [])

    if not required_vars:
        return None  # No requirements

    env_vars = load_env_file(hal_root)
    missing = [var for var in required_vars if var not in env_vars or not env_vars[var]]

    if missing:
        return f"ERROR: Missing required environment variables in .env: {', '.join(missing)}"

    return None

def enable_server(server_name, servers, hal_root, settings_path, mcp_config_path):
    """Enable an MCP server"""
    if server_name not in servers:
        available = ", ".join(servers.keys())
        return f"ERROR: Server '{server_name}' not in registry.\nAvailable: {available}"

    server_def = servers[server_name]

    # Check environment variables
    env_error = check_required_env_vars(hal_root, server_def)
    if env_error:
        return env_error

    # Load current settings
    settings = safe_file_operation(settings_path, "read")
    if isinstance(settings, str) and settings.startswith("ERROR"):
        return settings

    # Ensure selective control is enabled
    settings["enableAllProjectMcpServers"] = False

    # Add to enabled servers list
    enabled_servers = settings.get("enabledMcpjsonServers", [])
    if server_name in enabled_servers:
        return f"✓ Server '{server_name}' already enabled"

    enabled_servers.append(server_name)
    settings["enabledMcpjsonServers"] = enabled_servers

    # Load and update .mcp.json
    mcp_config = safe_file_operation(mcp_config_path, "read")
    if isinstance(mcp_config, str) and mcp_config.startswith("ERROR"):
        return mcp_config

    # Add server definition
    if "mcpServers" not in mcp_config:
        mcp_config["mcpServers"] = {}

    mcp_config["mcpServers"][server_name] = build_mcp_config(server_name, server_def, hal_root)

    # Save both files
    result = safe_file_operation(mcp_config_path, "write", mcp_config)
    if isinstance(result, str) and result.startswith("ERROR"):
        return result

    result = safe_file_operation(settings_path, "write", settings)
    if isinstance(result, str) and result.startswith("ERROR"):
        return result

    return f"✓ Server '{server_name}' enabled\n⚠ Restart session to apply changes"

def disable_server(server_name, servers, settings_path, mcp_config_path):
    """Disable an MCP server"""
    if server_name not in servers:
        available = ", ".join(servers.keys())
        return f"ERROR: Server '{server_name}' not in registry.\nAvailable: {available}"

    # Check if server is required
    server_def = servers[server_name]
    if server_def.get("required", False):
        return f"WARNING: '{server_name}' is marked as required for core functionality.\nDisabling may break agents: {', '.join(server_def.get('used_by', []))}\nContinue anyway? (You'll need to manually confirm this action)"

    # Load current settings
    settings = safe_file_operation(settings_path, "read")
    if isinstance(settings, str) and settings.startswith("ERROR"):
        return settings

    # Ensure selective control is enabled
    settings["enableAllProjectMcpServers"] = False

    # Remove from enabled servers list
    enabled_servers = settings.get("enabledMcpjsonServers", [])
    if server_name not in enabled_servers:
        return f"✓ Server '{server_name}' already disabled"

    enabled_servers.remove(server_name)
    settings["enabledMcpjsonServers"] = enabled_servers

    # Load and update .mcp.json
    mcp_config = safe_file_operation(mcp_config_path, "read")
    if isinstance(mcp_config, str) and mcp_config.startswith("ERROR"):
        return mcp_config

    # Remove server definition
    if "mcpServers" in mcp_config and server_name in mcp_config["mcpServers"]:
        del mcp_config["mcpServers"][server_name]

    # Save both files
    result = safe_file_operation(mcp_config_path, "write", mcp_config)
    if isinstance(result, str) and result.startswith("ERROR"):
        return result

    result = safe_file_operation(settings_path, "write", settings)
    if isinstance(result, str) and result.startswith("ERROR"):
        return result

    return f"✓ Server '{server_name}' disabled\n⚠ Restart session to apply changes"

def list_servers(servers, settings_path):
    """List all available servers and their status"""
    settings = safe_file_operation(settings_path, "read")
    if isinstance(settings, str) and settings.startswith("ERROR"):
        return settings

    enabled_servers = settings.get("enabledMcpjsonServers", [])
    enable_all = settings.get("enableAllProjectMcpServers", False)

    result = "═══════════════════════════════════════════════════════════\n"
    result += "HAL8000-Assistant MCP Server Status\n"
    result += "═══════════════════════════════════════════════════════════\n\n"

    # Control mode
    if enable_all:
        result += "⚠ CONTROL MODE: Auto-load ALL servers (enableAllProjectMcpServers=true)\n"
        result += "  Individual control DISABLED. Use 'disable' to enable selective mode.\n\n"
    else:
        result += "✓ CONTROL MODE: Selective loading (enableAllProjectMcpServers=false)\n\n"

    # List servers
    for name, config in servers.items():
        is_enabled = name in enabled_servers or enable_all
        status = "🟢 ENABLED" if is_enabled else "⚪ DISABLED"
        required = " [REQUIRED]" if config.get("required", False) else ""

        result += f"{name}{required}\n"
        result += f"  Status: {status}\n"
        result += f"  Type: {config['type']}\n"
        result += f"  Description: {config['description']}\n"

        if config.get("used_by"):
            result += f"  Used by: {', '.join(config['used_by'])}\n"

        if config.get("env_vars"):
            result += f"  Requires: {', '.join(config['env_vars'])}"
            if config.get("env_file"):
                result += f" (in {config['env_file']})"
            result += "\n"

        result += "\n"

    # Summary
    enabled_count = len(enabled_servers) if not enable_all else len(servers)
    estimated_tokens = enabled_count * 500

    result += "───────────────────────────────────────────────────────────\n"
    result += f"Currently Enabled: {enabled_count}/{len(servers)} servers\n"
    result += f"Estimated RAM Cost: ~{estimated_tokens} tokens on boot\n"
    result += "───────────────────────────────────────────────────────────\n"

    return result

def main():
    """Main execution"""
    # Validate environment
    env_error = validate_environment()
    if env_error:
        print(env_error)
        return 1

    # Get paths
    hal_root, registry_path, settings_path, mcp_config_path = get_absolute_paths()

    # Load registry
    servers, error = load_registry(registry_path)
    if error:
        print(error)
        return 1

    # Parse command
    if len(sys.argv) < 2:
        print("Usage: /HAL-mcp-control [status|enable|disable] [server_name]")
        return 1

    action = sys.argv[1]

    if action == "status":
        print(list_servers(servers, settings_path))
    elif action == "enable":
        if len(sys.argv) < 3:
            print("ERROR: Server name required for enable action")
            print("Usage: /HAL-mcp-control enable <server_name>")
            return 1
        server_name = sys.argv[2]
        print(enable_server(server_name, servers, hal_root, settings_path, mcp_config_path))
    elif action == "disable":
        if len(sys.argv) < 3:
            print("ERROR: Server name required for disable action")
            print("Usage: /HAL-mcp-control disable <server_name>")
            return 1
        server_name = sys.argv[2]
        print(disable_server(server_name, servers, settings_path, mcp_config_path))
    else:
        print(f"ERROR: Unknown action '{action}'")
        print("Usage: /HAL-mcp-control [status|enable|disable] [server_name]")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
