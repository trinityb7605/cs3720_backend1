import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

PRODUCTS_FILE = Path(__file__).with_name("products.json")
ORDERS_FILE = Path(__file__).with_name("orders.json")


class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        path = urlparse(self.path).path

        # PRODUCTS endpoint
        if path == "/products":
            with PRODUCTS_FILE.open(encoding="utf-8") as file:
                data = json.load(file)

        # ORDERS endpoint
        elif path == "/orders":
            with ORDERS_FILE.open(encoding="utf-8") as file:
                data = json.load(file)

        # Endpoint does not exist
        else:
            self.send_error(404, "Endpoint not found")
            return

        body = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", "8000"))

    server = ThreadingHTTPServer(
        ("0.0.0.0", port),
        StoreHandler
    )

    print(f"Server listening on port {port}", flush=True)

    server.serve_forever()