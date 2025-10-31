#!/bin/bash
# install_mcps.sh - Complete modular MCP server installation (local only)

set -e

# Configuration
MCP_DIR="$HOME/mcp-servers"
PROJECT_DIR="$(pwd)"
ENV_FILE="$PROJECT_DIR/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to ensure directory exists with proper permissions
ensure_directory() {
    local dir_path="$1"
    
    # Remove existing directory if it exists
    if [ -d "$dir_path" ]; then
        log_info "Removing existing directory: $dir_path"
        rm -rf "$dir_path"
    fi
    
    # Create directory with proper permissions
    mkdir -p "$dir_path"
    
    # Verify directory exists and is writable
    if [ ! -d "$dir_path" ] || [ ! -w "$dir_path" ]; then
        log_error "Cannot create or write to directory: $dir_path"
        exit 1
    fi
}

# Function to update or add environment variable in .env file
update_env_var() {
    local key="$1"
    local value="$2"
    
    # Create .env file if it doesn't exist
    if [ ! -f "$ENV_FILE" ]; then
        touch "$ENV_FILE"
    fi
    
    # Check if the key exists in the file
    if grep -q "^${key}=" "$ENV_FILE"; then
        # Update existing key
        sed -i "s/^${key}=.*/${key}=${value}/" "$ENV_FILE"
    else
        # Add new key
        echo "${key}=${value}" >> "$ENV_FILE"
    fi
}

# Function to get environment variable from .env file
get_env_var() {
    local key="$1"
    local default_value="$2"
    
    if [ -f "$ENV_FILE" ] && grep -q "^${key}=" "$ENV_FILE"; then
        grep "^${key}=" "$ENV_FILE" | cut -d'=' -f2-
    else
        echo "$default_value"
    fi
}

# MCP Server Installation Functions
install_wikipedia_mcp() {
    log_info "Installing Wikipedia MCP Server..."
    
    # Ensure clean directory
    local wikipedia_dir="$MCP_DIR/wikipedia-mcp"
    ensure_directory "$wikipedia_dir"
    
    cd /tmp
    git clone https://github.com/Rudra-ravi/wikipedia-mcp.git
    cd wikipedia-mcp
    
    npm install
    npm audit fix
    
    # Copy only necessary files (exclude .git to avoid permission issues)
    log_info "Copying Wikipedia MCP files..."
    rsync -av --exclude='.git' --exclude='node_modules' . "$wikipedia_dir/"
    
    cd /
    rm -rf /tmp/wikipedia-mcp
    
    log_success "Wikipedia MCP Server installed successfully!"
}

install_advanced_scraper() {
    log_info "Installing Advanced Scraper MCP Server..."
    
    # Ensure clean directory
    local scraper_dir="$MCP_DIR/advanced-scraper"
    ensure_directory "$scraper_dir"
    
    cat > "$scraper_dir/package.json" << 'EOF'
{
  "name": "advanced-scraper-mcp",
  "version": "1.0.0",
  "description": "Advanced web scraper MCP server",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "axios": "^1.6.0",
    "cheerio": "^1.0.0-rc.12",
    "puppeteer": "^21.0.0"
  }
}
EOF
    
    mkdir -p "$scraper_dir/src"
    cat > "$scraper_dir/src/index.js" << 'EOF'
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const axios = require('axios');
const cheerio = require('cheerio');

