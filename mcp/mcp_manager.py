"""
MCP Manager for Hello Pulse AI

Loads MCP servers from existing mcp_config.json and provides them 
to Pydantic AI agents efficiently.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from pydantic_ai.mcp import MCPServerStdio


class MCPManager:
    """Manages MCP servers for Pydantic AI integration"""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.servers: List[MCPServerStdio] = []
    
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration from JSON file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"MCP config not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def create_servers(self) -> List[MCPServerStdio]:
        """Create MCP server instances from config"""
        servers = []
        mcp_servers = self.config.get("mcpServers", {})
        
        for name, server_config in mcp_servers.items():
            try:
                # Extract configuration
                command = server_config.get("command")
                args = server_config.get("args", [])
                env = server_config.get("env", {})
                
                if not command:
                    print(f"⚠️  Skipping {name}: no command specified")
                    continue
                
                # Resolve environment variables
                resolved_env = {}
                for key, value in env.items():
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        env_var = value[2:-1]  # Remove ${ and }
                        resolved_value = os.getenv(env_var)
                        if resolved_value:
                            resolved_env[key] = resolved_value
                        else:
                            print(f"⚠️  Skipping {name}: missing env var {env_var}")
                            continue
                    else:
                        resolved_env[key] = value
                
                # Create MCP server
                server = MCPServerStdio(
                    command=command,
                    args=args,
                    env=resolved_env if resolved_env else None,
                    timeout=10,  # 10s timeout for startup
                    read_timeout=60  # 1min timeout for operations
                )
                
                servers.append(server)
                print(f"✅ MCP server '{name}' configured")
                
            except Exception as e:
                print(f"❌ Failed to configure MCP server '{name}': {e}")
                continue
        
        self.servers = servers
        return servers
    
    def get_server_names(self) -> List[str]:
        """Get list of configured server names"""
        return list(self.config.get("mcpServers", {}).keys())
    
    def is_enabled(self) -> bool:
        """Check if any MCP servers are configured"""
        return len(self.config.get("mcpServers", {})) > 0


# Global instance for easy importing
mcp_manager = MCPManager()
