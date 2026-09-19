"""Presentación compartida y exportaciones portables (Markdown, HTML y JSON)."""
from html import escape
from fractions import Fraction
import re
from agent import Analysis, METHOD_LABELS, STATUS_LABELS, decimal_text

REFERENCES = [
    ("MIT OpenCourseWare · Eliminación con matrices", "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/0903b4b404284cd14b66ecccea103fd4_MIT18_06SCF11_Ses1.2sum.pdf"),
    ("MIT OpenCourseWare · Multiplicación, Gauss-Jordan e inversa", "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf"),
    ("MIT OpenCourseWare · AX = B y variables libres", "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/solving-ax-b-row-reduced-form-r/"),
]
METHOD_GUIDES = {
    "gauss": {
        "summary": "Convierte [A | B] en una matriz triangular superior [U | C]. Después despeja las incógnitas desde la última ecuación hacia la primera.",
        "stages": ["Construir la matriz aumentada.", "Elegir un pivote no nulo; intercambiar filas si hace falta.", "Anular las entradas situadas debajo del pivote.", "Repetir en las columnas siguientes.", "Aplicar sustitución hacia atrás y verificar AX = B."],
        "formula": r"x_i=\frac{c_i-\sum_{j=i+1}^{n}u_{ij}x_j}{u_{ii}}",
    },
    "gauss_jordan": {
        "summary": "Reduce [A | B] hasta [I | X] cuando A es invertible. Cada pivote se hace 1 y se anulan los valores tanto arriba como abajo.",
        "stages": ["Construir [A | B] y seleccionar el pivote.", "Dividir la fila por el pivote para obtener 1.", "Eliminar las demás entradas de esa columna.", "Repetir hasta obtener la identidad.", "Leer X en la última columna y verificar."],
        "formula": r"[A\mid B]\longrightarrow[I\mid X]",
    },
    "inverse": {
        "summary": "Construye la inversa aplicando operaciones elementales a [A | I]. Una vez obtenido [I | A⁻¹], calcula cada componente del producto A⁻¹B.",
        "stages": ["Comprobar que det(A) no es cero.", "Formar [A | I], con dos bloques de n columnas.", "Reducir el bloque izquierdo hasta I con Gauss-Jordan.", "Extraer A⁻¹ del bloque derecho.", "Multiplicar A⁻¹ por B, fila por columna."],
        "formula": r"[A\mid I]\longrightarrow[I\mid A^{-1}],\qquad X=A^{-1}B",
    },
}


def fraction_latex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return sign + rf"\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


def matrix_latex(matrix, split=None, decimals=False) -> str:
    columns = len(matrix[0])
    spec = "r" * columns if split is None else "r" * split + "|" + "r" * (columns - split)
    fmt = decimal_text if decimals else fraction_latex
    rows = [" & ".join(fmt(v) for v in row) for row in matrix]
    return r"\left[\begin{array}{" + spec + "}" + r" \\ ".join(rows) + r"\end{array}\right]"


def matrix_text(matrix, split=None) -> str:
    values = [[str(v) for v in row] for row in matrix]
    widths = [max(len(row[j]) for row in values) for j in range(len(values[0]))]
    lines = []
    for row in values:
        cells = [v.rjust(widths[j]) for j, v in enumerate(row)]
        if split is not None:
            cells.insert(split, "|")
        lines.append("[ " + "  ".join(cells) + " ]")
    return "\n".join(lines)


