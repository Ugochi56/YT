# YTDL-CLI

```
__   __ _____ ____  _          ____ _     ___ 
\ \ / /|_   _|  _ \| |        / ___| |   |_ _|
 \   /   | | | | | | |   ____| |   | |    | | 
  | |    | | | |_| | |__|____| |___| |___ | | 
  |_|    |_| |____/|_____|    \____|_____|___|
```

> Advanced YouTube video downloader with an interactive CLI — powered by `yt-dlp` and `ffmpeg`.

---

## Features

- 🎬 Download any YouTube video at any available quality (144p → 4K)
- 🔊 Auto-merges best video + best audio into a single `.mkv` file
- 🎵 Audio-only mode (downloads as high-quality `.mp3`)
- 📁 Each download is automatically saved into its own named folder
- 🔁 Duplicate detection — skip, re-download, or overwrite existing files
- 🧹 Auto-cleanup of leftover partial/temp files from interrupted downloads
- 💻 Stylish Linux-style terminal interface using `rich`

---

## Requirements

- Python 3.8+
- `ffmpeg` (bundled automatically via `imageio-ffmpeg`)

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/ytdl-cli.git
cd ytdl-cli
pip install -r requirements.txt
```

---

## Usage

```bash
python ytdl.py
```

You will be prompted to paste a YouTube URL and select your desired quality:

```
[?] Enter YouTube URL: https://www.youtube.com/watch?v=...
[*] Extracting media metadata...
[+] Target locked: Video Title Here

[*] Available Format Streams:
  0. Best Quality (Auto-merge Video + Audio)
  1. Audio Only (Highest Bitrate MP3)
  2. 2160p Video + Best Audio
  3. 1440p Video + Best Audio
  4. 1080p Video + Best Audio
  ...

[?] Select stream ID (0):
```

After downloading, the file is placed in a dedicated folder:

```
ytdl-cli/
  └── Video Title Here/
        └── Video Title Here.mkv
```

---

## Why `.mkv`?

YouTube stores its highest quality video streams (1080p+) as separate video and audio tracks using modern codecs (VP9/AV1). The `.mkv` container is used because it natively supports these formats without re-encoding, preserving maximum quality.

---

## Dependencies

| Package | Purpose |
|---|---|
| `yt-dlp` | YouTube metadata extraction and downloading |
| `imageio-ffmpeg` | Bundled `ffmpeg` binary (no system install needed) |
| `rich` | Terminal UI formatting and styling |

---

## License

MIT
