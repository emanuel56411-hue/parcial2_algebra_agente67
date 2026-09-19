"""Álgebra lineal exacta y explicable, sin solucionadores de caja negra.

El núcleo solo usa la biblioteca estándar. Las matrices de cada paso son copias
independientes: consola, web e informes muestran el mismo procedimiento.
"""
from dataclasses import asdict, dataclass, field
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import re
from typing import Any

MAX_SIZE = 12
MAX_JSON_BYTES = 100_000
Matrix = list[list[Fraction]]
STATUS_LABELS = {"unique": "Solución única", "infinite": "Infinitas soluciones", "inconsistent": "Sin solución"}
METHOD_LABELS = {"gauss": "Eliminación de Gauss", "gauss_jordan": "Gauss-Jordan", "inverse": "Matriz inversa"}


class InputError(ValueError):
    """Datos que no representan un sistema admitido por la aplicación."""


def number(value: Any) -> Fraction:
    """Enteros, decimales, notación científica y fracciones, sin eval()."""
    if isinstance(value, Fraction):
        if max(value.numerator.bit_length(), value.denominator.bit_length()) > 256:
            raise InputError("El numerador o denominador supera el límite de 256 bits.")
        return value
    if isinstance(value, bool) or value is None:
        raise InputError("Usa números; no se aceptan booleanos ni celdas vacías.")
    if not isinstance(value, (str, int, float, Decimal, Fraction)):
        raise InputError("Cada celda debe contener un número o una fracción como 3/4.")
    text = str(value).strip()
    if len(text) > 64:
        raise InputError("Cada número puede ocupar como máximo 64 caracteres.")
    if any(abs(int(e)) > 50 for e in re.findall(r"[eE]([+-]?\d+)", text)):
        raise InputError("Usa exponentes científicos entre -50 y 50.")
    try:
        result = Fraction(text)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise InputError(f"Valor no válido: {text!r}. Usa 2, -1.5, 1e-3 o 3/4; no NaN/Infinity.") from exc
    if max(result.numerator.bit_length(), result.denominator.bit_length()) > 256:
        raise InputError("El numerador o denominador supera el límite de 256 bits.")
    return result


def validate_input(A: Any, B: Any) -> tuple[Matrix, list[Fraction]]:
    if not isinstance(A, (list, tuple)) or not 1 <= len(A) <= MAX_SIZE:
        raise InputError(f"A debe ser una matriz cuadrada de tamaño 1 a {MAX_SIZE}.")
    n = len(A)
    if any(not isinstance(row, (list, tuple)) or len(row) != n for row in A):
        raise InputError(f"A debe tener {n} filas y {n} columnas, sin filas incompletas.")
    if not isinstance(B, (list, tuple)) or len(B) != n:
        raise InputError(f"B debe contener exactamente {n} valores.")
    if all(isinstance(item, (list, tuple)) and len(item) == 1 for item in B):
        B = [item[0] for item in B]
    try:
        return [[number(v) for v in row] for row in A], [number(v) for v in B]
    except InputError as exc:
        raise InputError(f"Revisa las celdas de A y B. {exc}") from exc


def parse_json(text: str) -> tuple[Matrix, list[Fraction]]:
    if len(text.encode("utf-8")) > MAX_JSON_BYTES:
        raise InputError("El JSON no puede superar 100 kB.")
    try:
        data = json.loads(text, parse_float=Decimal)
    except (ValueError, RecursionError) as exc:
        raise InputError("JSON no válido. Usa un objeto con las claves A y B.") from exc
    if not isinstance(data, dict) or "A" not in data or "B" not in data:
        raise InputError('El JSON debe contener {"A": [[...], ...], "B": [...]}.')
    return validate_input(data["A"], data["B"])


