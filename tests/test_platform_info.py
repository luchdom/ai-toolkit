"""Execution-host routing must not confuse shell hints with the operating system."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("toolkit_platform_info", ROOT / "scripts/platform_info.py")
assert spec is not None and spec.loader is not None
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class PlatformInfoTests(unittest.TestCase):
    def test_execution_os_wins_over_shell_and_inherited_environment(self) -> None:
        cases = (("darwin", "macos", True), ("win32", "windows", True), ("linux", "linux", False))
        for runtime, expected, supported in cases:
            host = SimpleNamespace(platform=runtime, version_info=sys.version_info, executable=sys.executable)
            with self.subTest(runtime=runtime), mock.patch.object(probe, "sys", host), mock.patch.dict(
                probe.os.environ, {"SHELL": "/usr/local/bin/pwsh", "LOCALAPPDATA": "C:/old-host"}
            ):
                info = probe.platform_info()
                self.assertEqual(expected, info["platform"])
                self.assertEqual(supported, info["supportedPlatform"])

    def test_probe_reports_unusable_interpreter_and_unsupported_host(self) -> None:
        for runtime, version, expected in (("darwin", (3, 9, 6), 1), ("win32", (3, 11, 0), 0), ("linux", (3, 12, 0), 1)):
            host = SimpleNamespace(platform=runtime, version_info=version, executable=sys.executable)
            with self.subTest(runtime=runtime, version=version), mock.patch.object(probe, "sys", host), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(expected, probe.main())
                report = json.loads(output.getvalue())
                self.assertEqual(version[:2] >= (3, 11), report["python"]["supported"])
                self.assertEqual(probe.sys.executable, report["python"]["executable"])

    def test_missing_commands_are_explicit_and_paths_come_from_runtime(self) -> None:
        with mock.patch.object(probe.shutil, "which", return_value=None):
            info = probe.platform_info()
        self.assertTrue(all(path is None for path in info["commands"].values()))
        self.assertEqual(str(Path.home()), info["home"])
        self.assertEqual(str(ROOT), info["toolkitRoot"])


if __name__ == "__main__":
    unittest.main()