def markdown_report(report: Analysis, *, title="Análisis matricial", note="", full=True) -> str:
    lines = [f"# {title}", "", "TechChip Matrix Studio · procedimiento reproducible", ""]
    if note:
        lines += [note, ""]
    lines += ["## 1. Sistema de entrada", "", "```text", matrix_text([r + [b] for r, b in zip(report.A, report.B)], len(report.A)), "```", "",
              "## 2. Diagnóstico", "", f"- Estado: {STATUS_LABELS[report.status]}", f"- det(A) = {report.determinant}", f"- rango(A) = {report.rank_A}; rango([A|B]) = {report.rank_augmented}", "",
              "## 3. Interpretación", ""]
    lines += [f"- {text}" for text in report.interpretation]
    if report.solution is not None:
        lines += ["", "## 4. Solución y verificación", "", "| Variable | Valor exacto | Aproximación |", "|---|---:|---:|"]
        lines += [f"| x{i+1} | {v} | {decimal_text(v)} |" for i, v in enumerate(report.solution)]
        lines += ["", f"Los tres métodos coinciden: {'sí' if report.methods_agree else 'no'}.", f"Error máximo por componente: {report.max_error}; criterio exigido: < 10⁻⁶.", "", *report.substitution, ""]
    if report.particular is not None:
        lines += ["", "## 4. Familia de soluciones", "", f"Xₚ = ({', '.join(map(str, report.particular))})"]
        for i, vector in enumerate(report.nullspace):
            lines.append(f"v{i+1} = ({', '.join(map(str, vector))})")
        lines += ["X = Xₚ + " + " + ".join(f"t{i+1}·v{i+1}" for i in range(len(report.nullspace))), "Los parámetros t son números reales libres.", ""]
    if full:
        sequences = [("Diagnóstico: determinante y rangos", report.diagnostic_steps)]
        sequences += [(method.name, method.steps) for method in report.methods.values()]
        for title_, steps in sequences:
            lines += ["", f"## Procedimiento — {title_}", ""]
            for i, step in enumerate(steps, 1):
                lines += [f"### Paso {i}. {step.operation}", "", step.explanation, "", "```text", matrix_text(step.matrix, step.split), "```", ""]
    lines += ["## Referencias", ""] + [f"- [{title_}]({url})" for title_, url in REFERENCES]
    lines += ["", "Cálculo racional exacto respecto de los datos introducidos. Los decimales de presentación son aproximados.", ""]
    return "\n".join(lines)


def html_report(report: Analysis, *, title="Análisis matricial", note="") -> str:
    """HTML autocontenido, sin scripts ni conexión: se puede imprimir a PDF."""
    chunks = []
    code = False
    in_table = False
    for line in markdown_report(report, title=title, note=note).splitlines():
        if not code and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if all(re.fullmatch(r"[-:]+", cell) for cell in cells):
                continue
            tag = "td" if in_table else "th"
            if not in_table:
                chunks.append("<table>")
                in_table = True
            chunks.append("<tr>" + "".join(f"<{tag}>{escape(cell)}</{tag}>" for cell in cells) + "</tr>")
            continue
        if in_table:
            chunks.append("</table>")
            in_table = False
        if line.startswith("```"):
            chunks.append("</pre>" if code else "<pre>")
            code = not code
        elif code:
            chunks.append(escape(line) + "\n")
        elif line.startswith("### "):
            chunks.append("<h3>" + escape(line[4:]) + "</h3>")
        elif line.startswith("## "):
            chunks.append("<h2>" + escape(line[3:]) + "</h2>")
        elif line.startswith("# "):
            chunks.append("<h1>" + escape(line[2:]) + "</h1>")
        elif match := re.fullmatch(r"- \[([^\]]+)\]\((https://[^\s)]+)\)", line):
            chunks.append(f'<p><a href="{escape(match[2], quote=True)}">{escape(match[1])}</a></p>')
        elif line:
            chunks.append("<p>" + escape(line) + "</p>")
    return """<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>""" + escape(title) + """</title><style>
body{font:15px/1.6 system-ui,sans-serif;color:#16312f;max-width:1100px;margin:48px auto;padding:0 28px}
h1{font-size:34px;line-height:1.15}h2{border-top:1px solid #ccd8d5;margin-top:40px;padding-top:20px}
h3{break-after:avoid}pre{padding:20px;background:#f1f6f4;overflow:auto;font:12px/1.6 monospace;break-inside:avoid}
table{border-collapse:collapse;width:100%;margin:18px 0}th,td{padding:10px 14px;text-align:left;border-bottom:1px solid #dce7e2}th{background:#eaf2ee}a{color:#087968}
p{overflow-wrap:anywhere}@media print{body{margin:0;font-size:10pt}pre{font-size:8pt;white-space:pre-wrap}h2{break-before:auto}}
</style><body>""" + "\n".join(chunks) + "</body></html>"