const server = new Server(
  {
    name: 'advanced-scraper',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'scrape_url',
        description: 'Scrape content from a URL',
        inputSchema: {
          type: 'object',
          properties: {
            url: { type: 'string' },
            selector: { type: 'string', description: 'CSS selector to extract specific content' }
          },
          required: ['url']
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    if (name === 'scrape_url') {
      const response = await axios.get(args.url);
      const $ = cheerio.load(response.data);
      
      let content;
      if (args.selector) {
        content = $(args.selector).text();
      } else {
        content = $('body').text();
      }
      
      return {
        content: [
          {
            type: 'text',
            text: `Scraped content from ${args.url}:\n\n${content.substring(0, 5000)}`
          }
        ]
      };
    }
    
    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Advanced Scraper MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
EOF
    
    cd "$scraper_dir"
    npm install
    
    log_success "Advanced Scraper MCP Server installed successfully!"
}

install_searxng_mcp() {
    log_info "Installing SearXNG MCP Server via npm..."
    
    # Install globally
    npm install -g mcp-searxng
    
    log_success "SearXNG MCP Server installed via npm!"
}

install_local_firecrawl() {
    log_info "Installing Local Firecrawl with SearXNG..."
    
    # Ensure clean project directories
    ensure_directory "$PROJECT_DIR/localfirecrawl"
    
    cd /tmp
    git clone https://github.com/Ozamatash/localfirecrawl.git
    cd localfirecrawl
    
    # Generate or get existing secret key
    local searxng_secret_key
    searxng_secret_key=$(get_env_var "SEARXNG_SECRET_KEY" "")
    
    if [ -z "$searxng_secret_key" ]; then
        searxng_secret_key=$(openssl rand -hex 32)
        update_env_var "SEARXNG_SECRET_KEY" "$searxng_secret_key"
        log_info "Generated new SearXNG secret key"
    else
        log_info "Using existing SearXNG secret key"
    fi
    
    # Create .env file
    cat > .env << EOF
SEARXNG_SECRET_KEY=$searxng_secret_key
SEARXNG_ENGINES=google,duckduckgo,wikipedia
SEARXNG_CATEGORIES=general
PORT=3002
EOF
    
    # Create Dockerfile with npm install instead of npm ci
    cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Use npm install instead of npm ci to avoid package-lock.json requirement
RUN npm install --only=production

COPY . .

EXPOSE 3002

CMD ["npm", "start"]
EOF
    
    # Create package.json if it doesn't exist
    if [ ! -f "package.json" ]; then
        log_info "Creating missing package.json for Local Firecrawl..."
        cat > package.json << 'EOF'
{
  "name": "localfirecrawl",
  "version": "1.0.0",
  "description": "Local Firecrawl with SearXNG",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.18.0",
    "axios": "^1.6.0",
    "cheerio": "^1.0.0-rc.12"
  }
}
EOF
    fi
    
    # Create basic index.js if it doesn't exist
    if [ ! -f "index.js" ]; then
        log_info "Creating basic index.js for Local Firecrawl..."
        cat > index.js << 'EOF'
const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();
const PORT = process.env.PORT || 3002;

app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'localfirecrawl' });
});

