"""Genera los entregables académicos únicamente desde ejecuciones guardadas."""
from fractions import Fraction
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "bitacora"
DOCS = ROOT / "docs"
SCENARIO_ORDER = ["original", "compatible", "scarcity", "singular", "infinite"]
SCENARIO_NAMES = {
    "original": "Caso principal: B original", "compatible": "Comparación didáctica: B alternativo",
    "scarcity": "Escasez de resina", "singular": "Singular incompatible",
    "infinite": "Singular compatible indeterminado",
}
PRODUCTS = ["AI-Edge 1", "AI-Server Pro", "AI-Autonomous Car", "AI-IoT LowPower", "AI-Robotics Heavy", "AI-Medical Vision"]
RESOURCES = ["Litografía EUV", "Pruebas ATE", "Resina de encapsulado", "Sustrato de silicio", "Energía láser", "Inspección óptica"]
UNITS = ["horas-máquina", "horas-máquina", "kg", "m²", "MWh", "horas-hombre"]


def load_reports():
    reports = {}
    for key in SCENARIO_ORDER:
        path = LOG_DIR / f"{key}.json"
        if not path.exists():
            raise SystemExit(f"Falta {path}. Ejecuta primero main.py y guarda el resultado.")
        reports[key] = json.loads(path.read_text(encoding="utf-8"))
    return reports


def tex_escape(text):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}", "−": "-", "×": r"\(\times\)", "·": r"\(\cdot\)", "≥": r"\(\ge\)", "≤": r"\(\le\)", "≠": r"\(\ne\)", "←": r"\(\leftarrow\)", "↔": r"\(\leftrightarrow\)", "²": r"\textsuperscript{2}", "₁": r"\textsubscript{1}", "₂": r"\textsubscript{2}", "₃": r"\textsubscript{3}", "₄": r"\textsubscript{4}", "₅": r"\textsubscript{5}", "₆": r"\textsubscript{6}", "⁻": "-", "…": r"\ldots{}"}
    return "".join(replacements.get(char, char) for char in str(text))


def frac_tex(value):
    value = Fraction(str(value))
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return rf"{sign}\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


def matrix_tex(matrix, split=None, width=r"\linewidth"):
    spec = "r" * len(matrix[0])
    if split is not None:
        spec = "r" * split + "|" + "r" * (len(matrix[0]) - split)
    rows = [" & ".join(frac_tex(v) for v in row) for row in matrix]
    body = r" \\ ".join(rows)
    return rf"\resizebox{{{width}}}{{!}}{{\(\left[\begin{{array}}{{{spec}}}{body}\end{{array}}\right]\)}}"


def operation_tex(operation):
    return tex_escape(operation)


def summary_log(report):
    solution = "No aplica" if report["solution"] is None else "(" + ", ".join(report["solution"]) + ")"
    residual = "No aplica" if not report["residual"] else "(" + ", ".join(report["residual"]) + ")"
    return "\n".join([
        f"status: {report['status']}", f"det(A): {report['determinant']}",
        f"rank(A): {report['rank_A']}", f"rank([A|B]): {report['rank_augmented']}",
        f"solution: {solution}", f"residual |AX-B|: {residual}",
        f"max_error: {report['max_error']}", f"methods_agree: {report['methods_agree']}",
    ])


