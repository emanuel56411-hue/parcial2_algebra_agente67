"""Interfaz de análisis: datos editables, evidencia algebraica y decisiones claras."""
import json
import math
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from agent import MAX_SIZE, InputError, TechChipAgent, STATUS_LABELS, METHOD_LABELS, decimal_text, json_ready, matvec, parse_json, validate_input
from main import validation_battery
from reporting import METHOD_GUIDES, REFERENCES, html_report, markdown_report, matrix_latex
from scenarios import A_BASE, B_GUIDE, B_TARGET, GUIDE_NOTE, PRODUCTS, RESOURCES, SCENARIOS, UNITS, X_TARGET, get_scenario
from tutor_ui import render_step_tutor, render_tutor, reset_conversation

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="TechChip · Matrix Studio", page_icon=":material/grid_on:", layout="wide")


@st.cache_data(max_entries=32, show_spinner=False)
def analyze_cached(A, B, production):
    return TechChipAgent().analyze(A, B, production=production)


def clear_result():
    reset_conversation()
    for key in ("report", "report_title", "report_note", "report_techchip"):
        st.session_state.pop(key, None)


def render_steps(steps, key):
    view = st.segmented_control("Vista del procedimiento", ["Paso a paso", "Todos los pasos"], default="Paso a paso", key=f"view_{key}")
    decimals = st.toggle("Mostrar aproximaciones decimales", key=f"decimal_{key}")
    st.caption("Las operaciones se calculan con fracciones exactas. F indica una fila; el bloque a la derecha de la barra también se transforma.")
    if view == "Todos los pasos":
        with st.container(height=640, border=True):
            for i, step in enumerate(steps, 1):
                st.markdown(f"**Paso {i:02d} · {step.operation}**")
                st.caption(step.explanation)
                st.latex(matrix_latex(step.matrix, step.split, decimals))
    else:
        index_key = f"step_{key}"
        if index_key not in st.session_state or st.session_state[index_key] > len(steps):
            st.session_state[index_key] = 1
        index = st.select_slider("Paso", options=list(range(1, len(steps) + 1)), key=index_key)
        def move(delta):
            st.session_state[index_key] = max(1, min(len(steps), st.session_state[index_key] + delta))
        with st.container(horizontal=True):
            st.button("Anterior", icon=":material/arrow_back:", disabled=index == 1, on_click=move, args=(-1,), key=f"prev_{key}")
            st.button("Siguiente", icon=":material/arrow_forward:", disabled=index == len(steps), on_click=move, args=(1,), key=f"next_{key}")
        step = steps[index - 1]
        with st.container(border=True):
            st.caption(f"PASO {index:02d} DE {len(steps):02d}")
            st.markdown(f"**{step.operation}**")
            st.markdown(step.explanation)
            st.latex(matrix_latex(step.matrix, step.split, decimals))
        if index > 1:
            with st.expander("Ver la matriz del paso anterior"):
                prev = steps[index - 2]
                st.latex(matrix_latex(prev.matrix, prev.split, decimals))


