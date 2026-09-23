"""Utilidades HTTP compartidas por las funciones serverless de Vercel."""
from decimal import Decimal
from http.server import BaseHTTPRequestHandler
import json

from agent import InputError

# No se impone un límite de palabras. Este techo técnico evita leer cuerpos
# HTTP ilimitados y queda por debajo del límite de la plataforma serverless.
MAX_REQUEST_BYTES = 2_000_000


class JsonHandler(BaseHTTPRequestHandler):
    def _send_bytes(self, status: int, body: bytes, content_type: str, cache: str = "no-store") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, value: dict) -> None:
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _read_json(self):
        raw_length = self.headers.get("Content-Length", "")
        length = int(raw_length)
        if length <= 0 or length > MAX_REQUEST_BYTES:
            raise InputError("La solicitud debe contener JSON y no superar el límite técnico de 2 MB.")
        return json.loads(self.rfile.read(length).decode("utf-8"), parse_float=Decimal)

    def log_message(self, _format: str, *_args) -> None:
        """Evita incluir cuerpos o datos matemáticos en los logs de plataforma."""
        return
