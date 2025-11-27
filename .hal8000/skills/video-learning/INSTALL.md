# Video Learning Skill - Installation Guide

## Quick Installation

### For HAL Instances

1. **Copy this directory to your HAL instance**:
   ```bash
   cp -r video-learning /path/to/your/hal/.claude/skills/
   ```

2. **Copy command files** (these are required for the skill to work):
   ```bash
   # Command playbook (the actual instructions)
   cp HAL-learn-video-command.md /path/to/your/hal/.claude/commands/HAL-learn-video.md

   # Context pointer (UFC navigation)
   cp HAL-learn-video-context.md /path/to/your/hal/.claude/context/commands/HAL-learn-video.md
   ```

3. **Install dependencies**:
   ```bash
   # yt-dlp (video downloader)
   pip install yt-dlp

   # FFmpeg (frame extractor) - platform specific:
   # macOS: brew install ffmpeg
   # Ubuntu/WSL: sudo apt install ffmpeg
   # Windows: scoop install ffmpeg
   ```

4. **Verify installation**:
   ```bash
   yt-dlp --version
   ffmpeg -version
   ```

5. **Test the skill**:
   - Start Claude Code in your HAL directory
   - Try: "Learn from this video: https://youtu.be/dQw4w9WgXcQ"
   - Skill should auto-detect and invoke `/HAL-learn-video`

## What Gets Installed

### Skill Directory (`.claude/skills/video-learning/`)
- `SKILL.md` - Claude Code skill definition (auto-detection logic)
- `README.md` - User documentation
- `INSTALL.md` - This installation guide

### Command Files
- `.claude/commands/HAL-learn-video.md` - Command playbook (processing instructions)
- `.claude/context/commands/HAL-learn-video.md` - UFC context pointer

### Dependencies (External)
- `yt-dlp` - Python package for YouTube video/caption download
- `ffmpeg` - Media processing tool for frame extraction
- Fabric patterns - Should already exist at `.claude/tools/fabric-patterns/`

## Directory Structure After Installation

```
your-hal-instance/
├── .claude/
│   ├── skills/
│   │   └── video-learning/          ← Skill (this directory)
│   │       ├── SKILL.md
│   │       ├── README.md
│   │       └── INSTALL.md
│   ├── commands/
│   │   └── HAL-learn-video.md       ← Command playbook
│   ├── context/
│   │   └── commands/
│   │       └── HAL-learn-video.md   ← Context pointer
│   └── tools/
│       └── fabric-patterns/         ← Should already exist
└── inbox/
    └── video-learning/              ← Created on first use
```

## Dependency Installation Details

### yt-dlp

**Option 1: pip (recommended)**
```bash
pip install yt-dlp
```

**Option 2: System package manager**
```bash
# macOS
brew install yt-dlp

# Windows (Scoop)
scoop install yt-dlp

# Windows (Chocolatey)
choco install yt-dlp
```

**Verify installation:**
```bash
yt-dlp --version
# Should output: 2024.xx.xx or similar
```

### FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian/WSL:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows (Scoop):**
```bash
scoop install ffmpeg
```

**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Manual):**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg\` (or your preferred location)
3. Add `C:\ffmpeg\bin\` to PATH
4. Restart terminal

**Verify installation:**
```bash
ffmpeg -version
# Should output: ffmpeg version x.x.x
```

### Fabric Patterns

If your HAL instance doesn't have fabric patterns:

```bash
# Clone fabric repository
git clone https://github.com/danielmiessler/fabric.git /tmp/fabric

# Copy patterns to HAL
mkdir -p .claude/tools/fabric-patterns
cp -r /tmp/fabric/patterns/* .claude/tools/fabric-patterns/

# Or use HAL command if available
/HAL-update-fabric-patterns
```

## Platform-Specific Notes

### WSL2 + Windows
If running Claude Code in WSL2 with Windows as host:
- Install yt-dlp in WSL: `pip install yt-dlp`
- FFmpeg can be Windows or WSL installation
- Command handles path conversions automatically

### macOS
- Use homebrew for easy dependency management
- All paths are Unix-style, no special handling needed

### Native Windows
- Use Scoop or Chocolatey for dependencies
- Paths are Windows-style, command handles conversion
- Git Bash recommended for CLI operations

## Verification Checklist

After installation, verify:

- [ ] Skill directory exists: `.claude/skills/video-learning/`
- [ ] Command exists: `.claude/commands/HAL-learn-video.md`
- [ ] Context pointer exists: `.claude/context/commands/HAL-learn-video.md`
- [ ] yt-dlp installed: `yt-dlp --version` works
- [ ] FFmpeg installed: `ffmpeg -version` works
- [ ] Fabric patterns exist: `.claude/tools/fabric-patterns/` has content
- [ ] Test URL works: Try processing a short YouTube video

## Troubleshooting Installation

### "Skill not detected"
- Verify SKILL.md exists in `.claude/skills/video-learning/`
- Check YAML frontmatter format in SKILL.md
- Restart Claude Code session

### "Command not found: /HAL-learn-video"
- Verify `HAL-learn-video.md` exists in `.claude/commands/`
- File must be in commands directory, not skills directory

### "yt-dlp not found"
- Install via pip: `pip install yt-dlp`
- Check PATH: `which yt-dlp` (Unix) or `where yt-dlp` (Windows)
- Try full path in command if needed

### "ffmpeg not found"
- Install platform-specific FFmpeg (see above)
- Check PATH: `which ffmpeg` (Unix) or `where ffmpeg` (Windows)
- For WSL: Use Windows FFmpeg path: `/mnt/c/path/to/ffmpeg.exe`

### "No fabric patterns"
- Clone fabric repo and copy patterns (see Fabric Patterns section)
- Or create empty `.claude/tools/fabric-patterns/` and download later
- Skill will work without patterns but won't apply AI analysis

## Updating

To update the skill to a newer version:

1. **Backup current installation** (optional):
   ```bash
   cp -r .claude/skills/video-learning .claude/skills/video-learning.backup
   ```

2. **Copy new version**:
   ```bash
   cp -r new-video-learning/* .claude/skills/video-learning/
   ```

3. **Update commands if changed**:
   ```bash
   cp new-HAL-learn-video.md .claude/commands/HAL-learn-video.md
   cp new-HAL-learn-video-context.md .claude/context/commands/HAL-learn-video.md
   ```

4. **Restart Claude Code**

## Uninstallation

To remove the skill:

```bash
# Remove skill
rm -rf .claude/skills/video-learning

# Remove commands
rm .claude/commands/HAL-learn-video.md
rm .claude/context/commands/HAL-learn-video.md

# Optionally remove dependencies
pip uninstall yt-dlp
# (FFmpeg should be kept as other tools may use it)

# Keep or remove output
# .claude/tools/fabric-patterns/ - keep (used by other skills)
# inbox/video-learning/ - keep or remove based on preference
```

## Getting Help

If you encounter issues:

1. Check this INSTALL.md troubleshooting section
2. Verify dependencies with version commands
3. Check README.md for usage examples
4. Review SKILL.md for technical details
5. Test with a simple, short YouTube video first

## Version

- **Skill Version**: 1.0
- **Installation Guide**: 2025-10-30
- **Compatible with**: Claude Code, HAL 7000 system
