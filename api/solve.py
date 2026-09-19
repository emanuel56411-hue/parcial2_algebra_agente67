"""Endpoint serverless que expone el motor exacto sin depender de Streamlit."""
from decimal import Decimal
from http.server import BaseHTTPRequestHandler
import json
from pathlib import Path
from urllib.parse import urlsplit

from agent import InputError, TechChipAgent, validate_input
from ai_tutor import TutorError
from api.tutor import ask_tutor_serverless

MAX_REQUEST_BYTES = 100_000
ROOT = Path(__file__).resolve().parents[1]
STATIC_FILES = {
    "/": (ROOT / "web/index.html", "text/html; charset=utf-8"),
    "/web/index.html": (ROOT / "web/index.html", "text/html; charset=utf-8"),
    "/web/styles.css": (ROOT / "web/styles.css", "text/css; charset=utf-8"),
    "/web/app.js": (ROOT / "web/app.js", "text/javascript; charset=utf-8"),
    "/assets/logo.svg": (ROOT / "assets/logo.svg", "image/svg+xml"),
}


def solve_payload(payload: object) -> dict:
    """Valida un cuerpo JSON y devuelve un análisis serializable."""
    if not isinstance(payload, dict):
        raise InputError("Envía un objeto JSON con las claves A y B.")
    if "A" not in payload or "B" not in payload:
        raise InputError('El JSON debe contener {"A": [[...], ...], "B": [...]}.')
    production = payload.get("production", False)
    if not isinstance(production, bool):
        raise InputError("production debe ser verdadero o falso.")
    A, B = validate_input(payload["A"], payload["B"])
    return TechChipAgent().analyze(A, B, production=production).to_dict()


def analyze_payload(payload: object):
    """Reconstruye un Analysis confiable para el tutor desde A y B."""
    if not isinstance(payload, dict) or "A" not in payload or "B" not in payload:
        raise InputError('El tutor requiere {"A": [[...]], "B": [...]} del cálculo actual.')
    production = payload.get("production", False)
    if not isinstance(production, bool):
        raise InputError("production debe ser verdadero o falso.")
    A, B = validate_input(payload["A"], payload["B"])
    return TechChipAgent().analyze(A, B, production=production)


class handler(BaseHTTPRequestHandler):
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

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/solve":
            self._send_json(200, {"ok": True, "service": "TechChip Matrix Studio", "format": "exact-rational-v1"})
            return
        static = STATIC_FILES.get(path)
        if static is None:
            self._send_json(404, {"error": "Ruta no encontrada."})
            return
        file_path, content_type = static
        try:
            body = file_path.read_bytes()
        except OSError:
            self._send_json(500, {"error": "No se pudo cargar la interfaz."})
            return
        cache = "public, max-age=31536000, immutable" if path.endswith((".css", ".js", ".svg")) else "public, max-age=0, must-revalidate"
        self._send_bytes(200, body, content_type, cache)

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path not in ("/api/solve", "/api/tutor"):
            self._send_json(404, {"error": "Ruta no encontrada."})
            return
        try:
            raw_length = self.headers.get("Content-Length", "")
            length = int(raw_length)
            if length <= 0 or length > MAX_REQUEST_BYTES:
                raise InputError("La solicitud debe contener JSON y no superar 100 kB.")
            raw = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw, parse_float=Decimal)
            if path == "/api/solve":
                result = solve_payload(payload)
            else:
                report = analyze_payload(payload)
                forwarded = self.headers.get("X-Forwarded-For", "")
                client_id = forwarded.split(",", 1)[0].strip() or self.client_address[0]
                result = ask_tutor_serverless(report, payload, client_id)
        except (InputError, TutorError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            self._send_json(400, {"error": str(exc) or "Solicitud no válida."})
            return
        except Exception:
            self._send_json(500, {"error": "No se pudo completar el análisis. Inténtalo de nuevo."})
            return
        self._send_json(200, result)

    def log_message(self, _format: str, *_args) -> None:
        """Evita incluir cuerpos o datos matemáticos en los logs de plataforma."""
        return
