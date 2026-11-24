#!/usr/bin/env python3
"""
Universal Git Hook Installer for Mission Control
Installs non-blocking post-commit and pre-push hooks into any Git repository.
Automatically triggers Mission Control telemetry whenever code is committed or pushed.
Usage:
    python adapters/git_hooks.py install [path_to_repo]
    python adapters/git_hooks.py uninstall [path_to_repo]
"""

import os
import stat
import sys

POST_COMMIT_SCRIPT = """#!/bin/sh
# Mission Control Post-Commit Hook
COMMIT_MSG=$(git log -1 --pretty=%B | head -n 1)
python3 -c "
import urllib.request, json
try:
    req = urllib.request.Request(
        'http://localhost:7890/event',
        data=json.dumps({'source': 'git-hook', 'type': 'tool', 'station': 'engine', 'agent': 'Brix', 'detail': 'git commit: $COMMIT_MSG'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    urllib.request.urlopen(req, timeout=0.2)
except Exception:
    pass
" 2>/dev/null &
"""

PRE_PUSH_SCRIPT = """#!/bin/sh
# Mission Control Pre-Push Hook (Ship release)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
python3 -c "
import urllib.request, json
try:
    req = urllib.request.Request(
        'http://localhost:7890/event',
        data=json.dumps({'source': 'git-hook', 'type': 'ship', 'station': 'ops', 'agent': 'Nova', 'detail': 'git push origin $BRANCH'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    urllib.request.urlopen(req, timeout=0.2)
except Exception:
    pass
" 2>/dev/null &
"""

def install(repo_path="."):
    git_dir = os.path.join(repo_path, ".git")
    if not os.path.isdir(git_dir):
        print(f"Error: {repo_path} is not a git repository.")
        sys.exit(1)

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    # Post-commit
    post_commit_path = os.path.join(hooks_dir, "post-commit")
    with open(post_commit_path, "w") as f:
        f.write(POST_COMMIT_SCRIPT)
    os.chmod(post_commit_path, os.stat(post_commit_path).st_mode | stat.S_IEXEC)

    # Pre-push
    pre_push_path = os.path.join(hooks_dir, "pre-push")
    with open(pre_push_path, "w") as f:
        f.write(PRE_PUSH_SCRIPT)
    os.chmod(pre_push_path, os.stat(pre_push_path).st_mode | stat.S_IEXEC)

    print(f"✓ Mission Control Git hooks successfully installed in {hooks_dir}!")
    print("  - post-commit: triggers Brix & code engine events")
    print("  - pre-push: triggers Nova & ship celebration fanfare")

def uninstall(repo_path="."):
    hooks_dir = os.path.join(repo_path, ".git", "hooks")
    for hook in ("post-commit", "pre-push"):
        p = os.path.join(hooks_dir, hook)
        if os.path.exists(p):
            os.remove(p)
            print(f"Removed {p}")
    print("✓ Hooks uninstalled.")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "install"
    path = sys.argv[2] if len(sys.argv) > 2 else "."
    if action == "install":
        install(path)
    elif action == "uninstall":
        uninstall(path)
    else:
        print("Usage: python git_hooks.py [install|uninstall] [repo_path]")