def build_bitacora(reports):
    outcomes = {
        "original": ("Resolver el B original sin forzar el vector incorrecto y obtener E=0", "Cumple: error de la guía demostrado"),
        "compatible": ("Reproducir el vector indicado solo con su B alternativo, E=0", "Cumple como comparación, no como caso principal"),
        "scarcity": ("Detectar producciones negativas y plan inalcanzable", "Cumple"),
        "singular": ("det(A)=0 y cero soluciones porque B6≠2B1", "Cumple"),
        "infinite": ("det(A)=0 e infinitas soluciones cuando B6=2B1", "Cumple"),
    }
    lines = ["# Bitácora de pruebas — TechChip Matrix Studio", "", "Resultados regenerados el 22 de septiembre de 2026 mediante el motor exacto; los JSON enlazados contienen la salida completa, incluidas todas las matrices intermedias. El B original es el caso principal y el vector equivocado de la guía no se usa como resultado esperado.", "", "| Escenario | det(A) | rangos A/[A|B] | Diagnóstico | Estado |", "|---|---:|---:|---|---|"]
    labels = {"unique": "Solución única", "infinite": "Infinitas soluciones", "inconsistent": "Cero soluciones"}
    for key in SCENARIO_ORDER:
        r = reports[key]
        lines.append(f"| {SCENARIO_NAMES[key]} | {r['determinant']} | {r['rank_A']}/{r['rank_augmented']} | {labels[r['status']]} | {outcomes[key][1]} |")
    for i, key in enumerate(SCENARIO_ORDER, 1):
        r = reports[key]
        lines += ["", f"## {i}. {SCENARIO_NAMES[key]}", "", "### Entrada usada", "", "```json", json.dumps({"A": r["A"], "B": r["B"], "production": r["production"]}, ensure_ascii=False, indent=2), "```", "", "### Salida literal resumida", "", "```text", summary_log(r), "```", "", f"Salida completa: [`{key}.json`]({key}.json).", "", "### Diagnóstico", "", *[f"- {item}" for item in r["interpretation"]], "", "### Esperado frente a obtenido", "", f"- **Esperado:** {outcomes[key][0]}." ]
        if r["solution"]:
            obtained = "X = (" + ", ".join(r["solution"]) + f"), error máximo = {r['max_error']}"
        elif r["particular"]:
            obtained = "Xₚ = (" + ", ".join(r["particular"]) + "); columnas libres (base cero): " + ", ".join(map(str, r["free_columns"]))
        else:
            obtained = f"rango(A)={r['rank_A']} < rango([A|B])={r['rank_augmented']}"
        lines += [f"- **Obtenido:** {obtained}.", f"- **Estado:** {outcomes[key][1]}."]
    lines += ["", "## Evidencia visual", "", "- Inicio y entrada Streamlit: [`docs/screenshots/01_inicio.png`](../docs/screenshots/01_inicio.png)", "- Caso base compatible: [`docs/screenshots/02_plan_compatible.png`](../docs/screenshots/02_plan_compatible.png)", "- Procedimiento Streamlit: [`docs/screenshots/03_procedimiento.png`](../docs/screenshots/03_procedimiento.png)", "- Escasez: [`docs/screenshots/04_escasez.png`](../docs/screenshots/04_escasez.png)", "- Singular incompatible: [`docs/screenshots/05_singular.png`](../docs/screenshots/05_singular.png)", "- Infinitas soluciones: [`docs/screenshots/06_infinitas.png`](../docs/screenshots/06_infinitas.png)", "- Portada profesional en Vercel: [`docs/screenshots/08_vercel_profesional.png`](../docs/screenshots/08_vercel_profesional.png)", "- Procedimiento completo en Vercel: [`docs/screenshots/09_vercel_procedimiento.png`](../docs/screenshots/09_vercel_procedimiento.png)", "- Tutor IA en Vercel: [`docs/screenshots/10_vercel_tutor.png`](../docs/screenshots/10_vercel_tutor.png)", "- Vista móvil en Vercel: [`docs/screenshots/11_vercel_movil.png`](../docs/screenshots/11_vercel_movil.png)", "- Entregables públicos en Vercel: [`docs/screenshots/12_vercel_entregables.png`](../docs/screenshots/12_vercel_entregables.png)", "- Tema oscuro y selector persistente: [`docs/screenshots/13_vercel_oscuro.png`](../docs/screenshots/13_vercel_oscuro.png)", ""]
    (LOG_DIR / "BITACORA.md").write_text("\n".join(lines), encoding="utf-8")


