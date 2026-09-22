"""Conversión segura de ejercicios lineales escritos a matrices A y B.

No usa eval ni delega los números al modelo generativo. Solo admite sumas y
restas de términos lineales con coeficientes racionales o decimales.
"""
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import json
import re

from agent import InputError, json_ready, number, validate_input

_SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉−", "0123456789-")
_NUMBER = r"(?:(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?|\d+/\d+)"
_VARIABLE = r"(?:x[1-6]|[xyzwuv])"
_TERM = re.compile(rf"(?:(?P<coefficient>{_NUMBER})\*?)?(?P<variable>{_VARIABLE})$", re.I)
_CONSTANT = re.compile(rf"{_NUMBER}$")
_ALLOWED = re.compile(r"^[0-9A-Za-z_./*+\-]+$")
_SYMBOL_ORDER = {name: index for index, name in enumerate(("x", "y", "z", "w", "u", "v"))}


@dataclass(frozen=True)
class ParsedExercise:
    A: list[list[Fraction]]
    B: list[Fraction]
    variables: list[str]
    source: str

    def to_input(self, production: bool = False) -> dict:
        return {"A": json_ready(self.A), "B": json_ready(self.B), "production": production}


def _normalize(text: str) -> str:
    return (text.translate(_SUBSCRIPTS).replace("−", "-").replace("–", "-")
            .replace("＋", "+").replace("＝", "=").replace("·", "*").replace("×", "*"))


def _json_candidate(prompt: str):
    candidates = [prompt.strip()]
    if "{" in prompt and "}" in prompt:
        candidates.append(prompt[prompt.find("{"):prompt.rfind("}") + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate, parse_float=Decimal)
        except (ValueError, RecursionError):
            continue
        if isinstance(value, dict) and "A" in value and "B" in value:
            A, B = validate_input(value["A"], value["B"])
            return ParsedExercise(A, B, [f"x{i + 1}" for i in range(len(A))], "json")
    return None


def _matrix_notation(prompt: str):
    """Acepta A=[[...]], B=[...] aunque el resto del prompt sea texto."""
    decoder = json.JSONDecoder(parse_float=Decimal)
    match_a = re.search(r"\bA\s*=\s*", prompt, re.I)
    if not match_a:
        return None
    try:
        A, end_a = decoder.raw_decode(prompt, match_a.end())
    except (ValueError, RecursionError):
        return None
    match_b = re.search(r"\bB\s*=\s*", prompt[end_a:], re.I)
    if not match_b:
        return None
    start_b = end_a + match_b.end()
    try:
        B, _ = decoder.raw_decode(prompt, start_b)
    except (ValueError, RecursionError):
        return None
    A, B = validate_input(A, B)
    return ParsedExercise(A, B, [f"x{i + 1}" for i in range(len(A))], "matrix_notation")


def _expression(text: str) -> tuple[dict[str, Fraction], Fraction]:
    expression = re.sub(r"\s+", "", text).lower()
    if not expression or not _ALLOWED.fullmatch(expression):
        raise InputError("Cada lado debe contener solo términos lineales, por ejemplo 2x - 3y + 4.")
    pieces = re.split(r"(?<![eE])(?=[+-])", expression)
    if not pieces or any(not piece for piece in pieces) or "".join(pieces) != expression:
        raise InputError("Revisa los signos de la ecuación.")
    coefficients: dict[str, Fraction] = {}
    constant = Fraction(0)
    for piece in pieces:
        sign = Fraction(-1 if piece.startswith("-") else 1)
        body = piece[1:] if piece[:1] in "+-" else piece
        term = _TERM.fullmatch(body)
        if term:
            variable = term.group("variable").lower()
            coefficient = number(term.group("coefficient") or "1") * sign
            coefficients[variable] = coefficients.get(variable, Fraction(0)) + coefficient
        elif _CONSTANT.fullmatch(body):
            constant += number(body) * sign
        else:
            raise InputError(f"Término no lineal o no reconocido: {piece!r}. Usa x, y, z o x1…x6.")
    return coefficients, constant


def _equation_segments(prompt: str) -> list[str]:
    segments = []
    for raw in re.split(r"[;\n]+", prompt):
        if "=" not in raw:
            continue
        segment = raw.strip()
        if ":" in segment:
            segment = segment.rsplit(":", 1)[1].strip()
        else:
            # Permite un encabezado conversacional sin volver ambiguo el
            # lenguaje matemático que realmente se interpreta.
            segment = re.sub(
                r"^(?:(?:por\s+favor\s+)?(?:resuelve|resolver|calcula|calcular|soluciona|solucionar)"
                r"(?:\s+(?:este|el|un))?\s+(?:sistema\s+)?(?:por\s+(?:gauss(?:-jordan)?|matriz\s+inversa)\s*)?)",
                "",
                segment,
                flags=re.I,
            ).strip()
        segment = re.sub(r"^\s*\d+\s*[).:-]\s*", "", segment)
        if segment.count("=") != 1:
            raise InputError("Cada ecuación debe contener un solo signo igual.")
        segments.append(segment)
    return segments


def parse_exercise(prompt: str) -> ParsedExercise:
    if not isinstance(prompt, str) or not prompt.strip():
        raise InputError("Escribe o adjunta un ejercicio antes de resolverlo.")
    if len(prompt.encode("utf-8")) > 100_000:
        raise InputError("El ejercicio no puede superar 100 kB.")
    normalized = _normalize(prompt)
    structured = _json_candidate(normalized) or _matrix_notation(normalized)
    if structured:
        return structured

    equations = _equation_segments(normalized)
    if not equations:
        raise InputError("No encontré ecuaciones. Sepáralas con punto y coma o una ecuación por línea; ejemplo: 2x + y = 5; x - y = 1.")
    parsed_rows = []
    names: set[str] = set()
    for equation in equations:
        left, right = equation.split("=", 1)
        left_coefficients, left_constant = _expression(left)
        right_coefficients, right_constant = _expression(right)
        coefficients = dict(left_coefficients)
        for variable, value in right_coefficients.items():
            coefficients[variable] = coefficients.get(variable, Fraction(0)) - value
        names.update(variable for variable, value in coefficients.items() if value)
        parsed_rows.append((coefficients, right_constant - left_constant))

    indexed = all(re.fullmatch(r"x[1-6]", name) for name in names)
    symbolic = all(name in _SYMBOL_ORDER for name in names)
    if not names or not (indexed or symbolic):
        raise InputError("Usa variables x, y, z, w, u, v o bien x1…x6, sin mezclarlas.")
    if indexed:
        variables = sorted(names, key=lambda value: int(value[1:]))
        expected = [f"x{i + 1}" for i in range(len(variables))]
        if variables != expected:
            raise InputError("Las variables numeradas deben ser consecutivas desde x1.")
    else:
        variables = sorted(names, key=_SYMBOL_ORDER.get)
    if not 2 <= len(variables) <= 6:
        raise InputError("El prompt debe describir un sistema de 2 a 6 variables.")
    if len(equations) != len(variables):
        raise InputError(f"Encontré {len(equations)} ecuaciones y {len(variables)} variables; el sistema debe ser cuadrado.")
    A = [[coefficients.get(variable, Fraction(0)) for variable in variables] for coefficients, _ in parsed_rows]
    B = [right for _, right in parsed_rows]
    A, B = validate_input(A, B)
    return ParsedExercise(A, B, variables, "equations")
