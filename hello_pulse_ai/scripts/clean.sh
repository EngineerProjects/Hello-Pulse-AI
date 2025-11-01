#!/bin/bash

# Hello Pulse AI - Comprehensive Cleanup Script
# Removes all installed MCP servers, Docker containers, and generated files

set -euo pipefail

# === CONFIGURATION ===
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
readonly MCP_SERVERS_DIR="$PROJECT_ROOT/mcp_servers"
readonly DATA_DIR="$PROJECT_ROOT/data"
readonly LOGS_DIR="$PROJECT_ROOT/logs"
readonly TEMP_DIR="/tmp/hello-pulse-ai-install"

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

# === CONFIRMATION FUNCTION ===
confirm() {
    local prompt="$1"
    local default="${2:-n}"
    local response
    
    if [ "$default" = "y" ] || [ "$default" = "Y" ]; then
        prompt="$prompt [Y/n]: "
    else
        prompt="$prompt [y/N]: "
    fi
    
    while true; do
        read -p "$prompt" response
        response=${response:-$default}
        
        case $response in
            [Yy]|[Yy][Ee][Ss]) return 0 ;;
            [Nn]|[Nn][Oo]) return 1 ;;
            *) echo "Please answer yes or no." ;;
        esac
    done
}

# === CLEANUP FUNCTIONS ===
stop_and_remove_containers() {
    log_info "Stopping and removing Docker containers..."
    
    cd "$PROJECT_ROOT" 2>/dev/null || true
    
    # Stop and remove containers defined in docker-compose.yml
    if [ -f "docker-compose.yml" ]; then
        docker compose down --volumes --remove-orphans 2>/dev/null || true
        log_success "Docker containers stopped and removed"
    else
        log_warning "No docker-compose.yml found, skipping container cleanup"
    fi
    
    # Remove individual containers if they exist
    local containers=("searxng" "firecrawl" "deep-research" "chroma" "redis")
    for container in "${containers[@]}"; do
        if docker ps -a --format "table {{.Names}}" | grep -q "^$container$" 2>/dev/null; then
            log_info "Removing container: $container"
            docker rm -f "$container" 2>/dev/null || true
        fi
    done
}

remove_docker_images() {
    if confirm "Remove Docker images built for this project?"; then
        log_info "Removing Docker images..."
        
        # Remove images by tag pattern
        local images=(
            "hello-pulse-ai_firecrawl"
            "hello-pulse-ai_deep-research"
            "hello-pulse-ai-firecrawl"
            "hello-pulse-ai-deep-research"
        )
        
        for image in "${images[@]}"; do
            if docker images --format "table {{.Repository}}" | grep -q "$image" 2>/dev/null; then
                log_info "Removing image: $image"
                docker rmi "$image" 2>/dev/null || true
            fi
        done
        
        log_success "Docker images removed"
    fi
}

remove_docker_volumes() {
    if confirm "Remove Docker volumes (this will delete all data)?"; then
        log_info "Removing Docker volumes..."
        
        # Remove project-specific volumes
        local volumes=(
            "hello-pulse-ai_redis_data"
            "hello-pulse-ai_chroma_data"
            "redis_data"
            "chroma_data"
        )
        
        for volume in "${volumes[@]}"; do
            if docker volume ls --format "table {{.Name}}" | grep -q "$volume" 2>/dev/null; then
                log_info "Removing volume: $volume"
                docker volume rm "$volume" 2>/dev/null || true
            fi
        done
        
        log_success "Docker volumes removed"
    fi
}

remove_docker_network() {
    log_info "Removing Docker network..."
    
    if docker network ls --format "table {{.Name}}" | grep -q "mcp_network" 2>/dev/null; then
        docker network rm mcp_network 2>/dev/null || true
        log_success "Docker network removed"
    fi
}

uninstall_global_packages() {
    if confirm "Uninstall globally installed npm packages?"; then
        log_info "Uninstalling global npm packages..."
        
        # List of packages to uninstall
        local packages=("mcp-searxng" "chroma-mcp")
        
        for package in "${packages[@]}"; do
            if npm list -g --depth=0 2>/dev/null | grep -q "$package"; then
                log_info "Uninstalling: $package"
                npm uninstall -g "$package" 2>/dev/null || true
            fi
        done
        
        log_success "Global packages uninstalled"
    fi
}

