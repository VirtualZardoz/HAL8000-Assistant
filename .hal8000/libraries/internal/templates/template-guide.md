# HAL-Script Prompt Template Guide

**Version:** 1.0
**Created:** 2025-10-15
**Purpose:** Guide to using prompt templates for command creation

---

## Overview

This library provides **composable prompt templates** for creating HAL-Script commands. Templates follow the **"Lego Block"** principle: each section is a reusable building block that can be included or omitted based on your needs.

**Core Concept:** Start with a template, remove unused sections, fill in your logic.

---

## YAML Frontmatter (Important!)

**All templates include YAML frontmatter** - this is a Claude Code feature that enhances command discoverability and functionality.

### What is YAML Frontmatter?

YAML frontmatter appears at the beginning of command files, enclosed in `---` markers:

```yaml
---
name: command-name
description: Brief description for command palette
parameters:
  - name: param1
    description: What this parameter does
    type: string
    required: true
---
```

### Benefits

**For Commands:**
- ✅ Enhanced discoverability in Claude Code command palette
- ✅ Parameter hints when invoking commands
- ✅ Type safety and validation
- ✅ Better documentation integration

**For Agents:**
- ✅ Tool whitelisting (security + performance)
- ✅ Model selection (Sonnet/Haiku/Opus)
- ✅ Explicit capability declaration
- ✅ Improved agent selection

### Required Fields

**For Commands:**
```yaml
---
name: HAL-command-name        # Command identifier
description: What it does     # Shows in command palette
parameters:                   # Optional: if command takes arguments
  - name: param_name
    description: Param description
    type: string|number|boolean
    required: true|false
---
```

**For Agents:**
```yaml
---
name: agent-name
description: Agent purpose and capabilities
tools:                        # Whitelist of allowed tools
  - Read
  - Write
  - Bash
model: sonnet|haiku|opus      # Optional: model selection
---
```

### Best Practices

1. **Keep descriptions concise** - One sentence for command palette display
2. **Document all parameters** - Users see these as hints
3. **Use appropriate types** - string, number, boolean
4. **Mark required parameters** - Clear interface expectations
5. **Whitelist tools for agents** - Principle of least privilege
6. **Choose models wisely** - Haiku for speed, Sonnet for balance, Opus for complexity

### Example: Complete Command with Frontmatter

```yaml
---
name: HAL-example-search
description: Search codebase for pattern and generate report
parameters:
  - name: pattern
    description: Search pattern (regex supported)
    type: string
    required: true
  - name: output_file
    description: Report output location (default: data/reports/search-results.md)
    type: string
    required: false
---

# HAL-example-search

**Command Type:** Development
...
```

### Tool Specification for Agents

**Common Tool Sets:**

**File System Agents:**
```yaml
tools:
  - Read
  - Grep
  - Glob
  - mcp__filesystem__search_files
```

**Research Agents:**
```yaml
tools:
  - mcp__omnisearch__web_search
  - mcp__omnisearch__firecrawl_process
  - WebSearch
  - WebFetch
  - Read
  - Write
```

**Code Generation Agents:**
```yaml
tools:
  - Read
  - Write
  - Glob
  - Grep
```

**See:** `.claude/libraries/internal/tool-reference.md` for complete tool catalog and usage patterns.

---

## Master Template

**File:** `master-prompt-template.md`

**Purpose:** Shows ALL possible sections (complete Lego block catalog)

**Use when:**
- You need a comprehensive reference
- You're building a complex custom command
- You want to see all options available

**Sections included:**
- Purpose
- Usage
- Variables/Parameters
- Instructions
- Delegation Patterns
- Workflow Integration
- Output Format
- Error Handling
- Examples
- Dependencies
- Performance Considerations
- Testing & Validation
- Notes
- Metadata

---

## The 7 Levels: IndyDevDan's Framework Mapped to HAL-Script

### Level 1: Basic Prompt
**File:** `level-1-basic.md`

**Sections:**
- Purpose (required)
- Instructions (required)

**Use when:**
- Simple, single-step operation
- No parameters or configuration needed
- Direct execution, no delegation
- Minimal error handling

**Examples:**
- Display system status
- Show current time
- Read a specific file

**Complexity:** Minimal (1-2 paragraphs of instructions)

---

### Level 2: Workflow Prompt
**File:** `level-2-workflow.md`

**Sections:**
- Purpose
- Usage (parameters)
- Variables/Parameters (inputs/outputs)
- Instructions (multi-step workflow)
- Output Format (structured results)

**Use when:**
- Sequential multi-step process
- Needs input parameters
- Produces structured output
- Clear workflow phases

