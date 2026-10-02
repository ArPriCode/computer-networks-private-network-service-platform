from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import hashlib

HOST = "0.0.0.0"
PORT = 3002

class BackendHandler(BaseHTTPRequestHandler):

    def response_data(self):
        if self.path == "/api/status":
            return {
                "backend": "B",
                "status": "ok",
                "port": PORT
            }

        if self.path == "/":
            return {
                "backend": "B",
                "status": "ok",
                "message": "Backend B is running",
                "port": PORT
            }

        return {
            "backend": "B",
            "status": "not_found"
        }

    def send_response_data(self):
        data = json.dumps(self.response_data()).encode("utf-8")
        etag = hashlib.md5(data).hexdigest()

        self.send_response(200 if self.path in ["/", "/api/status"] else 404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=60")
        self.send_header("ETag", etag)
        self.send_header("X-Backend", "B")
        self.end_headers()

        return data

    def do_GET(self):
        data = self.send_response_data()
        if self.path in ["/", "/api/status"]:
            self.wfile.write(data)

    def do_HEAD(self):
        self.send_response_data()

    def log_message(self, format, *args):
        print(f"[Backend B] {self.address_string()} - {format % args}")

server = ThreadingHTTPServer((HOST, PORT), BackendHandler)

print("=" * 50)
print("Backend B started")
print(f"Listening on: {HOST}:{PORT}")
print(f"LAN URL: http://10.7.0.248:{PORT}")
print("=" * 50)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nBackend B stopped.")
finally:
    server.server_close()
