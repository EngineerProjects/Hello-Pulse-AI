# Hello Pulse AI - Scripts Guide

This directory contains scripts for managing your MCP servers and development environment.

## 🚀 Installation Scripts

### `install_mcps.sh` - Main Installation Script

Modular installation script for MCP servers with support for different environments.

#### Usage:
```bash
# Local development (default)
./scripts/install_mcps.sh
./scripts/install_mcps.sh local

# Production-ready setup
./scripts/install_mcps.sh production
```

#### What it installs:
- **Wikipedia MCP Server**: Free knowledge base access
- **SearXNG Stack**: Privacy-focused search engine
- **Advanced Scraper**: Web scraping capabilities
- **Docker Services**: Containers for SearXNG, Redis, Caddy (production)
- **Configuration Files**: MCP configuration for your client

#### Environment Differences:
| Feature | Local | Production |
|---------|-------|------------|
| Domain | localhost | localhost (configurable) |
| HTTPS | No | Yes (with Caddy) |
| Redis Cache | No | Yes |
| Security Headers | Basic | Full |
| Rate Limiting | No | Yes |

## 🧹 Cleanup Scripts

### `clean.sh` - Complete Cleanup Script

Comprehensive cleanup script that removes all installed components.

#### Usage:
```bash
# Interactive cleanup (prompts before deleting data)
./scripts/clean.sh

# Automated cleanup (keeps data)
echo "n" | ./scripts/clean.sh

# Full reset (deletes everything)
echo "y" | ./scripts/clean.sh
```

#### What it cleans:
- Python caches and build directories
- MCP servers (`~/mcp-servers`)
- Docker containers, networks, and images
- Configuration files (docker-compose.yml, Caddyfile, .env)
- SearXNG configuration and logs
- Temporary files

## 📋 Quick Start Guide

### For Local Development:
```bash
# 1. Install everything
./scripts/install_mcps.sh local

# 2. Check services
docker-compose ps

# 3. Test in your MCP client
# - Load mcp_config.json
# - Try searching with Wikipedia or SearXNG
```

### For Production Setup:
```bash
# 1. Install production stack
./scripts/install_mcps.sh production

# 2. (Optional) Configure domain
nano .env
# Edit: SEARXNG_HOSTNAME=your-domain.com

# 3. Restart services
docker-compose down && docker-compose up -d

# 4. Check services
docker-compose ps
```

### To Clean Everything:
```bash
# Interactive cleanup
./scripts/clean.sh

# Or to reinstall everything:
./scripts/clean.sh && ./scripts/install_mcps.sh local
```

## 🔧 Management Commands

### Docker Services:
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Update services
docker-compose pull && docker-compose up -d
```

### MCP Servers:
```bash
# Check installation
ls -la ~/mcp-servers/

# Test Wikipedia MCP
node ~/mcp-servers/wikipedia-mcp/src/index.js

# Test SearXNG
curl http://localhost:8888/search?q=test
```

## 🌐 Access Points

After installation:

| Service | Local URL | Production URL |
|---------|-----------|----------------|
| SearXNG UI | http://localhost:8888 | https://localhost |
| Wikipedia MCP | ~/mcp-servers/wikipedia-mcp/src/index.js | Same |
| Advanced Scraper | ~/mcp-servers/advanced-scraper/src/index.js | Same |

## ⚠️ Important Notes

1. **No Domain Required**: Local development works perfectly with `localhost`
2. **Data Protection**: Clean script asks before deleting data
3. **Port Conflicts**: Make sure port 8888 is available
4. **Docker Required**: Ensure Docker and Docker Compose are installed
5. **Node.js Required**: For MCP servers (use your existing Node.js installation)

## 🐛 Troubleshooting

### Port Already in Use:
```bash
# Check what's using port 8888
sudo lsof -i :8888

# Kill the process
sudo kill -9 <PID>
```

### Docker Issues:
```bash
# Reset Docker
docker system prune -f

# Rebuild containers
docker-compose down && docker-compose up -d --force-recreate
```

### MCP Server Not Working:
```bash
# Check installation
ls -la ~/mcp-servers/

# Reinstall specific MCP server
./scripts/install_mcps.sh && install_wikipedia_mcp
```

## 📁 File Structure

After installation, your project will look like:
```
Hello-Pulse-AI/
├── scripts/
│   ├── install_mcps.sh
│   └── clean.sh
├── docker-compose.yml
├── Caddyfile          # Production only
├── .env               # Production only
├── mcp_config.json
├── searxng/            # Production only
└── logs/               # Production only

~/mcp-servers/
├── wikipedia-mcp/
├── advanced-scraper/
└── mcp-searxng/        # If installed locally
```

## 🔄 Development Workflow

1. **Start**: `./scripts/install_mcps.sh local`
2. **Develop**: Test with your MCP client
3. **Clean**: `./scripts/clean.sh` (when needed)
4. **Production**: `./scripts/install_mcps.sh production`
```

---

## 📄 Save this as `scripts/README.md`

```bash
# Create the README file
cat > scripts/README.md << 'EOF'
[Paste the markdown content above here]
EOF
```

This README provides a comprehensive guide for anyone using your scripts, with clear instructions for different scenarios and troubleshooting tips!