**Examples:**
- Process files in directory
- Generate report from data
- Search and format results

**Complexity:** Low-Medium (3-5 step workflow)

---

### Level 3: Control Flow Prompt
**File:** `level-3-control-flow.md`

**Sections:**
- Purpose
- Usage
- Variables/Parameters (including config)
- Instructions (with conditionals/loops)
- Output Format
- Error Handling (conditions and branches)

**Use when:**
- Conditional logic required
- Loops over collections
- Different paths based on conditions
- Branch points in execution

**Examples:**
- Process files matching criteria
- Validate and fix errors
- Iterate until condition met

**Complexity:** Medium (conditionals, loops, branching)

---

### Level 4: Delegate Prompt
**File:** `level-4-delegate.md`

**Sections:**
- Purpose
- Usage
- Variables/Parameters
- Instructions (orchestration logic)
- Delegation Patterns (sub-agent invocation)
- Output Format
- Error Handling

**Use when:**
- Task requires sub-agent processing
- Context-heavy operations (save RAM)
- Specialized work (research, analysis, etc.)
- Need isolated processing

**Examples:**
- Research and synthesize information
- Discover and load system context
- Audit system health
- Generate complex documentation

**Complexity:** Medium-High (orchestrates other agents)

---

### Level 5: Supervisor Prompt
**File:** `level-5-supervisor.md`

**Sections:**
- Purpose
- Usage
- Variables/Parameters
- Instructions (coordination logic)
- Delegation Patterns (multi-agent)
- Workflow Integration (how agents compose)
- Output Format
- Error Handling (cross-agent)

**Use when:**
- Multiple agents needed
- Parallel agent execution
- Agent results need integration
- Complex multi-phase operations

**Examples:**
- Parallel research on multiple topics
- Multi-stage system validation
- Coordinated data processing pipeline

**Complexity:** High (multiple agents, coordination)

---

### Level 6: Workflow Composition Prompt
**File:** `level-6-workflow-composition.md`

**Sections:**
- Purpose
- Usage
- Variables/Parameters
- Instructions (high-level orchestration)
- Delegation Patterns (commands + agents)
- Workflow Integration (detailed integration)
- Output Format
- Error Handling
- Examples (workflow demonstrations)

**Use when:**
- Composing multiple commands
- End-to-end workflows
- System-level operations
- Application-like functionality

**Examples:**
- Complete analysis workflow (discover→analyze→report→checkpoint)
- Release process (build→test→document→deploy)
- Data pipeline (extract→transform→load→validate)

**Complexity:** High (multiple commands + agents)

---

### Level 7: System Prompt
**File:** `level-7-system.md`

**Sections:**
- ALL sections from master template
- Emphasis on: Dependencies, Performance, Testing, Integration

**Use when:**
- Core system infrastructure
- Self-modifying capabilities
- High reliability requirements
- Production-critical operations
- Extensive documentation needed

**Examples:**
- HAL-session-end (state persistence)
- HAL-system-check (integrity validation)
- HAL-command-create (meta-programming)

**Complexity:** Maximum (comprehensive, production-grade)

---

## Quick Selection Guide

**Choose your template based on:**

| Need | Level | Template |
|------|-------|----------|
| Simple task, no inputs | 1 | basic |
| Multi-step with parameters | 2 | workflow |
| Conditionals or loops | 3 | control-flow |
| Delegate to sub-agent | 4 | delegate |
| Multiple agents | 5 | supervisor |
| Compose commands | 6 | workflow-composition |
| Core system component | 7 | system |
| Custom/unsure | Master | master-prompt-template |

---

## The Lego Block Principle

**Master Template** = Complete set of all possible blocks

**Level Templates** = Pre-configured combinations for common patterns

**Your Command** = Start with template, customize as needed

**Process:**
1. Choose template that matches your needs (or use master)
2. Copy template to your command file
3. Remove sections you don't need
4. Fill in your specific logic
5. Add custom sections if needed (rare)

**Example:**
```markdown
Level 2 template has:
- Purpose ✓
- Usage ✓
- Variables ✓
- Instructions ✓
- Output Format ✓

But you also need error handling:
→ Copy that section from master template
→ Add it to your command
→ Now you have Level 2 + error handling (custom variation)
```

**Freedom:** Templates are guides, not constraints. Mix and match as needed.

---

## Section-by-Section Guide

### Purpose Section
**Required:** Yes (every command needs this)
**Length:** 1 sentence minimum, 1-2 paragraphs for complex commands
**Content:** What, why, when to use this command

