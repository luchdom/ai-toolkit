import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const cli = join(root, "node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs");

test("explicit workflow files are checked and fixed without touching other files", () => {
  const fixture = mkdtempSync(join(tmpdir(), "markdown-lint-"));
  try {
    for (const name of [".markdownlint-cli2.jsonc", ".markdownlint-audit.jsonc", "src/tool-instructions/shared/markdownlint.json"]) {
      const destination = join(fixture, name);
      mkdirSync(dirname(destination), { recursive: true });
      copyFileSync(join(root, name), destination);
    }
    const relative = ".ai/work/[draft] note.md";
    const target = join(fixture, relative);
    const untouched = join(fixture, ".ai/work/untouched.md");
    const invalid = "# Heading\n- item\n";
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, invalid);
    writeFileSync(untouched, invalid);
    writeFileSync(join(fixture, "README.md"), "# Example\n\nValid prose.\n");

    const run = (...args) => spawnSync(process.execPath, [cli, ...args], { cwd: fixture, encoding: "utf8" });
    const audit = run("--config", ".markdownlint-audit.jsonc");
    assert.equal(audit.status, 0, audit.stdout + audit.stderr);
    assert.match(audit.stdout, /Linting: 1 file/);

    const check = run("--no-globs", `:${relative}`);
    assert.equal(check.status, 1, check.stdout + check.stderr);
    assert.match(check.stderr, /MD032/);

    const fix = run("--no-globs", "--fix", `:${relative}`);
    assert.equal(fix.status, 0, fix.stdout + fix.stderr);
    const recheck = run("--no-globs", `:${relative}`);
    assert.equal(recheck.status, 0, recheck.stdout + recheck.stderr);
    assert.match(recheck.stdout, /Linting: 1 file/);
    assert.equal(readFileSync(untouched, "utf8"), invalid);
    assert.equal(readFileSync(target, "utf8"), "# Heading\n\n- item\n");
  } finally {
    rmSync(fixture, { recursive: true, force: true });
  }
});
