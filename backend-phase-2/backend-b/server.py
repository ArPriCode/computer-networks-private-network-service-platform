import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone

class BackendHandler(BaseHTTPRequestHandler):

    def send_json(self, data):
        body = json.dumps(data, indent=2).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Backend", "B")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_json({
                "service": "CN Private Network Platform",
                "backend": "B",
                "status": "running"
            })

        elif self.path == "/api/status":
            self.send_json({
                "backend": "B",
                "status": "ok",
                "machine": "Mac 2",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        print("[Backend B] " + (format % args))

server = HTTPServer(("0.0.0.0", 3002), BackendHandler)

print("Backend B running on http://0.0.0.0:3002")

server.serve_forever()
