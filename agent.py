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
    # Campos de presentación estructurados. Los campos anteriores se conservan
    # para que consola, informes y clientes antiguos sigan siendo compatibles.
    title: str | None = None
    what: str | None = None
    why: str | None = None
    calc: list[str] = field(default_factory=list)
    pivot: tuple[int, int] | None = None
    changed_rows: list[int] = field(default_factory=list)
    decimals: dict[str, str] = field(default_factory=dict)


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
        right_name = "B" if len(M[0]) == n + 1 else "I"
        steps = [Step(
            "Matriz aumentada inicial",
            f"Punto de partida: [A | {right_name}]. La barra separa los coeficientes del bloque derecho, "
            "pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.",
            snapshot(M), n,
            title=f"Formar [A | {right_name}]",
            what=f"Se construyó la matriz aumentada con el bloque {right_name} a la derecha.",
            why="Las operaciones elementales sobre filas conservan un sistema equivalente.",
            calc=[f"[A | {right_name}]"],
        )]
        pivots, pivot_values = [], []
        row, swaps = 0, 0
        for col in range(n):
            if row == len(M):
                break
            p = max(range(row, len(M)), key=lambda i: abs(M[i][col]))
            if M[p][col] == 0:
                steps.append(Step(
                    f"Columna {col + 1}: sin pivote",
                    "Desde la fila activa hacia abajo todas las entradas de esta columna son cero. No se puede crear un pivote aquí; la columna corresponderá a una variable libre si no aparece un pivote después.",
                    snapshot(M), n,
                    title=f"Revisar la columna {col + 1}",
                    what=f"Se comprobó que la columna {col + 1} no tiene una entrada no nula disponible.",
                    why="Todas las entradas disponibles son cero; no existe un pivote en esta columna.",
                    calc=[f"aᵢ,{col + 1} = 0 para i ≥ {row + 1}"],
                ))
                continue
            if p != row:
                M[row], M[p] = M[p], M[row]
                swaps += 1
                steps.append(Step(
                    f"F{row + 1} ↔ F{p + 1}",
                    f"Pivoteo parcial en la columna {col + 1}: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.",
                    snapshot(M), n, "swap", row, p,
                    title=f"Elegir el pivote de la columna {col + 1}",
                    what=f"Se intercambiaron las filas {row + 1} y {p + 1}.",
                    why="Intercambiar ecuaciones conserva las soluciones y evita dividir entre cero.",
                    calc=[f"F{row + 1} ↔ F{p + 1}"],
                    pivot=(row, col),
                    changed_rows=[row, p],
                    decimals={"pivote": decimal_text(M[row][col])},
                ))
            pivot = M[row][col]
            pivot_values.append(pivot)
            if reduced and pivot != 1:
                factor = 1 / pivot
                M[row] = [v * factor for v in M[row]]
                steps.append(Step(
                    f"F{row + 1} ← ({factor}) · F{row + 1}",
                    f"Se divide toda la fila entre el pivote {pivot}, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.",
                    snapshot(M), n, "scale", row, factor=factor,
                    title=f"Normalizar el pivote de la fila {row + 1}",
                    what=f"Se multiplicó la fila {row + 1} por {factor} para convertir el pivote {pivot} en 1.",
                    why="Multiplicar una ecuación por un número no nulo conserva sus soluciones.",
                    calc=[f"factor = 1 / ({pivot}) = {factor}", f"F{row + 1} ← ({factor}) · F{row + 1}"],
                    pivot=(row, col),
                    changed_rows=[row],
                    decimals={"pivote": decimal_text(pivot), "factor": decimal_text(factor)},
                ))
            targets = range(len(M)) if reduced else range(row + 1, len(M))
            for target in targets:
                if target == row or M[target][col] == 0:
                    continue
                factor = -M[target][col] / M[row][col]
                entry = M[target][col]
                M[target] = [a + factor * b for a, b in zip(M[target], M[row])]
                steps.append(Step(
                    f"F{target + 1} ← F{target + 1} + ({factor}) · F{row + 1}",
                    f"El multiplicador es −({entry})/({M[row][col]}) = {factor}; así, {entry} + ({factor})·({M[row][col]}) = 0 en la columna {col + 1}. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.",
                    snapshot(M), n, "add", target, row, factor,
                    title=f"Eliminar la columna {col + 1} en la fila {target + 1}",
                    what=f"Se sumó {factor} veces la fila {row + 1} a la fila {target + 1}.",
                    why="Sumar un múltiplo de otra fila es reversible y conserva las soluciones.",
                    calc=[
                        f"factor = −({entry}) / ({M[row][col]})",
                        f"factor = {factor}",
                        f"F{target + 1} ← F{target + 1} + ({factor}) · F{row + 1}",
                        f"{entry} + ({factor}) · ({M[row][col]}) = 0",
                    ],
                    pivot=(row, col),
                    changed_rows=[target],
                    decimals={"pivote": decimal_text(M[row][col]), "factor": decimal_text(factor)},
                ))
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
        determinant_calc = ([f"det(A) = (−1)^{swaps} · {formula}", f"det(A) = {det}"]
                            if rank_A == n else [f"rango(A) = {rank_A} < {n}", "det(A) = 0"])
        diagnostic.append(Step(
            f"det(A) = {det}", explanation, snapshot(upper), n,
            title="Calcular el determinante",
            what=f"Se obtuvo det(A) = {det} a partir de los pivotes y los intercambios.",
            why=("El producto de pivotes se ajusta con el signo de los intercambios."
                 if rank_A == n else "Sin n pivotes independientes, A es singular y su determinante es cero."),
            calc=determinant_calc,
            decimals={"det(A)": decimal_text(det)},
        ))
        status = "inconsistent" if contradictions else "infinite" if rank_A < n else "unique"
        report = Analysis(A, B, det, rank_A, rank_aug, status, diagnostic)
        if status != "unique":
            if contradictions:
                for i in contradictions:
                    diagnostic.append(Step(
                        f"Contradicción: 0 = {upper[i][n]}",
                        f"La fila {i + 1} demuestra que rango(A) = {rank_A} < rango([A|B]) = {rank_aug}. Se detienen los métodos de solución única.",
                        snapshot(upper), n,
                        title=f"Detectar una contradicción en la fila {i + 1}",
                        what=f"Se identificó la igualdad imposible 0 = {upper[i][n]}.",
                        why="Una igualdad 0 = c con c distinto de cero hace incompatible el sistema.",
                        calc=[f"0 = {upper[i][n]}", f"rango(A) = {rank_A} < rango([A|B]) = {rank_aug}"],
                        changed_rows=[i],
                        decimals={"término independiente": decimal_text(upper[i][n])},
                    ))
            else:
                rref, reduced_steps, pivot_cols, _, _ = self._eliminate(augmented, n, True)
                diagnostic.append(Step(
                    "Diagnóstico de variables libres",
                    "Se reduce el sistema para describir la familia de soluciones; no se intenta invertir A.",
                    snapshot(augmented), n,
                    title="Identificar variables libres",
                    what="Se preparó la reducción para describir la familia de soluciones.",
                    why="Los rangos iguales menores que n implican una o más variables libres.",
                    calc=[f"rango(A) = rango([A|B]) = {rank_A} < {n}"],
                ))
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
        gauss_steps.append(Step(
            "Matriz triangular superior U",
            "La eliminación terminó: debajo de cada pivote hay ceros. Ahora se resuelve U·X = C desde la última ecuación hacia la primera, porque cada fila solo depende de variables ya conocidas.",
            snapshot(upper), n,
            title="Completar la matriz triangular superior",
            what="Se terminó la eliminación de las entradas situadas debajo de los pivotes.",
            why="La forma triangular permite despejar las variables desde la última fila.",
            calc=["[A | B] → [U | C]"],
        ))
        for i in reversed(range(n)):
            products = [upper[i][j] * x[j] for j in range(i + 1, n)]
            total = sum(products, Fraction(0))
            x[i] = (upper[i][n] - total) / upper[i][i]
            expression = " + ".join(f"({upper[i][j]})·({x[j]})" for j in range(i + 1, n)) or "0"
            term_lines = [
                f"t{k + 1} = ({upper[i][j]}) · ({x[j]}) = {product}"
                for k, (j, product) in enumerate(zip(range(i + 1, n), products))
            ]
            sum_line = f"S = {' + '.join(f't{k + 1}' for k in range(len(products))) or '0'} = {total}"
            gauss_steps.append(Step(
                f"x{i + 1} = ({upper[i][n]} − ({expression})) / ({upper[i][i]}) = {x[i]}",
                f"En la fila {i + 1} se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x{i + 1}. El valor se conserva como fracción exacta.",
                snapshot(upper), n, "substitution",
                title=f"Despejar x{i + 1} por sustitución",
                what=f"Se usaron los valores conocidos de la fila {i + 1} para calcular x{i + 1}.",
                why="La forma triangular deja una sola incógnita nueva en cada fila.",
                calc=[*term_lines, sum_line, f"x{i + 1} = ({upper[i][n]} − ({total})) / ({upper[i][i]})", f"Resultado: x{i + 1} = {x[i]}"],
                pivot=(i, i),
                decimals={f"x{i + 1}": decimal_text(x[i])},
            ))
        report.methods["gauss"] = MethodResult(METHOD_LABELS["gauss"], x, gauss_steps)

        # Gauss-Jordan: reducción independiente de [A|B] a [I|X].
        rref, jordan_steps, _, _, _ = self._eliminate(augmented, n, True)
        x_jordan = [row[n] for row in rref]
        jordan_steps.append(Step(
            "[I | X]: lectura directa de la solución",
            "El bloque izquierdo es la identidad: la fila i representa 1·xᵢ = Xᵢ. Por eso la última columna se lee directamente, sin sustitución hacia atrás.",
            snapshot(rref), n,
            title="Leer la solución en [I | X]",
            what="Se leyó cada componente de X directamente en la última columna.",
            why="Con I a la izquierda, cada fila expresa directamente xᵢ = Xᵢ.",
            calc=[f"x{i + 1} = {value}" for i, value in enumerate(x_jordan)],
            decimals={f"x{i + 1}": decimal_text(value) for i, value in enumerate(x_jordan)},
        ))
        report.methods["gauss_jordan"] = MethodResult(METHOD_LABELS["gauss_jordan"], x_jordan, jordan_steps)

        # Inversa: reducir [A|I]; B solo interviene al multiplicar A⁻¹·B.
        identity = [[Fraction(i == j) for j in range(n)] for i in range(n)]
        inverse_aug = [row + right for row, right in zip(A, identity)]
        inverse_rref, inverse_steps, _, _, _ = self._eliminate(inverse_aug, n, True)
        inverse = [row[n:] for row in inverse_rref]
        inverse_steps.append(Step(
            "[I | A⁻¹]: inversa obtenida",
            "Aplicar las mismas operaciones elementales a [A | I] equivale a multiplicar ambos bloques por A⁻¹: A⁻¹A = I y A⁻¹I = A⁻¹.",
            snapshot(inverse_rref), n,
            title="Obtener la matriz inversa",
            what="Se transformó el bloque izquierdo en I y el derecho en A⁻¹.",
            why="Las mismas operaciones convierten A en I y, simultáneamente, I en A⁻¹.",
            calc=["[A | I] → [I | A⁻¹]", "A⁻¹A = I"],
        ))
        x_inverse = matvec(inverse, B)
        for i, value in enumerate(x_inverse):
            expr = " + ".join(f"({v})·({b})" for v, b in zip(inverse[i], B))
            products = [v * b for v, b in zip(inverse[i], B)]
            term_lines = [f"t{j + 1} = ({v}) · ({b}) = {product}" for j, (v, b, product) in enumerate(zip(inverse[i], B, products))]
            inverse_steps.append(Step(
                f"x{i + 1} = {expr} = {value}",
                f"Producto fila {i + 1} de A⁻¹ por la columna B. La suma de productos da la componente x{i + 1} de X = A⁻¹B.",
                snapshot(inverse_rref), n, "multiplication",
                title=f"Calcular x{i + 1} con A⁻¹·B",
                what=f"Se multiplicó la fila {i + 1} de A⁻¹ por la columna B.",
                why="El producto fila por columna produce la componente correspondiente de X.",
                calc=[*term_lines, f"x{i + 1} = {' + '.join(f't{j + 1}' for j in range(n))}", f"Resultado: x{i + 1} = {value}"],
                decimals={f"x{i + 1}": decimal_text(value)},
            ))
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
            report.interpretation = [
                "El sistema no tiene solución: ninguna combinación de valores puede satisfacer todas las ecuaciones al mismo tiempo.",
                f"La evidencia es rango(A) = {report.rank_A} y rango([A|B]) = {report.rank_augmented}; al ser distintos, aparece al menos una contradicción del tipo 0 = c, con c ≠ 0.",
                "Revisa especialmente las ecuaciones dependientes y sus términos independientes o disponibilidades; alguno de esos datos es incompatible con los demás.",
            ]
        elif report.status == "infinite":
            free_names = ", ".join(f"x{column + 1}" for column in report.free_columns)
            report.interpretation = [
                f"El sistema es compatible, pero no determina una respuesta única: tiene infinitas soluciones y {len(report.free_columns)} variable(s) libre(s) ({free_names}).",
                f"La evidencia es rango(A) = rango([A|B]) = {report.rank_A}, menor que las {len(A)} incógnitas.",
                "La expresión X = Xₚ + t₁v₁ + … reúne todas las soluciones; hace falta agregar restricciones independientes para obtener un solo resultado.",
            ]
            if production:
                report.interpretation.append("La viabilidad de esta familia bajo X ≥ 0 requiere un análisis adicional; no se declara un plan de producción viable.")
        else:
            negatives = [f"x{i + 1} = {value} (≈ {decimal_text(value)})" for i, value in enumerate(report.solution) if value < 0]
            exact_solution = ", ".join(f"x{i + 1} = {value}" for i, value in enumerate(report.solution))
            if production and negatives:
                report.interpretation = ["Plan de producción inalcanzable por restricción de materias primas: el único resultado algebraico viola X ≥ 0.", "La solución de AX = B exige cantidades negativas: " + "; ".join(negatives) + ".", f"Gauss, Gauss-Jordan y matriz inversa coinciden en X = ({exact_solution}); la sustitución produce AX = B con error exacto 0.", "No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa."]
            elif production:
                report.interpretation = ["Plan factible para el modelo continuo: la solución es única, todas las cantidades son no negativas y AX = B consume exactamente las disponibilidades indicadas.", f"Los tres métodos coinciden en X = ({exact_solution}) y la verificación tiene error exacto 0.", "X se expresa en miles de unidades; X·1000 se informa como cantidad continua, sin redondear a unidades enteras."]
            else:
                report.interpretation = [f"El sistema tiene una única solución: {exact_solution}.", f"Como det(A) = {report.determinant} ≠ 0, A es invertible; Gauss, Gauss-Jordan y matriz inversa coinciden y AX = B se verifica con error exacto 0.", "Si algún valor es negativo, sigue siendo una solución matemática válida; su aceptación práctica depende del contexto del problema."]
            report.interpretation.append("La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.")
        return report
