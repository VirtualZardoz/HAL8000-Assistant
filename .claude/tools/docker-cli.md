# Docker CLI - Containerized Tool Execution

**Category:** External Tool (Infrastructure)
**Interface:** Bash command-line tool
**Purpose:** Isolated execution environments for tools with dependencies
**Installation:** Host-installed
**Version:** 28.4.0

---

## Overview

Docker CLI provides containerized execution environments for tools with heavy dependencies. Unlike host-installed tools (Gemini CLI) or internal sub-agents, Docker creates isolated containers where tools run without polluting the host system.

**Architectural Position:**
```
HAL8000 (Claude, host environment)
    ↓ command
Docker Container (isolated environment)
    ↓ execute tool with dependencies
    ↓ output via stdout or mounted volumes
HAL8000 (receives results, container disposed)
```

---

## Use Cases

### Primary Use Cases

1. **Python Tools with Heavy Dependencies**
   - Tool needs specific Python packages
   - Dependencies conflict with host environment
   - Want to avoid pip install pollution

2. **Temporary Execution Environments**
   - One-off tasks requiring specific environment
   - Testing tools in isolation
   - Reproducible execution across different hosts

3. **Multi-Container Orchestration**
   - Tool requires multiple services (database + app)
   - Use Docker Compose for complex setups
   - Networked services in isolated environment

4. **Version-Specific Tools**
   - Need specific version of tool/runtime
   - Multiple versions of same tool
   - Lock dependencies for reproducibility

### When NOT to Use Docker

- Tool already installed on host and working (use host tool instead - Unix simplicity)
- Single-file scripts with no dependencies (run directly)
- Native binaries available (Docker overhead unnecessary)
- Real-time interaction required (container adds latency)

---

## Docker Environment Status

**Current Host:**
- Docker version: 28.4.0
- Docker daemon: Running
- Available images: 10
- Running containers: 5

**Running Services:**
- searxng (port 3100)
- open-webui (port 3200)
- watchtower (auto-update)
- perplexica-frontend (port 3300)
- perplexica-backend (port 3001)

---

## Command Patterns

### Temporary Containers (One-Off Tasks)

**Basic Pattern:**
```bash
docker run --rm [image] [command]
```

**With Mounted Volumes (for data exchange):**
```bash
docker run --rm -v /mnt/d/~HAL8000/data:/data [image] [command]
```

**Interactive Shell:**
```bash
docker run --rm -it [image] bash
```

**Environment Variables:**
```bash
docker run --rm -e API_KEY=$API_KEY [image] [command]
```

**Example - Python script with dependencies:**
```bash
# Create Dockerfile
cat > temp/Dockerfile <<EOF
FROM python:3.11-slim
RUN pip install pandas numpy requests
COPY script.py /app/script.py
WORKDIR /app
CMD ["python", "script.py"]
EOF

# Build image
docker build -t hal-python-tool temp/

# Run container
docker run --rm -v /mnt/d/~HAL8000/data:/data hal-python-tool
```

### Persistent Containers

**Create and start:**
```bash
docker create --name tool-container [image]
docker start tool-container
docker exec tool-container [command]
```

**Stop and remove:**
```bash
docker stop tool-container
docker rm tool-container
```

### Docker Compose (Multi-Container)

**Compose file pattern:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: python:3.11
    volumes:
      - ./data:/data
    environment:
      - API_KEY=${API_KEY}
    command: python /data/script.py
```

**Execute:**
```bash
docker-compose up -d  # Start in background
docker-compose logs   # View output
docker-compose down   # Stop and remove
```

---

## Integration with HAL8000

### Pattern 1: Dockerfile-Based Tool

**Structure:**
```
.claude/tools/
├── docker-cli.md (this file)
└── [tool-name]/
    ├── Dockerfile
    ├── requirements.txt
    └── README.md
```

**Workflow:**
1. Create Dockerfile defining environment
2. Build image: `docker build -t hal-[tool-name] .claude/tools/[tool-name]/`
3. Run when needed: `docker run --rm hal-[tool-name] [args]`
4. Results via stdout or mounted volume

### Pattern 2: Existing Image

**Use public images directly:**
```bash
# Example: Run Python script with pandas
docker run --rm -v $(pwd)/data:/data python:3.11 \
  bash -c "pip install pandas && python /data/script.py"
```

### Pattern 3: Data Exchange

**Input/Output via volumes:**
```bash
# Write input data
echo "data" > temp/input.txt

# Run container with volume
docker run --rm \
  -v /mnt/d/~HAL8000/temp:/workspace \
  [image] process-tool /workspace/input.txt > /workspace/output.txt

# Read output
cat temp/output.txt
```

---

## Best Practices

### 1. Clean Up After Yourself

**Always use `--rm` for temporary containers:**
```bash
docker run --rm ...  # Container auto-deleted after exit
```

**Prune unused resources periodically:**
```bash
docker system prune -a  # Remove unused images, containers, networks
```

### 2. Minimize Image Size

**Use slim base images:**
```dockerfile
FROM python:3.11-slim  # Not python:3.11 (500MB vs 1GB)
```

**Multi-stage builds:**
```dockerfile
# Build stage
FROM python:3.11 as builder
RUN pip install --user pandas

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
```

### 3. Security

**Don't run as root when possible:**
```dockerfile
USER nobody
```

**Use specific versions:**
```dockerfile
FROM python:3.11.5-slim  # Not :latest
```

**Don't embed secrets:**
```bash
docker run -e API_KEY=$API_KEY ...  # Pass via env, not in image
```

### 4. Reproducibility

**Pin versions in requirements.txt:**
```
pandas==2.0.3
numpy==1.24.3
```

**Document exact Docker version:**
```markdown
Tested with Docker 28.4.0
```

---

## Example: Creating a Python Analysis Tool

### Step 1: Define Tool

**File: `.claude/tools/data-analyzer/Dockerfile`**
```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir \
    pandas==2.0.3 \
    numpy==1.24.3 \
    matplotlib==3.7.2

