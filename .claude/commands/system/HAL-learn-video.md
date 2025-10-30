# HAL-learn-video

**Purpose**: Extract comprehensive knowledge from YouTube videos by combining transcript analysis with visual frame examination using Claude's vision capabilities and fabric pattern chaining.

## Command Syntax
`/HAL-learn-video <youtube-url>`

## Processing Instructions for Claude

When this command is invoked, follow these steps exactly:

### Step 1: Video Information Gathering
1. Extract video title, duration, and basic info using yt-dlp
2. Analyze title and description to determine video type (technical, educational, business, general)
3. Present interactive configuration dialogue

### Step 2: Interactive Parameter Configuration

Present this exact dialogue to the user:

```
🎥 Video Learning Configuration
================================
Video: [INSERT_VIDEO_TITLE]
Duration: [INSERT_DURATION]
Channel: [INSERT_CHANNEL]

Detected Type: [technical/educational/business/general]

1. **Processing Mode** (1/2/3):
   - [1] Fast: Transcript + key frames (scene threshold 0.3, ~10-20 frames)
   - [2] Smart: Selective frames + analysis (scene threshold 0.5, ~5-15 frames) ← Recommended
   - [3] Thorough: Dense extraction + chapters (scene threshold 0.6, ~3-10 frames)

2. **Frame Extraction Settings**:
   - Scene threshold: [RECOMMENDED_VALUE] (adjust: 0.3-0.6, or Enter to accept)
   - Extract code/diagram frames? (Y/n)

3. **Fabric Pattern Chain** for [DETECTED_TYPE]:
   Recommended: [PATTERN_CHAIN_FOR_TYPE]
   - Accept recommended? (Y/n)
   - Or specify custom: ________________

4. **Output Preferences**:
   - Include all extracted details? (Y/n) ← Recommended: Y
   - Embed frame images in markdown? (Y/n) ← Recommended: Y
   - Generate Mermaid diagrams from flowcharts? (Y/n) ← Recommended: Y

5. **Storage Options**:
   - Save location: data/videos/[SANITIZED_TITLE]/
   - Archive after processing? (y/N)
   - Keep video file for offline reference? (y/N)

Ready to proceed with these settings? (Y/n/customize)

[Wait for user confirmation before proceeding]
```

### Step 3: Pattern Chain Selection by Video Type

**Technical/Programming Videos**:
- Primary: `extract_wisdom` → `explain_code` → `create_summary` → `extract_instructions`
- Focus: Code examples, technical concepts, implementation details

**Educational/Lecture Videos**:
- Primary: `youtube_summary` → `extract_main_idea` → `extract_wisdom` → `create_video_chapters`
- Focus: Learning objectives, key concepts, structured knowledge

**Business/Professional Videos**:
- Primary: `extract_insights` → `analyze_presentation` → `extract_recommendations` → `create_summary`
- Focus: Business insights, strategies, actionable advice

**General/Mixed Content**:
- Primary: `extract_wisdom` → `youtube_summary` → `create_video_chapters`
- Focus: Universal wisdom, entertainment value, broad insights

### Step 4: Video Download and Processing

**IMPORTANT - Mixed Environment Compatibility**:
In Claude Code's bash environment on Windows, use full paths for Windows executables:
- FFmpeg: `/c/Users/[USERNAME]/AppData/Local/ffmpeg/bin/ffmpeg.exe`
- Commands may need Windows-style paths converted to bash-compatible format

Execute these commands in sequence:

1. **Download video and captions**:
   ```bash
   yt-dlp -f best --write-auto-sub --sub-lang en --sub-format vtt -o "%(title)s.%(ext)s" [YOUTUBE_URL]
   ```

2. **Create processing directory**:
   ```bash
   mkdir -p "data/videos/[SANITIZED_TITLE]/frames"
   ```

3. **Extract frames based on selected mode**:
   ```bash
   "/c/Users/Shahram-Dev/AppData/Local/ffmpeg/bin/ffmpeg.exe" -i "[VIDEO_FILE]" -vf "select='gt(scene,[THRESHOLD])'" -vsync vfr "data/videos/[SANITIZED_TITLE]/frames/frame_%06d.jpg"
   ```

   **Note**: Use full FFmpeg path due to Claude Code bash/Windows environment mixing. FFmpeg is installed but not in bash PATH.

4. **Move transcript to processing directory**:
   ```bash
   mv "[VIDEO_TITLE].vtt" "data/videos/[SANITIZED_TITLE]/transcript.vtt"
   ```

   **Note**: Use `mv` instead of `move` in bash environment.

### Step 5: Knowledge Extraction Process

1. **Read and parse transcript**:
   - Load the VTT file
   - Extract timestamps and text
   - Identify chapter markers if present
   - Create structured transcript data

2. **Analyze extracted frames**:
   - Use Claude's vision capabilities to examine each frame
   - Identify: slides, diagrams, code snippets, charts, whiteboards
   - Extract text using OCR analysis
   - Note visual elements and their relationships

3. **Apply fabric pattern chain**:
   For each pattern in the selected chain:
   - Apply pattern to transcript content
   - Apply pattern to visual content descriptions
   - Combine insights from both sources
   - Preserve all extracted information

### Step 6: Content Synthesis and Organization

Create comprehensive knowledge output using this structure:

```markdown
# Video Learning: [VIDEO_TITLE]

*Processed: [DATE] | Duration: [DURATION] | Source: [YOUTUBE_URL]*

## Executive Summary
[Apply youtube_summary pattern for high-level overview - what you need to know immediately]

## Key Insights & Wisdom
[Apply extract_wisdom pattern - core valuable takeaways from both audio and visual]

## Visual Content Analysis

### Diagrams & Flowcharts
[For each significant visual element]:

#### [Visual Description] - [Timestamp]
**Type**: [Diagram/Flowchart/Slide/Whiteboard/Code/Chart]
**Key Elements**:
- [Component 1]: [Description]
- [Component 2]: [Description]
- [Relationships]: [How elements connect]

**OCR Extracted Text**:
```
[All readable text from the frame]
```

**Mermaid Recreation** (when applicable):
```mermaid
[Recreate flowcharts/diagrams in Mermaid syntax]
```

**Insights**:
- [What this visual teaches]
- [How it connects to spoken content]
- [Practical applications]

*[Saved as: frames/frame_XXXXXX.jpg]*

---

## Detailed Analysis

### Chapter Breakdown
[Apply create_video_chapters pattern with enhanced descriptions]:

#### Chapter 1: [Title] - [Start-End Timestamps]
**Summary**: [Chapter overview]
**Key Points**:
- [Point 1 with timestamp]
- [Point 2 with timestamp]
**Visual Elements**: [Any diagrams/slides in this section]
**Takeaways**: [What to remember from this chapter]

### Complete Idea Extraction
[Apply extract_wisdom IDEAS section - all 20-50 ideas, nothing lost]

### Quotes & References
[Apply extract_wisdom QUOTES section with timestamps]:
- "[Exact quote text]" - [Speaker] at [timestamp]

### Practical Applications
[Apply extract_wisdom HABITS and RECOMMENDATIONS sections]:

**Habits Mentioned**:
- [Habit 1 with context]

**Recommendations**:
- [Recommendation 1 with reasoning]

### Technical Details
[For technical videos - apply explain_code or extract_instructions]:
- Code examples with explanations
- Implementation steps
- Technical specifications

---

## Reference Materials

### Frame Gallery
[List all extracted frames with descriptions]:
- `frame_000001.jpg` - [Timestamp] - [Description]
- `frame_000002.jpg` - [Timestamp] - [Description]

### Complete Transcript
[Full timestamped transcript for reference]:
```
[00:00:00] Speaker: [Text]
[00:00:15] Speaker: [Text]
...
```

### Source Information
- **Video URL**: [YOUTUBE_URL]
- **Channel**: [CHANNEL_NAME]
- **Upload Date**: [DATE]
- **Duration**: [DURATION]
- **Processing Date**: [CURRENT_DATE]
- **Patterns Applied**: [LIST_OF_PATTERNS]
- **Frames Extracted**: [COUNT]
- **Scene Threshold**: [THRESHOLD_VALUE]

### Related Resources
[Extract any books, tools, links, references mentioned in video]
```

### Step 7: File Organization and Storage

1. **Save main output**:
   - Save markdown to `data/videos/[SANITIZED_TITLE]/knowledge-brief.md`

2. **Organize supporting files**:
   - Keep frames in `frames/` subdirectory
   - Preserve original transcript as `transcript.vtt`
   - Create metadata file with processing details

3. **Create metadata.json**:
   ```json
   {
     "video_title": "[TITLE]",
     "youtube_url": "[URL]",
     "duration": "[DURATION]",
     "processed_date": "[DATE]",
     "patterns_applied": ["pattern1", "pattern2"],
     "frames_extracted": [COUNT],
     "scene_threshold": [THRESHOLD],
     "processing_mode": "[fast/smart/thorough]"
   }
   ```

4. **Optional archival**:
   - If user selected archival, copy entire folder to `data/videos/archive/`

### Step 8: Completion Summary

Present final summary:

```
✅ Video Learning Complete!

📁 Saved to: data/videos/[SANITIZED_TITLE]/
📄 Knowledge Brief: [FILE_SIZE]
🖼️ Frames Extracted: [COUNT]
⏱️ Processing Time: [DURATION]
🔗 Patterns Applied: [LIST]

📋 What was captured:
- Complete transcript with timestamps
- [COUNT] key visual frames analyzed
- Comprehensive knowledge synthesis
- All insights preserved in progressive detail format

Ready for your review! 🎓
```

## Error Handling Instructions

**If video download fails**:
- Check if URL is valid YouTube link
- Verify yt-dlp is installed and updated
- Try alternative format: `yt-dlp -f worst` for compatibility

**If no captions available**:
- Inform user that auto-generated captions not available
- Suggest they enable captions on YouTube or provide video with captions
- Do not proceed without transcript - visual-only analysis is insufficient

**If frame extraction fails**:
- Check if ffmpeg is installed
- Try lower scene threshold (0.2)
- Fall back to time-based extraction: extract frame every 30 seconds

**If processing directory exists**:
- Ask user whether to overwrite or append timestamp to folder name
- Preserve existing work unless explicitly told to overwrite

## Quality Assurance Checks

Before presenting final output:
1. Verify all patterns were applied successfully
2. Confirm all frames have descriptions
3. Check that timestamps are properly formatted
4. Ensure markdown formatting is valid
5. Verify all files are saved to correct locations

## Notes for Claude

- This command file contains instructions for YOU to follow, not documentation for users
- Use your vision capabilities to analyze frames - you ARE the vision LLM
- Apply fabric patterns exactly as specified in `.claude/tools/fabric-patterns/`
- Preserve ALL extracted information - nothing should be lost
- The interactive dialogue is crucial - always get user confirmation before processing
- Be methodical and thorough - this is knowledge extraction, not quick summarization