### Usage Section
**Required:** If command has parameters
**Length:** Brief (command syntax + parameter descriptions)
**Content:** How to invoke command, what arguments mean

### Variables/Parameters Section
**Required:** If command processes inputs or produces outputs
**Length:** List of variables with types and descriptions
**Content:** Input vars, config settings, output vars

### Instructions Section
**Required:** Yes (every command needs execution logic)
**Length:** Proportional to complexity (1 paragraph to multiple phases)
**Content:** Step-by-step what the command does

### Delegation Patterns Section
**Required:** If command invokes sub-agents
**Length:** Detailed (which agent, when, what task, what returns)
**Content:** Sub-agent invocation patterns and coordination

### Workflow Integration Section
**Required:** If command part of larger workflows
**Length:** Shows prerequisites, dependents, composition patterns
**Content:** How this command fits into bigger picture

### Output Format Section
**Required:** If command produces structured output
**Length:** Shows exact format with examples
**Content:** What user sees, files created, return values

### Error Handling Section
**Required:** For production commands or complex operations
**Length:** Error types, detection, responses, recovery
**Content:** How command handles failures gracefully

### Examples Section
**Required:** Highly recommended (helps users understand)
**Length:** 2-3 examples showing different use cases
**Content:** Real scenarios with inputs and outputs

### Dependencies Section
**Required:** If command relies on other files/commands/agents
**Length:** List of dependencies with explanations
**Content:** What must exist for command to work

### Performance Considerations Section
**Required:** For RAM-intensive or long-running commands
**Length:** RAM cost, execution time, optimizations
**Content:** Resource usage and efficiency notes

### Testing & Validation Section
**Required:** For system-level commands
**Length:** Test cases and validation checklist
**Content:** How to verify command works correctly

### Notes Section
**Required:** Optional (use for design rationale, limitations)
**Length:** Variable
**Content:** Context that doesn't fit elsewhere

### Metadata Section
**Required:** Yes (version, status, dates)
**Length:** Brief structured data
**Content:** Command lifecycle information

---

## Best Practices

### 1. Start Simple
- Use Level 1-2 templates for most commands
- Only add complexity when actually needed
- Don't include sections "just in case"

### 2. Be Explicit
- Instructions should be step-by-step clear
- Don't assume context or skip steps
- CPU (Claude) interprets literally

### 3. Handle Errors
- Production commands need Error Handling section
- Consider edge cases
- Provide graceful degradation

### 4. Show Examples
- Examples make commands understandable
- Show happy path and error cases
- Demonstrate integration patterns

### 5. Document Integration
- If command composes with others, show how
- Include workflow diagrams
- Make reusability obvious

### 6. Keep Updated
- Update version and last-updated dates
- Document changes in Notes
- Reflect current system state

---

## Common Patterns

### Pattern 1: File Processing Command
**Template:** Level 2 (Workflow)
**Key sections:** Variables (file path), Instructions (read→process→write), Output Format

### Pattern 2: System Validation Command
**Template:** Level 4 (Delegate) or Level 7 (System)
**Key sections:** Instructions (checks), Delegation (audit agent), Error Handling (report issues)

### Pattern 3: Data Pipeline Command
**Template:** Level 3 (Control Flow) or Level 6 (Workflow Composition)
**Key sections:** Instructions (stages), Control Flow (conditions), Output Format

### Pattern 4: Research Command
**Template:** Level 4 (Delegate)
**Key sections:** Variables (query), Delegation (research-synthesizer), Output Format

### Pattern 5: Meta-Programming Command
**Template:** Level 7 (System)
**Key sections:** All sections (comprehensive documentation needed)

---

## Template Maintenance

**When to update templates:**
- New pattern discovered through usage
- Section structure improvements identified
- Best practices evolve

**How to update:**
- Modify master template first
- Cascade changes to level templates
- Update this guide
- Version bump templates

**Who updates:**
- You (system maintainer)
- Future sessions (system evolution)
- Community contributions (if shared)

---

## Related Documentation

- `master-prompt-template.md` - Complete Lego block catalog
- `level-1-basic.md` through `level-7-system.md` - Pre-configured templates
- `.claude/commands/README.md` - Command creation guide
- `data/architecture/hal-script-language.md` - HAL-Script language specification
- `CLAUDE.md` - BIOS with standard library reference

---

## Credits

**Inspired by:** IndyDevDan's "7 Levels of Agentic Prompt Formats"
**Adapted for:** HAL8000-Assistant architecture and HAL-Script programming language
**Framework:** Composable Lego Block principle
**Created:** 2025-10-15 as part of v1.2.0 development

---

**Use these templates to build consistent, well-structured, reusable commands.**