# Create workspace
WORKDIR /workspace

# Default command
CMD ["python"]
```

**File: `.claude/tools/data-analyzer/README.md`**
```markdown
# Data Analyzer Tool

Dockerized Python environment for data analysis.

## Build
docker build -t hal-data-analyzer .claude/tools/data-analyzer/

## Usage
docker run --rm -v $(pwd)/data:/workspace hal-data-analyzer python script.py
```

### Step 2: Build Image

```bash
docker build -t hal-data-analyzer .claude/tools/data-analyzer/
```

### Step 3: Use Tool

```bash
# Write analysis script
cat > data/analyze.py <<EOF
import pandas as pd
df = pd.read_csv('/workspace/data.csv')
print(df.describe())
EOF

# Run analysis
docker run --rm -v /mnt/d/~HAL8000/data:/workspace \
  hal-data-analyzer python /workspace/analyze.py
```

---

## Available Images

**Host has these images:**
- `ghcr.io/open-webui/open-webui:main-cuda` (16.6GB - GPU support)
- `ghcr.io/searxng/searxng:latest` (218MB)
- `us-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.4.1` (1.26GB - Gemini sandbox)
- `python:3.11-slim` (not shown but available via Docker Hub)
- `mariadb:10.4` (527MB)

**Public registries:**
- Docker Hub: `docker pull [image]`
- GitHub Container Registry: `docker pull ghcr.io/[org]/[image]`
- Google Artifact Registry: `docker pull [region]-docker.pkg.dev/[project]/[image]`

---

## RAM vs Docker Comparison

**Docker vs Sub-Agents:**

| Aspect | Sub-Agent (Task tool) | Docker Container |
|--------|---------------------|------------------|
| RAM Impact | Uses HAL8000 context (200K) | No context impact (external process) |
| Execution | Inside Claude Code | Outside Claude Code |
| Dependencies | HAL8000 tools only | Any dependencies (pip, npm, etc.) |
| Overhead | Minimal (context spawn) | Higher (container startup ~1-2s) |
| Use For | Research, discovery, light tasks | Heavy computation, isolated deps |

**Docker vs Gemini CLI:**

| Aspect | Gemini CLI (External Agent) | Docker Container |
|--------|---------------------------|------------------|
| Purpose | AI agent with huge context | Tool execution environment |
| Context | 1M tokens | N/A (not an AI) |
| Use For | Heavy AI analysis/refactoring | Isolated tool execution |
| Installation | Host npm package | Container runtime |

---

## Comparison: Host vs Docker vs Gemini

**Decision Matrix:**

```
Tool Type: Python script with heavy dependencies
Host: ❌ (pollutes environment)
Docker: ✅ (isolated, clean)
Gemini: ❌ (overkill for non-AI task)

Tool Type: Massive codebase analysis
Host: ❌ (insufficient context)
Docker: ❌ (not an AI agent)
Gemini: ✅ (1M context, perfect fit)

Tool Type: Simple bash command
Host: ✅ (Unix simplicity)
Docker: ❌ (unnecessary overhead)
Gemini: ❌ (overkill)
```

---

## Integration Pattern

**When user requests tool creation:**

1. **Assess Requirements:**
   - Dependencies needed?
   - Conflicts with host?
   - Reproducibility important?

2. **Choose Approach:**
   - Host tool if simple/available
   - Docker if dependencies/isolation needed
   - Gemini if AI analysis required

3. **Implement:**
   - Create Dockerfile if needed
   - Build image
   - Document usage in `.claude/tools/[tool-name]/README.md`
   - Update tools index

4. **Execute:**
   - Run via `docker run --rm ...`
   - Capture output via stdout or volumes
   - Clean up containers automatically

---

## Tool Discovery

Docker CLI is discoverable via:
1. **Tool index:** `.claude/indexes/tools.json`
2. **Direct path:** `.claude/tools/docker-cli.md` (this file)
3. **Context finder:** `/HAL-context-find docker` loads this doc

---

## Future Enhancements

**Potential additions:**
- Pre-built images for common tools (Python, Node.js, Rust)
- Docker Compose templates for multi-service tools
- Volume management helpers
- Image registry for HAL-specific tools
- Automated cleanup scheduler

---

## Related Documentation

- **Gemini CLI:** `.claude/tools/gemini-cli.md` - External AI agent
- **MCP Tools:** `.claude/tools/mcp/` - MCP server management
- **I/O System:** `data/architecture/hal8000-io-system.md` - Extended I/O interfaces

---

## Summary

Docker CLI enables HAL8000 to execute tools in isolated containers:
- **No host pollution** - Dependencies stay in containers
- **Reproducible** - Same environment every time
- **Flexible** - Any tool, any language, any dependencies
- **Unix philosophy** - Compose containers like Unix pipes
- **RAM efficient** - Execution happens outside context window

**Integration Pattern:**
```
Task Needs Dependencies → Create Dockerfile → Build Image → Run Container → Get Results
```

This extends HAL8000's capabilities beyond what's installed on the host, enabling execution of any tool in any environment while maintaining system cleanliness.
