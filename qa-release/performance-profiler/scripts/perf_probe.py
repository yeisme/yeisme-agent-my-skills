#!/usr/bin/env python3
"""Small dependency-free performance probe for repo commands and local HTTP URLs."""

from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


MARKER = "__PERF_PROBE_TIME__"
SCRIPT_KEYWORDS = ("bench", "perf", "profile", "build", "test", "start", "dev")


def tail(text: str | bytes | None, limit: int = 4000) -> str:
    if text is None:
        return ""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[-limit:]


def run_quiet(args: list[str], cwd: Path, timeout: int = 10) -> str | None:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def command_version(binary: str, cwd: Path) -> str | None:
    if not shutil.which(binary):
        return None
    version_args = {
        "python": [sys.executable, "--version"],
        "python3": [sys.executable, "--version"],
    }.get(binary, [binary, "--version"])
    out = run_quiet(version_args, cwd)
    return out.splitlines()[0] if out else None


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def discover_package_scripts(cwd: Path) -> dict[str, str]:
    package_json = read_json(cwd / "package.json")
    if not package_json:
        return {}
    scripts = package_json.get("scripts", {})
    if not isinstance(scripts, dict):
        return {}
    selected = {}
    for name, command in scripts.items():
        if any(keyword in name.lower() for keyword in SCRIPT_KEYWORDS):
            selected[name] = str(command)
    return selected


def discover_taskfile_tasks(cwd: Path) -> list[str]:
    for name in ("Taskfile.yml", "Taskfile.yaml", "taskfile.yml", "taskfile.yaml"):
        path = cwd / name
        if not path.exists():
            continue
        tasks: list[str] = []
        in_tasks = False
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if re.match(r"^tasks:\s*$", line):
                in_tasks = True
                continue
            if in_tasks:
                match = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
                if match:
                    tasks.append(match.group(1))
        return tasks
    return []


def git_file_stats(cwd: Path) -> dict[str, int] | None:
    out = run_quiet(["git", "ls-files", "-z"], cwd)
    if out is None:
        return None
    files = [item for item in out.split("\0") if item]
    total_bytes = 0
    for item in files:
        try:
            total_bytes += (cwd / item).stat().st_size
        except OSError:
            continue
    return {"tracked_files": len(files), "tracked_bytes": total_bytes}


def discover(cwd: Path) -> dict[str, Any]:
    manifests = [
        "package.json",
        "bun.lockb",
        "bun.lock",
        "pnpm-lock.yaml",
        "package-lock.json",
        "go.mod",
        "Cargo.toml",
        "pyproject.toml",
        "requirements.txt",
        "Taskfile.yml",
        "Taskfile.yaml",
    ]
    found_manifests = [name for name in manifests if (cwd / name).exists()]
    candidate_commands: list[str] = []

    scripts = discover_package_scripts(cwd)
    for name in scripts:
        if shutil.which("bun"):
            candidate_commands.append(f"bun run {name}")
        elif shutil.which("pnpm"):
            candidate_commands.append(f"pnpm run {name}")
        elif shutil.which("npm"):
            candidate_commands.append(f"npm run {name}")

    if (cwd / "go.mod").exists():
        candidate_commands.extend(["go test ./...", "go test -bench . -benchmem ./..."])
    if (cwd / "Cargo.toml").exists():
        candidate_commands.extend(["cargo test", "cargo bench"])
    if (cwd / "pyproject.toml").exists() or (cwd / "requirements.txt").exists():
        candidate_commands.append("python -m pytest")

    taskfile_tasks = discover_taskfile_tasks(cwd)
    for task in taskfile_tasks:
        if any(keyword in task.lower() for keyword in SCRIPT_KEYWORDS):
            candidate_commands.append(f"task {task}")

    tools = {}
    for binary in ("node", "bun", "npm", "pnpm", "go", "cargo", "python3", "git", "task"):
        version = command_version(binary, cwd)
        if version:
            tools[binary] = version

    return {
        "cwd": str(cwd),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "manifests": found_manifests,
        "package_scripts": scripts,
        "taskfile_tasks": taskfile_tasks,
        "candidate_commands": sorted(dict.fromkeys(candidate_commands)),
        "tools": tools,
        "git": git_file_stats(cwd),
    }


