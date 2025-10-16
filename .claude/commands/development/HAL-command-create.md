---
name: HAL-command-create
description: Automatically generates production-ready HAL-Script commands using the Prompt Template System
parameters:
  - name: description
    description: Natural language description of the desired command
    type: string
    required: true
---

# HAL-command-create

**Command Type:** Development
**Category:** development/
**Level:** 4 - Delegate Prompt
**Created:** 2025-10-15
**Version:** 1.1

---

## Purpose

Automatically generates production-ready HAL-Script commands using the Prompt Template System. Delegates to the `command-builder` sub-agent which loads all templates, analyzes requirements, selects appropriate template, and composes complete command file ready for use.

---

## Usage

```bash
/HAL-command-create "description of desired command"
```

**Parameters:**
- `description` - Natural language description of what the command should do

**Examples:**
```bash
/HAL-command-create "Find all TODO comments in Python files and create markdown report"
/HAL-command-create "Check if indexes are stale and update them automatically"
/HAL-command-create "Research a technical topic and save findings to data/research/"
```

---

## Variables/Parameters

**Input Variables:**
- `command_description` - String - User's natural language description of desired command
- `requirements` - Implicit - Functional requirements parsed from description

**Output Variables:**
- `generated_command` - String - Complete command content ready to save
- `command_name` - String - Recommended command name (HAL-*)
- `location` - String - Recommended file location (.claude/commands/[category]/)
- `template_used` - String - Which template was selected

---

## Instructions

**Orchestration Logic:**

1. **Preparation Phase**: Validate input
   - Ensure description is provided (not empty)
   - Check that description is clear enough for analysis
   - If description too vague, request clarification from user

2. **Delegation Phase**: Invoke command-builder sub-agent
   - Tool: Task (subagent_type: "general-purpose")
   - Agent specification: `.claude/agents/command-builder.md`
   - Pass complete description and requirements

3. **Processing Phase**: Receive and validate generated command
   - Extract command content from agent output
   - Verify command structure is complete
   - Validate command follows HAL-Script conventions

4. **Presentation Phase**: Display to user for review
   - Show generated command
   - Provide save instructions
   - Offer refinement if needed

---

## Delegation Patterns

**Sub-Agent:** command-builder (using general-purpose agent with command-builder.md specification)

**When to delegate:**
- User requests command creation
- This command is invoked

**Task description for agent:**

Launch command-builder sub-agent with:
- **Agent File:** `.claude/agents/command-builder.md`
- **Task:** Generate HAL-Script command based on user requirements

**Prompt to agent:**
```markdown
You are the command-builder agent. Your mission is to generate a complete HAL-Script command file using the Prompt Template System.

**User's Request:**
[command_description from user]

**Your Workflow:**

1. **Load all template resources** (MANDATORY FIRST STEP):
   - Load: .claude/libraries/internal/templates/template-guide.md
   - Load: .claude/libraries/internal/templates/master-prompt-template.md
   - Load all 7 level templates (level-1-basic.md through level-7-system.md)

2. **Analyze the user's requirements:**
   - What is the primary purpose?
   - What complexity level is needed? (1-7)
   - Does it need sub-agents, control flow, command composition?
   - Which Lego blocks (template sections) are required?

3. **Select the appropriate template:**
   - Use template-guide.md selection logic
   - Choose level that matches complexity
   - Document your rationale

4. **Compose the complete command:**
   - Copy selected template
   - Remove unused sections (Lego Block principle)
   - Fill in command logic with HAL-Script instructions
   - Include all necessary sections (Purpose, Instructions, Examples)
   - Add complete metadata

5. **Return structured report** with:
   - Template selection rationale
   - Complete command content (ready to save)
   - Recommended command name and location
   - Usage instructions
   - Any implementation notes

**Quality Standards:**
- Command must be production-ready (no placeholders)
- Follow HAL-Script programming conventions
- Include practical examples
- Clear error handling (if complex command)
- Single responsibility (Unix philosophy)

**Output Format:**
Use the standard Command Builder Report format specified in your agent file.
```

**Benefits:**
- **RAM efficiency:** Agent uses isolated 200K context to load all templates (~12K tokens), main session only receives final command (~2-4K tokens) = 60-85% savings
- **Specialization:** Agent is expert in template selection and HAL-Script composition
- **Quality:** Consistent, well-structured commands following all best practices
- **Self-improvement:** System creates its own commands (von Neumann self-modifying code)

---

## Output Format

**What user sees:**

