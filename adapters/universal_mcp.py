#!/usr/bin/env python3
"""
Universal Model Context Protocol (MCP) Server for Mission Control
Allows ANY MCP-compatible coding agent (Antigravity, Claude Code, Claude Desktop,
Cursor, Windsurf, Zed, Continue.dev, etc.) to natively interact with Mission Control.
Zero external dependencies (pure Python standard library JSON-RPC over stdio).
"""

import json
import sys
import urllib.request

BRIDGE_URL = "http://localhost:7890/event"

def post_bridge_event(event_type: str, detail: str, station: str, agent: str):
    payload = {
        "source": "mcp-agent",
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
        with urllib.request.urlopen(req, timeout=0.25) as res:
            return res.status == 200
    except Exception:
        return False

TOOLS = [
    {
        "name": "mission_control_plan",
        "description": "Report a high-level mission goal, plan, or prompt decomposition to Mission Control.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "goal": {"type": "string", "description": "The mission goal or plan summary"},
                "agent_name": {"type": "string", "description": "Your agent name (default: Zorya)", "default": "Zorya"}
            },
            "required": ["goal"]
        }
    },
    {
        "name": "mission_control_tool",
        "description": "Report an active tool call, file edit, or code generation to the Dev Lab in Mission Control.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tool_name": {"type": "string", "description": "Name of tool being run (e.g. edit_file, bash, git)"},
                "target": {"type": "string", "description": "Target file or command summary"},
                "agent_name": {"type": "string", "description": "Your agent name (default: Brix)", "default": "Brix"}
            },
            "required": ["tool_name"]
        }
    },
    {
        "name": "mission_control_test",
        "description": "Report unit test or QA validation results to the QA Chamber in Mission Control.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "test_suite": {"type": "string", "description": "Name of test suite or test command"},
                "passed": {"type": "boolean", "description": "Whether tests passed or failed", "default": True},
                "agent_name": {"type": "string", "description": "Your agent name (default: Quinn)", "default": "Quinn"}
            },
            "required": ["test_suite"]
        }
    },
    {
        "name": "mission_control_approval",
        "description": "Signal that the AI agent is waiting for user confirmation or security approval.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The question or action requiring user OK"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "mission_control_ship",
        "description": "Celebrate the completion of a milestone, PR merge, or release with Mission Control fanfare.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "release_name": {"type": "string", "description": "Milestone or release name"}
            },
            "required": ["release_name"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mission-control-mcp", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS}
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "mission_control_plan":
            post_bridge_event("plan", args.get("goal"), "strategy", args.get("agent_name", "Zorya"))
            msg = f"✓ Mission goal '{args.get('goal')}' reported to War Room."
        elif tool_name == "mission_control_tool":
            detail = f"{args.get('tool_name')}({args.get('target', '')})"
            post_bridge_event("tool", detail, "engine", args.get("agent_name", "Brix"))
            msg = f"✓ Tool call '{detail}' sent to Dev Lab."
        elif tool_name == "mission_control_test":
            detail = f"{args.get('test_suite')}: {'PASSED' if args.get('passed', True) else 'FAILED'}"
            post_bridge_event("test", detail, "qa", args.get("agent_name", "Quinn"))
            msg = f"✓ QA verification '{detail}' sent to QA Chamber."
        elif tool_name == "mission_control_approval":
            post_bridge_event("needsYou", args.get("prompt"), "ops", "Nova")
            msg = "✓ User approval alert triggered on bridge."
        elif tool_name == "mission_control_ship":
            post_bridge_event("ship", args.get("release_name"), "ops", "Nova")
            msg = f"✓ Ship celebration fired for '{args.get('release_name')}'!"
        else:
            msg = f"Unknown tool: {tool_name}"

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": msg}]
            }
        }
    return None

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line.strip())
            resp = handle_request(req)
            if resp:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception:
            pass

if __name__ == "__main__":
    main()
