#!/usr/bin/env python3
"""
validate_relay.py - validate AI relay drops. NEVER executes payload content.

Checks, per changed file under proposals/ checkpoints/ tasks/:
  1. YAML front matter parses and satisfies schema/relay.schema.json core rules.
  2. Secret scan: rejects token-like strings (ghp_/gho_/github_pat_/sk-/xox/AKIA/
     eyJ headers, private keys, generic 'token: <literal>' assignments).
  3. URL lint: rejects hardcoded non-allowlisted URLs (allowlist: github.com/ajdhoward,
     api.github.com, docs.github.com, raw.githubusercontent.com/ajdhoward).
  4. Executable payload scan: rejects curl/wget/eval/sudo/rm -rf/chmod/ssh/nc
     invocations inside relay bodies.

Exit 0 = all clean; exit 1 = violations found (report printed, nothing executed).
Run with: python3 .github/scripts/validate_relay.py [paths...]  (default: git diff)
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
WATCHED = ("proposals/", "checkpoints/", "tasks/")

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"gho_[A-Za-z0-9]{20,}"),
    re.compile(r"ghu_[A-Za-z0-9]{20,}"),
    re.compile(r"ghs_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[bposa]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"cf_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|secret|password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._-]{16,}"),
]

URL_ALLOW = re.compile(
    r"https?://("
    r"[a-z0-9.-]*github\.com/ajdhoward|github\.com/ajdhoward|"
    r"api\.github\.com|docs\.github\.com|"
    r"raw\.githubusercontent\.com/ajdhoward"
    r")"
)
URL_ANY = re.compile(r"https?://[^\s)\]>'\"<>]+")

EXEC_PATTERNS = [
    re.compile(r"(?m)^\s*(sudo\s+)?(curl|wget)\b"),
    re.compile(r"\beval\b\s*\("),
    re.compile(r"(?m)^\s*rm\s+-rf\b"),
    re.compile(r"(?m)^\s*chmod\s+(777|[+\-][xX])"),
    re.compile(r"(?m)^\s*ssh\b\s"),
    re.compile(r"(?m)^\s*nc\b\s"),
]

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

REQUIRED_FM = {"task_id", "provider", "account_slot", "status", "next_action", "confidence"}
STATUS_ENUM = {"COMPLETE", "PARTIAL", "BLOCKED"}
NEXT_ENUM = {"CONTINUE", "REASSIGN_NEXT_ACCOUNT", "REVIEW"}
TASK_ID_RE = re.compile(r"^(T-[0-9]{4}|S0-T[0-9]+)$")
ACCOUNT_RE = re.compile(r"^[a-z0-9-]+-acct-[0-9]+$")


def changed_files() -> list[str]:
    args = sys.argv[1:]
    if args:
        return args
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, check=False,
        ).stdout
        if not out.strip():
            out = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True, text=True, check=False,
            ).stdout
        return [ln for ln in out.splitlines() if ln.strip()]
    except Exception:
        return []


def parse_front_matter(text: str) -> dict:
    """Minimal YAML front-matter parser (flat scalar keys, lists with '- ')."""
    m = FRONT_MATTER.match(text)
    if not m:
        raise ValueError("missing or malformed '---' front matter block")
    data: dict = {}
    current_list: list | None = None
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("  - ") or line.startswith("- "):
            item = line.strip()[2:].strip().strip('"')
            if current_list is not None:
                current_list.append(item)
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            current_list = []
            data[key] = current_list
            continue
        current_list = None
        data[key] = val.strip("'\"")
    return data


def lint_file(path: pathlib.Path) -> list[str]:
    problems: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: unreadable ({exc})"]

    # Secret scan (whole file, including front matter).
    for pat in SECRET_PATTERNS:
        for mobj in pat.finditer(text):
            problems.append(f"{path}: SECRET pattern {pat.pattern!r} matched")

    # Executable payload scan (body only — front matter rarely holds commands,
    # but the body is what must stay data-only).
    body = FRONT_MATTER.sub("", text, count=1) if FRONT_MATTER.match(text) else text
    for pat in EXEC_PATTERNS:
        for mobj in pat.finditer(body):
            problems.append(f"{path}: EXECUTABLE payload pattern {pat.pattern!r} matched")

    # URL lint.
    for mobj in URL_ANY.finditer(text):
        url = mobj.group(0)
        if not URL_ALLOW.match(url):
            problems.append(f"{path}: non-allowlisted URL {url}")

    # Front matter validation for relay drops (proposals/ and checkpoints/).
    rel = path.as_posix()
    if rel.startswith(("proposals/", "checkpoints/")) and path.suffix == ".md":
        if path.name == ".gitkeep":
            return problems
        try:
            fm = parse_front_matter(text)
        except ValueError as exc:
            problems.append(f"{path}: {exc}")
            return problems
        missing = REQUIRED_FM - set(fm)
        if missing:
            problems.append(f"{path}: front matter missing {sorted(missing)}")
        if "task_id" in fm and not TASK_ID_RE.match(str(fm["task_id"])):
            problems.append(f"{path}: task_id {fm['task_id']!r} fails pattern")
        if "account_slot" in fm and not ACCOUNT_RE.match(str(fm["account_slot"])):
            problems.append(f"{path}: account_slot {fm['account_slot']!r} fails pattern")
        if fm.get("status") not in STATUS_ENUM:
            problems.append(f"{path}: status {fm.get('status')!r} not in {sorted(STATUS_ENUM)}")
        if fm.get("next_action") not in NEXT_ENUM:
            problems.append(f"{path}: next_action {fm.get('next_action')!r} not in {sorted(NEXT_ENUM)}")
        try:
            conf = int(fm.get("confidence", "x"))
            if not 0 <= conf <= 10:
                problems.append(f"{path}: confidence {conf} out of range 0-10")
        except ValueError:
            problems.append(f"{path}: confidence must be integer 0-10")

    return problems


def main() -> int:
    schema_path = ROOT / "schema" / "relay.schema.json"
    schema_note = "schema file present" if schema_path.exists() else "WARN: schema file missing"
    files = [f for f in changed_files() if f.startswith(WATCHED)]
    if not files:
        print("validate-relay: no watched files changed; nothing to validate.")
        print(f"schema: {schema_note}")
        return 0

    all_problems: list[str] = []
    for f in files:
        p = ROOT / f
        if p.exists():
            all_problems.extend(lint_file(p))

    print(f"validate-relay: checked {len(files)} file(s); {schema_note}")
    if all_problems:
        print(f"FAIL: {len(all_problems)} violation(s):")
        for pr in all_problems:
            print(f"  - {pr}")
        print("Relays are data-only. No content was executed.")
        return 1
    print("PASS: all relays valid (front matter, secrets, URLs, executable payloads).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
