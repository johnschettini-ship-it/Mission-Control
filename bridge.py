#!/usr/bin/env python3
"""
Mission Control - Ultra-Lightweight Live Event Bridge
Zero-dependency HTTP + Server-Sent Events (SSE) server for Claude Code and Antigravity.
Runs on Python standard library only (no pip dependencies required).
"""

import http.server
import json
import os
import sys
import threading
import time

PORT = 7890
CLIENTS = set()
CLIENTS_LOCK = threading.Lock()

class EventBridgeHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            queue = []
            with CLIENTS_LOCK:
                CLIENTS.add(self.wfile)

            try:
                # Send initial handshake ping
                self.wfile.write(b'event: connected\ndata: {"status": "ok", "bridge": "Mission-Control"}\n\n')
                self.wfile.flush()
                while True:
                    time.sleep(1)
            except Exception:
                pass
            finally:
                with CLIENTS_LOCK:
                    CLIENTS.discard(self.wfile)
            return

        # Serve index.html as root
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/event':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else b'{}'
            try:
                data = json.loads(body.decode('utf-8'))
            except Exception:
                data = {}

            # Broadcast event to all connected browsers (SSE)
            payload = f"data: {json.dumps(data)}\n\n".encode('utf-8')
            with CLIENTS_LOCK:
                dead_clients = []
                for client in CLIENTS:
                    try:
                        client.write(payload)
                        client.flush()
                    except Exception:
                        dead_clients.append(client)
                for dc in dead_clients:
                    CLIENTS.discard(dc)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'received': True, 'broadcast': len(CLIENTS)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    server = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), EventBridgeHandler)
    print("=" * 60)
    print(f"🚀 Mission Control Bridge running at http://localhost:{PORT}")
    print(f"   - Web UI: http://localhost:{PORT}")
    print(f"   - Event endpoint: POST http://localhost:{PORT}/event")
    print(f"   - SSE Stream: GET http://localhost:{PORT}/events")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping bridge server.")
        server.server_close()

if __name__ == '__main__':
    main()
