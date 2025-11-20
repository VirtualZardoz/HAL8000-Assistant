# HAL8000-Assistant Feature Selection Guide
# Skills vs. Sub-Agents vs. Commands Decision Framework

**Version:** 1.0
**Created:** 2025-10-30
**Based on:** Claude Code best practices and HAL8000-Assistant architecture validation

---

## Purpose

This guide provides a systematic framework for deciding when to use **Skills**, **Sub-Agents**, or **Commands** when extending HAL8000-Assistant capabilities. Each feature type serves distinct architectural purposes, and choosing correctly impacts context efficiency, user experience, and system maintainability.

**Reference:** This framework aligns with Claude Code community best practices as documented in `data/videos/i-finally-cracked-claude-agent-skills/knowledge-brief.md`.

---

## The Three-Layer Model

HAL8000-Assistant's extensibility is built on a three-layer pattern where each layer has specific characteristics:

```
┌─────────────────────────────────────────────────────────┐
│ SKILLS (Proactive Intelligence)                         │
│ - Agent-triggered automatically                         │
│ - Context-efficient (progressive disclosure)            │
│ - High modularity (dedicated directories)               │
│ - Use for: Repeat solutions, pattern detection          │
└─────────────────────────────────────────────────────────┘
                         ↓ Delegates to
┌─────────────────────────────────────────────────────────┐
│ COMMANDS (User Control)                                 │
│ - User-triggered explicitly (/HAL-*)                    │
│ - Context persistent                                    │
│ - Medium modularity (HAL-Script files)                  │
│ - Use for: State operations, critical workflows         │
└─────────────────────────────────────────────────────────┘
                         ↓ Delegates to
┌─────────────────────────────────────────────────────────┐
│ SUB-AGENTS (Context Isolation)                          │
│ - CPU-triggered (delegated from Skills/Commands)        │
│ - Isolated 200K RAM (fresh context)                     │
│ - No persistence (volatility by design)                 │
│ - Use for: Heavy processing, context protection         │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Decision Tree

Start here for rapid feature classification:

```
┌─ Need to extend HAL8000-Assistant capabilities ─┐
│                                        │
├─ Q1: Who should trigger it?            │
│  ├─ Agent automatically  → SKILL       │
│  ├─ User explicitly      → COMMAND     │
│  └─ CPU delegates work   → SUB-AGENT   │
│                                        │
├─ Q2: Context requirements?             │
│  ├─ Need persistence     → SKILL/COMMAND
│  ├─ Need isolation       → SUB-AGENT   │
│  └─ Heavy processing     → SUB-AGENT   │
│                                        │
├─ Q3: Repeat solution pattern?          │
│  ├─ Yes, modular         → SKILL       │
│  ├─ Yes, user-controlled → COMMAND     │
│  └─ One-off task         → (any)       │
│                                        │
└─ Q4: Context efficiency critical?      │
   ├─ Avoid window explosion → SKILL    │
   ├─ Need isolation         → SUB-AGENT│
   └─ Varies                 → COMMAND   │
