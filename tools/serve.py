#!/usr/bin/env python3
"""
Rosette App Store Local Development Server

Serves the compiled catalog and static assets over HTTP.
"""

import os
import sys
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler


class AppStoreHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()


def main():
    parser = argparse.ArgumentParser(description="Rosette App Store Local Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface (default 0.0.0.0)")
    parser.add_argument("--dir", default=None, help="Directory to serve (default dist/)")
    args = parser.parse_args()

    serve_dir = args.dir or os.path.join(os.path.dirname(__file__), "..", "dist")
    serve_dir = os.path.abspath(serve_dir)

    if not os.path.isdir(serve_dir):
        print(f"Directory {serve_dir} does not exist. Run tools/build_catalog.py first.", file=sys.stderr)
        sys.exit(1)

    os.chdir(serve_dir)
    server_address = (args.host, args.port)
    httpd = HTTPServer(server_address, AppStoreHandler)
    print(f"Rosette App Store Server listening at http://{args.host}:{args.port}")
    print(f"Serving directory: {serve_dir}")
    print(f"Catalog URL: http://{args.host}:{args.port}/apps.json")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")


if __name__ == "__main__":
    main()