def render_results(report, title, note, techchip):
    n = len(report.A)
    st.header("02 · Resultado del análisis")
    st.caption(f"Último cálculo enviado: {title}. Si editas las celdas, pulsa «Resolver sistema» para actualizarlo.")
    cols = st.columns(4)
    cols[0].metric("Estado matemático", STATUS_LABELS[report.status], border=True)
    cols[1].metric("Determinante", str(report.determinant), border=True)
    cols[2].metric("Rangos A / [A|B]", f"{report.rank_A} / {report.rank_augmented}", border=True)
    cols[3].metric("Error máximo |AX − B|", str(report.max_error) if report.max_error is not None else "No aplica", border=True)
    if report.solution is not None:
        production_invalid = report.production and any(v < 0 for v in report.solution)
        if production_invalid:
            st.warning(report.interpretation[0], icon=":material/warning:")
        else:
            st.success(report.interpretation[0], icon=":material/check_circle:")
    elif report.status == "inconsistent":
        st.error(report.interpretation[0], icon=":material/error:")
    else:
        st.info(report.interpretation[0], icon=":material/info:")

    tab_summary, tab_steps, tab_verify, tab_exports, tab_tutor = st.tabs(["Resumen", "Procedimiento", "Verificación", "Exportar", "Tutor IA"])
    with tab_summary:
        if report.solution is not None:
            left, right = st.columns([1.25, 1])
            with left:
                st.subheader("Solución por variable")
                names = PRODUCTS if techchip else [f"Variable {i+1}" for i in range(n)]
                data = []
                for i, (name, v) in enumerate(zip(names, report.solution)):
                    item = {"Variable": f"x{i+1}", "Descripción": name, "Exacto": str(v), "Decimal ≈": decimal_text(v)}
                    if report.production:
                        item["Unidades ≈"] = decimal_text(v * 1000, 3)
                        item["Factibilidad"] = "No viable" if v < 0 else "No negativa"
                    data.append(item)
                st.dataframe(pd.DataFrame(data), hide_index=True, width="stretch")
                st.caption("Valores de X en miles de unidades." if report.production else "Valores de X sin unidades asumidas.")
            with right:
                st.subheader("Distribución de la solución")
                try:
                    values = [float(v) for v in report.solution]
                    if not all(math.isfinite(v) for v in values):
                        raise OverflowError
                    chart_data = pd.DataFrame({"Variable": [f"x{i+1}" for i in range(n)], "Valor": values,
                                               "Signo": ["Negativo" if v < 0 else "No negativo" for v in values]})
                    chart = alt.Chart(chart_data).mark_bar(cornerRadiusEnd=4).encode(
                        x=alt.X("Valor:Q", title="Miles de unidades" if report.production else "Valor"),
                        y=alt.Y("Variable:N", sort=None, title=None),
                        color=alt.Color("Signo:N", scale=alt.Scale(domain=["No negativo", "Negativo"], range=["#087968", "#B34D55"]), legend=None),
                        tooltip=["Variable", alt.Tooltip("Valor", format=".6g"), "Signo"],
                    ).properties(height=max(210, n * 30))
                    st.altair_chart(chart, width="stretch")
                except OverflowError:
                    st.caption("La magnitud supera la escala del gráfico. Consulta los valores exactos de la tabla.")
        elif report.particular is not None:
            st.subheader("Familia de soluciones")
            st.latex("X = " + matrix_latex([[v] for v in report.particular]) + " + " + " + ".join(f"t_{{{i+1}}}" + matrix_latex([[v] for v in vector]) for i, vector in enumerate(report.nullspace)))
            st.caption("Parámetros reales libres: " + ", ".join(f"t{i+1} = x{col+1}" for i, col in enumerate(report.free_columns)))
        for text in report.interpretation[1:]:
            st.markdown(text)
        if report.production and report.solution is not None:
            st.subheader("Balance de recursos")
            ax = matvec(report.A, report.solution)
            resource_names = RESOURCES if techchip else [f"Recurso {i+1}" for i in range(n)]
            resource_units = UNITS if techchip else ["Unidad del recurso" for _ in range(n)]
            st.dataframe(pd.DataFrame([{"Recurso": name, "Unidad": unit, "Disponible B": str(b), "Consumo algebraico AX": str(v), "Diferencia": str(v-b)} for name, unit, b, v in zip(resource_names, resource_units, report.B, ax)]), hide_index=True)
            if any(v < 0 for v in report.solution):
                st.caption("Este balance algebraico requiere producción negativa; no representa un consumo físicamente realizable.")
    with tab_steps:
        options = ["diagnosis"] + list(report.methods)
        labels = {"diagnosis": "Diagnóstico", **METHOD_LABELS}
        selected = st.selectbox("Método", options, format_func=labels.get, key="method")
        if selected == "diagnosis":
            steps = report.diagnostic_steps
            st.caption("El determinante se obtiene de los pivotes y los intercambios; los rangos cuentan ecuaciones independientes.")
        else:
            guide = METHOD_GUIDES[selected]
            st.markdown(guide["summary"])
            st.latex(guide["formula"])
            steps = report.methods[selected].steps
        render_steps(steps, selected)
        if st.session_state.get(f"view_{selected}") == "Paso a paso":
            render_step_tutor(report, title, note, selected, st.session_state.get(f"step_{selected}", 1) - 1)
    with tab_verify:
        if report.solution is not None:
            st.success("Los tres métodos coinciden exactamente. Todos los errores por componente son menores que 10⁻⁶.")
            st.dataframe(pd.DataFrame({"Variable": [f"x{i+1}" for i in range(n)], **{m.name: [str(v) for v in m.solution] for m in report.methods.values()}}), hide_index=True)
            st.subheader("Sustitución directa, fila por fila")
            for text in report.substitution:
                st.code(text, language=None, wrap_lines=True)
            inverse = report.methods["inverse"].inverse
            with st.expander("Matriz inversa calculada"):
                st.latex(r"A^{-1}=" + matrix_latex(inverse))
            st.caption("El error es cero en aritmética racional para los datos introducidos. Los valores decimales mostrados están redondeados.")
        else:
            st.markdown(f"**det(A) = 0**. Rango de A: **{report.rank_A}**. Rango aumentado: **{report.rank_augmented}**.")
            st.markdown("La existencia de una fila 0 = c, con c ≠ 0, demuestra incompatibilidad." if report.status == "inconsistent" else f"Hay {n-report.rank_A} variables libres. Se verifica A·Xₚ = B y A·v = 0 para cada vector de la familia.")
    with tab_exports:
        st.subheader("Un análisis que puedes revisar y compartir")
        st.caption("Cada informe incluye entradas, diagnóstico, operaciones de fila, matrices intermedias, sustitución y conclusiones.")
        with st.container(horizontal=True):
            st.download_button("Informe HTML / imprimir PDF", html_report(report, title=title, note=note), "analisis_techchip.html", "text/html", icon=":material/description:")
            st.download_button("Procedimiento Markdown", markdown_report(report, title=title, note=note), "procedimiento.md", "text/markdown", icon=":material/download:")
            st.download_button("Resultados JSON", json.dumps({"title": title, "note": note, **report.to_dict()}, ensure_ascii=False, indent=2), "resultado.json", "application/json", icon=":material/data_object:")
            st.download_button("Datos de entrada JSON", json.dumps(json_ready({"A": report.A, "B": report.B}), indent=2), "sistema.json", "application/json")
        st.caption("Para un PDF de este cálculo, abre el HTML descargado y selecciona Imprimir → Guardar como PDF.")
    with tab_tutor:
        render_tutor(report, title, note)


