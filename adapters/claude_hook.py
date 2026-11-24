#!/usr/bin/env python3
"""
Ultra-Lightweight Claude Code Hook Adapter for Mission Control
Replaces heavy software rasterizers with a sub-5ms non-blocking HTTP event ping.
"""

import json
import sys
import urllib.request

BRIDGE_URL = "http://localhost:7890/event"

def send_event(event_type, detail="", station="engine", agent="Brix"):
    payload = {
        "source": "claude-code",
        "type": event_type,
        "station": station,
        "agent": agent,
        "detail": detail
    }
    try:
        req = urllib.request.Request(
            BRIDGE_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        # 0.2 second timeout so Claude Code is NEVER delayed
        urllib.request.urlopen(req, timeout=0.2)
    except Exception:
        # Silent pass if bridge isn't running
        pass

def main():
    hook_type = sys.argv[1] if len(sys.argv) > 1 else "tool"
    detail = sys.argv[2] if len(sys.argv) > 2 else ""

    if hook_type in ("SessionStart", "plan"):
        send_event("plan", detail or "Session started / Prompting", "strategy", "Zorya")
    elif hook_type in ("PostToolUse", "tool"):
        send_event("tool", detail or "Tool execution", "engine", "Brix")
    elif hook_type in ("test", "qa"):
        send_event("test", detail or "QA verification suite", "qa", "Quinn")
    elif hook_type in ("PermissionRequest", "needsYou"):
        send_event("needsYou", detail or "Permission requested", "ops", "Nova")
    elif hook_type in ("Stop", "ship"):
        send_event("ship", detail or "Turn completed", "ops", "Nova")

if __name__ == "__main__":
    main()