def parse_time_marker(stderr: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    retained_lines: list[str] = []
    for line in stderr.splitlines():
        if line.startswith(MARKER):
            parts = line.split()
            if len(parts) == 5:
                parsed = {
                    "time_wall_sec": float(parts[1]),
                    "user_sec": float(parts[2]),
                    "system_sec": float(parts[3]),
                    "max_rss_kb": int(float(parts[4])),
                }
            continue
        retained_lines.append(line)
    parsed["stderr_without_marker"] = "\n".join(retained_lines)
    return parsed


def run_command_probe(command: str, cwd: Path, timeout: int) -> dict[str, Any]:
    time_bin = "/usr/bin/time"
    use_gnu_time = Path(time_bin).exists()
    if use_gnu_time:
        args: list[str] | str = [time_bin, "-f", f"{MARKER} %e %U %S %M", "bash", "-lc", command]
        shell = False
    else:
        args = command
        shell = True

    started = time.perf_counter()
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "command": command,
            "exit_code": None,
            "timed_out": True,
            "timeout_sec": timeout,
            "wall_ms": elapsed_ms,
            "stdout_tail": tail(exc.stdout),
            "stderr_tail": tail(exc.stderr),
        }

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    marker = parse_time_marker(completed.stderr) if use_gnu_time else {}
    stderr = marker.pop("stderr_without_marker", completed.stderr)
    result = {
        "command": command,
        "exit_code": completed.returncode,
        "timed_out": False,
        "wall_ms": elapsed_ms,
        "stdout_tail": tail(completed.stdout),
        "stderr_tail": tail(stderr),
    }
    result.update(marker)
    return result


def probe_url(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "perf-probe/1.0"},
        method="GET",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(1024 * 1024)
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            return {
                "url": url,
                "ok": True,
                "status": response.status,
                "elapsed_ms": elapsed_ms,
                "bytes_read": len(body),
            }
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "url": url,
            "ok": False,
            "status": None,
            "elapsed_ms": elapsed_ms,
            "error": str(exc),
        }


def summarize_numeric(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    sorted_values = sorted(values)
    p95_index = max(0, min(len(sorted_values) - 1, int(round((len(sorted_values) - 1) * 0.95))))
    return {
        "min": round(min(values), 2),
        "median": round(statistics.median(values), 2),
        "p95": round(sorted_values[p95_index], 2),
        "max": round(max(values), 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect lightweight performance baseline evidence.")
    parser.add_argument("--cwd", default=".", help="Working directory for discovery and command probes.")
    parser.add_argument("--cmd", action="append", default=[], help="Command to time. May be repeated.")
    parser.add_argument("--cmd-repeat", type=int, default=1, help="Number of times to run each command.")
    parser.add_argument("--url", action="append", default=[], help="HTTP URL to probe. May be repeated.")
    parser.add_argument("--url-repeat", type=int, default=5, help="Number of times to probe each URL.")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per command or URL probe in seconds.")
    parser.add_argument("--discover-only", action="store_true", help="Only emit discovery output.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.exists():
        print(f"missing cwd: {cwd}", file=sys.stderr)
        return 2

    report: dict[str, Any] = {
        "schema": "performance-profiler.perf-probe.v1",
        "generated_at_unix": int(time.time()),
        "discovery": discover(cwd),
    }

    if not args.discover_only:
        command_runs = []
        for command in args.cmd:
            for iteration in range(1, max(1, args.cmd_repeat) + 1):
                result = run_command_probe(command, cwd, args.timeout)
                result["iteration"] = iteration
                command_runs.append(result)
        report["command_runs"] = command_runs

        url_runs = []
        for url in args.url:
            for iteration in range(1, max(1, args.url_repeat) + 1):
                result = probe_url(url, args.timeout)
                result["iteration"] = iteration
                url_runs.append(result)
        report["url_runs"] = url_runs

        command_groups: dict[str, list[float]] = {}
        for run in command_runs:
            if run.get("exit_code") == 0 and isinstance(run.get("wall_ms"), (int, float)):
                command_groups.setdefault(run["command"], []).append(float(run["wall_ms"]))
        report["command_summary_ms"] = {
            command: summarize_numeric(values) for command, values in command_groups.items()
        }

        url_groups: dict[str, list[float]] = {}
        for run in url_runs:
            if run.get("ok") and isinstance(run.get("elapsed_ms"), (int, float)):
                url_groups.setdefault(run["url"], []).append(float(run["elapsed_ms"]))
        report["url_summary_ms"] = {url: summarize_numeric(values) for url, values in url_groups.items()}

    output = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