remove_project_directories() {
    log_info "Removing project directories..."
    
    # Remove MCP servers directory
    if [ -d "$MCP_SERVERS_DIR" ]; then
        rm -rf "$MCP_SERVERS_DIR"
        log_success "Removed: $MCP_SERVERS_DIR"
    fi
    
    # Remove data directory
    if [ -d "$DATA_DIR" ]; then
        if confirm "Remove data directory (contains application data)?"; then
            rm -rf "$DATA_DIR"
            log_success "Removed: $DATA_DIR"
        fi
    fi
    
    # Remove logs directory
    if [ -d "$LOGS_DIR" ]; then
        rm -rf "$LOGS_DIR"
        log_success "Removed: $LOGS_DIR"
    fi
    
    # Remove temp directory
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        log_success "Removed: $TEMP_DIR"
    fi
}

remove_configuration_files() {
    log_info "Removing configuration files..."
    
    cd "$PROJECT_ROOT"
    
    # List of files to remove
    local files=(
        ".dockerignore"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            log_success "Removed: $file"
        fi
    done
}

clean_python_artifacts() {
    log_info "Cleaning Python artifacts..."
    
    cd "$PROJECT_ROOT"
    
    # Remove Python cache files and directories
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    
    # Remove virtual environments
    if [ -d "venv" ]; then
        rm -rf venv
        log_success "Removed Python virtual environment"
    fi
    
    if [ -d ".venv" ]; then
        rm -rf .venv
        log_success "Removed Python virtual environment (.venv)"
    fi
    
    log_success "Python artifacts cleaned"
}

clean_node_artifacts() {
    log_info "Cleaning Node.js artifacts..."
    
    cd "$PROJECT_ROOT"
    
    # Remove node_modules directories
    find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
    
    # Remove package-lock.json files
    find . -type f -name "package-lock.json" -delete 2>/dev/null || true
    
    # Remove npm cache
    find . -type d -name ".npm" -exec rm -rf {} + 2>/dev/null || true
    
    log_success "Node.js artifacts cleaned"
}

clean_environment_file() {
    if confirm "Remove MCP-related entries from .env file?"; then
        if [ -f "$PROJECT_ROOT/.env" ]; then
            # Remove MCP-related environment variables
            sed -i '/SEARXNG_SECRET_KEY=/d' "$PROJECT_ROOT/.env" 2>/dev/null || true
            sed -i '/FIRECRAWL_/d' "$PROJECT_ROOT/.env" 2>/dev/null || true
            sed -i '/CHROMA_/d' "$PROJECT_ROOT/.env" 2>/dev/null || true
            
            log_success "Cleaned .env file"
        fi
    fi
}

remove_cloned_repositories() {
    log_info "Removing cloned repositories..."
    
    # Check for repositories that might have been cloned to project root
    local repos=("deep-research-mcp" "localfirecrawl")
    
    for repo in "${repos[@]}"; do
        if [ -d "$PROJECT_ROOT/$repo" ]; then
            rm -rf "$PROJECT_ROOT/$repo"
            log_success "Removed cloned repository: $repo"
        fi
    done
}

# === MAIN CLEANUP FUNCTION ===
main() {
    echo "🧹 Hello Pulse AI - Comprehensive Cleanup"
    echo "========================================="
    echo ""
    
    log_warning "This script will remove all MCP servers, Docker containers, and related files."
    echo ""
    
    if ! confirm "Are you sure you want to proceed with the cleanup?"; then
        log_info "Cleanup cancelled by user"
        exit 0
    fi
    
    echo ""
    log_info "Starting cleanup process..."
    echo ""
    
    # Docker cleanup
    stop_and_remove_containers
    remove_docker_images
    remove_docker_volumes
    remove_docker_network
    
    # Global packages cleanup
    uninstall_global_packages
    
    # Project files cleanup
    remove_project_directories
    remove_configuration_files
    remove_cloned_repositories
    
    # Development artifacts cleanup
    clean_python_artifacts
    clean_node_artifacts
    
    # Environment cleanup
    clean_environment_file
    
    echo ""
    log_success "🎉 Cleanup completed successfully!"
    echo ""
    echo "📋 What was cleaned:"
    echo "  ✅ Docker containers and images"
    echo "  ✅ Docker volumes and networks"
    echo "  ✅ Global npm packages"
    echo "  ✅ Project directories and files"
    echo "  ✅ Python and Node.js artifacts"
    echo "  ✅ Configuration files"
    echo "  ✅ Temporary files"
    echo ""
    echo "🔄 To reinstall everything, run:"
    echo "   ./scripts/install_mcps.sh"
    echo ""
}

# Run the cleanup
main "$@"
