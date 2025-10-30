---
name: Video Learning
description: Extract comprehensive knowledge from YouTube videos through transcript analysis and visual frame examination. Use when user wants to learn from videos, analyze video content, or extract insights from video presentations.
allowed-tools:
  - SlashCommand
  - Bash
  - Read
  - Write
---

# Video Learning Skill

## Overview
Comprehensive YouTube video knowledge extraction system that combines transcript analysis with visual frame examination using Claude's vision capabilities and fabric pattern chaining.

**Architecture**: Skill (auto-detect) → HAL Command (orchestrate) → External Tools (process) → Knowledge Output

## When This Skill Activates

**Auto-detection triggers:**
- "learn from this video"
- "analyze this YouTube video"
- "extract knowledge from [URL]"
- "what's in this video?"
- "summarize this video tutorial"
- "help me understand this presentation"
- "process this lecture/course/talk"
- Any YouTube URL mentioned with learning intent

## Instructions

When user needs video learning:

1. **Invoke HAL-learn-video command** using SlashCommand tool:
   ```
   /HAL-learn-video <youtube-url>
   ```

2. **Interactive configuration** (command handles):
   - Processing mode selection (fast/smart/thorough)
   - Frame extraction settings (scene threshold)
   - Fabric pattern chain selection by content type
   - Output preferences (details, images, diagrams)
   - Storage options (location, archival)

3. **Processing pipeline** (command orchestrates):
   - Video download via yt-dlp
   - Transcript extraction with timestamps
   - Scene-change frame extraction via FFmpeg
   - Vision analysis of each frame (diagrams, slides, code)
   - Fabric pattern chain application
   - Knowledge synthesis and organization

4. **Return comprehensive output**:
   - Executive summary
   - Key insights and wisdom
   - Visual content analysis with Mermaid diagrams
   - Chapter breakdown with timestamps
   - Complete idea extraction
   - Practical applications
   - Full reference materials

## Capabilities

### Content Analysis
- **Transcript Processing**: Auto-generated captions with timestamp preservation
- **Visual Analysis**: Slides, diagrams, flowcharts, code snippets, whiteboards, charts
- **OCR Extraction**: Text from visual elements
- **Pattern Application**: 227 Fabric AI patterns for comprehensive extraction

### Processing Modes
- **Fast**: Transcript + key frames (threshold 0.3, ~10-20 frames)
- **Smart**: Selective frames + analysis (threshold 0.5, ~5-15 frames) ← Recommended
- **Thorough**: Dense extraction + chapters (threshold 0.6, ~3-10 frames)

### Content Type Optimization

**Technical/Programming Videos**:
- Patterns: `extract_wisdom` → `explain_code` → `create_summary` → `extract_instructions`
- Focus: Code examples, technical concepts, implementation details

**Educational/Lecture Videos**:
- Patterns: `youtube_summary` → `extract_main_idea` → `extract_wisdom` → `create_video_chapters`
- Focus: Learning objectives, key concepts, structured knowledge

**Business/Professional Videos**:
- Patterns: `extract_insights` → `analyze_presentation` → `extract_recommendations` → `create_summary`
- Focus: Business insights, strategies, actionable advice

**General/Mixed Content**:
- Patterns: `extract_wisdom` → `youtube_summary` → `create_video_chapters`
- Focus: Universal wisdom, entertainment value, broad insights

## Output Structure

The command generates comprehensive markdown knowledge brief:

```
# Video Learning: [VIDEO_TITLE]

## Executive Summary
[High-level overview - immediate takeaways]

## Key Insights & Wisdom
[Core valuable knowledge from audio + visual]

## Visual Content Analysis
[Each diagram/slide with]:
- Type and description
- OCR extracted text
- Mermaid recreation (when applicable)
- Insights and connections
- Embedded image reference

## Detailed Analysis
- Chapter breakdown with timestamps
- Complete idea extraction (all 20-50 ideas)
- Quotes with timestamps
- Practical applications
- Technical details (for tech videos)

## Reference Materials
- Frame gallery
- Complete transcript
- Source information
- Related resources
```

## Dependencies

**External Tools Required**:
- **yt-dlp**: Video and caption download
- **FFmpeg**: Frame extraction from video
- **Fabric Patterns**: Located at `.claude/tools/fabric-patterns/`

**Installation Verification**:
- Command checks for yt-dlp and FFmpeg before processing
- Reports clear error if dependencies missing

## Storage Organization

**Output Location**: `data/videos/[SANITIZED_TITLE]/`

**File Structure**:
```
data/videos/[video-name]/
├── knowledge-brief.md      # Main comprehensive output
├── transcript.vtt          # Original transcript with timestamps
├── metadata.json           # Processing details
└── frames/                 # Extracted frame images
    ├── frame_000001.jpg
    ├── frame_000002.jpg
    └── ...
```

**Optional Archival**: User can choose to archive completed processing within `data/videos/archive/`

## Integration with HAL System

### UFC Compliance
- Command playbook: `.claude/commands/system/HAL-learn-video.md`
- Skill detection: `.claude/skills/video-learning/SKILL.md` (this file)
- Output directory: `data/videos/`

### ADHD Optimization
- Interactive configuration prevents cognitive overload
- Progressive detail format (summary-first, deep-dive optional)
- Visual organization with timestamps for easy navigation
- Preserved complete reference for future review

### Token Economics
- Skill detection: ~100 tokens (main context)
- Command orchestration: 2-5K tokens (sequential processing)
- Vision analysis: Per-frame processing (separate context)
- **Benefit**: Preserves main conversation context for strategic discussion

## Common Workflows

**Simple video learning:**
```
User: "Learn from https://youtu.be/..."
→ Skill auto-detects
→ Command processes with smart defaults
→ Returns comprehensive knowledge brief
```

**Customized processing:**
```
User: "Analyze this technical talk thoroughly: [URL]"
→ Skill auto-detects
→ Interactive configuration presented
→ User selects thorough mode + technical patterns
→ Returns comprehensive analysis with code examples
```

**Quick extraction:**
```
User: "What's the summary of this video?"
→ Skill auto-detects
→ Fast mode with youtube_summary pattern
→ Returns quick overview
```

## Quality Assurance

**Before completion, command verifies:**
- All patterns applied successfully
- All frames have descriptions
- Timestamps properly formatted
- Markdown formatting valid
- All files saved to correct locations

## Error Handling

**Video download fails**: Validates URL, checks yt-dlp installation
**No captions available**: Informs user, suggests alternatives
**Frame extraction fails**: Checks FFmpeg, adjusts threshold, provides fallback
**Processing directory exists**: Asks user to overwrite or rename

## Environment Notes

**WSL2/Windows Mixed Environment**:
- Command handles Windows executable paths (FFmpeg, yt-dlp)
- Converts between Windows and bash path formats as needed
- Tested on Claude Code with Windows host + WSL2 Ubuntu

## See Also
- Command: `/HAL-learn-video`
- Playbook: `.claude/commands/HAL-learn-video.md`
- Context pointer: `.claude/context/commands/HAL-learn-video.md`
- Fabric patterns: `.claude/tools/fabric-patterns/`
- Related skills: fabric-pattern-library
