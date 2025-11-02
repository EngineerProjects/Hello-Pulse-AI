#!/bin/bash

# === CONFIGURATION ===
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_SERVERS_DIR="$PROJECT_ROOT/mcp_servers"
DATA_DIR="$PROJECT_ROOT/data"
ENV_FILE="$PROJECT_ROOT/.env"

# === COLORS FOR OUTPUT ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    echo -e "${RED}[ERROR]${NC} $1"
}

# === UTILITY FUNCTIONS ===
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available. Please update Docker to the latest version."
        exit 1
    fi
    
    # Check npm for MCP server installation
    if ! command -v npm &> /dev/null; then
        log_error "npm is not installed. Please install Node.js and npm first."
        exit 1
    fi
    
    log_success "All requirements met!"
}

create_directory_structure() {
    log_info "Creating directory structure..."
    
    # Create only SearXNG directories
    mkdir -p "$MCP_SERVERS_DIR/searxng/settings"
    mkdir -p "$DATA_DIR/searxng"
    mkdir -p "$PROJECT_ROOT/logs"
    
    log_success "Directory structure created!"
}

generate_searxng_secret() {
    log_info "Generating SearXNG secret key..."
    
    # Generate a secure random key
    local secret_key
    secret_key=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xxd -p)
    
    # Create or update .env file
    if [ -f "$ENV_FILE" ]; then
        # Update existing key or add if not present
        if grep -q "SEARXNG_SECRET_KEY=" "$ENV_FILE"; then
            sed -i "s/SEARXNG_SECRET_KEY=.*/SEARXNG_SECRET_KEY=$secret_key/" "$ENV_FILE"
        else
            echo "SEARXNG_SECRET_KEY=$secret_key" >> "$ENV_FILE"
        fi
    else
        echo "SEARXNG_SECRET_KEY=$secret_key" > "$ENV_FILE"
    fi
    
    log_success "SearXNG secret key generated!"
}

install_searxng_mcp() {
    log_info "Installing SearXNG MCP Server..."
    
    # Install globally via npm (official package)
    npm install -g mcp-searxng
    
    log_success "SearXNG MCP Server installed globally!"
}

create_searxng_config() {
    log_info "Creating optimized SearXNG configuration..."
    
    # Only create if doesn't exist
    if [ ! -f "$MCP_SERVERS_DIR/searxng/settings/settings.yml" ]; then
        cat > "$MCP_SERVERS_DIR/searxng/settings/settings.yml" << 'EOF'
# SearXNG Configuration - Optimized for MCP
use_default_settings: true

general:
  debug: false
  instance_name: "Hello Pulse AI Search"
  enable_metrics: false

search:
  safe_search: 0
  autocomplete: ""
  default_lang: "all"
  ban_time_on_fail: 5
  max_ban_time_on_fail: 120
  # Results configuration
  results_on_new_tab: 0
  infinite_scroll: false
  formats:
    - html
    - json

server:
  port: 8080
  bind_address: "0.0.0.0"
  secret_key: "ultrasecretkey"
  base_url: false
  image_proxy: true
  method: "GET"
  http_protocol_version: "1.1"

ui:
  static_use_hash: false
  default_theme: simple
  default_locale: ""
  theme_args:
    simple_style: auto
  hotkeys: disabled

# Redis cache configuration
redis:
  url: redis://redis:6379/0

# Optimized outgoing configuration
outgoing:
  request_timeout: 10.0
  max_request_timeout: 15.0
  useragent_suffix: "Hello-Pulse-AI"
  pool_connections: 100
  pool_maxsize: 20
  enable_http2: true

# Default search engines with result limits
engines:
  - name: duckduckgo
    engine: duckduckgo
    categories: [general, web]
    shortcut: ddg
    disabled: false
    timeout: 10.0
    # DuckDuckGo specific settings
    paging: true

  - name: google
    engine: google
    categories: [general, web]
    shortcut: go
    disabled: false
    timeout: 10.0
    # Google specific settings
    paging: true
    use_mobile_ui: false

  - name: wikipedia
    engine: wikipedia
    categories: [general]
    shortcut: wp
    disabled: false
    timeout: 10.0
    paging: true

  - name: bing
    engine: bing
    categories: [general, web]
    shortcut: bi
    disabled: false
    timeout: 10.0
    paging: true

  - name: startpage
    engine: startpage
    categories: [general, web]
    shortcut: sp
    disabled: false
    timeout: 10.0
    paging: true
EOF
    fi
    
    # Replace the secret key placeholder with the actual key
    local secret_key
    secret_key=$(grep "SEARXNG_SECRET_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    sed -i "s/ultrasecretkey/$secret_key/g" "$MCP_SERVERS_DIR/searxng/settings/settings.yml"
    
    log_success "Optimized SearXNG configuration created!"
}

start_services() {
    log_info "Starting Docker services..."
    
    cd "$PROJECT_ROOT"
    
    # Stop any existing services
    docker compose down 2>/dev/null || true
    
    # Start services (no build needed - only official images)
    log_info "Starting SearXNG and Redis services..."
    docker compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 20
    
    # Check service health
    log_info "Checking service status..."
    docker compose ps
    
    log_success "Services started!"
}

# === MAIN FUNCTION ===
main() {
    echo "🚀 Hello Pulse AI - SearXNG MCP Installation (Optimized)"
    echo "======================================================"
    echo ""
    
    check_requirements
    create_directory_structure
    generate_searxng_secret
    
    # Install SearXNG MCP (the only thing we need)
    install_searxng_mcp
    
    # Configure and start services
    create_searxng_config
    start_services
    
    echo ""
    echo "📋 Services Running:"
    echo "  - SearXNG: http://localhost:8888"
    echo "  - Redis: Internal cache"
    echo ""
    echo "🛠  MCP Server Installed:"
    echo "  - mcp-searxng (global npm package)"
    echo ""
    echo "⚙️  SearXNG Features:"
    echo "  - 5 search engines (DDG, Google, Bing, Wikipedia, Startpage)"
    echo "  - Optimized timeouts (10s per engine)"
    echo "  - Redis caching enabled"
    echo "  - Pagination support"
    echo ""
    echo "✅ Setup Complete! SearXNG MCP is ready to use in OpenCode."
    echo ""
    echo "💡 Usage Tips:"
    echo "  - Control results via MCP: searxng_web_search(query='...', pageno=1)"
    echo "  - Default: ~10 results per page, use pageno for more"
    echo "  - Use web_url_read for detailed content extraction"
    echo ""
}

# Run the installation
main "$@"