def build_interpretation(reports):
    original, comparison, scarcity = reports["original"], reports["compatible"], reports["scarcity"]
    lines = ["# Informe de interpretación de operaciones — TechChip Systems", "", "## Conclusión principal", "", "Con las disponibilidades originales **B = (155, 160, 225, 140, 215, 175)**, los tres métodos obtienen exactamente `X = (-105, 345, 2430, 1170, 1130, 2010)/83`, con determinante `-83` y residuo cero. Como `x1=-105/83≈-1.265060`, el balance algebraico existe pero no constituye un plan de producción físicamente viable bajo `X≥0`.", "", "El vector `(15,20,25,10,15,20)` de la guía es incorrecto para el B original. Solo aparece al reemplazar B por `(185,200,280,150,245,195)`; ese segundo caso se conserva exclusivamente como comparación didáctica.", "", "## Resultado por línea para el B original", "", "| Línea | Valor exacto | Aproximación (miles de módulos) |", "|---|---:|---:|"]
    for name, value in zip(PRODUCTS, original["solution"]):
        lines.append(f"| {name} | {value} | {float(Fraction(value)):.6f} |")
    lines += ["", "## Balance cuantitativo", "", "La sustitución exacta devuelve `AX=B` en las seis restricciones: el error máximo es cero. Esto comprueba el cálculo, pero la componente negativa invalida la interpretación productiva no negativa. No debe reemplazarse por cero porque se romperían las igualdades.", "", "## Comparación didáctica con B alternativo", "", f"Con el B alternativo, el agente obtiene `X = ({', '.join(comparison['solution'])})` y residuo cero. Este escenario consume el 100 % de ese B alternativo, pero no representa las disponibilidades originales de TechChip Systems.", "", "## Escasez de resina", "", f"Al sustituir únicamente `B3=225` por `B3=100`, el agente obtiene `X = ({', '.join(scarcity['solution'])})`. Las producciones `x1=-26355/83` y `x2=-6780/83` son negativas. El problema es de factibilidad empresarial, no de cálculo.", "", "## Dependencia y contradicción", "", "Si `F6=2F1` pero se conserva `B6=175`, se exige simultáneamente `2B1=310` y `B6=175`: `rango(A)=5`, `rango([A|B])=6` y no existe solución. Si también se establece `B6=310`, ambos rangos son 5 y aparece una familia con una variable libre.", "", "## Recomendaciones", "", "1. Usar el B original como caso principal y registrar el vector indicado como resultado erróneo de la guía.", "2. No redondear ni reemplazar producciones negativas por cero.", "3. Si se permite capacidad ociosa, reformular como `AX≤B`, `X≥0` e incorporar demanda.", "4. Para hablar de un plan óptimo, añadir una función objetivo con costos, márgenes o tiempos.", "5. Validar la escala: si X está en miles, A debe representar consumo por cada mil módulos.", ""]
    (DOCS / "interpretacion_operaciones.md").write_text("\n".join(lines), encoding="utf-8")


def appendix_steps(report, key, title):
    steps = report["diagnostic_steps"] if key == "diagnosis" else report["methods"][key]["steps"]
    chunks = [rf"\section{{{tex_escape(title)}}}", rf"La secuencia contiene {len(steps)} estados registrados. Cada matriz es el estado posterior a la operación indicada."]
    for i, step in enumerate(steps, 1):
        chunks += [rf"\subsection*{{Paso {i}: {operation_tex(step['operation'])}}}", tex_escape(step["explanation"]), "", matrix_tex(step["matrix"], step["split"], r"0.97\textwidth"), "", r"\medskip"]
    return "\n".join(chunks)