with st.sidebar:
    st.image(str(ROOT / "assets/logo.svg"), width=245)
    st.caption("ANÁLISIS MATRICIAL EXPLICABLE")
    page = st.radio("Espacio de trabajo", ["Calculadora", "Guía de métodos", "Validación del parcial"], key="page")
    st.space("large")
    st.markdown("**De los datos a la evidencia**")
    st.caption("1. Define tu sistema\n\n2. Compara tres métodos\n\n3. Revisa cada operación\n\n4. Exporta el análisis")
    st.space("large")
    st.badge("Cálculo racional exacto", color="green", icon=":material/verified:")
    st.caption("Cálculo local · Tutor IA opcional\n\nMatrices de 1 × 1 a 12 × 12\n\nOperaciones exactas y explicaciones guiadas")

if page == "Calculadora":
    st.caption("TECHCHIP SYSTEMS / LABORATORIO DE DECISIONES")
    st.title("Cada resultado, con su procedimiento.")
    st.markdown("Resuelve sistemas lineales, contrasta tres métodos y entiende qué significan los resultados.")
    st.header("01 · Define el sistema")
    source = st.segmented_control("Origen de los datos", ["Escenarios", "Matriz propia", "Importar JSON"], default="Escenarios", key="source", on_change=clear_result)
    source = source or "Escenarios"
    techchip, production, note = False, False, ""
    title = "Sistema personalizado"
    if source == "Escenarios":
        scenario = st.selectbox("Escenario", list(SCENARIOS), format_func=lambda key: SCENARIOS[key][0], key="scenario", on_change=clear_result)
        A, B = get_scenario(scenario)
        title, note = SCENARIOS[scenario]
        st.caption(note)
        techchip = scenario != "example"
        production = techchip
        if techchip:
            with st.expander("Discrepancia en los datos de la guía", expanded=scenario == "original"):
                st.warning(GUIDE_NOTE)
                st.caption("Unidades del modelo: cada x está en miles de unidades; los coeficientes se interpretan como consumo por cada mil módulos.")
            note += " " + GUIDE_NOTE
    elif source == "Matriz propia":
        n = st.number_input("Número de ecuaciones e incógnitas", min_value=1, max_value=MAX_SIZE, value=3, step=1, key="dimension", on_change=clear_result)
        A = [[int(i == j) for j in range(n)] for i in range(n)]
        B = [1] * n
    if not techchip:
        production = st.toggle("Interpretar como producción (miles de unidades)", value=False, key="production", on_change=clear_result,
                               help="Activa X ≥ 0 como condición de viabilidad. En modo matemático las soluciones negativas son válidas.")
    with st.form("system_form", border=True):
        if source == "Importar JSON":
            st.caption('Formato: {"A": [[2, 1], [1, -1]], "B": [5, 1]}. Usa "1/3" para fracciones exactas.')
            uploaded = st.file_uploader("Cargar archivo JSON (máximo 100 kB de contenido)", type=["json"], key="json_file")
            raw = st.text_area("O pega tu JSON", value='{"A": [[2, 1], [1, -1]], "B": [5, 1]}', height=150, key="json_text")
            st.caption("Si cargas un archivo se utilizará su contenido en lugar del texto.")
        else:
            columns = [f"x{i+1}" for i in range(len(A))] + ["B"]
            table = pd.DataFrame([[str(v) for v in row] + [str(b)] for row, b in zip(A, B)], columns=columns,
                                 index=[f"F{i+1}" for i in range(len(A))])
            st.markdown("**Matriz A y vector B**")
            st.caption("Edita cualquier celda. Se admiten enteros, decimales con punto y fracciones: 2, −1.5, 3/4.")
            editor_key = f"editor_{source}_{scenario if source == 'Escenarios' else len(A)}"
            edited = st.data_editor(table, key=editor_key, height="content", width="stretch")
        submitted = st.form_submit_button("Resolver sistema", icon=":material/play_arrow:", type="primary", width="stretch")
    if submitted:
        clear_result()
        try:
            if source == "Importar JSON":
                if uploaded is not None and uploaded.size > 100_000:
                    raise InputError("El JSON no puede superar 100 kB.")
                text = uploaded.getvalue().decode("utf-8-sig") if uploaded is not None else raw
                inputs_A, inputs_B = parse_json(text)
            else:
                inputs_A, inputs_B = validate_input(edited.iloc[:, :-1].values.tolist(), edited.iloc[:, -1].tolist())
                if source == "Escenarios" and (inputs_A != A or inputs_B != B):
                    title += " · modificado"
                    note = "Datos editados por el usuario a partir de: " + note
            with st.spinner("Validando, resolviendo y verificando los tres métodos…"):
                report = analyze_cached(inputs_A, inputs_B, production)
            st.session_state.report = report
            st.session_state.report_title = title
            st.session_state.report_note = note
            st.session_state.report_techchip = techchip
            for key in list(st.session_state):
                if key.startswith("step_"):
                    del st.session_state[key]
        except (InputError, UnicodeError) as exc:
            st.error(str(exc), icon=":material/error:")
    if "report" in st.session_state:
        render_results(st.session_state.report, st.session_state.report_title, st.session_state.report_note, st.session_state.report_techchip)
    else:
        with st.container(border=True):
            st.subheader("Un sistema. Tres caminos para comprobarlo.")
            cols = st.columns(3)
            for col, (key, label) in zip(cols, METHOD_LABELS.items()):
                with col:
                    st.markdown(f"**{label}**")
                    st.caption(METHOD_GUIDES[key]["summary"])
        st.caption("El análisis aparecerá aquí al resolver. Ningún dato se sustituye para forzar un resultado.")

