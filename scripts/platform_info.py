"""Report the execution host without installing or changing anything.

Keep this probe runnable on Python 3.9 so older macOS interpreters can report
the toolkit's Python requirement before build or sync is attempted.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from pathlib import Path


MINIMUM_PYTHON = (3, 11)
COMMANDS = ("py", "python", "python3", "git", "gh", "node", "npm", "brew", "winget", "uv", "dotnet", "ffmpeg", "yt-dlp")


def platform_info() -> dict:
    host = {"win32": "windows", "darwin": "macos"}.get(sys.platform, sys.platform)
    return {
        "platform": host,
        "supportedPlatform": host in {"windows", "macos"},
        "architecture": platform.machine(),
        "python": {
            "executable": sys.executable,
            "version": ".".join(str(part) for part in sys.version_info[:3]),
            "minimumVersion": ".".join(str(part) for part in MINIMUM_PYTHON),
            "supported": sys.version_info[:2] >= MINIMUM_PYTHON,
        },
        "home": str(Path.home()),
        "toolkitRoot": str(Path(__file__).resolve().parents[1]),
        # Environment variables are hints, not evidence of the active shell.
        "shellHints": {name: os.environ.get(name) for name in ("SHELL", "COMSPEC")},
        "commands": {name: shutil.which(name) for name in COMMANDS},
    }


def main() -> int:
    info = platform_info()
    print(json.dumps(info, indent=2))
    return 0 if info["supportedPlatform"] and info["python"]["supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
