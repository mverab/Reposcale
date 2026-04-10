"""Backend server — raw HTTP handler, no framework."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from db import query, execute


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/items":
            rows = query("SELECT id, name, price FROM items")
            self.send_json(200, rows)
        elif self.path == "/api/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if self.path == "/api/items":
            execute(
                "INSERT INTO items (name, price) VALUES (%s, %s)",
                (body["name"], body["price"]),
            )
            self.send_json(201, {"created": True})
        else:
            self.send_json(404, {"error": "not found"})

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), APIHandler)
    print("Server running on :8000")
    server.serve_forever()