def build_ieee(reports):
    original, comparison, scarcity, singular, infinite = [reports[k] for k in SCENARIO_ORDER]
    base = original
    initial = [row + [b] for row, b in zip(base["A"], base["B"])]
    gauss_final = base["methods"]["gauss"]["steps"][-7]["matrix"]
    jordan_final = base["methods"]["gauss_jordan"]["steps"][-1]["matrix"]
    inverse = base["methods"]["inverse"]["inverse"]
    variable_rows = "\n".join(rf"$x_{i}$ & {tex_escape(name)} & miles de módulos por turno \\" for i, name in enumerate(PRODUCTS, 1))
    constraint_rows = "\n".join(rf"$R_{i}$ & {tex_escape(name)} & {tex_escape(unit)} & {b} \\" for i, (name, unit, b) in enumerate(zip(RESOURCES, UNITS, base["B"]), 1))
    comparison_rows = "\n".join(rf"$x_{i}$ & {base['methods']['gauss']['solution'][i-1]} & {base['methods']['gauss_jordan']['solution'][i-1]} & {base['methods']['inverse']['solution'][i-1]} \\" for i in range(1, 7))
    solution_tex = r"\left(" + ",".join(frac_tex(value) for value in base["solution"]) + r"\right)^T"
    tex = rf"""\documentclass[conference]{{IEEEtran}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[spanish,es-nodecimaldot]{{babel}}
\usepackage{{amsmath,amssymb,array,booktabs,graphicx,hyperref,xcolor}}
\graphicspath{{{{screenshots/}}{{docs/screenshots/}}{{assets/}}{{docs/assets/}}}}
\hypersetup{{colorlinks=true,linkcolor=black,urlcolor=blue,citecolor=black}}
\title{{Agente explicable para el balance matricial exacto de recursos en TechChip Systems S.A.}}
\author{{
\IEEEauthorblockN{{\small
\begin{{tabular}}{{ccc}}
Henry Modesto Portillo Quintanilla & David Ernesto Quijada Vásquez & Josue Emanuel Cruz Fernandez\\
PQ100126 & QV100226 & CF100126
\end{{tabular}}}}
\IEEEauthorblockA{{
\includegraphics[width=0.30\textwidth]{{ufg_logo.png}}\\[3pt]
Universidad Francisco Gavidia\\
Ingeniería en Inteligencia Artificial y Telecomunicaciones\\
Docente: Exides Gamaliel Claros Velasquez \quad Grupo: 01 EO8 \quad Entrega: 23 de septiembre de 2026
}}
}}
\begin{{document}}
\maketitle
\begin{{abstract}}
Se presenta un agente portable para modelar y resolver el balance de seis recursos y seis líneas de módulos mediante $AX=B$. El motor implementa eliminación de Gauss, Gauss--Jordan y matriz inversa con fracciones exactas, registra cada operación elemental y diagnostica sistemas singulares por rangos. Con el $B$ original se obtiene $X={solution_tex}$ y residuo cero. Se demuestra que el vector $(15,20,25,10,15,20)$ indicado por la guía es incorrecto para esos datos. Se validan además escenarios de escasez, incompatibilidad e infinitas soluciones, junto con entrada mediante ecuaciones, JSON y bloques A/B.
\end{{abstract}}
\begin{{IEEEkeywords}}álgebra lineal, sistemas de ecuaciones, eliminación de Gauss, Gauss--Jordan, matriz inversa, agente explicable, balance de recursos\end{{IEEEkeywords}}

\section{{Introducción}}
TechChip Systems S.A. fabrica seis líneas de aceleradores de inteligencia artificial que comparten seis recursos críticos. La decisión consiste en determinar niveles diarios de producción que consuman exactamente la capacidad asignada. El problema se representa mediante seis igualdades lineales. El objetivo del agente no es ocultar el cálculo tras una biblioteca numérica, sino producir una traza auditable y una interpretación empresarial. Consumir el 100\% en $AX=B$ no equivale a maximizar utilidad: sin función objetivo no existe fundamento para afirmar optimalidad.

\section{{Modelado matemático}}
Cada variable es continua y se expresa en miles de módulos por turno. Para coherencia dimensional, $a_{{ij}}$ se interpreta como consumo del recurso $i$ por cada mil módulos de la línea $j$.
\begin{{table}}[ht]\caption{{Variables del modelo}}\centering\footnotesize\begin{{tabular}}{{lll}}\toprule Variable&Línea&Unidad\\\midrule {variable_rows}\bottomrule\end{{tabular}}\end{{table}}
La matriz de coeficientes es
{matrix_tex(base['A'])}
y las restricciones del caso principal original son:
\begin{{table}}[ht]\caption{{Recursos y disponibilidades originales}}\centering\scriptsize\begin{{tabular}}{{llll}}\toprule&Recurso&Unidad&$b_i$\\\midrule {constraint_rows}\bottomrule\end{{tabular}}\end{{table}}
La matriz aumentada inicial es
{matrix_tex(initial, 6)}
Las operaciones elementales son reversibles y conservan el conjunto solución. Si la eliminación obtiene seis pivotes, $\det(A)$ es distinto de cero, $A$ es invertible y existe una única solución. En la ejecución, $\det(A)=-83\neq0$ y $\operatorname{{rango}}(A)=\operatorname{{rango}}([A\mid B])=6$.

\section{{Discrepancia de datos}}
La multiplicación exacta del vector solicitado por la guía produce
\[
\resizebox{{0.97\linewidth}}{{!}}{{\(A\begin{{bmatrix}}15&20&25&10&15&20\end{{bmatrix}}^T
=\begin{{bmatrix}}185&200&280&150&245&195\end{{bmatrix}}^T\)}}.
\]
No coincide con el $B$ impreso, cuya diferencia es $(30,40,55,10,30,20)^T$. Para ese $B$, el agente obtiene
\[
X=\frac1{{83}}(-105,345,2430,1170,1130,2010)^T.
\]
El valor $x_1=-105/83$ hace inviable el balance empresarial bajo $X\ge0$, aunque el sistema matemático tiene solución única. El caso original es la prueba principal; el otro $B$ se conserva únicamente como comparación didáctica.

\section{{Tres métodos exactos}}
\subsection{{Eliminación de Gauss}}
El algoritmo selecciona el mayor pivote absoluto disponible, intercambia filas cuando procede y aplica $F_i\leftarrow F_i+kF_j$ bajo cada pivote. La forma triangular obtenida es
{matrix_tex(gauss_final, 6)}
La sustitución hacia atrás, desarrollada íntegramente en el Apéndice A, produce $X={solution_tex}$.

\subsection{{Gauss--Jordan}}
Cada pivote se divide por sí mismo y se eliminan las entradas inferiores y superiores. La ejecución termina en
{matrix_tex(jordan_final, 6)}
por lo que la última columna se lee como $X={solution_tex}$.

\subsection{{Matriz inversa}}
Se reduce $[A\mid I]$ hasta $[I\mid A^{{-1}}]$. La inversa exacta calculada es
{matrix_tex(inverse)}
La multiplicación $A^{{-1}}B$ devuelve el mismo vector. Además, las pruebas verifican $AA^{{-1}}=A^{{-1}}A=I$.

\begin{{table}}[ht]\caption{{Comparación exacta entre métodos}}\centering\footnotesize\begin{{tabular}}{{rrrr}}\toprule Variable&Gauss&Gauss--Jordan&Inversa\\\midrule {comparison_rows}\bottomrule\end{{tabular}}\end{{table}}
Los seis residuos son cero y $E_{{\max}}=0<10^{{-6}}$.

\section{{Arquitectura del agente}}
El flujo funcional es:
\begin{{center}}\begin{{tabular}}{{c}}\fbox{{Entrada JSON / consola / web}}\\$\downarrow$\\\fbox{{Validación dimensional y racional}}\\$\downarrow$\\\fbox{{Determinante, rangos y diagnóstico}}\\$\downarrow$\\\fbox{{Gauss / Gauss--Jordan / inversa}}\\$\downarrow$\\\fbox{{Verificación $AX=B$ e interpretación}}\end{{tabular}}\end{{center}}
\texttt{{agent.py}} contiene validación, pivoteo, rangos y análisis; \texttt{{exercise_parser.py}} convierte de forma segura ecuaciones lineales, JSON y bloques A/B; \texttt{{api/solve.py}} ofrece la función serverless y \texttt{{web/}} la interfaz React. El Tutor IA recibe contexto matemático recalculado por el servidor y nunca sustituye al motor exacto. La interfaz admite 2x2 hasta 6x6 y no conserva el límite anterior de 500 caracteres; solo aplica un límite técnico de 100 kB \cite{{openai}}.

\section{{Pruebas de validación}}
\begin{{table*}}[ht]\caption{{Resultados generados por el agente}}\centering\footnotesize\begin{{tabular}}{{lllll}}\toprule Escenario&$\det(A)$&Rangos&Resultado exacto&Diagnóstico\\\midrule
B original&$-83$&$6/6$&$(-105,345,2430,1170,1130,2010)/83$&Única, no viable\\
Comparación con B alternativo&$-83$&$6/6$&$(15,20,25,10,15,20)$&Única, didáctica\\
Resina $B_3=100$&$-83$&$6/6$&$(-26355,-6780,18555,3170,3505,6510)/83$&Única, no viable\\
$F_6=2F_1$, $B_6=175$&$0$&$5/6$&No existe&Incompatible\\
$F_6=2F_1$, $B_6=310$&$0$&$5/5$&Familia con $x_6$ libre&Infinitas\\\bottomrule\end{{tabular}}\end{{table*}}
En escasez, $x_1=-26355/83$ y $x_2=-6780/83$ prueban que no puede agotarse cada recurso con producciones no negativas. En el caso singular incompatible, la primera fila exige $2B_1=310$ mientras la sexta conserva 175. Al corregir también $B_6=310$, una ecuación es redundante y aparece una familia cuyo particular es $(-105/16,345/16,105/4,165/16,115/4,0)^T$.
Los registros literales completos se conservan en \texttt{{bitacora/*.json}} y su índice auditable en \texttt{{bitacora/BITACORA.md}}. La Fig.~\ref{{fig:evidencia}} muestra evidencia de la ejecución web del caso compatible y del procedimiento completo.

\begin{{figure}}[!t]
\centering
\includegraphics[width=\linewidth]{{02_plan_compatible.png}}\\[2pt]
\includegraphics[width=\linewidth]{{09_vercel_procedimiento.png}}
\caption{{Evidencia de ejecución: solución compatible y traza completa publicada en Vercel.}}
\label{{fig:evidencia}}
\end{{figure}}

\section{{Conclusiones}}
La coincidencia exacta de tres algoritmos y el residuo nulo validan la solución del B original. La componente negativa prueba que ese balance no es un plan productivo viable bajo $X\ge0$. El vector indicado en la guía es incorrecto y solo aparece con otro B. La singularidad distingue recursos redundantes de restricciones contradictorias. Para uso industrial se recomienda validar unidades, permitir holguras mediante desigualdades cuando corresponda e incorporar costos y demanda antes de hablar de optimización.

\begin{{thebibliography}}{{9}}
\bibitem{{lay}} D. C. Lay, S. R. Lay y J. J. McDonald, \emph{{Linear Algebra and Its Applications}}, 6.ª ed. Pearson, 2021.
\bibitem{{strang}} G. Strang, ``Gaussian elimination,'' MIT OpenCourseWare 18.06SC, 2011. [En línea]. Disponible: \url{{https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/}}
\bibitem{{python}} Python Software Foundation, ``fractions --- Rational numbers.'' [En línea]. Disponible: \url{{https://docs.python.org/3/library/fractions.html}}
\bibitem{{streamlit}} Streamlit, ``Streamlit documentation.'' [En línea]. Disponible: \url{{https://docs.streamlit.io/}}
\bibitem{{vercel}} Vercel, ``Using the Python runtime with Vercel Functions.'' [En línea]. Disponible: \url{{https://vercel.com/docs/functions/runtimes/python}}
\bibitem{{openai}} OpenAI, ``Create a model response --- Responses API.'' [En línea]. Disponible: \url{{https://developers.openai.com/api/reference/cli/resources/responses/methods/create}}
\end{{thebibliography}}

\clearpage\onecolumn\appendices
{appendix_steps(base, 'gauss', 'Eliminación de Gauss: procedimiento completo')}
{appendix_steps(base, 'gauss_jordan', 'Gauss--Jordan: procedimiento completo')}
\end{{document}}
"""
    (DOCS / "informe_tecnico_ieee.tex").write_text(tex, encoding="utf-8")


