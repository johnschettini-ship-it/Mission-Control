# Mission Control 🚀

> **Next-Gen Autonomous Agent Command Bridge**
> A silky-smooth 60 FPS real-time visual operations deck for coding agents, multi-agent swarms, and autonomous workflows.

Created by **John Schettini** ([@johnschettini-ship-it](https://github.com/johnschettini-ship-it)).

---

## 🌟 Overview

**Mission Control** is the high-performance successor to *Board-Room / Digital Workplace*. It transforms abstract AI agent events (prompts, decomposition, parallel tool bursts, tests, permission prompts, and ships) into a rich, panoramic, real-time command deck.

Unlike classic terminal-hook or software-rasterized mods, Mission Control runs directly on a hardware-accelerated **HTML5 Canvas & WebGL** engine with sub-pixel animation, zero camera cuts, and built-in procedural Web Audio chiptune telemetry.

---

## ⚡ Key Improvements Over Board-Room

| Feature | Classic Board-Room | Next-Gen Mission Control |
| :--- | :--- | :--- |
| **Render Engine** | Headless software rasterizer + SVG/PNG delta frames | **Native 60 FPS Canvas/WebGL** with `requestAnimationFrame` |
| **Camera System** | Jerky "door-pop" cuts between walled rooms | **Unified Panoramic Bridge** with zero camera hops |
| **Tool Coordination** | Characters physically walking & bumping into desks | **Quantum Data Conduit** with instant high-speed data pulses |
| **Audio** | External OS audio player required | **Pure Web Audio API** procedural chiptune synth |
| **Telemetry & HUD** | Static text lines | **Interactive Click-to-Inspect Glass HUD** for all stations |
| **Platform** | Tied to terminal hook panes | **Zero Dependencies** — runs in any browser, Codespaces, or GitHub Pages |

---

## 🛰️ The Command Deck Stations

1. **War Room / Strategy**: Mission planning, task decomposition, and prompt orchestration (Specialist: **Zorya**).
2. **Dev Lab / Core Engine**: Rapid code generation, file edits, and tool burst execution (Specialist: **Brix**).
3. **Diagnostic & QA Chamber**: Automated test suites, diff inspections, and eval verification (Specialist: **Quinn**).
4. **Launch Ops & Ship Bay**: Deployments, security approvals, and celebration releases (Specialist: **Nova**).

---

## 🔌 Universal Bridge Suite (Connect Any Agent)

Mission Control includes a universal adapter suite that connects to **any** AI agent, terminal workflow, or framework with zero latency:

```
Mission-Control/
├── index.html                   # 60 FPS Canvas UI (auto-connects to SSE stream)
├── bridge.py                    # Zero-dependency local event bridge (HTTP + SSE)
└── adapters/
    ├── universal_mcp.py         # MCP Server for Cursor, Antigravity, Claude, Zed, Windsurf
    ├── claude_hook.py           # Featherweight hook for Claude Code (< 2ms execution)
    ├── antigravity_bridge.py    # Native event emitter for Antigravity & Swarms
    ├── cli_wrapper.py           # Universal CLI runner for any terminal command
    ├── git_hooks.py             # Auto post-commit & pre-push git hooks
    └── agent_frameworks.py      # Callbacks for LangChain, CrewAI, AutoGen, OpenAI
```

### 1. Model Context Protocol (MCP) — For Cursor, Antigravity, Claude Desktop, Zed
Add to your agent's MCP config:
```json
{
  "mcpServers": {
    "mission-control": {
      "command": "python",
      "args": ["path/to/adapters/universal_mcp.py"]
    }
  }
}
```

### 2. Claude Code (< 2ms Featherweight Hook)
Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [{ "hooks": [{ "type": "command", "command": "python adapters/claude_hook.py tool" }] }],
    "Stop": [{ "hooks": [{ "type": "command", "command": "python adapters/claude_hook.py ship" }] }]
  }
}
```

### 3. Google Antigravity & Swarms
```python
from adapters.antigravity_bridge import emit

emit("tool", detail="edit_file('auth.ts')", station="engine", agent="Brix")
```

### 4. Universal CLI Wrapper (`mc-run`)
Wrap ANY command to auto-detect tests, builds, and commits:
```bash
python adapters/cli_wrapper.py pytest tests/
python adapters/cli_wrapper.py git commit -m "feat: user login"
```

### 5. Git Hooks (Automatic Commit & Push Telemetry)
```bash
python adapters/git_hooks.py install
```
Every `git commit` triggers Brix, and every `git push` triggers the Nova release fanfare!

### 6. One-Line cURL (Bash, CI/CD, GitHub Actions)
```bash
curl -X POST http://localhost:7890/event \
  -H "Content-Type: application/json" \
  -d '{"type":"tool","station":"engine","agent":"Brix","detail":"CI build passed"}'
```

---

## 🚀 Live Web Demo

Play with the live web deployment directly in your browser:
👉 **[https://johnschettini-ship-it.github.io/Mission-Control/](https://johnschettini-ship-it.github.io/Mission-Control/)**

---

## 💻 Running the Live Bridge

1. Start the event bridge server:
   ```bash
   python bridge.py
   ```
2. Open `http://localhost:7890` in your browser.
3. The bridge status turns green: **`LIVE AGENT LINKED`**.

---

## 📜 License

MIT © 2026 John Schettini.
