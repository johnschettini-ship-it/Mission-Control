#!/usr/bin/env python3
"""
Universal CLI Wrapper for Mission Control (mc-run)
Wrap ANY arbitrary CLI command, script, or build step.
Auto-detects test runners (pytest, jest, vitest), compilers (tsc, cargo),
git commands, and deployments, sending live telemetry to Mission Control.
Usage:
    python adapters/cli_wrapper.py npm test
    python adapters/cli_wrapper.py git commit -m "ship it"
    python adapters/cli_wrapper.py cargo build
"""

import json
import subprocess
import sys
import urllib.request

BRIDGE_URL = "http://localhost:7890/event"

def emit(event_type: str, detail: str, station: str, agent: str):
    try:
        req = urllib.request.Request(
            BRIDGE_URL,
            data=json.dumps({
                "source": "cli-wrapper",
                "type": event_type,
                "station": station,
                "agent": agent,
                "detail": detail
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=0.25)
    except Exception:
        pass

def classify_command(cmd_args):
    cmd_str = " ".join(cmd_args).lower()
    
    # QA / Tests
    if any(k in cmd_str for k in ("test", "pytest", "jest", "vitest", "mocha", "cargo test", "go test")):
        return ("test", "qa", "Quinn")
    
    # Dev / Build / Compile
    if any(k in cmd_str for k in ("build", "tsc", "compile", "webpack", "vite", "cargo build", "go build")):
        return ("tool", "engine", "Brix")
    
    # Ship / Release / Git commit / push
    if any(k in cmd_str for k in ("git commit", "git push", "deploy", "release", "ship")):
        return ("ship", "ops", "Nova")
    
    # Default tool execution
    return ("tool", "engine", "Brix")

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_wrapper.py <command> [args...]")
        sys.exit(1)

    cmd_args = sys.argv[1:]
    cmd_name = cmd_args[0]
    cmd_display = " ".join(cmd_args[:4])

    event_type, station, agent = classify_command(cmd_args)
    
    # Pre-execution event
    emit(event_type, f"Running: {cmd_display}", station, agent)

    # Run the actual command pass-through
    start_code = subprocess.run(cmd_args)

    # Post-execution status
    if start_code.returncode == 0:
        if event_type == "test":
            emit("test", f"✓ {cmd_display} (PASSED)", "qa", "Quinn")
        elif event_type == "ship":
            emit("ship", f"🚀 {cmd_display} (SUCCESS)", "ops", "Nova")
        else:
            emit("tool", f"✓ {cmd_display} (COMPLETED)", "engine", "Brix")
    else:
        emit("needsYou", f"⚠ {cmd_display} (FAILED code {start_code.returncode})", "ops", "Nova")

    sys.exit(start_code.returncode)

if __name__ == "__main__":
    main()
