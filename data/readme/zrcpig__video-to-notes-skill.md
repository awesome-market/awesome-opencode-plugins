# Video Notes

[中文说明](README.zh-CN.md)

Transform online videos into structured reading notes with AI-powered transcription.

## What This Does

Input a video link, get:
- Video archive
- Lossless audio track  
- Full transcript (logically segmented)
- Structured summary notes (with AI assistance)

## Quick Start

```bash
# 1. Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
brew install ffmpeg  # or apt/choco on other platforms
uv tool install yt-dlp
uv tool install funasr --with torch --with torchaudio

# 2. Run the workflow
./video-notes.sh "https://www.bilibili.com/video/BVxxxx" "topic-name"

# 3. Find outputs in ~/video-notes/YYMMDD-topic-name/
```

## Why Fun-ASR-Nano?

| Feature | Fun-ASR-Nano | Whisper |
|---------|-------------|---------|
| Chinese CER | ~8% | ~20% |
| Homophone correction | Built-in LLM | None |
| Speed | 0.2-0.4 RTF | 0.1-0.3 RTF |
| English mixed content | Excellent | Good |

## Legal & Compliance

This tool is designed for:
- Personal learning and research
- Content archival (your own videos, Creative Commons, public domain)
- Accessibility purposes

**You are responsible for complying with platform Terms of Service.** Only download content you have the legal right to access. Do not redistribute downloaded content.

## Repository Structure

```
video-notes/
├── SKILL.md              # Agent Skills standard format
├── README.md             # This file
├── LICENSE               # MIT
├── video-notes.sh        # One-click workflow script
└── examples/             # Sample outputs (optional)
```

## Contributing

Issues and PRs welcome. Please ensure any contributed code respects platform ToS and copyright law.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video download
- [FunASR](https://github.com/modelscope/FunASR) - Speech recognition
- [ffmpeg](https://ffmpeg.org/) - Media processing
