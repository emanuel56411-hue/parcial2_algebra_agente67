"""Endpoint serverless que expone el motor exacto sin depender de Streamlit."""
import json

from agent import InputError, TechChipAgent, validate_input
from api._http import JsonHandler


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


class handler(JsonHandler):
    def do_GET(self) -> None:
        self._send_json(200, {"ok": True, "service": "TechChip Matrix Studio", "format": "exact-rational-v1"})

    def do_POST(self) -> None:
        try:
            result = solve_payload(self._read_json())
        except (InputError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            self._send_json(400, {"error": str(exc) or "Solicitud no válida."})
            return
        except Exception:
            self._send_json(500, {"error": "No se pudo completar el análisis. Inténtalo de nuevo."})
            return
        self._send_json(200, result)
