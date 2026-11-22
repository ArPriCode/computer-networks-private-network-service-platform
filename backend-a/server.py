import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "3001"))
BACKEND = os.environ.get("BACKEND", "A")


class BackendHandler(BaseHTTPRequestHandler):
    def response_data(self):
        if self.path == "/api/status":
            return {"backend": BACKEND, "status": "ok", "server": f"Backend {BACKEND}"}
        if self.path == "/":
            return {"backend": BACKEND, "message": f"Hello from Backend {BACKEND}"}
        return {"backend": BACKEND, "status": "not_found"}

    def send_response_data(self):
        data = json.dumps(self.response_data(), separators=(",", ":")).encode("utf-8")
        known_endpoint = self.path in ("/", "/api/status")
        status = 200 if known_endpoint else 404
        quoted_etag = f'"{hashlib.md5(data).hexdigest()}"'

        if known_endpoint and self.headers.get("If-None-Match") == quoted_etag:
            self.send_response(304)
        else:
            self.send_response(status)
            if known_endpoint:
                self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=60")
        self.send_header("ETag", quoted_etag)
        self.send_header("X-Backend", BACKEND)
        self.end_headers()
        return b"" if known_endpoint and self.headers.get("If-None-Match") == quoted_etag else data

    def do_GET(self):
        self.wfile.write(self.send_response_data())

    def do_HEAD(self):
        self.send_response_data()

    def log_message(self, format, *args):
        print(f"[Backend {BACKEND}] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), BackendHandler)
    print(f"Backend {BACKEND} running on http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\nBackend {BACKEND} stopped.")
    finally:
        server.server_close()