elif page == "Guía de métodos":
    st.caption("BIBLIOTECA / FUNDAMENTOS")
    st.title("Entiende el camino, no solo la respuesta.")
    st.markdown("Los tres métodos conservan las soluciones mediante operaciones elementales sobre las filas.")
    st.latex(r"AX=B\qquad A\in\mathbb{R}^{n\times n},\quad X,B\in\mathbb{R}^{n}")
    with st.container(border=True):
        st.subheader("Las tres operaciones permitidas")
        st.latex(r"F_i\leftrightarrow F_j\qquad F_i\leftarrow kF_i\;(k\ne0)\qquad F_i\leftarrow F_i+kF_j")
        st.caption("Intercambiar ecuaciones, multiplicar por un número no nulo o sumar un múltiplo de otra fila mantiene el conjunto de soluciones.")
    for key, guide in METHOD_GUIDES.items():
        with st.container(border=True):
            st.subheader(METHOD_LABELS[key])
            st.markdown(guide["summary"])
            st.latex(guide["formula"])
            st.markdown("\n".join(f"{i}. {step}" for i, step in enumerate(guide["stages"], 1)))
    st.subheader("Cómo distinguir los tres diagnósticos")
    st.table(pd.DataFrame({"Condición": ["rango(A) = rango([A|B]) = n", "rango(A) = rango([A|B]) < n", "rango(A) < rango([A|B])"], "Conclusión": ["Solución única; det(A) ≠ 0", "Infinitas soluciones; det(A) = 0", "Sin solución; det(A) = 0"]}))
    st.caption("El pivoteo parcial elige el mayor valor absoluto de la columna disponible. La inversa comparte operaciones con Gauss-Jordan, pero actúa sobre [A|I] y después multiplica por B.")
    st.subheader("Fuentes consultadas")
    for name, url in REFERENCES:
        st.markdown(f"[{name}]({url})")
    st.caption("Explicaciones originales resumidas a partir de material docente de MIT OpenCourseWare. Consulta: 19 de septiembre de 2026.")

