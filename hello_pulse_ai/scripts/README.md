# Hello Pulse AI - Scripts

Management scripts for MCP servers installation and maintenance.

## 🚀 Quick Start

```bash
# Install all MCP servers
./scripts/install_mcps.sh

# Clean everything
./scripts/clean.sh
```

## 📁 Scripts Overview

### `install_mcps.sh`
Installs and configures all MCP servers with Docker:
- **SearXNG**: Privacy-focused search engine (port 8888)
- **Firecrawl**: Web scraping service (port 3002)
- **Deep Research**: AI research agent (Docker container)
- **Chroma**: Vector database (port 8000)
- **Redis**: Caching for SearXNG

**Features:**
- Automatic secret key generation for SearXNG
- Optimized Docker configurations
- Health checks for all services
- Proper network isolation

### `clean.sh`
Comprehensive cleanup script that removes:
- Docker containers, images, and volumes
- Global npm packages
- Project directories and configuration files
- Python/Node.js artifacts
- Cloned repositories

**Safety features:**
- Interactive confirmation prompts
- Selective cleanup options
- Preserves user data by default

## 🔧 Usage Examples

```bash
# Check service status
docker compose ps

# View logs
docker compose logs -f [service_name]

# Restart services
docker compose restart

# Stop services
docker compose down

# Complete removal and reinstall
./scripts/clean.sh && ./scripts/install_mcps.sh
```

## 🌐 Service Endpoints

After installation, services are available at:
- **SearXNG UI**: http://localhost:8888
- **Firecrawl API**: http://localhost:3002
- **Chroma API**: http://localhost:8000
- **Health checks**: Add `/health` or `/api/v1/heartbeat`

## 📋 Requirements

- Docker & Docker Compose
- Node.js & npm
- Git
- OpenSSL

## 🔑 Environment Variables

The installation script automatically generates:
- `SEARXNG_SECRET_KEY`: Secure key for SearXNG

Optional variables you can add to `.env`:
- `OPENAI_API_KEY`: For Deep Research MCP
- `TAVILY_API_KEY`: For Tavily search

## 🗂️ Directory Structure

```
project_root/
├── mcp_servers/          # MCP server configurations
│   ├── searxng/         # SearXNG settings
│   ├── firecrawl/       # Local Firecrawl source
│   ├── deep-research/   # Deep Research MCP source
│   └── chroma/          # Chroma configurations
├── data/                # Persistent data
└── docker-compose.yml   # Main services configuration
```

## 🛠️ Troubleshooting

**Services won't start:**
```bash
# Check logs
docker compose logs

# Restart specific service
docker compose restart [service_name]
```

**Port conflicts:**
Edit `docker-compose.yml` to change port mappings.

**Clean install:**
```bash
./scripts/clean.sh
./scripts/install_mcps.sh
```

---

*For manual MCP servers installation (Desktop Commander, Chrome MCP), please refer to their respective GitHub repositories.*
