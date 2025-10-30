# Video Learning Skill

**Comprehensive YouTube video knowledge extraction through transcript and visual analysis**

## What This Skill Does

Automatically extracts and synthesizes knowledge from YouTube videos by:
- Downloading video transcripts with timestamps
- Extracting key visual frames (slides, diagrams, code)
- Analyzing visual content using Claude's vision capabilities
- Applying AI patterns for comprehensive knowledge extraction
- Generating structured markdown output with progressive detail

## Quick Start

### Installation

1. **Copy skill to your HAL instance**:
   ```bash
   # Copy the skill directory
   cp -r .claude/skills/video-learning /path/to/your/hal/.claude/skills/

   # Copy the command playbook
   cp .claude/commands/HAL-learn-video.md /path/to/your/hal/.claude/commands/

   # Copy the context pointer
   cp .claude/context/commands/HAL-learn-video.md /path/to/your/hal/.claude/context/commands/
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   # Install yt-dlp (video downloader)
   pip install yt-dlp
   # or: brew install yt-dlp (macOS)
   # or: scoop install yt-dlp (Windows)

   # Install FFmpeg (frame extractor)
   # macOS: brew install ffmpeg
   # Ubuntu/WSL: sudo apt install ffmpeg
   # Windows: scoop install ffmpeg or download from ffmpeg.org
   ```

3. **Verify installation**:
   ```bash
   yt-dlp --version
   ffmpeg -version
   ```

### Usage

Simply mention learning from a video in conversation:

```
"Learn from this video: https://youtu.be/..."
"Analyze this YouTube tutorial"
"Extract knowledge from [video URL]"
"What's in this video?"
```

Or use the command directly:
```
/HAL-learn-video <youtube-url>
```

## Features

### Intelligent Content Detection
- **Auto-detection**: Skill activates when you mention video learning
- **Content typing**: Detects technical, educational, business, or general content
- **Pattern selection**: Automatically selects optimal AI patterns for content type

### Interactive Configuration
Choose processing depth before extraction:
- **Fast**: Quick transcript + key frames (~10-20 frames)
- **Smart**: Selective analysis with balanced detail (~5-15 frames) ← Recommended
- **Thorough**: Dense extraction with complete chapters (~3-10 frames)

### Visual Intelligence
- Extracts slides, diagrams, flowcharts, code snippets
- OCR text extraction from visual elements
- Mermaid diagram recreation for flowcharts
- Timestamp correlation between audio and visual

### Knowledge Synthesis
Applies multiple AI patterns in sequence:
- Technical videos: `extract_wisdom` → `explain_code` → `create_summary`
- Educational: `youtube_summary` → `extract_main_idea` → `create_video_chapters`
- Business: `extract_insights` → `analyze_presentation` → `extract_recommendations`

## Output Format

### Comprehensive Knowledge Brief

```markdown
# Video Learning: [Title]

## Executive Summary
[What you need to know immediately]

## Key Insights & Wisdom
[Core valuable takeaways]

## Visual Content Analysis
[Diagrams with descriptions, OCR text, Mermaid recreations]

## Detailed Analysis
- Chapter breakdown with timestamps
- Complete idea extraction (nothing lost)
- Quotes with timestamps
- Practical applications
- Technical details (for tech content)

## Reference Materials
- Frame gallery
- Complete transcript
- Source information
- Related resources
```

### File Organization

```
inbox/video-learning/[video-name]/
├── knowledge-brief.md      # Main output
├── transcript.vtt          # Timestamped transcript
├── metadata.json           # Processing details
└── frames/                 # Visual elements
    ├── frame_000001.jpg
    └── ...
```

## Dependencies

### Required
- **yt-dlp**: Video and caption download
  - Install: `pip install yt-dlp`
  - Verify: `yt-dlp --version`

- **FFmpeg**: Frame extraction
  - Install: Platform-specific (see Quick Start)
  - Verify: `ffmpeg -version`

- **Fabric Patterns**: AI extraction patterns
  - Location: `.claude/tools/fabric-patterns/`
  - Should be included in HAL installation

### Optional
- **Mermaid CLI**: For diagram rendering (if you want PNG outputs)
  - Install: `npm install -g @mermaid-js/mermaid-cli`

## Configuration Options

### Processing Modes
- **Fast** (0.3 threshold): Maximum frames, quick processing
- **Smart** (0.5 threshold): Balanced quality/speed ← Default
- **Thorough** (0.6 threshold): High-value frames only

### Pattern Chains
- Customizable per video type
- Override recommendations during configuration
- Supports all 227 Fabric patterns

### Storage Options
- Default: `inbox/video-learning/`
- Optional archival to `archive/video-learning/`
- Optional video file retention for offline reference

## Examples

### Technical Tutorial
```
User: "Learn from this Docker tutorial: https://youtu.be/..."

→ Detects technical content
→ Applies code extraction patterns
→ Captures architecture diagrams
→ Returns: Code examples + explanations + visual architecture
```

### Business Presentation
```
User: "Analyze this startup pitch: https://youtu.be/..."

→ Detects business content
→ Applies insight extraction patterns
→ Captures slide deck
→ Returns: Key insights + recommendations + visual slides
```

### Educational Lecture
```
User: "What are the main points of this lecture?"

→ Detects educational content
→ Applies learning-focused patterns
→ Creates chapter structure
→ Returns: Organized knowledge with chapters + timestamps
```

## Troubleshooting

### "yt-dlp not found"
- Install: `pip install yt-dlp`
- Or add to PATH if already installed

### "ffmpeg not found"
- Install platform-specific FFmpeg
- For WSL: Use full path `/c/Users/.../ffmpeg.exe`

### "No captions available"
- Video must have auto-generated or manual captions
- Enable captions on YouTube if you own the video
- Some videos don't support caption extraction

### "Processing directory exists"
- Command will ask to overwrite or rename
- Previous work is preserved unless explicitly overwritten

## Advanced Usage

### Custom Pattern Chains
During configuration, specify custom patterns:
```
Custom patterns: extract_wisdom,create_summary,label_and_rate
```

### Scene Threshold Tuning
- Lower (0.3): More frames, more detail, slower
- Higher (0.6): Fewer frames, key moments only, faster
- Adjust during configuration based on content density

### Batch Processing
Process multiple videos by running command multiple times. Each gets its own directory.

## Integration Notes

### HAL System Integration
- Follows UFC (Unified File-based Context) architecture
- ADHD-optimized with progressive detail format
- Token-efficient through command delegation
- Maintains conversation context during processing

### Platform Compatibility
- **Tested on**: WSL2 (Ubuntu) + Windows
- **Should work on**: macOS, Linux, native Windows
- **Note**: Path handling adjusted for mixed environments

## Support

For issues or questions:
1. Check troubleshooting section above
2. Verify dependencies installed correctly
3. Ensure YouTube URL is valid and has captions
4. Check command playbook at `.claude/commands/HAL-learn-video.md`

## Version History

- **v1.0** (2025-10-30): Initial skill packaging
  - Auto-detection capability
  - Interactive configuration
  - Comprehensive knowledge extraction
  - Visual analysis with Mermaid recreation
  - Multi-pattern chaining
  - Progressive detail output format

## License

Part of the HAL 7000 system. Shared for community use.

## Credits

- **HAL 7000 System**: Alexandre Sabeti
- **Fabric Patterns**: Daniel Miessler ([danielmiessler/fabric](https://github.com/danielmiessler/fabric))
- **Claude Code**: Anthropic
