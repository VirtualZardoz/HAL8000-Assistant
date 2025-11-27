---
name: Context Awareness
description: Detect when user questions require loading files not currently in context. Use when user asks about specific code, files, components, or implementation details that aren't in current RAM. Activate when user mentions file paths, function names, component names, or asks "which file" questions.
allowed-tools: Read, Glob, Grep, AskUserQuestion
---

# Context Awareness

This Skill implements HAL8000-Assistant's Context Awareness Protocol (defined in CLAUDE.md) to proactively detect missing context and prevent incorrect assumptions.

## Purpose

Prevent answering questions confidently when necessary context is missing. Instead of guessing or loading speculatively, ASK the user to clarify what to load.

## When to Activate

**Signals that context is missing:**
- User mentions specific file/path/component not in current RAM
- User references "that file", "the component", "this function" without clear antecedent
- User asks "which file has X?" (implies I should know the file set)
- User asks implementation details when I haven't loaded implementation
- User uses project-specific terms/names not in current context
- Question is specific but I only have general knowledge

## Protocol

### Step 1: Parse Question for Missing Context Signals

Check if any signals above are present.

### Step 2: Proactive Context Check

**IF missing context signals detected:**

ASK USER immediately:
```
I notice you're asking about [X]. To assist accurately:
- Should I search the codebase for [term]?
- Do you mean [specific file/path]?
- Is this about [project/component]?

Current context: [briefly state what I DO have loaded]
```

**Purpose:**
- Prevent wrong assumptions
- Let user guide me to right location (saves RAM)
- Make RAM limitations visible
- Get clarification before expensive operations

### Step 3: Context Acquisition (After User Clarifies)

User clarifies what to search/load:
→ Use hal-context-finder sub-agent for discovery
→ Load only essential files
→ Report what was loaded: "I've loaded [X]. Proceeding..."

### Step 4: Answer with Context Transparency

When answering:
- State basis: "Based on [current context/loaded files]..."
- If answer might benefit from more context:
  "I can answer with current files, but would you like me to also check [X] for completeness?"
- If confident but haven't verified everything:
  "Based on [files loaded], the answer is [X]. I haven't checked [other areas] - should I?"

## Anti-Patterns to Avoid

- ❌ Answering confidently when context is clearly insufficient
- ❌ Loading files speculatively without asking
- ❌ Assuming user knows what's in my RAM
- ❌ Waiting for user to tell me to search (be proactive)
- ❌ Searching before clarifying what to search for

## Examples

### Example 1: Missing File Context

**User:** "Which file contains the authentication logic?"

**✅ RIGHT:**
```
I don't currently have authentication files loaded. Should I search
the codebase for authentication-related files? Or is there a specific
directory/component I should check?
```

**❌ WRONG:**
```
[searches entire codebase with sub-agent without asking]
```

### Example 2: Vague Reference

**User:** "Fix the bug in that function"

**✅ RIGHT:**
```
I don't have enough context - which function do you mean? Could you
point me to the file or function name?
```

**❌ WRONG:**
```
[guesses which function and loads random file]
```

### Example 3: Proactive Clarification

**User:** "How does the session handling work?"

**✅ RIGHT:**
```
I can explain session handling at an architectural level based on
CLAUDE.md currently in context, but I haven't loaded the actual session
command implementation. Would you like me to load
.claude/commands/system/HAL-session-end.md for implementation details?
```

## Integration with HAL8000-Assistant Architecture

**Follows BIOS Operating Principle:**
- Context Awareness Protocol (CLAUDE.md)
- Selective Loading Discipline (Resource Management Protocol)
- Reduce and Delegate (Unix Philosophy)

**Works with:**
- hal-context-finder agent (for discovery after clarification)
- CONTEXT_MANIFEST register (track what's loaded)
- RAM_ZONE register (avoid overloading)
