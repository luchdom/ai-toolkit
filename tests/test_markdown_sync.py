"""Protect existing user instructions when installing Markdown lint guidance."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("markdown_sync", ROOT / "scripts" / "sync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class MarkdownSyncTests(unittest.TestCase):
    def test_append_refresh_and_idempotence_preserve_user_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest = home / "AGENTS.md"
            original = b"# Personal rules\r\n\r\n@RTK.md\r\n"
            dest.write_bytes(original)
            with mock.patch.object(Path, "home", return_value=home):
                sync.sync_markdown_guidance(dest)
                first = dest.read_bytes()
                self.assertTrue(first.startswith(original))
                self.assertEqual(1, first.count(b"<!-- AI-TOOLKIT-MARKDOWN:START -->"))
                config = home / ".config" / "ai-toolkit" / "markdownlint-cli2.jsonc"
                self.assertEqual(
                    (sync.DIST / "tool-instructions/shared/markdownlint-cli2.jsonc").read_bytes(),
                    config.read_bytes(),
                )
                dest.write_bytes(first + b"\r\n# More personal rules\r\n")
                sync.sync_markdown_guidance(dest)
                refreshed = dest.read_bytes()
                self.assertEqual(first + b"\r\n# More personal rules\r\n", refreshed)
                sync.sync_markdown_guidance(dest)
                self.assertEqual(refreshed, dest.read_bytes())

    def test_fresh_home_gets_guidance_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest = home / ".claude" / "CLAUDE.md"
            with mock.patch.object(Path, "home", return_value=home):
                sync.sync_markdown_guidance(dest)
            self.assertIn("markdownlint-cli2", dest.read_text())
            self.assertTrue((home / ".config/ai-toolkit/markdownlint-cli2.jsonc").is_file())

    def test_malformed_or_duplicate_markers_are_preserved(self) -> None:
        start = "<!-- AI-TOOLKIT-MARKDOWN:START -->"
        end = "<!-- AI-TOOLKIT-MARKDOWN:END -->"
        for original in (start, end, end + start, start + end + start + end):
            with self.subTest(original=original), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                dest = home / "AGENTS.md"
                dest.write_text(original)
                with mock.patch.object(Path, "home", return_value=home):
                    with self.assertRaisesRegex(ValueError, "Malformed Markdown lint markers"):
                        sync.sync_markdown_guidance(dest)
                self.assertEqual(original, dest.read_text())
                self.assertFalse((home / ".config").exists())


if __name__ == "__main__":
    unittest.main()
