#!/usr/bin/env python3
"""
Universal Agent Framework Callbacks for Mission Control
Drop-in observers for LangChain, CrewAI, AutoGen, and custom Python LLM pipelines.
Directly visualizes multi-agent swarms, tool dispatches, and chain execution.
"""

import functools
import json
import time
import urllib.request

BRIDGE_URL = "http://localhost:7890/event"

def emit(event_type: str, detail: str, station: str, agent: str):
    try:
        req = urllib.request.Request(
            BRIDGE_URL,
            data=json.dumps({
                "source": "agent-framework",
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

# 1. Universal Decorator for Python functions & Tool calls
def track_tool(tool_name: str = None, agent: str = "Brix"):
    def decorator(func):
        name = tool_name or func.__name__
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            emit("tool", f"{name}() started", "engine", agent)
            start_t = time.time()
            try:
                res = func(*args, **kwargs)
                dur = round((time.time() - start_t) * 1000)
                emit("tool", f"✓ {name}() ({dur}ms)", "engine", agent)
                return res
            except Exception as e:
                emit("needsYou", f"⚠ {name}() error: {str(e)[:40]}", "ops", agent)
                raise
        return wrapper
    return decorator

# 2. LangChain / LangGraph Callback Handler
class MissionControlLangChainHandler:
    """Drop-in BaseCallbackHandler for LangChain / LangGraph chains."""
    def on_chain_start(self, serialized, inputs, **kwargs):
        name = (serialized or {}).get("name", "Chain")
        emit("plan", f"Starting chain: {name}", "strategy", "Zorya")

    def on_tool_start(self, serialized, input_str, **kwargs):
        name = (serialized or {}).get("name", "Tool")
        emit("tool", f"Executing {name}", "engine", "Brix")

    def on_tool_end(self, output, **kwargs):
        emit("tool", "Tool finished", "engine", "Brix")

    def on_chain_end(self, outputs, **kwargs):
        emit("ship", "Chain completed", "ops", "Nova")

# 3. CrewAI Task / Agent Observer
class MissionControlCrewObserver:
    """Observer for CrewAI task delegation and role execution."""
    @staticmethod
    def on_task_start(agent_role: str, task_description: str):
        emit("plan", f"[{agent_role}] {task_description[:50]}", "strategy", agent_role)

    @staticmethod
    def on_tool_use(agent_role: str, tool_name: str):
        emit("tool", f"[{agent_role}] {tool_name}", "engine", agent_role)

    @staticmethod
    def on_crew_complete(summary: str = "Mission Accomplished"):
        emit("ship", summary, "ops", "Nova")

if __name__ == "__main__":
    print("Testing universal agent tracking...")
    @track_tool(tool_name="synthesize_data", agent="Brix")
    def sample_task():
        time.sleep(0.1)
        return "data ready"

    sample_task()
    print("✓ Tool tracked and broadcast to Mission Control.")
