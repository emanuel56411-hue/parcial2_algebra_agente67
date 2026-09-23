"""Endpoint serverless que expone el motor exacto sin depender de Streamlit."""
import json
import mimetypes
from pathlib import Path
from urllib.parse import urlsplit

from agent import InputError, TechChipAgent, validate_input
from ai_tutor import TutorError
from api._http import JsonHandler
from api.tutor import ask_tutor_serverless
from exercise_interpreter import interpret_exercise

STATIC_ROOT = Path(__file__).resolve().parents[1] / "web" / "dist"


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


def solve_exercise_payload(payload: object) -> dict:
    """Convierte un prompt lineal seguro a A/B y lo resuelve con el motor exacto."""
    if not isinstance(payload, dict) or not isinstance(payload.get("exercise"), str):
        raise InputError("Envía el ejercicio escrito en el campo exercise.")
    production = payload.get("production", False)
    if not isinstance(production, bool):
        raise InputError("production debe ser verdadero o falso.")
    parsed = interpret_exercise(payload["exercise"])
    report = TechChipAgent().analyze(parsed.A, parsed.B, production=production)
    return {
        "input": parsed.to_input(production),
        "analysis": report.to_dict(),
        "variables": parsed.variables,
        "source": parsed.source,
        "preferred_method": parsed.preferred_method,
        "evidence": parsed.evidence,
    }


class handler(JsonHandler):
    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/solve":
            self._send_json(200, {"ok": True, "service": "TechChip Matrix Studio", "format": "exact-rational-v1"})
            return
        relative = "index.html" if path in ("/", "/index.html") else path.lstrip("/")
        target = (STATIC_ROOT / relative).resolve()
        if STATIC_ROOT.resolve() not in target.parents or not target.is_file():
            self._send_json(404, {"error": "Ruta no encontrada."})
            return
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        cache = "public, max-age=31536000, immutable" if relative.startswith("assets/") else "public, max-age=0, must-revalidate"
        self._send_bytes(200, target.read_bytes(), content_type, cache)

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path not in ("/api/solve", "/api/tutor", "/api/exercise"):
            self._send_json(404, {"error": "Ruta no encontrada."})
            return
        try:
            payload = self._read_json()
            if path == "/api/solve":
                result = solve_payload(payload)
            elif path == "/api/exercise":
                result = solve_exercise_payload(payload)
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
