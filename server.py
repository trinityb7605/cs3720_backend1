import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

DATA_FILE = Path(__file__).with_name("products.json")


class ProductHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path != "/products":
            self.send_error(404, "Endpoint not found")
            return

        with DATA_FILE.open(encoding="utf-8") as file:
            products = json.load(file)

        body = json.dumps(products).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("PRODUCTS VERSION - OCT 5", flush=True)
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), ProductHandler)

    print(f"Server listening on port {port}", flush=True)
    server.serve_forever()