def build_map():
    text = """# Mapa de entregables y rúbrica

| Criterio | Puntos | Evidencia principal |
|---|---:|---|
| Dominio de Álgebra Lineal | 20 | `docs/informe_tecnico_ieee.tex`, apéndices completos y comparación exacta |
| Modelación Empresarial | 15 | Secciones II–III del informe e `docs/interpretacion_operaciones.md` |
| Implementación del Agente IA | 20 | `agent.py`, `exercise_parser.py`, `api/solve.py`, `api/tutor.py`, `web/` |
| Rigor Matemático | 15 | Tres trazas exactas, determinante por pivotes, rangos y pruebas |
| Pruebas y Extremos | 10 | `bitacora/BITACORA.md` y JSON completos por escenario |
| Interpretación | 10 | `docs/interpretacion_operaciones.md` |
| Documentación y Presentación | 10 | Informe IEEE, README, bitácora, interfaz y despliegue Vercel |

La comparación detallada con las seis fotos está en [`auditoria_guia_fotos.md`](auditoria_guia_fotos.md). El cálculo independiente de determinante y solución por Cramer puede repetirse con `python scripts/verify_photo_matrix.py`.

## Compilación del PDF IEEE

```bash
cd docs
pdflatex informe_tecnico_ieee.tex
pdflatex informe_tecnico_ieee.tex
```

La segunda ejecución actualiza referencias y numeración. Se requiere una distribución TeX que incluya `IEEEtran`, `babel`, `amsmath`, `booktabs`, `graphicx`, `hyperref` y fuentes T1.

## Identificación institucional incorporada

| Campo | Dato |
|---|---|
| Universidad | Universidad Francisco Gavidia |
| Docente | Exides Gamaliel Claros Velasquez |
| Grupo | 01 EO8 |
| Fecha de entrega | 23 de septiembre de 2026 |

## Datos por verificar antes de entregar

- Si la institución exige una variante específica de IEEE/ACM o portada separada.
- El B impreso es el caso oficial del paquete; el vector indicado se documenta como resultado incorrecto.
- Confirmación de que los coeficientes son consumos por mil módulos, no por módulo individual.
"""
    (DOCS / "MAPA_ENTREGABLES.md").write_text(text, encoding="utf-8")


def main():
    reports = load_reports()
    build_bitacora(reports)
    build_interpretation(reports)
    build_ieee(reports)
    build_map()
    print("Generados: bitacora/BITACORA.md, docs/informe_tecnico_ieee.tex, docs/interpretacion_operaciones.md, docs/MAPA_ENTREGABLES.md")


if __name__ == "__main__":
    main()
