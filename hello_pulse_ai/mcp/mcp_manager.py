"""
MCP Manager for Hello Pulse AI

Loads MCP servers from existing mcp_config.json and provides them 
to Pydantic AI agents efficiently with enhanced configuration support.
"""
import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from pydantic_ai.mcp import MCPServerStdio

# Configure logging
logger = logging.getLogger(__name__)


class MCPManagerError(Exception):
    """Custom exception for MCP Manager errors"""
    pass


class MCPManager:
    """
    Manages MCP servers for Pydantic AI integration
    
    Features:
    - Environment variable resolution with ${VAR} syntax
    - Configurable timeouts and tool prefixes
    - Comprehensive error handling and validation
    - Extensible for future HTTP server support
    """
    
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.servers: List[MCPServerStdio] = []
        
        # Set up logging
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration from JSON file"""
        if not self.config_path.exists():
            raise MCPManagerError(f"MCP config not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if not isinstance(config, dict):
                raise MCPManagerError("Config must be a JSON object")
                
            if "mcpServers" not in config:
                logger.warning("No 'mcpServers' section found in config")
                config["mcpServers"] = {}
                
            return config
            
        except json.JSONDecodeError as e:
            raise MCPManagerError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise MCPManagerError(f"Failed to load config: {e}")
    
    def _resolve_environment_variables(self, env_config: Dict[str, Any]) -> Dict[str, str]:
        """
        Resolve environment variables in configuration
        
        Supports:
        - ${VAR_NAME} syntax
        - Direct string values
        - Default values with ${VAR_NAME:-default}
        """
        resolved_env = {}
        
        for key, value in env_config.items():
            if not isinstance(value, str):
                resolved_env[key] = str(value)
                continue
            
            # Handle ${VAR} or ${VAR:-default} syntax
            if value.startswith("${") and value.endswith("}"):
                var_expr = value[2:-1]  # Remove ${ and }
                
                # Check for default value syntax
                if ":-" in var_expr:
                    var_name, default_value = var_expr.split(":-", 1)
                    resolved_value = os.getenv(var_name.strip(), default_value.strip())
                else:
                    var_name = var_expr.strip()
                    resolved_value = os.getenv(var_name)
                    
                    if resolved_value is None:
                        logger.warning(f"Environment variable '{var_name}' not found for key '{key}'")
                        continue
                
                resolved_env[key] = resolved_value
            else:
                resolved_env[key] = value
        
        return resolved_env
    
    def _validate_server_config(self, name: str, config: Dict[str, Any]) -> bool:
        """Validate server configuration"""
        if not isinstance(config, dict):
            logger.error(f"Server '{name}' config must be an object")
            return False
        
        if "command" not in config:
            logger.error(f"Server '{name}' missing required 'command' field")
            return False
        
        command = config["command"]
        if not isinstance(command, str) or not command.strip():
            logger.error(f"Server '{name}' command must be a non-empty string")
            return False
        
        return True
    
    def create_servers(self) -> List[MCPServerStdio]:
        """Create MCP server instances from config with enhanced validation"""
        servers = []
        mcp_servers = self.config.get("mcpServers", {})
        
        if not mcp_servers:
            logger.info("No MCP servers configured")
            return servers
        
        logger.info(f"Configuring {len(mcp_servers)} MCP server(s)")
        
        for name, server_config in mcp_servers.items():
            try:
                # Validate configuration
                if not self._validate_server_config(name, server_config):
                    continue
                
                # Extract configuration with defaults
                command = server_config["command"].strip()
                args = server_config.get("args", [])
                env_config = server_config.get("env", {})
                
                # Enhanced configuration options
                timeout = server_config.get("timeout", 10)
                read_timeout = server_config.get("read_timeout", 60)
                tool_prefix = server_config.get("tool_prefix", "")
                
                # Validate types
                if not isinstance(args, list):
                    logger.error(f"Server '{name}' args must be a list")
                    continue
                
                if not isinstance(timeout, (int, float)) or timeout <= 0:
                    logger.warning(f"Server '{name}' invalid timeout, using default: 10s")
                    timeout = 10
                
                if not isinstance(read_timeout, (int, float)) or read_timeout <= 0:
                    logger.warning(f"Server '{name}' invalid read_timeout, using default: 60s")
                    read_timeout = 60
                
                # Resolve environment variables
                resolved_env = self._resolve_environment_variables(env_config)
                
                # Create MCP server
                server_kwargs = {
                    "command": command,
                    "args": args,
                    "timeout": timeout,
                    "read_timeout": read_timeout
                }
                
                # Add environment if any variables resolved
                if resolved_env:
                    server_kwargs["env"] = resolved_env
                
                # Add tool prefix if specified
                if tool_prefix:
                    server_kwargs["tool_prefix"] = tool_prefix
                
                server = MCPServerStdio(**server_kwargs)
                servers.append(server)
                
                logger.info(f"✅ MCP server '{name}' configured successfully")
                logger.debug(f"   Command: {command}")
                logger.debug(f"   Args: {args}")
                logger.debug(f"   Timeout: {timeout}s")
                logger.debug(f"   Environment vars: {len(resolved_env)}")
                if tool_prefix:
                    logger.debug(f"   Tool prefix: '{tool_prefix}'")
                
            except Exception as e:
                logger.error(f"❌ Failed to configure MCP server '{name}': {e}")
                continue
        
        self.servers = servers
        logger.info(f"Successfully configured {len(servers)} MCP server(s)")
        return servers
    
    def get_server_names(self) -> List[str]:
        """Get list of configured server names"""
        return list(self.config.get("mcpServers", {}).keys())
    
    def get_server_count(self) -> int:
        """Get count of successfully configured servers"""
        return len(self.servers)
    
    def is_enabled(self) -> bool:
        """Check if any MCP servers are configured and available"""
        return len(self.servers) > 0
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current configuration"""
        mcp_servers = self.config.get("mcpServers", {})
        return {
            "config_file": str(self.config_path),
            "servers_defined": len(mcp_servers),
            "servers_active": len(self.servers),
            "server_names": list(mcp_servers.keys())
        }
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        logger.info("Reloading MCP configuration")
        self.config = self._load_config()
        self.servers = []  # Clear existing servers
    
    def set_log_level(self, level: str) -> None:
        """Set logging level (DEBUG, INFO, WARNING, ERROR)"""
        logger.setLevel(getattr(logging, level.upper()))


# Global instance for easy importing
mcp_manager = MCPManager()
