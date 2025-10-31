#!/bin/bash
# clean.sh - Comprehensive cleanup for Hello Pulse AI project

set -e

echo "🧹 Cleaning Hello Pulse AI project..."

# Define variables
MCP_DIR="$HOME/mcp-servers"
PROJECT_DIR="$(pwd)"

# Remove Python caches
echo "🗑️  Removing Python caches..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove build directories
echo "🗑️  Removing build directories..."
rm -rf build/ dist/ *.egg-info/ .coverage .pytest_cache/ .mypy_cache/ 2>/dev/null || true

# Remove temporary logs and histories
echo "🗑️  Removing temporary files..."
rm -rf chat_histories/*.json 2>/dev/null || true
rm -rf *.log .DS_Store Thumbs.db 2>/dev/null || true

# Remove virtual environment if exists
if [ -d "venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf venv/
fi

# Remove MCP servers
if [ -d "$MCP_DIR" ]; then
    echo "🗑️  Removing MCP servers..."
    rm -rf "$MCP_DIR"
    echo "✅ Removed $MCP_DIR"
else
    echo "ℹ️ MCP servers directory not found"
fi

# Clean up Docker containers and resources
echo "🐳 Cleaning up Docker resources..."
if [ -f "$PROJECT_DIR/docker-compose.yml" ]; then
    cd "$PROJECT_DIR"
    
    # Stop and remove containers
    echo "🛑 Stopping and removing containers..."
    docker compose down 2>/dev/null || true
    
    # Remove volumes (be careful with this - it will delete all data)
    read -p "❓ Remove all Docker volumes? This will delete all data (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing Docker volumes..."
        docker compose down -v 2>/dev/null || true
    fi
    
    # Remove networks
    echo "🗑️  Removing Docker networks..."
    docker network rm "$(basename "$PROJECT_DIR")_searxng" 2>/dev/null || true
    
    # Remove images (optional)
    read -p "❓ Remove Docker images? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing Docker images..."
        docker compose down --rmi all 2>/dev/null || true
    fi
else
    echo "ℹ️ No docker-compose.yml found"
fi

# Clean up configuration files
echo "🗑️  Removing configuration files..."
rm -f "$PROJECT_DIR/Caddyfile" 2>/dev/null || true
rm -f "$PROJECT_DIR/docker-compose.yml" 2>/dev/null || true

# Clean up SearXNG configuration directory
if [ -d "$PROJECT_DIR/searxng" ]; then
    echo "🗑️  Removing SearXNG configuration..."
    rm -rf "$PROJECT_DIR/searxng"
fi

# Clean up logs directory
if [ -d "$PROJECT_DIR/logs" ]; then
    echo "🗑️  Removing logs..."
    rm -rf "$PROJECT_DIR/logs"
fi

# Clean up temporary files in /tmp
echo "🗑️  Cleaning up temporary files..."
rm -rf /tmp/wikipedia-mcp 2>/dev/null || true
rm -rf /tmp/mcp-searxng 2>/dev/null || true

# Clean up Docker system (optional)
read -p "❓ Clean up unused Docker system resources? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Cleaning up Docker system..."
    docker system prune -f 2>/dev/null || true
fi

echo ""
echo "✅ Cleanup completed!"
echo "💡 To reinstall: ./scripts/install_mcps.sh"
echo "💡 To reinstall Python packages: pip install -r requirements.txt"