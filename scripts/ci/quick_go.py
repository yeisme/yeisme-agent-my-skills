#!/usr/bin/env python3
"""Run cached Go checks for changed packages and their in-module consumers."""
import json
import os
from pathlib import Path
import subprocess
import sys
import re

from changed_scope import changed_paths


def decode_packages(text):
    decoder = json.JSONDecoder()
    result = []
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        result.append(value)
        text = text[end:]
    return result


def affected(packages, files, all_packages=False, include_integration=False):
    by_name = {p["ImportPath"]: p for p in packages}
    changed = {str(Path(f).parent.resolve()) for f in files}
    chosen = {n for n, p in by_name.items() if all_packages or str(Path(p["Dir"]).resolve()) in changed}
    # Test-only imports matter: changing a library must rerun its consumers' tests.
    while True:
        additions = {n for n, p in by_name.items() if chosen.intersection(
            p.get("Imports", []) + p.get("TestImports", []) + p.get("XTestImports", []))}
        if additions <= chosen:
            break
        chosen |= additions
    return sorted(n for n in chosen if include_integration or not any(part in n.split("/") for part in ("integration", "e2e", "system", "component")))


def run(args, cwd, env):
    print("+ " + " ".join(args), flush=True)
    subprocess.run(args, cwd=cwd, env=env, check=True)


def affected_modules(modules, files):
    contents = {mod: mod.read_text() for mod in modules}
    names = {mod: re.search(r"(?m)^module\s+[\"']?([^\s\"']+)", text).group(1) for mod, text in contents.items()}
    chosen = {mod for mod in modules if any(file.is_relative_to(mod.parent) and
              not any(file.is_relative_to(other.parent) for other in modules if other != mod and other.parent.is_relative_to(mod.parent)) for file in files)}
    while True:
        expanded = chosen | {mod for mod in modules if any(
            re.search(r"(?<![\w/.-])" + re.escape(names[dependency]) + r"(?![\w/.-])", contents[mod])
            for dependency in chosen if dependency != mod)}
        if expanded == chosen:
            return chosen
        chosen = expanded


def main():
    root = Path.cwd()
    event = os.environ.get("GITHUB_EVENT_NAME", os.environ.get("GITEA_EVENT_NAME", "workflow_dispatch"))
    paths, uncertain = changed_paths(event, os.environ.get("GITHUB_EVENT_PATH", os.environ.get("GITEA_EVENT_PATH")))
    force_all = "--all" in sys.argv[1:]
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    modules = [root / p for p in tracked if Path(p).name == "go.mod" and
               not any(x in Path(p).parts for x in ("vendor", "third_party", "testdata", "fixtures", "legacy"))]
    if (root / "go.mod").exists() and root / "go.mod" not in modules:
        modules.insert(0, root / "go.mod")
    if not modules:
        raise ValueError("no maintained Go modules found")
    go_files = [root / p for p in paths if p.endswith(".go")]
    module_closure = affected_modules(modules, go_files)
    env = {**os.environ, "CGO_ENABLED": "0", "GOWORK": "off", "GOFLAGS": os.environ.get("GOFLAGS", "")}
    if any(flag == "-race" or flag.startswith("-race=") for flag in env["GOFLAGS"].split()):
        raise ValueError("race is not allowed in automatic CI")
    for mod in modules:
        directory = mod.parent
        local = [p for p in go_files if p.is_relative_to(directory) and
                 not any(p.is_relative_to(other.parent) for other in modules if other != mod and other.parent.is_relative_to(directory))]
        all_packages = force_all or uncertain or not go_files or (mod in module_closure and not local)
        if not all_packages and mod not in module_closure:
            continue
        run(["go", "mod", "verify"], directory, env)
        fmt_files = [str(p) for p in local if p.is_file()]
        if fmt_files:
            unformatted = subprocess.check_output(["gofmt", "-l", *fmt_files], text=True)
            if unformatted:
                raise ValueError("unformatted Go files:\n" + unformatted)
        listing = ["go", "list", "-json", "./..."]
        if (directory / "scripts/taskfile-go-scope.sh").exists():
            listing = ["sh", "scripts/taskfile-go-scope.sh", "list", "-json"]
        packages = decode_packages(subprocess.check_output(listing, cwd=directory, env=env, text=True))
        selected = affected(packages, local, all_packages, force_all)
        if not selected:
            # A deleted package can disappear from go list. Check all maintained
            # packages instead of reporting a false no-op.
            selected = affected(packages, [], True, force_all)
        if not selected:
            raise ValueError("no non-integration Go packages selected")
        print(f"quick-go: module={directory.relative_to(root)} packages={len(selected)}", flush=True)
        run(["go", "vet", *selected], directory, env)
        run(["go", "test", "-timeout=10m", *selected], directory, env)
        run(["go", "build", *(["-o", os.devnull] if len(selected) == 1 else []), *selected], directory, env)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
