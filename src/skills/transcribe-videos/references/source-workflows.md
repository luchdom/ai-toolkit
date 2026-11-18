# Source workflows

## Public video and YouTube

The one-line `yt-dlp` commands below work in PowerShell and zsh/bash. Use paths that exist on the current host, regardless of paths recorded in earlier sessions.

Inspect metadata without downloading media:

```powershell
yt-dlp --no-playlist --skip-download --dump-single-json "<url>"
```

For transcription, let `transcribe_media.py` download the best audio-only format into a disposable directory. Audio-only selection normally avoids an `ffmpeg` merge.

When the user explicitly wants to keep the video and `ffmpeg` is available:

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format mp4 -P "<output-dir>" -o "%(title)s [%(id)s].%(ext)s" "<url>"
```

Without `ffmpeg`, retain the best single-file format and disclose the possible quality tradeoff:

```powershell
yt-dlp --no-playlist -f "b" -P "<output-dir>" -o "%(title)s [%(id)s].%(ext)s" "<url>"
```

Do not leave `.info.json`, subtitle, thumbnail, or partial-download files in a text-only output directory.

## Logged-in courses

1. Open the lesson in the user’s existing authenticated browser session.
2. Enumerate every visible phase and lesson link in the sidebar. Expand collapsed groups and record the expected count.
3. Navigate each lesson and inspect the player iframe, `video`/`source` elements, and network-visible non-DRM media sources through the authorized page.
4. Keep direct media URLs only in a temporary manifest. Do not print them in status messages or store them in the final Markdown.
5. If the player uses an accessible signed HLS stream, mark the manifest item as `direct_media: true` so the helper streams it directly into the transcription engine.
6. If the stream requires browser-only headers or encrypted playback, continue through the browser when supported or report the boundary. Do not export the browser’s cookie store as a shortcut.

Navigation can change course progress state. Tell the user before opening every lesson in a batch.

## Batch manifest

Store the manifest only in the task’s temporary directory:

```json
{
  "items": [
    {
      "slug": "lesson-01-introduction",
      "title": "Lesson 01 - Introduction",
      "input": "https://temporary-authorized-media.example/stream.m3u8",
      "direct_media": true
    },
    {
      "slug": "public-video",
      "title": "Public video",
      "input": "https://www.youtube.com/watch?v=example",
      "direct_media": false
    }
  ]
}
```

Run one batch so the Whisper model is loaded only once. Run from the installed skill directory, or replace `scripts/transcribe_media.py` with its absolute path. Use the isolated environment prepared below.

macOS with zsh/bash (backslash continues a line):

```sh
"<venv>/bin/python" scripts/transcribe_media.py \
  --manifest "<temporary-dir>/manifest.json" \
  --output-dir "<temporary-dir>/transcripts" \
  --model small \
  --device cpu \
  --compute-type int8 \
  --language <language-code>
```

Windows with PowerShell (backtick continues a line):

```powershell
& "<venv>\Scripts\python.exe" scripts/transcribe_media.py `
  --manifest "<temporary-dir>/manifest.json" `
  --output-dir "<temporary-dir>/transcripts" `
  --model small `
  --device cpu `
  --compute-type int8 `
  --language <language-code>
```

The raw JSON intentionally omits input URLs. It is an intermediate artifact and must be deleted after the Markdown is verified.

## Dependency setup

Use `yt-dlp` from the official project. The `ai-toolkit` repository records Windows and macOS installation options in `EXTERNAL-TOOLS.md`.

Choose Python 3.11 or newer from the current host: verify `python3 --version` on macOS, or `py -3 --version` on Windows, is at least 3.11. A verified absolute interpreter or Windows `python` at version 3.11 or newer is also suitable. The runtime OS determines the venv layout; PowerShell on macOS still uses `bin/python`.

Install `faster-whisper` in an isolated environment when it is unavailable. macOS with zsh/bash:

```sh
python3 -m venv "<venv>"
"<venv>/bin/python" -m pip install --upgrade pip faster-whisper
```

Windows with PowerShell:

```powershell
py -3 -m venv "<venv>"
& "<venv>\Scripts\python.exe" -m pip install --upgrade pip faster-whisper
```

For PowerShell on macOS, use `& "<venv>/bin/python"` to invoke the quoted executable; use PowerShell backticks or a single line for continuations. Use a user-local runtime directory outside Git repositories if the environment should be reused. A task-local environment may be deleted with the other temporary state.