def decimal_text(value: Fraction, places: int = 6) -> str:
    with localcontext() as ctx:
        ctx.prec = max(places + 8, 24)
        dec = Decimal(value.numerator) / Decimal(value.denominator)
        if dec and (abs(dec) >= Decimal("1e12") or abs(dec) < Decimal("1e-6")):
            return f"{dec:.{places}E}"
        return f"{dec:.{places}f}"


def snapshot(M: Matrix) -> Matrix:
    return [row[:] for row in M]


def matvec(A: Matrix, x: list[Fraction]) -> list[Fraction]:
    return [sum((a * v for a, v in zip(row, x)), Fraction(0)) for row in A]


def json_ready(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    return value


@dataclass
class Step:
    operation: str
    explanation: str
    matrix: Matrix
    split: int
    kind: str = "note"
    target: int | None = None
    source: int | None = None
    factor: Fraction | None = None


@dataclass
class MethodResult:
    name: str
    solution: list[Fraction]
    steps: list[Step]
    inverse: Matrix | None = None


@dataclass
class Analysis:
    A: Matrix
    B: list[Fraction]
    determinant: Fraction
    rank_A: int
    rank_augmented: int
    status: str
    diagnostic_steps: list[Step]
    methods: dict[str, MethodResult] = field(default_factory=dict)
    solution: list[Fraction] | None = None
    residual: list[Fraction] = field(default_factory=list)
    substitution: list[str] = field(default_factory=list)
    particular: list[Fraction] | None = None
    nullspace: list[list[Fraction]] = field(default_factory=list)
    free_columns: list[int] = field(default_factory=list)
    interpretation: list[str] = field(default_factory=list)
    production: bool = False

    @property
    def methods_agree(self) -> bool:
        return bool(self.methods) and all(m.solution == self.solution for m in self.methods.values())

    @property
    def max_error(self) -> Fraction | None:
        return max(self.residual) if self.residual else None

    def to_dict(self) -> dict:
        return json_ready({**asdict(self), "methods_agree": self.methods_agree,
                           "max_error": self.max_error, "format": "exact-rational-v1"})


class LinearAlgebraSolver:
    """Pivoteo parcial y aritmética racional en tres métodos explícitos."""

    @staticmethod
    def _eliminate(M: Matrix, n: int, reduced: bool) -> tuple[Matrix, list[Step], list[int], int, list[Fraction]]:
        M = snapshot(M)
        steps = [Step("Matriz inicial", "El bloque a la derecha también participa en cada operación de fila.", snapshot(M), n)]
        pivots, pivot_values = [], []
        row, swaps = 0, 0
        for col in range(n):
            if row == len(M):
                break
            p = max(range(row, len(M)), key=lambda i: abs(M[i][col]))
            if M[p][col] == 0:
                steps.append(Step(f"Columna {col + 1}: sin pivote", "Todas las entradas disponibles son cero. Se continúa en la siguiente columna.", snapshot(M), n))
                continue
            if p != row:
                M[row], M[p] = M[p], M[row]
                swaps += 1
                steps.append(Step(f"F{row + 1} ↔ F{p + 1}", f"Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna {col + 1}.", snapshot(M), n, "swap", row, p))
            pivot = M[row][col]
            pivot_values.append(pivot)
            if reduced and pivot != 1:
                factor = 1 / pivot
                M[row] = [v * factor for v in M[row]]
                steps.append(Step(f"F{row + 1} ← ({factor}) · F{row + 1}", f"Se convierte el pivote {pivot} en 1.", snapshot(M), n, "scale", row, factor=factor))
            targets = range(len(M)) if reduced else range(row + 1, len(M))
            for target in targets:
                if target == row or M[target][col] == 0:
                    continue
                factor = -M[target][col] / M[row][col]
                entry = M[target][col]
                M[target] = [a + factor * b for a, b in zip(M[target], M[row])]
                steps.append(Step(f"F{target + 1} ← F{target + 1} + ({factor}) · F{row + 1}", f"Se anula la entrada {entry} en la columna {col + 1}; se opera sobre la fila completa.", snapshot(M), n, "add", target, row, factor))
            pivots.append(col)
            row += 1
        return M, steps, pivots, swaps, pivot_values

    def analyze(self, A: Any, B: Any) -> Analysis:
        A, B = validate_input(A, B)
        n = len(A)
        augmented = [row + [b] for row, b in zip(A, B)]
        upper, diagnostic, pivots, swaps, values = self._eliminate(augmented, n, False)
        rank_A = len(pivots)
        contradictions = [i for i, row in enumerate(upper) if all(v == 0 for v in row[:n]) and row[n] != 0]
        rank_aug = rank_A + bool(contradictions)
        det = Fraction((-1) ** swaps) if rank_A == n else Fraction(0)
        if rank_A == n:
            for value in values:
                det *= value
        formula = " · ".join(f"({v})" for v in values)
        explanation = (f"{swaps} intercambio(s). Las sumas de filas conservan el determinante. "
                       f"det(A) = (-1)^{swaps} · {formula} = {det}.") if rank_A == n else "No hay n pivotes independientes; det(A) = 0. No existe A⁻¹."
        diagnostic.append(Step(f"det(A) = {det}", explanation, snapshot(upper), n))
        status = "inconsistent" if contradictions else "infinite" if rank_A < n else "unique"
        report = Analysis(A, B, det, rank_A, rank_aug, status, diagnostic)
        if status != "unique":
            if contradictions:
                for i in contradictions:
                    diagnostic.append(Step(f"Contradicción: 0 = {upper[i][n]}", f"La fila {i + 1} demuestra que rango(A) = {rank_A} < rango([A|B]) = {rank_aug}. Se detienen los métodos de solución única.", snapshot(upper), n))
            else:
                rref, reduced_steps, pivot_cols, _, _ = self._eliminate(augmented, n, True)
                diagnostic.append(Step("Diagnóstico de variables libres", "Se reduce el sistema para describir la familia de soluciones; no se intenta invertir A.", snapshot(augmented), n))
                diagnostic.extend(reduced_steps[1:])
                report.free_columns = [c for c in range(n) if c not in pivot_cols]
                report.particular = [Fraction(0) for _ in range(n)]
                for i, col in enumerate(pivot_cols):
                    report.particular[col] = rref[i][n]
                for free in report.free_columns:
                    vector = [Fraction(0) for _ in range(n)]
                    vector[free] = Fraction(1)
                    for i, col in enumerate(pivot_cols):
                        vector[col] = -rref[i][free]
                    report.nullspace.append(vector)
            return report

        # Gauss: matriz triangular y sustitución hacia atrás.
        x = [Fraction(0) for _ in range(n)]
        gauss_steps = diagnostic[:]
        gauss_steps.append(Step("Matriz triangular superior U", "Se resuelve U·X = C desde la última fila hacia la primera.", snapshot(upper), n))
        for i in reversed(range(n)):
            total = sum((upper[i][j] * x[j] for j in range(i + 1, n)), Fraction(0))
            x[i] = (upper[i][n] - total) / upper[i][i]
            expression = " + ".join(f"({upper[i][j]})·({x[j]})" for j in range(i + 1, n)) or "0"
            gauss_steps.append(Step(f"x{i + 1} = ({upper[i][n]} − ({expression})) / ({upper[i][i]}) = {x[i]}", "Sustitución hacia atrás: se usan las incógnitas ya calculadas.", snapshot(upper), n, "substitution"))
        report.methods["gauss"] = MethodResult(METHOD_LABELS["gauss"], x, gauss_steps)

        # Gauss-Jordan: reducción independiente de [A|B] a [I|X].
        rref, jordan_steps, _, _, _ = self._eliminate(augmented, n, True)
        x_jordan = [row[n] for row in rref]
        jordan_steps.append(Step("[I | X]: lectura de la solución", "Cada fila contiene una incógnita con coeficiente 1; la última columna es X.", snapshot(rref), n))
        report.methods["gauss_jordan"] = MethodResult(METHOD_LABELS["gauss_jordan"], x_jordan, jordan_steps)

        # Inversa: reducir [A|I]; B solo interviene al multiplicar A⁻¹·B.
        identity = [[Fraction(i == j) for j in range(n)] for i in range(n)]
        inverse_aug = [row + right for row, right in zip(A, identity)]
        inverse_rref, inverse_steps, _, _, _ = self._eliminate(inverse_aug, n, True)
        inverse = [row[n:] for row in inverse_rref]
        inverse_steps.append(Step("[I | A⁻¹]: inversa obtenida", "Las operaciones que convierten A en I convierten I en A⁻¹.", snapshot(inverse_rref), n))
        x_inverse = matvec(inverse, B)
        for i, value in enumerate(x_inverse):
            expr = " + ".join(f"({v})·({b})" for v, b in zip(inverse[i], B))
            inverse_steps.append(Step(f"x{i + 1} = {expr} = {value}", "Producto fila por columna en X = A⁻¹·B.", snapshot(inverse_rref), n, "multiplication"))
        report.methods["inverse"] = MethodResult(METHOD_LABELS["inverse"], x_inverse, inverse_steps, inverse)
        report.solution = x
        ax = matvec(A, x)
        report.residual = [abs(v - b) for v, b in zip(ax, B)]
        report.substitution = [
            f"Fila {i + 1}: " + " + ".join(f"({a})·({v})" for a, v in zip(row, x))
            + f" = {ax[i]}; B{i + 1} = {B[i]}; |AX − B| = {report.residual[i]}"
            for i, row in enumerate(A)
        ]
        if not report.methods_agree or any(report.residual):
            raise ArithmeticError("Los métodos o la sustitución discrepan. No se debe usar este resultado.")
        return report


class TechChipAgent:
    """Agente determinista: valida → diagnostica → resuelve → verifica → explica."""

    def __init__(self):
        self.solver = LinearAlgebraSolver()

    def analyze(self, A: Any, B: Any, *, production: bool = False) -> Analysis:
        A, B = validate_input(A, B)
        if production and (any(value < 0 for row in A for value in row) or any(value < 0 for value in B)):
            raise InputError("En modo producción, los consumos A y las disponibilidades B deben ser no negativos. Usa el modo matemático para coeficientes negativos.")
        report = self.solver.analyze(A, B)
        report.production = production
        if report.status == "inconsistent":
            report.interpretation = ["Las restricciones se contradicen: no existe un vector X que cumpla todas las igualdades.", "Revisa las ecuaciones dependientes y sus disponibilidades antes de proponer un plan."]
        elif report.status == "infinite":
            report.interpretation = [f"Hay {len(report.free_columns)} variable(s) libre(s): los datos no determinan una solución única.", "La familia X = Xₚ + t₁v₁ + … describe todas las soluciones reales; hacen falta restricciones independientes para reducir la ambigüedad."]
            if production:
                report.interpretation.append("La viabilidad de esta familia bajo X ≥ 0 requiere un análisis adicional; no se declara un plan de producción viable.")
        else:
            negatives = [f"x{i + 1} = {value} (≈ {decimal_text(value)})" for i, value in enumerate(report.solution) if value < 0]
            if production and negatives:
                report.interpretation = ["Plan de producción inalcanzable por restricción de materias primas.", "La solución de AX = B exige cantidades negativas: " + "; ".join(negatives) + ".", "No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa."]
            elif production:
                report.interpretation = ["Plan factible para el modelo continuo: todas las cantidades son no negativas y AX = B consume el 100 % de cada disponibilidad.", "X se expresa en miles de unidades; X·1000 se informa como cantidad continua, sin redondear a unidades enteras."]
            else:
                report.interpretation = ["El sistema tiene una única solución y los tres métodos coinciden exactamente.", "Los valores negativos son soluciones matemáticas válidas; su interpretación depende del contexto del problema."]
            report.interpretation.append("La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.")
        return report
