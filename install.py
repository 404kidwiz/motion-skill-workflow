#!/usr/bin/env python3
"""Install audited motion Agent Skills without executing upstream scripts."""

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
CORE = "motion-skill-workflow"
OFFICIAL = ("lottiefiles-motion-design", "gsap-core", "gsap-frameworks", "gsap-performance", "gsap-plugins", "gsap-react", "gsap-scrolltrigger", "gsap-timeline", "gsap-utils")
AVAILABLE = (CORE,) + OFFICIAL
MARKER = ".motion-skill-workflow-install.json"
TOOL_DIRS = {
    "master": ".skills", "hermes": ".hermes/skills", "codex": ".codex/skills",
    "claude": ".claude/skills", "cursor": ".cursor/skills",
    "gemini-antigravity": ".gemini/skills", "opencode": ".config/opencode/skills",
    "opencode-legacy": ".opencode/skills", "openclaude": ".openclaude/skills",
    "grok": ".grok/skills", "zcode": ".zcode/skills", "agents": ".agents/skills",
}


def skill_source(name):
    return SOURCE if name == CORE else SOURCE / "third_party" / name


def skill_files(name):
    if name == CORE:
        return ("SKILL.md", "references/catalog.md")
    root = skill_source(name)
    markdown = [str(p.relative_to(root)) for p in root.rglob("*.md") if p.is_file()]
    return tuple(sorted(markdown + ["LICENSE"]))


def linked_content(root, names):
    for name in names:
        path = root
        for part in Path(name).parts:
            path = path / part
            if path.is_symlink():
                return True
    return False


def file_hashes(root, names):
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}


def run(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools", default="all", help="Comma-separated target tools or all")
    parser.add_argument("--skills", default=CORE, help="Comma-separated skill names (default: routing skill)")
    parser.add_argument("--official", action="store_true", help="Also install all bundled MIT LottieFiles and GSAP skills")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Target home directory")
    parser.add_argument("--mode", choices=("auto", "link", "copy"), default="auto")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)
    tools = list(TOOL_DIRS) if args.tools == "all" else list(dict.fromkeys(args.tools.split(",")))
    skills = list(dict.fromkeys(args.skills.split(",") + (list(OFFICIAL) if args.official else [])))
    if any(t not in TOOL_DIRS for t in tools) or any(s not in AVAILABLE for s in skills):
        parser.error("unknown tool or skill; use --help and inspect TOOL_DIRS / AVAILABLE")
    for skill in skills:
        src = skill_source(skill)
        names = skill_files(skill)
        if not names or "SKILL.md" not in names or any(not (src / n).is_file() for n in names):
            parser.error(f"missing files in {src}")
        if linked_content(src, names) or any(p.is_symlink() for p in src.rglob("*")):
            parser.error(f"symlinked source content in {src}")
        if skill != CORE and any(p.is_file() and p.suffix != ".md" and p.name != "LICENSE" for p in src.rglob("*")):
            parser.error(f"unexpected file in bundled skill {src}")
    home = args.home.expanduser().resolve()
    mode = ("copy" if os.name == "nt" else "link") if args.mode == "auto" else args.mode
    problems = 0
    for tool in tools:
        for skill in skills:
            src = skill_source(skill)
            names = skill_files(skill)
            expected = file_hashes(src, names)
            dest = home / TOOL_DIRS[tool] / skill
            label = f"{tool}/{skill}"
            if dest == src or (dest.exists() and dest.resolve() == src):
                print(f"OK {label}: source or linked")
                continue
            if dest.is_symlink():
                print(f"CONFLICT {label}: link points elsewhere; left untouched")
                problems += 1
                continue
            if dest.exists():
                marker = dest / MARKER
                try:
                    if not dest.is_dir() or marker.is_symlink():
                        raise ValueError("unmanaged or linked marker")
                    saved = json.loads(marker.read_text(encoding="utf-8"))
                    old = saved["files"]
                    if not isinstance(old, dict) or not set(old).issubset(set(names)):
                        raise ValueError("unknown managed file")
                    if linked_content(dest, tuple(old) + names) or old != file_hashes(dest, old):
                        raise ValueError("installed files changed or linked")
                    if any((dest / n).exists() for n in set(names) - set(old)):
                        raise ValueError("new source path collides with user file")
                except (OSError, ValueError, TypeError, KeyError):
                    print(f"CONFLICT {label}: not an unchanged managed copy; left untouched")
                    problems += 1
                    continue
                if args.verify:
                    same = old == expected
                    print(f"{'OK' if same else 'STALE'} {label}: managed copy")
                    problems += not same
                elif args.dry_run:
                    print(f"WOULD UPDATE {label}: managed copy")
                else:
                    for name in names:
                        target = dest / name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src / name, target)
                    marker.write_text(json.dumps({"files": expected}, indent=2) + "\n", encoding="utf-8")
                    print(f"UPDATED {label}: managed copy")
                continue
            if args.verify:
                print(f"MISSING {label}: {dest}")
                problems += 1
                continue
            if args.dry_run:
                print(f"WOULD {mode.upper()} {label}: {dest}")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            if mode == "link":
                dest.symlink_to(src, target_is_directory=True)
            else:
                dest.mkdir()
                for name in names:
                    target = dest / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src / name, target)
                (dest / MARKER).write_text(json.dumps({"files": expected}, indent=2) + "\n", encoding="utf-8")
            print(f"INSTALLED {label}: {mode}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(run())
