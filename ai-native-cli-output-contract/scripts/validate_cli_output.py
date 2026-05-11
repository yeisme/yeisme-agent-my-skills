#!/usr/bin/env python3
"""Validate Yeisme AI-native CLI output samples.

This is a lightweight guardrail for skill users. It intentionally avoids external
dependencies so it can run in any project checkout.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
KEY_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$")
COMMAND_RE = re.compile(r"^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)+$")
STATUSES = {"success", "partial", "failed"}
MODES = {"summary", "agent", "json", "events", "explain"}
EVENT_TYPES = {
    "start",
    "progress",
    "fact",
    "finding",
    "action",
    "evidence",
    "warning",
    "error",
    "end",
}


def fail(message: str) -> None:
    print(f"invalid: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_input(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def reject_ansi(text: str, allow_ansi: bool) -> None:
    if not allow_ansi and ANSI_RE.search(text):
        fail("output contains ANSI escape sequences")


def require_str(obj: dict[str, Any], key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(f"missing or invalid string field: {key}")
    return value


def validate_envelope(obj: Any, expected_mode: str, expected_command: str | None) -> None:
    if not isinstance(obj, dict):
        fail("JSON envelope must be an object")

    spec_version = require_str(obj, "spec_version")
    if not VERSION_RE.match(spec_version):
        fail("spec_version must look like 1.0 or 1.0.0")

    mode = require_str(obj, "mode")
    if mode not in MODES:
        fail(f"mode must be one of {sorted(MODES)}")
    if mode != expected_mode:
        fail(f"mode must be {expected_mode}, got {mode}")

    command = require_str(obj, "command")
    if not COMMAND_RE.match(command):
        fail("command must be normalized like domain.action")
    if expected_command and command != expected_command:
        fail(f"command must be {expected_command}, got {command}")

    status = require_str(obj, "status")
    if status not in STATUSES:
        fail(f"status must be one of {sorted(STATUSES)}")

    confidence = obj.get("confidence")
    if confidence is not None and not (
        isinstance(confidence, (int, float)) and 0 <= float(confidence) <= 1
    ):
        fail("confidence must be a number from 0 to 1")

    actions = obj.get("actions")
    if actions is not None:
        if not isinstance(actions, list):
            fail("actions must be an array")
        for index, item in enumerate(actions):
            if not isinstance(item, dict):
                fail(f"actions[{index}] must be an object")
            require_str(item, "name")
            require_str(item, "command")

    if status == "failed":
        error = obj.get("error")
        if not isinstance(error, dict):
            fail("failed envelopes must include error object")
        require_str(error, "code")
        require_str(error, "message")


def validate_json(text: str, expected_command: str | None) -> None:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"stdout is not valid JSON: {exc}")
    validate_envelope(obj, "json", expected_command)


def parse_agent(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line_number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("{"):
            fail(f"agent line {line_number} looks like JSON, expected key=value")
        if "=" not in line:
            fail(f"agent line {line_number} is not key=value")
        key, value = line.split("=", 1)
        if not KEY_RE.match(key):
            fail(f"agent line {line_number} has invalid key: {key}")
        if "\n" in value or "\r" in value:
            fail(f"agent line {line_number} has multiline value")
        result[key] = value
    return result


def validate_agent(text: str, expected_command: str | None) -> None:
    values = parse_agent(text)
    for key in ("spec_version", "mode", "command", "status"):
        if key not in values or not values[key]:
            fail(f"agent output missing {key}")
    if not VERSION_RE.match(values["spec_version"]):
        fail("agent spec_version must look like 1.0 or 1.0.0")
    if values["mode"] != "agent":
        fail("agent mode must be agent")
    if not COMMAND_RE.match(values["command"]):
        fail("agent command must be normalized like domain.action")
    if expected_command and values["command"] != expected_command:
        fail(f"agent command must be {expected_command}, got {values['command']}")
    if values["status"] not in STATUSES:
        fail(f"agent status must be one of {sorted(STATUSES)}")


def validate_events(text: str, expected_command: str | None) -> None:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        fail("events output is empty")

    events: list[dict[str, Any]] = []
    previous_seq: int | None = None
    for line_number, line in enumerate(lines, 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"event line {line_number} is not valid JSON: {exc}")
        if not isinstance(event, dict):
            fail(f"event line {line_number} must be an object")
        event_type = event.get("type")
        if event_type not in EVENT_TYPES:
            fail(f"event line {line_number} has invalid type: {event_type}")
        command = event.get("command")
        if expected_command and command is not None and command != expected_command:
            fail(f"event line {line_number} command must be {expected_command}, got {command}")
        seq = event.get("seq")
        if seq is not None:
            if not isinstance(seq, int):
                fail(f"event line {line_number} seq must be an integer")
            if previous_seq is not None and seq <= previous_seq:
                fail(f"event line {line_number} seq is not increasing")
            previous_seq = seq
        events.append(event)

    if events[0].get("type") != "start":
        fail("events output must start with type=start")
    if events[-1].get("type") not in {"end", "error"}:
        fail("events output must end with type=end or type=error")
    final_status = events[-1].get("status")
    if final_status is not None and final_status not in STATUSES:
        fail(f"final event status must be one of {sorted(STATUSES)}")


def validate_human(text: str, mode: str) -> None:
    stripped = text.strip()
    if not stripped:
        fail(f"{mode} output is empty")
    if stripped.startswith("{") or stripped.startswith("["):
        fail(f"{mode} output must not default to raw JSON")
    if mode == "explain":
        for marker in ("结论", "证据"):
            if marker not in stripped:
                fail(f"explain output must include {marker}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI-native CLI output samples.")
    parser.add_argument("--mode", required=True, choices=sorted(MODES))
    parser.add_argument("--command", help="Expected normalized command name, such as task.get.")
    parser.add_argument("--file", help="Read output from a file instead of stdin.")
    parser.add_argument("--allow-ansi", action="store_true", help="Allow ANSI escape sequences.")
    args = parser.parse_args()

    text = read_input(args.file)
    reject_ansi(text, args.allow_ansi)

    if args.mode == "json":
        validate_json(text, args.command)
    elif args.mode == "agent":
        validate_agent(text, args.command)
    elif args.mode == "events":
        validate_events(text, args.command)
    else:
        validate_human(text, args.mode)

    print("valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