```

---

## Detailed Comparison

### Architectural Dimensions

| Dimension | Skills | Commands | Sub-Agents |
|-----------|--------|----------|------------|
| **Invocation** | Automatic (agent) | Explicit (user) | Delegated (CPU) |
| **Trigger Mechanism** | Agent detects context | User types `/HAL-*` | CPU invokes via Task |
| **Context Efficiency** | ⭐⭐⭐ High (progressive) | ⭐⭐ Varies | N/A (isolated) |
| **Context Persistence** | ✅ Yes (main session) | ✅ Yes (main session) | ❌ No (by design) |
| **RAM Impact** | Minimal (selective) | Varies | Zero (isolated) |
| **Modularity** | ⭐⭐⭐ High (directories) | ⭐⭐ Medium (files) | ⭐⭐ Medium (files) |
| **Control Level** | Collaborative | User control | CPU control |
| **Best For** | Repeat solutions | Critical workflows | Context isolation |
| **Progressive Disclosure** | ✅ 3 levels | ❌ No | ❌ No (isolation instead) |

### Progressive Disclosure Explained

**Skills implement 3-level progressive disclosure:**
1. **Level 1 (Metadata)**: Always loaded - name, description, triggers (lightweight)
2. **Level 2 (Instructions)**: Loaded when skill activated - SKILL.md content
3. **Level 3 (Resources)**: Loaded only when referenced - forms, schemas, scripts

This prevents "context window explosion" where all capabilities load into RAM upfront (like MCP servers).

**Sub-Agents use context isolation instead:**
- Main session: Lightweight (only delegation logic)
- Sub-agent: Heavy (loads everything in isolated 200K RAM)
- Return: Summary only (discards intermediate data)

Result: Main session RAM impact = summary size only (~2-5K tokens), not full processing cost (50-150K tokens).

---

## When to Use Each Type

### ✅ Use SKILLS When:

**Primary Indicators:**
- [ ] Agent should trigger automatically based on context
- [ ] Need context efficiency (progressive disclosure)
- [ ] Building reusable, modular solution
- [ ] Pattern will repeat across sessions
- [ ] Want dedicated directory structure
- [ ] Solution composes with other capabilities

**HAL8000-Assistant Examples:**
- **context-awareness**: Detects missing context signals → asks user before loading
- **architecture-consultant**: Detects design decisions → validates against principles
- **hal-script-assistant**: Detects command creation → guides template selection
- **video-learning**: Detects video URL → extracts knowledge automatically

**Anti-Pattern (Don't Use Skill When):**
- User should control when it runs (use Command instead)
- One-time task (no modularity benefit)
- Need context isolation (use Sub-Agent)

---

### ✅ Use COMMANDS When:

**Primary Indicators:**
- [ ] User should explicitly control triggering
- [ ] State operation requiring user confirmation
- [ ] Critical workflow (commits, deployments, session-end)
- [ ] Need context persistence
- [ ] Part of user's workflow routine
- [ ] Composes multiple operations

**HAL8000-Assistant Examples:**
- **/HAL-session-end**: User must confirm RAM wipe → saves state before reset
- **/HAL-system-check**: User triggers audit → delegates to system-maintenance agent
- **/HAL-index-update**: User decides when to sync → delegates indexing work
- **/HAL-learn-video**: User provides video URL → extracts knowledge (could be Skill, but explicit is safer)

**Anti-Pattern (Don't Use Command When):**
- Agent should trigger proactively (use Skill)
- Need context isolation (use Sub-Agent directly, Command can delegate to it)

---

### ✅ Use SUB-AGENTS When:

**Primary Indicators:**
- [ ] Need context isolation (protect main RAM)
- [ ] Heavy processing (>30K intermediate data)
- [ ] Parallel workflows
- [ ] Don't need context persistence (volatility acceptable)
- [ ] Input >> Output (large processing → small summary)
- [ ] Main session RAM in CAUTION/DANGER zone

**HAL8000-Assistant Examples:**
- **research-synthesizer**: Web research (150K processing) → 5K summary (60-85% RAM savings)
- **hal-context-finder**: System navigation (80K context) → 3K summary (96% savings)
- **system-maintenance**: System audit (100K checking) → 5K report (95% savings)
- **command-builder**: Template generation (50K processing) → command file only

**Anti-Pattern (Don't Use Sub-Agent When):**
- Need context persistence (data lost at sub-agent completion)
- Small processing task (<10K tokens - overhead not worth it)
- Need to maintain state across invocations

**Critical Constraint:**
> "Sub-agent results are returned to main session RAM and are volatile. Results must be fully processed and persisted to files BEFORE session-end." - BIOS Operating Principles

---

## Decision Frameworks

### Framework 1: Trigger-First Approach

**Start with trigger mechanism:**

```
Who triggers this capability?

┌─ Agent automatically? ─────────────┐
│ → SKILL                             │
│ Examples:                           │
│ - Detect patterns                   │
│ - Suggest actions                   │
│ - Validate decisions                │
└─────────────────────────────────────┘

┌─ User explicitly? ─────────────────┐
│ → COMMAND                           │
│ Examples:                           │
│ - State operations                  │
│ - Critical workflows                │
│ - User confirmation required        │
└─────────────────────────────────────┘

┌─ CPU delegates heavy work? ────────┐
│ → SUB-AGENT                         │
│ Examples:                           │
│ - Web research                      │
│ - System audit                      │
│ - Large file processing             │
└─────────────────────────────────────┘
```

### Framework 2: Context-First Approach

**Start with context requirements:**

```
What are the context requirements?

┌─ Context Efficiency Critical? ─────┐
│ → SKILL (progressive disclosure)   │
│ Avoid loading everything upfront   │
└─────────────────────────────────────┘

┌─ Context Persistence Required? ────┐
│ → SKILL or COMMAND                  │
│ State must survive across ops       │
└─────────────────────────────────────┘

