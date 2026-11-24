#!/usr/bin/env python3
"""
Antigravity Bridge Adapter for Mission Control
Emits live multi-agent events, subagent activities, and swarm transitions
from Google Antigravity into the 60 FPS Mission Control command deck.
"""

import json
import urllib.request

BRIDGE_URL = "http://localhost:7890/event"

def emit(event_type: str, detail: str = "", station: str = "strategy", agent: str = "Antigravity", tokens: int = 0):
    """
    Emit an event to the local Mission Control bridge.
    
    event_type: 'plan' | 'tool' | 'test' | 'needsYou' | 'ship'
    station: 'strategy' | 'engine' | 'qa' | 'ops'
    agent: name of the active agent / subagent / swarm worker
    """
    payload = {
        "source": "antigravity",
        "type": event_type,
        "station": station,
        "agent": agent,
        "detail": detail,
        "tokens": tokens
    }
    try:
        req = urllib.request.Request(
            BRIDGE_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=0.25) as res:
            return res.status == 200
    except Exception:
        return False

# Convenience wrappers for Antigravity workflows
def on_plan(goal: str, agent: str = "Zorya"):
    emit("plan", detail=goal, station="strategy", agent=agent)

def on_tool_call(tool_name: str, args_summary: str = "", agent: str = "Brix"):
    emit("tool", detail=f"{tool_name}({args_summary})", station="engine", agent=agent)

def on_qa_test(test_suite: str, passed: bool = True, agent: str = "Quinn"):
    detail = f"{test_suite}: {'PASSED' if passed else 'FAILED'}"
    emit("test", detail=detail, station="qa", agent=agent)

def on_user_approval_needed(prompt: str, agent: str = "Nova"):
    emit("needsYou", detail=prompt, station="ops", agent=agent)

def on_ship_complete(release_name: str, agent: str = "Nova"):
    emit("ship", detail=f"Shipped {release_name}", station="ops", agent=agent)

if __name__ == "__main__":
    # Test emission
    print("Testing emission to Mission Control...")
    ok = emit("tool", detail="antigravity_bridge.py active", station="engine", agent="Antigravity")
    if ok:
        print("✓ Event successfully broadcast to Mission Control bridge!")
    else:
        print("ℹ Bridge not running on port 7890 (run python bridge.py first).")
