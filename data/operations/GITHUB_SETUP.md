# GitHub Setup Guide

**Note:** This guide is for the original HAL8000-Assistant system setup. If you are **forking HAL8000-Assistant to create your own personalized system**, use the **Fork and Rebrand Protocol** instead:
- See: `data/architecture/fork-and-rebrand-protocol.md`
- The Fork and Rebrand Protocol covers cloning, renaming, and GitHub repository isolation

This guide is for pushing the original HAL8000-Assistant repository to GitHub.

## Prerequisites

- Git installed
- GitHub account
- GitHub CLI (`gh`) installed (optional, but recommended)

## Step 1: Configure Git Identity

Before creating commits, configure your git identity:

```bash
# Set your name and email (used for commits)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Or set it only for this repository (without --global)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Step 2: Create Initial Commit

Now that git is configured, create the initial commit:

```bash
git commit -m "$(cat <<'EOF'
Initial commit: HAL8000-Assistant v1.4.0

Complete computer architecture system for Claude Code sessions.

Features:
- Modified von Neumann architecture (CPU/RAM/Memory model)
- HAL-Script natural language programming
- 11 built-in commands (system, development, documentation)
- 6 specialized sub-agents (research, context-finding, maintenance)
- 3 external tools (diagrams, document processing, gemini)
- MCP integration (omnisearch, filesystem, IDE)
- Session continuity protocol
- 7-level prompt template system
- Complete reference manual (HTML)

System Components:
- BIOS: CLAUDE.md (boot instructions, architecture principles)
- Commands: .claude/commands/ (HAL-Script executable programs)
- Agents: .claude/agents/ (specialized sub-processes)
- Libraries: .claude/libraries/ (internal templates + external fabric patterns)
- Tools: .claude/tools/ (diagram-generation, docling-cli, gemini-cli)
- Data: research, architecture docs, reference manual

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Step 3: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

```bash
# Create repository (choose public or private)
gh repo create HAL8000-Assistant --public --source=. --remote=origin --push

# Or for private repository
gh repo create HAL8000-Assistant --private --source=. --remote=origin --push
```

This command will:
- Create the repository on GitHub
- Add GitHub as the remote 'origin'
- Push your code automatically

### Option B: Using GitHub Web Interface

