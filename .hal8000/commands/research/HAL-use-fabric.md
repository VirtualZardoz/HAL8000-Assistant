---
name: HAL-use-fabric
description: Apply a Fabric Pattern (specialized AI persona) to a target file.
parameters:
  - name: pattern_name
    description: Name of the Fabric pattern (e.g., extract_wisdom, analyze_malware)
    required: true
  - name: target_file
    description: Path to the file to analyze
    required: true
---

# HAL Use Fabric

**Purpose:** Apply expert "Fabric" patterns to data without context bloat.

## Usage

```bash
/HAL-use-fabric [pattern_name] [target_file]
```

## Execution Steps

1. **Locate Pattern:** Finds `.hal8000/libraries/external/fabric-patterns/[pattern_name]/system.md`.
2. **Read Target:** Reads content of `[target_file]`.
3. **Delegate:** Spawns an isolated sub-agent initialized with the pattern.
4. **Report:** Returns the specific analysis.

## Source Code (Bash Implementation)

```bash
#!/bin/bash
PATTERN_NAME="$1"
TARGET_FILE="$2"
PATTERN_PATH=".hal8000/libraries/external/fabric-patterns/${PATTERN_NAME}/system.md"

# Validation
if [ ! -f "$PATTERN_PATH" ]; then
    echo "❌ Error: Pattern '${PATTERN_NAME}' not found."
    echo "Tip: Check .hal8000/indexes/fabric-patterns.json for available patterns."
    exit 1
fi

if [ ! -f "$TARGET_FILE" ]; then
    echo "❌ Error: Target file '${TARGET_FILE}' not found."
    exit 1
fi

echo "🧵 Applying Fabric Pattern: ${PATTERN_NAME}..."
echo "📄 Target: ${TARGET_FILE}"

# Construct Prompt
# We place the Pattern content first (System Role) followed by the Target content.
FULL_PROMPT="$(cat "$PATTERN_PATH")

---
Task: Apply the above pattern to the following content:

$(cat "$TARGET_FILE")"

# Execute via Gemini CLI (Isolated Process)
# Using --yolo to skip confirmation for this deterministic task
echo "$FULL_PROMPT" | gemini --yolo
```
