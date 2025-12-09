# 🎯 Hello Pulse AI - Optimized Structure

Complete AI agent with MCP (Model Context Protocol) servers for data science and research tasks.

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <your-repo>
cd Hello-Pulse-AI

# 2. Install MCP servers
chmod +x scripts/*.sh
./scripts/install_mcps.sh

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start development
python main.py
```

## 📁 Project Structure

```
Hello-Pulse-AI/
├── README.md                    # This file
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── docker-compose.yml           # Main services configuration
├── requirements.txt             # Python dependencies
├── config.yml                   # Agent configuration
├── mcp_config.json             # MCP servers configuration
├── main.py                     # Main application entry
│
├── scripts/                    # Management scripts
│   ├── README.md               # Scripts documentation
│   ├── install_mcps.sh         # Install all MCP servers
│   ├── clean.sh                # Complete cleanup
│   └── dockerfiles/            # Custom Dockerfiles
│       ├── Dockerfile.firecrawl
│       └── Dockerfile.deepresearch
│
├── mcp_servers/                # MCP servers (auto-generated)
│   ├── searxng/                # SearXNG configuration
│   ├── firecrawl/              # Local Firecrawl source
│   ├── deep-research/          # Deep Research MCP source
│   └── chroma/                 # Chroma configurations
│
├── data/                       # Persistent data (auto-generated)
│   ├── searxng/                # SearXNG data
│   ├── firecrawl/              # Firecrawl data
│   ├── deep-research/          # Research reports
│   └── chroma/                 # Vector database data
│
├── mcp/                        # MCP manager
│   └── mcp_manager.py          # MCP integration logic
│
└── logs/                       # Application logs (auto-generated)
```

## 🛠️ MCP Servers Included

### 🔍 **SearXNG** (Port 8888)
- Privacy-focused search engine
- No API costs, fully local
- JSON API for programmatic access
- Redis caching for performance

### 🕷️ **Local Firecrawl** (Port 3002)
- Web scraping without API costs
- Markdown conversion
- Rate limiting and caching
- SearXNG integration for search

### 🔬 **Deep Research MCP**
- AI-powered iterative research
- Source reliability scoring
- Comprehensive report generation
- Integration with local services

### 🧠 **Chroma Vector DB** (Port 8000)
- Vector search and storage
- Embedding support
- Knowledge base functionality
- Local deployment

### 📚 **Wikipedia MCP**
- Direct Wikipedia access
- No API limitations
- Structured knowledge retrieval

### 🌐 **SearXNG MCP**
- MCP interface for SearXNG
- Programmatic search capabilities
- Pagination and filtering

## 🔧 Key Features

### ✅ **Fully Local & Private**
- No external API dependencies for core search
- Data remains on your infrastructure
- Privacy-focused architecture

### ✅ **Cost Effective**
- Avoid expensive search APIs
- Free alternatives to premium services
- Minimal resource requirements

### ✅ **Docker-First Architecture**
- Easy deployment and scaling
- Isolated services
- Health checks and monitoring

### ✅ **Modular Design**
- Independent MCP servers
- Easy to add/remove components
- Clean separation of concerns

## 🔑 Environment Variables

Required:
- `GOOGLE_API_KEY`: For main AI agent

Optional:
- `OPENAI_API_KEY`: For Deep Research MCP
- `TAVILY_API_KEY`: Enhanced search capabilities

Auto-generated:
- `SEARXNG_SECRET_KEY`: Secure SearXNG deployment

## 🚀 Service Management

```bash
# Check service status
docker compose ps

# View logs
docker compose logs -f [service_name]

# Restart specific service
docker compose restart [service_name]

# Stop all services
docker compose down

# Complete cleanup and reinstall
./scripts/clean.sh && ./scripts/install_mcps.sh
```

## 🌐 Access Points

After installation:
- **SearXNG Interface**: http://localhost:8888
- **Firecrawl API**: http://localhost:3002
- **Chroma Database**: http://localhost:8000
- **Deep Research**: Available via MCP

## 📋 Manual Installations

Some MCP servers require manual installation:

### Desktop Commander
```bash
npm install -g desktop-commander-mcp
```

### Chrome MCP
```bash
npm install -g mcp-chrome-bridge
```

Refer to their respective GitHub repositories for detailed instructions.

## 🔄 Development Workflow

1. **Setup**: Run `./scripts/install_mcps.sh`
2. **Develop**: Modify agent logic in `main.py`
3. **Test**: Use MCP servers via the agent
4. **Debug**: Check logs with `docker compose logs`
5. **Clean**: Use `./scripts/clean.sh` for fresh start

## 🐛 Troubleshooting

### Services won't start
```bash
# Check Docker status
docker compose ps

# View detailed logs
docker compose logs [service_name]

# Restart problematic service
docker compose restart [service_name]
```

### Port conflicts
Edit `docker-compose.yml` to change port mappings.

### Permission issues
```bash
# Fix script permissions
chmod +x scripts/*.sh
```

### Clean reinstall
```bash
./scripts/clean.sh
./scripts/install_mcps.sh
```

## 🎯 Use Cases

- **Research Automation**: Deep dive into topics with source verification
- **Data Collection**: Web scraping and content aggregation
- **Knowledge Management**: Vector-based storage and retrieval
- **Market Analysis**: Automated research and report generation
- **Content Creation**: Research-backed content development

## 🛡️ Security

- Non-root Docker containers
- Local data processing
- No external data transmission
- Secure secret management
- Network isolation

## 📈 Performance

- Redis caching for search
- Optimized Docker images
- Health checks and monitoring
- Horizontal scaling ready

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test with `docker compose up`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using Pydantic AI + MCP Protocol**
