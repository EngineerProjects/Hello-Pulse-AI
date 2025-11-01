#!/bin/bash

# Hello Pulse AI - MCP Servers Installation Script
# Optimized version with proper structure and cleanup

set -euo pipefail

# === CONFIGURATION ===
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
readonly MCP_SERVERS_DIR="$PROJECT_ROOT/mcp_servers"
readonly TEMP_DIR="/tmp/hello-pulse-ai-install"
readonly ENV_FILE="$PROJECT_ROOT/.env"

# === COLORS ===
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# === LOGGING FUNCTIONS ===
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# === HELPER FUNCTIONS ===
check_requirements() {
    log_info "Checking system requirements..."
    
    local missing_deps=()
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker")
    fi
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        missing_deps+=("docker-compose")
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        missing_deps+=("node.js")
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        missing_deps+=("npm")
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    # Check OpenSSL
    if ! command -v openssl &> /dev/null; then
        missing_deps+=("openssl")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install them and run this script again."
        exit 1
    fi
    
    log_success "All requirements met!"
}

create_directory_structure() {
    log_info "Creating directory structure..."
    
    # Main directories
    mkdir -p "$MCP_SERVERS_DIR"/{searxng,firecrawl,deep-research,chroma}
    mkdir -p "$PROJECT_ROOT/data"/{searxng,firecrawl,deep-research,chroma}
    mkdir -p "$PROJECT_ROOT/logs"
    mkdir -p "$TEMP_DIR"
    
    # SearXNG specific directories
    mkdir -p "$MCP_SERVERS_DIR/searxng/settings"
    
    log_success "Directory structure created!"
}

update_env_var() {
    local key="$1"
    local value="$2"
    
    # Create .env file if it doesn't exist
    if [ ! -f "$ENV_FILE" ]; then
        touch "$ENV_FILE"
    fi
    
    # Check if key exists and update, or append new key
    if grep -q "^${key}=" "$ENV_FILE"; then
        # Update existing key
        sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    else
        # Add new key on a new line
        echo "" >> "$ENV_FILE"
        echo "${key}=${value}" >> "$ENV_FILE"
    fi
}

generate_searxng_secret() {
    log_info "Generating SearXNG secret key..."
    
    local secret_key
    secret_key=$(openssl rand -hex 32)
    
    # Update .env file properly
    update_env_var "SEARXNG_SECRET_KEY" "$secret_key"
    
    log_success "SearXNG secret key generated and stored in .env"
}

