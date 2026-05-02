import sys
import os
import shutil
import yt_dlp
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def print_info(text):
    console.print(f"[bold blue]\\[*][/] {text}")

def print_success(text):
    console.print(f"[bold green]\\[+][/] {text}")

def print_error(text):
    console.print(f"[bold red]\\[!][/] {text}")

def print_warn(text):
    console.print(f"[bold yellow]\\[!][/] {text}")

def cleanup_stale_files(cwd):
    """Rescue leftover files from a previously interrupted download."""
    import re
    rescued = False

    # 1. Rename any *.temp.mkv → *.mkv (ffmpeg merged but couldn't rename)
    for f in os.listdir(cwd):
        if f.endswith('.temp.mkv'):
            src = os.path.join(cwd, f)
            final_name = f.replace('.temp.mkv', '.mkv')
            dst = os.path.join(cwd, final_name)
            try:
                os.rename(src, dst)
                print_warn(f"Rescued merged file: [dim]{f}[/] → [bold white]{final_name}[/]")
                rescued = True
                # Move the rescued .mkv into its own named folder
                folder_name = final_name.replace('.mkv', '').strip()
                folder_name = ''.join(c if c not in r'\/:*?"<>|' else '_' for c in folder_name)[:80]
                os.makedirs(os.path.join(cwd, folder_name), exist_ok=True)
                shutil.move(dst, os.path.join(cwd, folder_name, final_name))
                print_warn(f"Moved to folder:  [bold white]{folder_name}/[/]")
            except OSError as e:
                print_error(f"Could not rescue {f}: {e}")

    # 2. Move any loose .mkv / .mp3 files in the root into their named folder
    for f in os.listdir(cwd):
        fpath = os.path.join(cwd, f)
        if os.path.isfile(fpath) and f.lower().endswith(('.mkv', '.mp3')):
            stem = f.rsplit('.', 1)[0].strip()
            folder_name = ''.join(c if c not in r'\/:*?"<>|' else '_' for c in stem)[:80]
            folder_path = os.path.join(cwd, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            shutil.move(fpath, os.path.join(folder_path, f))
            print_warn(f"Moved loose file: [dim]{f}[/] → [bold white]{folder_name}/[/]")
            rescued = True

    # 3. Delete raw stream shards (*.f123.webm / *.f123.m4a) — check root and subfolders
    stream_pattern = re.compile(r'^(.+)\.f\d+\.(webm|m4a|mp4)$')
    for f in os.listdir(cwd):
        m = stream_pattern.match(f)
        if m:
            merged = os.path.join(cwd, m.group(1) + '.mkv')
            if os.path.exists(merged):
                try:
                    os.remove(os.path.join(cwd, f))
                    print_warn(f"Removed stale stream shard: [dim]{f}[/]")
                    rescued = True
                except OSError:
                    pass

    # 3. Wipe incomplete .part files from the temp dir
    temp_dir = os.path.join(cwd, '.ytdl_temp')
    if os.path.isdir(temp_dir):
        for f in os.listdir(temp_dir):
            if f.endswith('.part'):
                try:
                    os.remove(os.path.join(temp_dir, f))
                    print_warn(f"Removed incomplete part file: [dim]{f}[/]")
                    rescued = True
                except OSError:
                    pass

    if rescued:
        console.print()

def print_logo():
    logo = r"""
__   __ _____ ____  _          ____ _     ___ 
\ \ / /|_   _|  _ \| |        / ___| |   |_ _|
 \   /   | | | | | | |   ____| |   | |    | | 
  | |    | | | |_| | |__|____| |___| |___ | | 
  |_|    |_| |____/|_____|    \____|_____|___|
"""
    console.print(f"[bold cyan]{logo}[/]", highlight=False)
    console.print("  [dim]Advanced YouTube Downloader  //  powered by yt-dlp + ffmpeg[/]")
    console.print("  [dim]─────────────────────────────────────────────────────────[/]\n")

def main():
    console.clear()
    print_logo()
    cleanup_stale_files(os.getcwd())
    
    url = Prompt.ask("[bold yellow]\\[?][/] Enter YouTube URL")
    url = url.strip()
    if not url:
        print_error("No URL provided. Exiting.")
        return

    print_info("Extracting media metadata...")
    
    ydl_opts = {
        'listformats': False,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            title = info.get('title', 'Unknown Title')
    except Exception as e:
        print_error(f"Failed to fetch metadata: {e}")
        return

    if not formats:
        print_error("No downloadable formats found.")
        return

    print_success(f"Target locked: [bold white]{title}[/]")

    # Build the destination folder name now so we can check for it early
    safe_folder = ''.join(c if c not in r'\/:*?"<>|' else '_' for c in title).strip()
    safe_folder = safe_folder[:80]

    # --- Duplicate detection ---
    if os.path.isdir(safe_folder) and os.listdir(safe_folder):
        console.print()
        console.print(f"  [bold yellow][!][/] Folder already exists: [bold white]{safe_folder}/[/]")
        console.print("  [dim]  1.[/] Skip  (abort download)")
        console.print("  [dim]  2.[/] Re-download  (keep existing files, add new ones)")
        console.print("  [dim]  3.[/] Overwrite  (delete existing files, download fresh)")
        console.print()
        action = Prompt.ask("[bold yellow]\\[?][/] Choose action", choices=["1", "2", "3"], default="1")
        if action == "1":
            print_info("Skipping. Nothing was downloaded.")
            return
        elif action == "3":
            shutil.rmtree(safe_folder)
            print_info(f"Cleared existing folder: [dim]{safe_folder}/[/]")
        # action == "2" falls through — yt-dlp will resume/skip files it already has

    console.print()
    print_info("Available Format Streams:")
    
    # Filter and group formats
    video_formats = []
    audio_formats = []

    for f in formats:
        if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
            video_formats.append(f)
        elif f.get('vcodec') != 'none' and f.get('acodec') == 'none':
            video_formats.append(f)
        elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
            audio_formats.append(f)

    # Print options
    console.print("  [bold magenta]0.[/] [white]Best Quality[/] [dim](Auto-merge Video + Audio)[/]")
    console.print("  [bold magenta]1.[/] [white]Audio Only[/] [dim](Highest Bitrate MP3)[/]")
    
    resolutions = {}
    for f in video_formats:
        h = f.get('height')
        if h and isinstance(h, int):
            if h not in resolutions:
                resolutions[h] = []
            resolutions[h].append(f)
    
    sorted_res = sorted(resolutions.keys(), reverse=True)
    idx = 2
    res_map = {}
    for h in sorted_res:
        console.print(f"  [bold magenta]{idx}.[/] [white]{h}p Video[/] [dim]+ Best Audio[/]")
        res_map[idx] = h
        idx += 1

    console.print()
    choice_str = Prompt.ask("[bold yellow]\\[?][/] Select stream ID", default="0")
    
    try:
        choice = int(choice_str)
    except ValueError:
        print_error("Invalid selection. Aborting.")
        return
        
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ffmpeg_path = None
    
    # Use a dedicated temp folder to avoid Windows file-locking on rename
    temp_dir = os.path.join(os.getcwd(), '.ytdl_temp')
    os.makedirs(temp_dir, exist_ok=True)

    download_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path if ffmpeg_path and os.path.exists(ffmpeg_path) else None,
        'quiet': False,
        'no_warnings': True,
        # Sanitize filenames for Windows (replaces emojis/special chars safely)
        'windowsfilenames': True,
        # Download temp parts to a separate folder so Windows Explorer/Defender
        # can't lock them before ffmpeg renames them to the final file
        'paths': {'temp': temp_dir},
    }

    if choice == 0:
        download_opts['format'] = 'bestvideo+bestaudio/best'
        download_opts['merge_output_format'] = 'mkv'
    elif choice == 1:
        download_opts['format'] = 'bestaudio/best'
        download_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif choice in res_map:
        h = res_map[choice]
        download_opts['format'] = f'bestvideo[height<={h}]+bestaudio/best'
        download_opts['merge_output_format'] = 'mkv'
    else:
        print_error("Invalid stream ID. Aborting.")
        return

    console.print()
    print_info("Initializing download sequence...")
    print_info(f"Using FFmpeg engine: [dim]{'Bundled' if ffmpeg_path else 'System Default'}[/]\n")
    
    # Snapshot existing files so we can detect what was newly downloaded
    existing_files = set(os.listdir(os.getcwd()))

    with yt_dlp.YoutubeDL(download_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            console.print()
            print_error(f"Download terminated with errors: {e}")
            return

    console.print()
    print_success("Download sequence completed successfully!")

    # Detect newly created files (ignore hidden/temp dirs)
    new_files = [
        f for f in os.listdir(os.getcwd())
        if f not in existing_files and not f.startswith('.')
    ]

    if new_files:
        os.makedirs(safe_folder, exist_ok=True)

        print_info(f"Moving files into folder: [bold white]{safe_folder}/[/]")
        for f in new_files:
            src = os.path.join(os.getcwd(), f)
            dst = os.path.join(safe_folder, f)
            shutil.move(src, dst)
            print_info(f"  [dim]{f}[/]")

        print_success(f"Done! Files saved to [bold white]{safe_folder}/[/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nProcess interrupted by user. Exiting.")
        sys.exit(1)