┌─ Context Isolation Required? ──────┐
│ → SUB-AGENT                         │
│ Protect main RAM from heavy work   │
└─────────────────────────────────────┘
```

### Framework 3: Use Case Patterns

**Match to common patterns:**

| Use Case | Type | Reasoning |
|----------|------|-----------|
| Detect missing context | Skill | Agent-triggered, pattern detection |
| Validate architecture | Skill | Agent-triggered, proactive |
| Web research | Sub-Agent | Heavy processing, isolation |
| Save session state | Command | User-explicit, critical |
| System health audit | Command → Sub-Agent | User triggers, delegates heavy work |
| Generate diagram | Command | User-explicit, state operation |
| Extract video knowledge | Skill or Command | Depends on trigger preference |
| Code review | Skill | Agent-triggered, pattern |
| Git commit | Command | User-explicit, critical |
| Large file analysis | Sub-Agent | Heavy processing, isolation |

---

## HAL8000-Assistant Architecture Validation

**HAL8000-Assistant's current features have been validated against this framework:**

### Skills (All Correctly Classified ✅)
| Skill | Trigger | Context Efficiency | Modularity | ✅ |
|-------|---------|-------------------|------------|-----|
| context-awareness | Agent (user question) | High (progressive) | High (dedicated dir) | ✅ |
| architecture-consultant | Agent (design decision) | High (progressive) | High (dedicated dir) | ✅ |
| hal-script-assistant | Agent (command creation) | High (progressive) | High (dedicated dir) | ✅ |
| documentation-generator | Agent (doc request) | High (progressive) | High (dedicated dir) | ✅ |
| video-learning | Agent (video URL) | High (progressive) | High (dedicated dir) | ✅ |

### Commands (All Correctly Classified ✅)
| Command | User-Explicit | State Operation | Critical | ✅ |
|---------|---------------|-----------------|----------|-----|
| /HAL-session-end | ✅ | ✅ (state.json) | ✅ (RAM wipe) | ✅ |
| /HAL-system-check | ✅ | ❌ (read-only) | ✅ (system audit) | ✅ |
| /HAL-index-update | ✅ | ✅ (indexes) | ⭐ (medium) | ✅ |
| /HAL-library-update | ✅ | ✅ (libraries) | ⭐ (medium) | ✅ |
| /HAL-mcp-control | ✅ | ✅ (MCP config) | ✅ (RAM impact) | ✅ |
| /HAL-learn-video | ✅ | ❌ | ⭐ (could be Skill) | ✅ |

### Sub-Agents (All Correctly Classified ✅)
| Sub-Agent | Isolation | Heavy Work | No Persistence | ✅ |
|-----------|-----------|------------|----------------|-----|
| research-synthesizer | ✅ (200K isolated) | ✅ (web research) | ✅ (by design) | ✅ |
| hal-context-finder | ✅ (200K isolated) | ✅ (system navigation) | ✅ (by design) | ✅ |
| system-maintenance | ✅ (200K isolated) | ✅ (system audit) | ✅ (by design) | ✅ |
| command-builder | ✅ (200K isolated) | ✅ (template processing) | ✅ (by design) | ✅ |
| claude-code-validator | ✅ (200K isolated) | ✅ (doc validation) | ✅ (by design) | ✅ |

**Result: 100% of HAL8000-Assistant features are correctly classified according to Claude Code best practices!**

---

## Common Pitfalls & Solutions

### Pitfall 1: "Skills for Everything"
**Problem:** Treating Skills as catch-all solution
**Solution:** Ask "Does agent need to trigger automatically?" If no → Command
**Example:** Git commit should be Command (user-explicit), not Skill (agent-triggered)

### Pitfall 2: "Ignoring Context Isolation"
**Problem:** Loading heavy data into main session RAM
**Solution:** Ask "Is input >> output?" If yes → Sub-Agent
**Example:** Web research (150K processing) should use Sub-Agent, not direct WebSearch

### Pitfall 3: "Sub-Agent Persistence Expectation"
**Problem:** Expecting sub-agent data to persist across sessions
**Solution:** Process and persist sub-agent results immediately to files
**Example:** research-synthesizer returns summary → must save to `data/research/` before session-end

### Pitfall 4: "Command Modularity"
**Problem:** Creating many similar Commands without shared structure
**Solution:** Extract common patterns into Skills or library templates
**Example:** Multiple diagram commands → use template + parameterization

### Pitfall 5: "MCP Server Context Explosion"
**Problem:** MCP servers "explode context window on bootup"
**Solution:** Prefer Skills (progressive disclosure) or Sub-Agents (isolation) over MCP
**Example:** HAL8000-Assistant uses minimal MCP (omnisearch, filesystem, IDE only)

---

## Composition Patterns

Features compose in predictable ways:

### Pattern 1: Command → Sub-Agent
**Description:** User triggers Command, Command delegates to Sub-Agent
**Use:** User control + context isolation
**Examples:**
- `/HAL-system-check` → delegates to `system-maintenance` sub-agent
- `/HAL-index-update` → delegates to indexing sub-agent
- User controls when, sub-agent provides isolation

### Pattern 2: Skill → Sub-Agent
**Description:** Agent triggers Skill, Skill delegates to Sub-Agent
**Use:** Automatic detection + context isolation
**Examples:**
- `context-awareness` skill could delegate to `hal-context-finder` sub-agent
- `video-learning` skill processes in main session (already efficient)
- Agent triggers, sub-agent provides isolation

### Pattern 3: Skill → Command
**Description:** Skill detects pattern, suggests Command to user
**Use:** Pattern detection + user confirmation
**Examples:**
- Skill detects missing indexes → suggests `/HAL-index-update`
- Skill detects RAM_ZONE=DANGER → suggests `/HAL-session-end`
- Agent suggests, user controls execution

### Pattern 4: Command → Skill
**Description:** Command explicitly invokes Skill capabilities
**Use:** User-initiated workflow using Skill logic
**Examples:**
- Command could explicitly invoke `documentation-generator` skill
- Less common pattern (Skills usually agent-triggered)

---

## Extension Guidelines

When creating new HAL8000-Assistant capabilities:

### Step 1: Define the Capability
```
What does it do?
Who benefits?
When should it run?
```

### Step 2: Apply Decision Tree
```
Q1: Who triggers? → Skill/Command/Sub-Agent
Q2: Context needs? → Persistence/Isolation
Q3: Modularity?   → Repeat pattern?
Q4: Efficiency?   → Progressive/Isolated
```

### Step 3: Choose Implementation
```
→ Skill:     Create `.claude/skills/[name]/SKILL.md`
→ Command:   Create `.claude/commands/[category]/HAL-[name].md`
→ Sub-Agent: Create `.claude/agents/[name].md`
```

### Step 4: Validate Choice
```
- Does trigger mechanism match use case?
- Are context requirements satisfied?
- Is modularity level appropriate?
- Does it compose well with existing features?
```

### Step 5: Document Decision
```
- Add to this guide's HAL8000-Assistant validation table
- Update BIOS if architectural principle
- Reference in CHANGELOG.md
```

---

## References

### Primary Sources
- **HAL8000-Assistant BIOS**: `CLAUDE.md` - Operating Principles, Three-Layer Model
- **Video Analysis**: `data/videos/i-finally-cracked-claude-agent-skills/knowledge-brief.md` - Industry best practices
- **HAL-Script Guide**: `data/architecture/hal-script-language.md` - Command programming
- **Command Organization**: `.claude/commands/README.md` - Command structure

### Feature Documentation
- **Skills**: `.claude/skills/*/SKILL.md` - Individual skill definitions
- **Commands**: `.claude/commands/*/HAL-*.md` - Individual command definitions
- **Sub-Agents**: `.claude/agents/*.md` - Individual agent definitions

### Architecture Docs
- **System Design**: `data/architecture/hal8000-system-design.md` - Complete architecture
- **Von Neumann**: `data/research/01-von-neumann-architecture.md` - Architectural foundation
- **Unix Philosophy**: `data/research/02-unix-philosophy.md` - Design principles

---

## Quick Reference Card

**Copy this for rapid decision-making:**

```
╔════════════════════════════════════════════════════════╗
║ HAL8000-Assistant FEATURE SELECTION QUICK REFERENCE              ║
╠════════════════════════════════════════════════════════╣
║ SKILLS (Agent-Triggered)                               ║
║ ✓ Agent auto-triggers                                  ║
║ ✓ Progressive disclosure (3 levels)                    ║
║ ✓ High modularity (dedicated dirs)                     ║
║ ✓ Repeat solutions, patterns                           ║
║                                                        ║
║ COMMANDS (User-Explicit)                               ║
║ ✓ User types /HAL-*                                    ║
║ ✓ Context persistence                                  ║
║ ✓ State operations, critical flows                     ║
║ ✓ User confirmation required                           ║
║                                                        ║
║ SUB-AGENTS (Context Isolation)                         ║
║ ✓ CPU delegates heavy work                             ║
║ ✓ Isolated 200K RAM                                    ║
║ ✓ No persistence (volatility)                          ║
║ ✓ Input >> Output (60-95% RAM savings)                 ║
╚════════════════════════════════════════════════════════╝

DECISION TREE:
1. Agent trigger? → SKILL
2. User control? → COMMAND
3. Isolation needed? → SUB-AGENT
4. Repeat pattern? → SKILL
5. Heavy processing? → SUB-AGENT
```

---

**End of Feature Selection Guide**

*This guide validates HAL8000-Assistant's architecture against Claude Code community best practices and provides a systematic framework for extending the system correctly.*
