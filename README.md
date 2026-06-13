# 🚀 Multi-Platform Video Downloader & 4K Upscaler

```text
__   __ _____ ____  _          ____ _     ___ 
\ \ / /|_   _|  _ \| |        / ___| |   |_ _|
 \   /   | | | | | | |   ____| |   | |    | | 
  | |    | | | |_| | |__|____| |___| |___ | | 
  |_|    |_| |____/|_____|    \____|_____|___|

  Advanced Media Downloader  //  powered by yt-dlp + ffmpeg
```

> [!NOTE]  
> A professional, interactive CLI utility engineered to download, format, and upscale video and audio assets from YouTube, TikTok, Instagram, and other major media platforms.

---

## 💡 Why I Built This

Teams and creators frequently require high-quality media assets (B-roll, reference clips, demo audio, and mockups) from various social media and video platforms. Relying on sketchy web-based downloaders introduces security risks, popups, and inconsistent output qualities. 

I built this command-line utility to serve as a **secure, unified, and automated pipeline** for developers and content teams. It ensures:
1. **Safety & Speed**: Clean downloading directly from terminal without external web dependencies.
2. **Upscaling Capability**: Easily upscale reference clips to 4K resolution (3840x2160) for high-fidelity presentations.
3. **No Setup Friction**: Automatically embeds and configures the required FFmpeg engine so users don't have to manually install or configure system environment paths.
4. **Clean Asset Management**: Sanitizes names and neatly organizes downloaded files into distinct, clean directories automatically.

---

## ✨ Features

*   **Multi-Platform Compatibility**: Native prompts optimized for **YouTube**, **TikTok**, **Instagram**, and general video URLs.
*   **4K Upscaling Engine**: Post-processes and upscales video streams to 4K (3840x2160) using a high-quality **Lanczos scaling filter** via FFmpeg.
*   **Targeted Platform Formatting**: 
    *   **YouTube**: Displays full resolution stream tables (1080p, 720p, etc.) and outputs in high-fidelity `.mkv` to avoid quality-loss re-encoding.
    *   **TikTok & Instagram**: Displays simplified menus (Best Quality / Audio Only) and outputs directly in `.mp4` for maximum compatibility on mobile devices and slide decks.
*   **Smart Duplicate Management**: Prompts to skip, re-download (add to folder), or overwrite if a target video directory already exists.
*   **Network Resiliency & Cleanup**: Built-in download retries and automatic cleanup routines to rescue or prune partial files from interrupted downloads.
*   **Interactive Session Loop**: Keeps the session alive, asking the user whether to continue with another download or exit.

---

## 🛠️ Requirements

*   **Python 3.8+**
*   **FFmpeg** (automatically resolved and bundled via `imageio-ffmpeg`; no system installation or environment configuration required).

---

## 🚀 Installation & Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_TEAM_OR_ORG/ytdl-cli.git
    cd ytdl-cli
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Usage

To launch the interactive tool, execute:
```bash
python ytdl.py
```

### Flow Walkthrough:
1. **Platform Selection**: Select the platform you are downloading from.
2. **URL Input**: Paste your target video or audio link.
3. **Format Options**: Choose your preferred download option (best quality, audio-only, or select custom resolutions for YouTube).
4. **4K Upscaling**: Decide whether to upscale your video output to 4K (3840x2160).
5. **Session Control**: After download completion, choose to either download another asset or exit the CLI cleanly.

---

## 📦 Core Dependencies

| Package | Purpose |
| :--- | :--- |
| **`yt-dlp`** | Active, industry-standard engine for media metadata extraction and stream fetching. |
| **`imageio-ffmpeg`** | Packages the precompiled FFmpeg binaries, eliminating OS-specific configuration friction. |
| **`rich`** | Powers the modern interactive terminal UI, colors, prompts, and tables. |

---

## 👥 Contributing

Contributions, bug reports, and suggestions are welcome! Feel free to submit issues, features, or pull requests to extend platform configurations or add new post-processing options.
