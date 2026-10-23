#!/usr/bin/env python3
"""Offline change selection shared by independent repository CI entry points.

Generated owner copies are installed by maintain-workspace-ci.py. No network,
production credentials, database access, or provider calls are used here.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import shutil
from urllib.parse import unquote, urlsplit


DOC_NAMES = {"AGENTS.md", "CLAUDE.md", "LICENSE", "LICENSE.md", "NOTICE"}
RISK = re.compile(r"(^|/)(\.github|\.gitea|scripts|gateway-core|sdk|gen|migrations?|schemas?|contracts?|auth|authorization|permissions|policy)(/|$)|\.proto$|(^|/)(go\.(mod|sum|work)|package\.json|.*lock.*|Taskfile.*|Makefile|Dockerfile.*|.*compose.*|pyproject\.toml|requirements.*|.*goreleaser.*)$", re.I)
INTEGRATION = re.compile(r"(^|/)(integration|component|system|e2e|migrations?|contracts?|auth|authorization|permissions)(/|$)", re.I)
CODE = re.compile(r"\.(go|ts|tsx|js|jsx|mjs|cjs|py|rs|css|scss|html|sh|sql|proto)$")


def is_doc(path):
    p = Path(path)
    if any(part in p.parts for part in ("testdata", "fixtures")):
        return False
    # Prompt/catalog Markdown and executable/config examples are not prose-only.
    return (p.name in DOC_NAMES or p.name == "README" or (p.name.startswith("README") and p.suffix.lower() in (".md", ".rst", ".txt")) or
            ((path.startswith("docs/") or path.startswith("openspec/")) and p.suffix == ".md"))


def classify(paths, event="pull_request", uncertain=False):
    paths = sorted(set(p.replace("\\", "/") for p in paths))
    integration = any(INTEGRATION.search(p) for p in paths)
    if uncertain or not paths:
        level, reason = "full", "change range unavailable or empty"
    elif all(is_doc(p) for p in paths):
        level, reason = "docs", "documentation-only change"
    elif event != "pull_request":
        level, reason = "full", "default branch or explicit full validation"
    elif integration or any(RISK.search(p) or re.search(r"_(windows|darwin)\.go$", p) for p in paths):
        level, reason = "full", "dependency, workflow, contract, or security change"
    elif all(is_doc(p) or CODE.search(p) for p in paths):
        level, reason = "quick", "source change"
    else:
        level, reason = "full", "unclassified path"
    broad = level == "full"
    return {"level": level, "reason": reason, "integration": integration,
            "docs_changed": any(is_doc(p) for p in paths),
            "go_changed": broad or any(p.endswith(".go") or p.startswith(("internal/", "cmd/")) for p in paths),
            "python_changed": broad or any(p.endswith(".py") for p in paths),
            "web_changed": broad or any(re.search(r"\.(tsx?|jsx?|css|scss|html)$", p) and not p.startswith(("legacy/", "apps/cli/")) for p in paths),
            "legacy_changed": broad or any(p.startswith(("legacy/", "apps/cli/")) for p in paths),
            "spec_changed": any(p.startswith(("openspec/changes/", "openspec/specs/")) and "/archive/" not in p for p in paths),
            "skills_changed": any(p.startswith((".skills/", ".agents/skills/", ".claude/skills/")) or p in ("scripts/skills.sh", "scripts/update-runtime-skill-block.py", ".gitmodules") for p in paths),
            "paths": paths, "uncertain": uncertain}


def git(*args):
    return subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)


def changed_paths(event, event_path=None):
    try:
        payload = json.loads(Path(event_path).read_text()) if event_path else {}
        if event == "pull_request":
            base = payload["pull_request"]["base"]["sha"]
            head = payload["pull_request"]["head"]["sha"]
            base = git("merge-base", base, head).decode().strip()
        elif event == "push":
            base, head = payload["before"], payload["after"]
            if set(base) == {"0"}:
                return [], True
        else:
            return [], True
        for ref in (base, head):
            if not re.fullmatch(r"[a-fA-F0-9]{40,64}", ref):
                return [], True
        # --no-renames includes both old and new paths, including removed files.
        return [os.fsdecode(x) for x in git("diff", "--no-renames", "--name-only", "-z", base, head, "--").split(b"\0") if x], False
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError):
        return [], True


def select():
    event = os.environ.get("GITHUB_EVENT_NAME", os.environ.get("GITEA_EVENT_NAME", "workflow_dispatch"))
    event_path = os.environ.get("GITHUB_EVENT_PATH", os.environ.get("GITEA_EVENT_PATH"))
    paths, uncertain = changed_paths(event, event_path)
    result = classify(paths, event, uncertain)
    output = os.environ.get("GITHUB_OUTPUT", os.environ.get("GITEA_OUTPUT"))
    if output:
        with open(output, "a") as f:
            f.write("level=" + result["level"] + "\n")
            f.write("integration=" + str(result["integration"]).lower() + "\n")
            for field in ("docs_changed", "go_changed", "python_changed", "web_changed", "legacy_changed", "spec_changed", "skills_changed"):
                f.write(field + "=" + str(result[field]).lower() + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return result


def docs(paths):
    tracked = [os.fsdecode(p) for p in git("ls-files", "-z", "--", "*.md").split(b"\0") if p]
    gitlinks = [Path(os.fsdecode(row.split(b"\t", 1)[1])).resolve()
                for row in git("ls-files", "--stage", "-z").split(b"\0")
                if row.startswith(b"160000 ") and b"\t" in row]
    selected = {p for p in paths if p.endswith(".md")}
    # Include incoming references to moved/deleted documents; skip immutable history.
    errors = []
    checked = 0
    for name in sorted(set(tracked) | selected):
        p = Path(name)
        if not p.is_file() or any(x in p.parts for x in ("vendor", "node_modules", ".agents", ".claude", "archive", "third_party")):
            continue
        source = p.read_text(errors="replace")
        prose = re.sub(r"```.*?```", "", source, flags=re.S)
        links = re.findall(r"\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", prose)
        relevant = name in selected
        resolved = []
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or (not parsed.path and not parsed.fragment) or parsed.path.startswith("/"):
                continue
            target = (p.parent / unquote(parsed.path)).resolve() if parsed.path else p.resolve()
            resolved.append((link, target, unquote(parsed.fragment)))
            if any(target == Path(changed).resolve() for changed in paths):
                relevant = True
        if not relevant:
            continue
        checked += 1
        for link, target, fragment in resolved:
            # Runtime symlinks may be absent in standalone checkout; do not hide
            # a missing ordinary Markdown file behind an existence heuristic.
            if not target.is_relative_to(Path.cwd().resolve()):
                continue  # Cross-owner links are checked by the workspace, not standalone CI.
            if not target.exists():
                if target.relative_to(Path.cwd().resolve()).parts[0] in ("temp", ".local", "dist", ".understand-anything"):
                    continue  # Per-run evidence/build artifacts are not checked-in docs.
                if any(target.is_relative_to(module) and not (module / ".git").exists() for module in gitlinks):
                    continue  # Standalone checkout has not initialized this independent owner.
                errors.append(f"{name}: missing link target {link}")
            elif fragment and target.suffix == ".md":
                content = re.sub(r"```.*?```", "", target.read_text(errors="replace"), flags=re.S)
                anchors = set(re.findall(r'<[^>]+(?:id|name)=[\"\']([^\"\']+)', content))
                counts = {}
                for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", content, re.M):
                    heading = re.sub(r"[^\w\-\s]", "", heading.lower()).strip().replace(" ", "-")
                    count = counts.get(heading, 0)
                    counts[heading] = count + 1
                    anchors.add(heading + (f"-{count}" if count else ""))
                if fragment not in anchors:
                    errors.append(f"{name}: missing anchor {link}")
    for error in errors:
        print(error, file=sys.stderr)
    ids = {Path(p).parts[2] for p in paths if p.startswith(("openspec/changes/", "openspec/specs/")) and len(Path(p).parts) > 2 and "/archive/" not in p}
    for identifier in sorted(ids):
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", identifier):
            errors.append("invalid OpenSpec identifier")
            continue
        if not any((Path("openspec") / kind / identifier).exists() for kind in ("changes", "specs")):
            continue  # Removed/archived items are checked through incoming links.
        executable = ["openspec"] if shutil.which("openspec") else ["npx", "--yes", "@fission-ai/openspec@1.6.0"]
        result = subprocess.run([*executable, "validate", identifier, "--strict", "--no-interactive"], capture_output=True)
        if result.returncode:
            errors.append(f"OpenSpec validation failed: {identifier}")
            print(errors[-1], file=sys.stderr)
    print(f"docs: checked={checked} errors={len(errors)}")
    return 1 if errors else 0


def gate(level, results):
    """Results are supplied through environment variables, never shell interpolation."""
    expected = {"docs": "docs", "quick": "quick", "full": "full"}[level]
    for lane, result in results.items():
        wanted = "success" if lane == expected else "skipped"
        if result != wanted:
            raise ValueError(f"{lane}: expected {wanted}, got {result}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["select", "docs"])
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    if args.command == "select":
        select()
        return 0
    if args.paths:
        return docs(args.paths)
    result = select()
    return docs(result["paths"])


if __name__ == "__main__":
    sys.exit(main())
