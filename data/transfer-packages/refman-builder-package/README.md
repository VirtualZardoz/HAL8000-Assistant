# Reference Manual Builder - Transfer Package

**A complete system for building comprehensive technical documentation across multiple Claude Code sessions.**

---

## Quick Start

1. **Read SETUP_GUIDE.md** for complete installation and usage instructions
2. **Copy files** to your project structure:
   - `commands/HAL-refman.md` → `.claude/commands/documentation/`
   - `agents/documentation-writer.md` → `.claude/agents/`
3. **Create your manual** at `data/reference-manual/index.html`
4. **Run** `/HAL-refman status` to verify setup

---

## What This Does

- ✅ **Session-independent manual development** - Work across multiple sessions
- ✅ **Intelligent context management** - Save ~70% RAM per section
- ✅ **Structured workflow** - Status tracking, priorities, dependencies
- ✅ **Multiple operation modes** - Status, development, auto-select, export, diagrams

---

## Package Contents

```
refman-builder-package/
├── README.md                         # This file (quick overview)
├── SETUP_GUIDE.md                    # Complete installation & usage guide
├── commands/
│   └── HAL-refman.md                 # Main command
├── agents/
│   └── documentation-writer.md       # Content generation agent
└── example/
    └── reference-manual-template.html # Working example (32 sections)
```

---

## Requirements

- Claude Code
- Directory structure: `.claude/commands/`, `.claude/agents/`
- State tracking: `.claude/state.json`

**No dependency on HAL8000** (works standalone)

---

## Key Features

### Context Optimization
- Main session: Loads only metadata (~2K tokens)
- Sub-agent: Handles heavy writing in isolated context
- Integration: Returns clean HTML only
- **Result: ~70% RAM savings vs. direct approach**

### Section Metadata System
Each section tracks:
- Status (draft → in_progress → complete)
- Priority (1-5)
- Source files to read
- Dependencies on other sections
- Writing guidelines (hidden in HTML)

### Workflow Modes
```bash
/HAL-refman status              # Progress dashboard
/HAL-refman next                # Auto-select next priority section
/HAL-refman [section-id]        # Work on specific section
/HAL-refman diagrams            # List visual placeholders
/HAL-refman export              # Generate final clean manual
```

---

## Proven In Production

**Tested with:**
- HAL8000 Reference Manual v1.2.0
- 32 sections, 75,000+ words
- 21 visual placeholders
- Multiple development sessions
- Complete success

---

## Documentation

**SETUP_GUIDE.md contains:**
- Detailed installation steps
- Section metadata schema reference
- Complete usage guide
- Technical architecture overview
- Customization instructions
- Troubleshooting guide
- Examples and best practices

**Start there for everything you need.**

---

## License

Part of HAL8000 system. See main repository for license.

---

**Ready to build? Read SETUP_GUIDE.md and start documenting!**
