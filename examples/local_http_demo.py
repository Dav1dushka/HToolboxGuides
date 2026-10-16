#!/usr/bin/env python3
"""Safe HTTP demo: start a local-only server and request it.

This example binds exclusively to 127.0.0.1 and sends only a GET request
to that same loopback address. It does not contact external systems.
Requires Python 3.9+; uses only the standard library.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.error import URLError
from urllib.request import urlopen


HOST = "127.0.0.1"
PORT = 8765


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 — method name required by stdlib
        body = b'{"message":"Hello from the local test server","ok":true}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        # Keep the output readable for beginners.
        print(f"[local-server] {format % args}")


def main() -> int:
    server = HTTPServer((HOST, PORT), DemoHandler)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    url = f"http://{HOST}:{PORT}/demo"

    try:
        print(f"Sending a test GET request to {url}")
        with urlopen(url, timeout=3) as response:
            payload = response.read().decode("utf-8")
            print(f"Status: {response.status} {response.reason}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Body: {payload.strip()}")
        return 0
    except (TimeoutError, URLError) as exc:
        print(f"Local demo request failed: {exc}")
        return 1
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=1)


if __name__ == "__main__":
    raise SystemExit(main())
