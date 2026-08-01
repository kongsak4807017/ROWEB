#!/usr/bin/env python3
"""Serve Player-visible Content Studio with safe local preview/reveal endpoints."""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import subprocess
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


class StudioHandler(SimpleHTTPRequestHandler):
    asset_root: Path

    def _resolve_allowed(self, raw: str) -> Path | None:
        try:
            path = Path(unquote(raw)).resolve()
            path.relative_to(self.asset_root)
            return path if path.is_file() else None
        except (ValueError, OSError):
            return None

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/asset":
            raw = parse_qs(parsed.query).get("path", [""])[0]
            path = self._resolve_allowed(raw)
            if not path:
                self.send_error(HTTPStatus.NOT_FOUND, "Asset not found or outside asset root")
                return
            content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(path.stat().st_size))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            with path.open("rb") as handle:
                self.copyfile(handle, self.wfile)
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid-json"})
            return
        path = self._resolve_allowed(str(payload.get("path", "")))
        if not path:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid-path"})
            return
        if parsed.path == "/api/reveal":
            if os.name != "nt":
                self._json(HTTPStatus.NOT_IMPLEMENTED, {"ok": False, "error": "windows-only"})
                return
            subprocess.Popen(["explorer.exe", "/select,", str(path)])
            self._json(HTTPStatus.OK, {"ok": True})
            return
        if parsed.path == "/api/open":
            if os.name != "nt":
                self._json(HTTPStatus.NOT_IMPLEMENTED, {"ok": False, "error": "windows-only"})
                return
            os.startfile(path)  # type: ignore[attr-defined]
            self._json(HTTPStatus.OK, {"ok": True})
            return
        self.send_error(HTTPStatus.NOT_FOUND)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    directory = args.directory.resolve()
    asset_root = args.assets.resolve()
    if not directory.is_dir() or not asset_root.is_dir():
        raise SystemExit("Studio directory or asset root does not exist")
    os.chdir(directory)
    StudioHandler.asset_root = asset_root
    server = ThreadingHTTPServer(("127.0.0.1", args.port), StudioHandler)
    print(f"Player-visible Content Studio: http://127.0.0.1:{args.port}/player-visible-content-studio.html")
    print(f"Allowed asset root: {asset_root}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