1. Go to [GitHub](https://github.com) and log in
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `HAL8000-Assistant`
4. Description: "Computer architecture for Claude Code sessions - von Neumann principles, HAL-Script programming, session continuity"
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (we already have them)
7. Click **Create repository**

Then connect your local repository:

```bash
# Add remote
git remote add origin https://github.com/VirtualZardoz/HAL8000-Assistant.git

# Push to GitHub
git push -u origin main
```

## Step 4: Verify Upload

Check that everything uploaded correctly:

```bash
# View remote URL
git remote -v

# Check what's on GitHub
gh repo view --web
# Or manually visit: https://github.com/VirtualZardoz/HAL8000-Assistant
```

## Step 5: Update README.md (Complete!)

The README.md has been updated with your GitHub repository URL:
- Repository: https://github.com/VirtualZardoz/HAL8000-Assistant
- Clone command: `git clone https://github.com/VirtualZardoz/HAL8000-Assistant.git`
- Issues link: https://github.com/VirtualZardoz/HAL8000-Assistant/issues

## Security Checklist

Before pushing, verify these sensitive files are NOT included:

```bash
# Check that .env is NOT staged
git status | grep ".env$" && echo "⚠️  WARNING: .env is staged!" || echo "✓ .env excluded"

# Check that settings.local.json is NOT staged
git status | grep "settings.local.json" && echo "⚠️  WARNING: settings.local.json is staged!" || echo "✓ settings.local.json excluded"

# View all staged files
git ls-files
```

If any sensitive files are staged:

```bash
# Remove from staging
git rm --cached .env
git rm --cached .claude/settings.local.json

# Commit the removal
git commit -m "Remove sensitive files from tracking"
```

## Excluded Files (by .gitignore)

The following files are automatically excluded and will NOT be pushed to GitHub:

### Security (Sensitive Data)
- `.env` - API keys and secrets
- `.claude/settings.local.json` - Personal paths and permissions
- `*.key`, `*.pem`, `*secret*`, `*credential*` - Any other sensitive files

### System State
- `.claude/system.log` - Large runtime log

### Temporary Files
- `*.tmp`, `*.cache`, `*.log`
- `__pycache__/`, `*.pyc`
- `node_modules/`, `dist/`, `build/`

### Work-in-Progress
- `*draft*` files
- `data/reference-manual/refactored/` - Working versions
- `data/reference-manual/critiques/` - Editorial reviews
- `data/reference-manual/prompts/` - Development prompts

### IDE Files
- `.vscode/`, `.idea/`
- `*.swp`, `.DS_Store`

## Optional: Add GitHub Topics

After creating the repository, add topics for discoverability:

1. Go to your repository on GitHub
2. Click the gear icon next to "About"
3. Add topics: `claude-code`, `ai-architecture`, `von-neumann`, `hal-script`, `mcp`, `prompt-engineering`, `agent-systems`, `session-continuity`

## Optional: Create LICENSE

If you want to add an open-source license:

```bash
# Create MIT License (or choose another at https://choosealicense.com)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Add and commit
git add LICENSE
git commit -m "Add MIT License"
git push
```

## Ongoing Maintenance

### Making Changes

```bash
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Before Each Commit

1. **Verify no sensitive data**: Check that no new API keys or personal paths were accidentally added
2. **Test locally**: Ensure system boots and commands work
3. **Update VERSION and CHANGELOG**: If making a release

### Recommended Workflow

```bash
# Work on feature/fix
# ...make changes...

# Check what changed
git status
git diff

# Stage changes
git add <specific files>  # or git add . for all

# Commit
git commit -m "Brief description

Detailed explanation if needed"

# Push
git push
```

## Troubleshooting

### "Permission denied (publickey)"

Set up SSH keys or use HTTPS:

```bash
# Switch to HTTPS
git remote set-url origin https://github.com/VirtualZardoz/HAL8000-Assistant.git
```

### "Updates were rejected"

Someone else pushed changes (if collaborating):

```bash
git pull --rebase origin main
git push
```

### Accidentally Committed Sensitive File

```bash
# Remove from history (DANGER: rewrites history)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (only if you haven't shared the repo yet)
git push origin --force --all
```

**Better**: If you just committed but haven't pushed:

```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Remove sensitive file
git rm --cached .env

# Add to .gitignore
echo ".env" >> .gitignore

# Commit again
git add .gitignore
git commit -m "Remove sensitive file and update .gitignore"
```

## Next Steps

After pushing to GitHub:

1. ⭐ Star your own repository (for easy access)
2. 📝 Update README.md with your actual GitHub username
3. 🔍 Add GitHub topics for discoverability
4. 📄 Add LICENSE if desired
5. 🎯 Create GitHub Issues for planned features
6. 📊 Set up GitHub Actions for CI/CD (optional)

## For Fork Users

If you forked HAL8000-Assistant to create your own personalized system, follow the complete **Fork and Rebrand Protocol**:
- **Location:** `data/architecture/fork-and-rebrand-protocol.md`
- **What it covers:**
  - Cloning from GitHub (fork or direct clone)
  - Complete filesystem rebrand (all references updated)
  - Git isolation (prevent commits to original HAL8000-Assistant)
  - Git reconnection (connect to your new repository)
  - Verification and testing
- **Why use it:** Ensures your customizations stay in your repository and don't accidentally get pushed to the original HAL8000-Assistant repo

## Resources

- [GitHub Documentation](https://docs.github.com)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Choose a License](https://choosealicense.com)
- [Git Documentation](https://git-scm.com/doc)

---

**You're ready to share HAL8000-Assistant with the world!** 🚀