// Search endpoint
app.post('/v1/search', async (req, res) => {
  try {
    const { query, limit = 10 } = req.body;
    
    // For now, return a simple response
    // In a full implementation, this would use SearXNG
    res.json({
      results: [
        {
          title: `Search result for: ${query}`,
          url: `https://example.com/search?q=${encodeURIComponent(query)}`,
          snippet: `This is a placeholder result for the query: ${query}`
        }
      ]
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Scrape endpoint
app.post('/v1/scrape', async (req, res) => {
  try {
    const { url } = req.body;
    
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    
    const title = $('title').text();
    const content = $('body').text().substring(0, 5000);
    
    res.json({
      title,
      content,
      url
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Local Firecrawl running on port ${PORT}`);
});
EOF
    fi
    
    # Copy to project directory (exclude .git)
    log_info "Copying Local Firecrawl files..."
    rsync -av --exclude='.git' --exclude='node_modules' . "$PROJECT_DIR/localfirecrawl/"
    
    cd /
    rm -rf /tmp/localfirecrawl
    
    log_success "Local Firecrawl installed!"
    log_info "🔑 SearXNG Secret Key stored in .env file"
}

install_deep_research_mcp() {
    log_info "Installing Deep Research MCP Server..."
    
    # Ensure clean project directories
    ensure_directory "$PROJECT_DIR/deep-research-mcp"
    
    cd /tmp
    git clone https://github.com/Ozamatash/deep-research-mcp.git
    cd deep-research-mcp
    
    # Create Dockerfile for the MCP server
    cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start:http"]
EOF
    
    # Create .env.local file
    cat > .env.local << EOF
FIRECRAWL_BASE_URL=http://localfirecrawl:3002
MODEL=local
EOF
    
    # Copy to project directory (exclude .git)
    log_info "Copying Deep Research MCP files..."
    rsync -av --exclude='.git' --exclude='node_modules' . "$PROJECT_DIR/deep-research-mcp/"
    
    # Create reports directory
    mkdir -p "$PROJECT_DIR/deep-research-mcp/reports"
    
    cd /
    rm -rf /tmp/deep-research-mcp
    
    log_success "Deep Research MCP Server installed!"
}

# Docker Compose Generation Function
create_docker_compose() {
    local compose_file="$PROJECT_DIR/docker-compose.yml"
    
    log_info "Creating docker-compose.yml for local environment..."
    
    # Get the secret key from .env
    local searxng_secret_key
    searxng_secret_key=$(get_env_var "SEARXNG_SECRET_KEY" "")
    
    cat > "$compose_file" << EOF
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"
    restart: unless-stopped
    networks:
      - mcp_network

  localfirecrawl:
    build:
      context: ./localfirecrawl
      dockerfile: Dockerfile
    container_name: localfirecrawl
    environment:
      - SEARXNG_SECRET_KEY=$searxng_secret_key
      - SEARXNG_ENGINES=google,duckduckgo,wikipedia
      - SEARXNG_CATEGORIES=general
      - PORT=3002
    depends_on:
      - searxng
    restart: unless-stopped
    networks:
      - mcp_network
    ports:
      - "3002:3002"

  deep-research:
    build:
      context: ./deep-research-mcp
      dockerfile: Dockerfile
    container_name: deep-research
    environment:
      - FIRECRAWL_BASE_URL=http://localfirecrawl:3002
      - MODEL=local
    depends_on:
      - localfirecrawl
    restart: unless-stopped
    networks:
      - mcp_network
    volumes:
      - ./deep-research-mcp/reports:/app/reports

networks:
  mcp_network:
    driver: bridge
EOF
    
    log_success "docker-compose.yml created for local environment"
}

# Environment Setup Function
setup_local_environment() {
    log_info "Setting up LOCAL development environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f "$ENV_FILE" ]; then
        touch "$ENV_FILE"
        log_info "Created .env file"
    fi
    
    # Install all MCP servers
    install_wikipedia_mcp
    install_advanced_scraper
    install_searxng_mcp
    install_local_firecrawl
    install_deep_research_mcp
    
    # Create docker-compose.yml
    create_docker_compose
    
    # Start services
    cd "$PROJECT_DIR"
    log_info "Starting Docker services..."
    docker compose up -d
    
    # Create local MCP config
    create_mcp_config
    
    log_success "Local environment setup complete!"
    log_info "🌐 SearXNG UI: http://localhost:8888"
    log_info "🔥 Firecrawl API: http://localhost:3002"
    log_info "🔬 Deep Research: http://localhost:3000/mcp"
}

# MCP Configuration Function
create_mcp_config() {
    local config_file="$PROJECT_DIR/mcp_config.json"
    
    log_info "Creating MCP configuration for local environment..."
    
    # Base configuration with npm-based SearXNG MCP
    cat > "$config_file" << EOF
{
  "serverConfig": {
    "command": "/bin/sh",
    "args": ["-c"]
  },
  "mcpServers": {
    "desktop-commander": {
      "command": "/home/amiche/.nvm/versions/node/v22.21.0/bin/desktop-commander"
    },
    "chrome": {
      "command": "node",
      "args": [
        "/home/amiche/.nvm/versions/node/v22.21.0/lib/node_modules/mcp-chrome-bridge/dist/mcp/mcp-server-stdio.js"
      ]
    },
    "tavily": {
      "command": "python",
      "args": ["-m", "mcp_server_tavily"],
      "env": {
        "TAVILY_API_KEY": "\${TAVILY_API_KEY}"
      }
    },
    "wikipedia": {
      "command": "node",
      "args": [
        "$MCP_DIR/wikipedia-mcp/src/index.js"
      ]
    },
    "searxng": {
      "command": "mcp-searxng",
      "env": {
        "SEARXNG_URL": "http://localhost:8888"
      }
    },
    "advanced-scraper": {
      "command": "node",
      "args": [
        "$MCP_DIR/advanced-scraper/src/index.js"
      ]
    },
    "deep-research": {
      "command": "docker",
      "args": [
        "exec", "-i", "deep-research", "node", "dist/index.js"
      ],
      "env": {
        "FIRECRAWL_BASE_URL": "http://localfirecrawl:3002"
      }
    }
  }
}
EOF
    
    log_success "MCP configuration created: $config_file"
}

# Main execution
main() {
    echo "🚀 Hello Pulse AI - Local MCP Server Installation"
    echo "==============================================="
    echo ""
    
    log_info "MCP Directory: $MCP_DIR"
    log_info "Project Directory: $PROJECT_DIR"
    log_info "Environment File: $ENV_FILE"
    echo ""
    
    # Only local environment setup
    setup_local_environment
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 15
    
    # Check service status
    log_info "Checking service status..."
    docker compose ps
    
    echo ""
    log_success "🎉 Local installation finished!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Restart your MCP client (Claude Desktop, Cursor, etc.)"
    echo "2. Load the configuration from: $PROJECT_DIR/mcp_config.json"
    echo "3. Test the MCP servers"
    echo ""
    echo "🔧 Management Commands:"
    echo "  - Check services: docker compose ps"
    echo "  - View logs: docker compose logs -f"
    echo "  - Stop services: docker compose down"
    echo "  - Clean everything: ./clean.sh"
    echo ""
    echo "🌐 Access Points:"
    echo "  - SearXNG: http://localhost:8888"
    echo "  - Firecrawl API: http://localhost:3002"
    echo "  - Deep Research: http://localhost:3000/mcp"
    echo ""
    echo "🔑 Secret Key Management:"
    echo "  - SearXNG Secret Key stored in: $ENV_FILE"
    echo "  - To view: cat $ENV_FILE"
    echo "  - To update: update_env_var SEARXNG_SECRET_KEY new_key"
}

# Run main function
main "$@"