install_firecrawl() {
    log_info "Installing Local Firecrawl..."
    
    cd "$TEMP_DIR"
    
    # Clone repository
    if [ ! -d "localfirecrawl" ]; then
        git clone https://github.com/Ozamatash/localfirecrawl.git
    fi
    
    cd localfirecrawl
    
    # Create optimized Dockerfile
    cat > "$MCP_SERVERS_DIR/firecrawl/Dockerfile" << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache curl

# Copy package files
COPY package*.json ./

# Install dependencies (use install instead of ci since we're creating package.json)
RUN npm install --only=production && npm cache clean --force

# Copy source code
COPY . .

# Expose port
EXPOSE 3002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3002/health || exit 1

# Start the application
CMD ["npm", "start"]
EOF
    
    # Create a simple package.json
    cat > "$MCP_SERVERS_DIR/firecrawl/package.json" << 'EOF'
{
  "name": "local-firecrawl",
  "version": "1.0.0",
  "description": "Local Firecrawl API with SearXNG integration",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "axios": "^1.6.0",
    "cheerio": "^1.0.0-rc.12",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
EOF
    
    # Create simplified Firecrawl server
    cat > "$MCP_SERVERS_DIR/firecrawl/index.js" << 'EOF'
const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3002;
const SEARXNG_URL = process.env.SEARXNG_URL || 'http://searxng:8080';

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Search endpoint compatible with Firecrawl API
app.post('/v1/search', async (req, res) => {
  try {
    const { query, limit = 10 } = req.body;
    
    const searchUrl = `${SEARXNG_URL}/search?q=${encodeURIComponent(query)}&format=json`;
    const response = await axios.get(searchUrl);
    
    const results = response.data.results.slice(0, limit).map(result => ({
      title: result.title,
      url: result.url,
      content: result.content || '',
      score: result.score || 0
    }));
    
    res.json({
      success: true,
      data: results,
      total: results.length
    });
  } catch (error) {
    console.error('Search error:', error.message);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Scrape endpoint
app.post('/v1/scrape', async (req, res) => {
  try {
    const { url } = req.body;
    
    const response = await axios.get(url, {
      timeout: 30000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; LocalFirecrawl/1.0)'
      }
    });
    
    const $ = cheerio.load(response.data);
    
    // Remove script and style elements
    $('script, style').remove();
    
    const title = $('title').text().trim();
    const content = $('body').text().replace(/\s+/g, ' ').trim();
    
    res.json({
      success: true,
      data: {
        title,
        content: content.substring(0, 10000), // Limit content length
        url,
        markdown: `# ${title}\n\n${content.substring(0, 5000)}`
      }
    });
  } catch (error) {
    console.error('Scrape error:', error.message);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Local Firecrawl server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
EOF
    
    log_success "Local Firecrawl installed!"
}

install_deep_research() {
    log_info "Installing Deep Research MCP..."
    
    cd "$TEMP_DIR"
    
    # Clone repository
    if [ ! -d "deep-research-mcp" ]; then
        git clone https://github.com/Ozamatash/deep-research-mcp.git
    fi
    
    cd deep-research-mcp
    
    # Copy source files
    cp -r src "$MCP_SERVERS_DIR/deep-research/" 2>/dev/null || true
    cp package*.json "$MCP_SERVERS_DIR/deep-research/" 2>/dev/null || true
    cp tsconfig.json "$MCP_SERVERS_DIR/deep-research/" 2>/dev/null || true
    
    # Create optimized Dockerfile with Node 20 (requirement for eventsource-parser)
    cat > "$MCP_SERVERS_DIR/deep-research/Dockerfile" << 'EOF'
FROM node:20-alpine

WORKDIR /app

# Install TypeScript globally
RUN npm install -g typescript

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build TypeScript
RUN npm run build

# Create reports directory
RUN mkdir -p reports

# Expose port
EXPOSE 3000

# Start the HTTP server
CMD ["npm", "run", "start:http"]
EOF
    
    # Create .env.local for configuration
    cat > "$MCP_SERVERS_DIR/deep-research/.env.local" << 'EOF'
FIRECRAWL_BASE_URL=http://firecrawl:3002
MODEL=local
NODE_ENV=production
EOF
    
    log_success "Deep Research MCP installed!"
}

install_searxng_mcp() {
    log_info "Installing SearXNG MCP Server..."
    
    # Install globally via npm
    npm install -g mcp-searxng
    
    log_success "SearXNG MCP Server installed globally!"
}

create_searxng_config() {
    log_info "Creating SearXNG configuration..."
    
    # Create settings.yml for SearXNG
    cat > "$MCP_SERVERS_DIR/searxng/settings/settings.yml" << 'EOF'
# SearXNG Configuration
use_default_settings: true

general:
  debug: false
  instance_name: "Hello Pulse AI Search"

search:
  safe_search: 0
  autocomplete: ""
  default_lang: "all"
  formats:
    - html
    - json

server:
  port: 8080
  bind_address: "0.0.0.0"
  secret_key: "ultrasecretkey"
  base_url: false
  image_proxy: true

ui:
  static_use_hash: false
  default_theme: simple
  default_locale: ""
  theme_args:
    simple_style: auto

redis:
  url: redis://redis:6379/0

engines:
  - name: duckduckgo
    engine: duckduckgo
    categories: general
    shortcut: ddg
    disabled: false

  - name: google
    engine: google
    categories: general
    shortcut: go
    disabled: false

  - name: wikipedia
    engine: wikipedia
    categories: general
    shortcut: wp
    disabled: false

  - name: bing
    engine: bing
    categories: general
    shortcut: bi
    disabled: false
EOF
    
    # Replace the secret key placeholder with the actual key
    local secret_key
    secret_key=$(grep "SEARXNG_SECRET_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    sed -i "s/ultrasecretkey/$secret_key/g" "$MCP_SERVERS_DIR/searxng/settings/settings.yml"
    
    log_success "SearXNG configuration created!"
}

create_mcp_config() {
    log_info "Creating MCP configuration..."
    
    cat > "$PROJECT_ROOT/mcp_config.json" << 'EOF'
{
  "mcpServers": {
    "searxng": {
      "command": "mcp-searxng",
      "env": {
        "SEARXNG_URL": "http://localhost:8888"
      }
    },
    "deep-research": {
      "command": "docker",
      "args": [
        "exec", "-i", "deep-research", 
        "node", "dist/index.js"
      ],
      "env": {
        "FIRECRAWL_BASE_URL": "http://firecrawl:3002"
      }
    },
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type", "http",
        "--host", "localhost",
        "--port", "8000"
      ]
    }
  }
}
EOF
    
    log_success "MCP configuration created!"
}

start_services() {
    log_info "Starting Docker services..."
    
    cd "$PROJECT_ROOT"
    
    # Build and start services
    docker compose build
    docker compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    log_info "Checking service status..."
    docker compose ps
    
    log_success "Services started!"
}

cleanup_temp() {
    log_info "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    log_success "Cleanup completed!"
}

# === MAIN FUNCTION ===
main() {
    echo "🚀 Hello Pulse AI - MCP Servers Installation"
    echo "============================================="
    echo ""
    
    check_requirements
    create_directory_structure
    generate_searxng_secret
    
    # Install MCP servers
    install_firecrawl
    install_deep_research
    install_searxng_mcp
    
    # Configure services
    create_searxng_config
    create_mcp_config
    
    # Start everything
    start_services
    
    # Cleanup
    cleanup_temp
    
    echo ""
    log_success "🎉 Installation completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Configure your MCP client to use: $PROJECT_ROOT/mcp_config.json"
    echo "2. Test the services:"
    echo "   - SearXNG: http://localhost:8888"
    echo "   - Firecrawl: http://localhost:3002/health"
    echo "   - Chroma: http://localhost:8000/api/v1/heartbeat"
    echo ""
    echo "🔧 Management Commands:"
    echo "  - Check status: docker compose ps"
    echo "  - View logs: docker compose logs -f [service_name]"
    echo "  - Stop services: docker compose down"
    echo "  - Restart: docker compose restart"
    echo ""
}

# Run the installation
main "$@"