```markdown
# Command Builder Report

## Selected Template
[Template name - Level X: Description]
[Rationale for selection]

## Command Specification

**Name:** HAL-[command-name]
**Location:** .claude/commands/[subdirectory]/HAL-[command-name].md
**Template Used:** level-X-[type].md
**Complexity Level:** X

## Generated Command

[Complete markdown command file - ready to copy]

## Usage Instructions

1. Review the generated command above
2. If changes needed, request refinements
3. When satisfied, I can save it to: `.claude/commands/[subdirectory]/HAL-[command-name].md`
4. Command will be immediately usable via `/HAL-[command-name]`

## Notes

[Implementation notes, optional features, future enhancements]
```

**Follow-up Options:**
- User can request refinements: "Make it [more detailed/simpler/add feature]"
- User can approve: "Save it" → CPU saves to specified location
- User can customize: "Change [aspect]" → regenerate with modifications

---

## Error Handling

**Sub-agent failures:**
- If agent returns error: Display error to user, suggest providing more details in description
- If agent can't select template: Agent will ask clarifying questions (passed to user)
- If results incomplete: Request regeneration with specific missing sections

**Input validation:**
- If description empty: Prompt user: "Please provide a description of the command you want to create"
- If description ambiguous: Agent will request clarification through its output

**Quality validation:**
- Verify generated command has required sections (Purpose, Instructions)
- Verify command name follows HAL-* convention
- Verify HAL-Script instructions are executable (no placeholders)

**Fallback:**
- If automated generation fails repeatedly, direct user to manual template usage:
  "For now, please use templates manually: see `.claude/libraries/internal/templates/template-guide.md`"

---

## Examples

### Example 1: Simple Search Command

**User Input:**
```bash
/HAL-command-create "Find all TODO comments in Python files"
```

**Generated Command Features:**
- Template Selected: Level 1 - Basic
- Uses: Grep tool for pattern matching
- Output: List of files and line numbers with TODO comments

---

### Example 2: Multi-Step Workflow

**User Input:**
```bash
/HAL-command-create "Count files in each directory under data/ and create markdown summary"
```

**Generated Command Features:**
- Template Selected: Level 2 - Workflow
- Steps: Traverse directories → count files → format markdown → save report
- Output: Markdown file with directory statistics

---

### Example 3: Research Command with Sub-Agent

**User Input:**
```bash
/HAL-command-create "Research a technical topic using web search and save findings"
```

**Generated Command Features:**
- Template Selected: Level 4 - Delegate
- Sub-Agent: research-synthesizer
- Steps: Accept topic → delegate research → format results → save to data/research/
- Output: Structured research document

---

## Dependencies

**Required Agents:**
- `command-builder` - Located at `.claude/agents/command-builder.md`
- Launched via Task tool with general-purpose subagent type

**Required Templates:**
- Template library at `.claude/libraries/internal/templates/`
- Agent loads templates in isolated context (not main session)

**System Requirements:**
- Prompt Template System operational (Phase 1 & 2 complete)
- Template files present and accessible

---

## Metadata

**Version History:**
- v1.0 (2025-10-15) - Initial implementation for Phase 3 automation

**Status:** Production (Phase 3 complete)
**Template Level:** 4 - Delegate (sub-agent orchestration)

**Integration:**
- Part of Prompt Template System (Phase 3: Automation)
- Enables recursive self-improvement (system creates its own commands)
- Embodies von Neumann self-modifying code principle

**Framework Credit:**
- Based on IndyDevDan's "7 Levels of Agentic Prompt Formats"
- Adapted for HAL8000 architecture and HAL-Script programming language
- Enhanced with Lego Block composability principle

---

## Notes

### Design Philosophy

This command represents the culmination of the Prompt Template System:

1. **Phase 1:** Created template library (Lego blocks)
2. **Phase 2:** Documented and integrated into system
3. **Phase 3:** This command - full automation

### Recursive Self-Improvement

This command enables HAL8000's self-modification capability:
- System creates its own commands
- Commands extend system capabilities
- New capabilities enable more command creation
- Positive feedback loop (von Neumann architecture)

### Token Efficiency Pattern

**Without automation:**
- User request → CPU loads all templates (12K tokens) → compose command → main session RAM: +12K

**With this command:**
- User request → delegate to agent (agent loads templates in isolated 200K) → agent returns command only (2-4K) → main session RAM: +2-4K
- **Savings:** 60-85% RAM reduction

This is the "Reduce and Delegate" principle in action.

### Future Enhancements

**Potential improvements:**
- Template versioning support
- Command refinement loop (iterative generation)
- Learning from user modifications (pattern recognition)
- Command validation before saving
- Integration with version control (track command evolution)

### Usage Recommendation

**For command creators:**
- Start simple: describe command in plain language
- Be specific about inputs/outputs expected
- Mention if you need error handling, examples, etc.
- Review generated command before saving
- Iterate if needed (request refinements)

**This command makes command creation accessible:**
- No need to manually navigate templates
- No need to remember template structure
- Consistent quality across all generated commands
- Fast iteration (seconds vs minutes)