else:
    st.caption("CONTROL DE CALIDAD / PARCIAL 2")
    st.title("La evidencia detrás del resultado.")
    st.warning(GUIDE_NOTE)
    st.dataframe(pd.DataFrame({"Recurso": RESOURCES, "B de la guía": B_GUIDE, "A·X esperado": B_TARGET, "Diferencia": [a-b for a, b in zip(B_TARGET, B_GUIDE)]}), hide_index=True)
    st.markdown("**No se puede cumplir simultáneamente el B original y el vector esperado.** Debe aclararse cuál dato corregir con el docente. La aplicación conserva ambos escenarios.")
    st.caption("También se explicita el consumo por mil módulos para que las unidades sean coherentes con X.")
    if st.button("Ejecutar batería de validación", type="primary", icon=":material/fact_check:"):
        st.session_state.validation = validation_battery()
    if "validation" in st.session_state:
        result = st.session_state.validation
        if result["all_passed"]:
            st.success("6 escenarios verificados, incluida la discrepancia del enunciado.")
        else:
            st.error("Hay una discrepancia en la batería de validación.")
        st.dataframe(pd.DataFrame([{"Escenario": SCENARIOS[k][0], "Verificado": r["passed"], "Diagnóstico": STATUS_LABELS[r["status"]], "det(A)": r["determinant"], "Rangos": f"{r['rank_A']} / {r['rank_augmented']}", "Error máximo": r["error_max"] or "No aplica"} for k, r in result["scenarios"].items()]), hide_index=True)
        st.download_button("Descargar bitácora JSON", json.dumps(result, ensure_ascii=False, indent=2), "validacion.json", "application/json")
    st.subheader("Alcance del proyecto")
    st.markdown("El agente explica decisiones mediante reglas verificables y aritmética exacta. Funciona sin un modelo generativo ni servicios propietarios. Es una herramienta de balance de igualdades; no incorpora una función objetivo de optimización industrial.")
    pdf = ROOT / "docs/informe_tecnico.pdf"
    if pdf.exists():
        st.download_button("Informe técnico del parcial (PDF)", pdf.read_bytes(), "informe_tecnico.pdf", "application/pdf", icon=":material/picture_as_pdf:")
