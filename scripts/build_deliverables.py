"""Genera ejemplos, bitácoras, procedimientos e informe PDF desde el mismo motor.

Uso: python scripts/build_deliverables.py
El PDF requiere reportlab; el resto se puede regenerar sin dependencias.
"""
from html import escape
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent import TechChipAgent, decimal_text
from main import validation_battery
from reporting import REFERENCES, markdown_report, matrix_text
from scenarios import GUIDE_NOTE, PRODUCTS, RESOURCES, SCENARIOS, UNITS, get_scenario


def technical_pdf(reports):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Table, TableStyle, Preformatted, PageBreak, NextPageTemplate, KeepTogether, FrameBreak

    width, height = letter
    margin, gutter = 45, 18
    column = (width - 2*margin - gutter)/2
    doc = BaseDocTemplate(str(ROOT / "docs/informe_tecnico.pdf"), pagesize=letter,
                          title="TechChip Systems: análisis matricial exacto y explicable", author="Proyecto TechChip Matrix Studio")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("Paper", fontName="Times-Roman", fontSize=9, leading=12, spaceAfter=6, alignment=4))
    styles.add(ParagraphStyle("PaperTitle", fontName="Times-Bold", fontSize=18, leading=21, spaceAfter=12))
    styles.add(ParagraphStyle("PaperHeading", fontName="Times-Bold", fontSize=10, leading=13, spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle("AppendixHeading", fontName="Times-Bold", fontSize=13, leading=16, spaceAfter=8))
    def footer(canvas, document):
        canvas.setStrokeColor(colors.HexColor("#DCE7E2"))
        canvas.line(margin, 34, width-margin, 34)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(margin, 22, "TechChip Matrix Studio | Parcial 2 - Algebra Lineal | 22 septiembre 2026")
        canvas.drawRightString(width-margin, 22, str(document.page))
    frames = [Frame(margin, 45, column, height-90, id="left"), Frame(margin+column+gutter, 45, column, height-90, id="right")]
    first_frames = [Frame(margin, height-135, width-2*margin, 90, id="title"),
                    Frame(margin,45,column,height-183,id="first-left"),
                    Frame(margin+column+gutter,45,column,height-183,id="first-right")]
    doc.addPageTemplates([PageTemplate(id="first", frames=first_frames, onPage=footer, autoNextPageTemplate="paper"),
                          PageTemplate(id="paper", frames=frames, onPage=footer),
                          PageTemplate(id="appendix", frames=[Frame(margin,45,width-2*margin,height-90,id="full")], onPage=footer)])
    replacements = {"←":"<-", "↔":"<->", "→":"->", "−":"-", "·":"*", "⁻¹":"^-1", "ₚ":"p", "₁":"1", "₂":"2", "₃":"3", "₆":"6", "⁻⁶":"^-6", "≥":">=", "≠":"!=", "≈":"~", "…":"...", "×":"x", "≤":"<=", "₄":"4", "₅":"5"}
    def safe(text):
        for old, new in replacements.items():
            text = text.replace(old, new)
        return escape(text)
    def p(text, style="Paper"):
        return Paragraph(safe(text), styles[style])
    def heading(text):
        return p(text, "PaperHeading")
    def matrix(M, split, available):
        text = matrix_text(M, split)
        size = min(8, (available-16)/(max(map(len,text.splitlines()))*0.60))
        style = ParagraphStyle("Matrix", fontName="Courier", fontSize=size, leading=size*1.35, spaceAfter=8)
        return Preformatted(text, style)
    def table(rows, widths):
        t = Table([[p(str(cell)) for cell in row] for row in rows], colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EAF2EE")),("LINEBELOW",(0,0),(-1,0),0.5,colors.HexColor("#087968")),("VALIGN",(0,0),(-1,-1),"TOP"),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        return t
    original = reports["original"]
    story = [p("TechChip Systems: balance de recursos con álgebra lineal exacta", "PaperTitle"),
             p("Documento técnico del Parcial 2. Ingeniería en Inteligencia Artificial y Telecomunicaciones. Diseño de artículo a dos columnas inspirado en IEEE; no es una publicación de IEEE ni usa su plantilla oficial."), FrameBreak(),
             heading("Resumen"),
             p("Se implementa un agente explicable para analizar sistemas cuadrados AX = B mediante Gauss, Gauss-Jordan e inversa. Los algoritmos registran operaciones elementales y usan números racionales exactos. El caso industrial 6 x 6 tiene determinante -83, pero su solución con las capacidades originales contiene una variable negativa. Se demuestra que el vector indicado por la guía es incorrecto para ese B, sin modificar silenciosamente los datos. La solución se ofrece por consola y web con exportaciones reproducibles y un tutor opcional de IA."),
             p("Palabras clave: sistemas lineales; pivoteo parcial; rango; balance de recursos; trazabilidad."),
             heading("I. Modelado y unidades"),
             p("Cada xj representa miles de módulos por turno. Las filas son recursos y las columnas, líneas de producción. Para que las unidades sean coherentes, aij se interpreta como unidades del recurso i por cada mil módulos j. La frase 'por unidad' del enunciado debe aclararse con el docente si se refiere a módulos individuales. El modelo continuo permite fracciones; no impone producción entera."),
             table([["Variable", "Producto"]]+[[f"x{i+1}", name] for i,name in enumerate(PRODUCTS)], [50,column-62]),
             p("El balance completo por turno es AX = B. La matriz aumentada conserva las seis disponibilidades originales:"),
             matrix([row+[b] for row,b in zip(original.A, original.B)],6,column-12),
             table([["Recurso", "Unidad"]]+list(zip(RESOURCES, UNITS)), [column*.60-6,column*.40-6]),
             heading("II. Auditoría del enunciado"), p(GUIDE_NOTE),
             p("La diferencia A X esperado - B original es (30, 40, 55, 10, 30, 20). Por ello la prueba que exige el vector (15,20,25,10,15,20) no puede pasar con el B original. Se conserva un escenario separado con B compatible, sin presentarlo como el original."),
             heading("III. Métodos algebraicos"),
             p("Gauss transforma [A|B] en [U|C] anulando entradas bajo los pivotes. Se intercambian filas para seleccionar el mayor pivote absoluto de la columna disponible. La sustitución inversa despeja xi = (ci - suma de uij*xj para j>i)/uii [1]."),
             p("Gauss-Jordan normaliza cada pivote a 1 y elimina la columna tanto arriba como abajo. Si hay n pivotes, la matriz final es [I|X]. Las operaciones elementales son reversibles y conservan el conjunto solución [2]."),
             p("La inversa se calcula por reducción de [A|I] a [I|A^-1], independientemente de B. Cada xi es el producto de la fila i de A^-1 con B [2]. No se usan numpy.linalg.solve, inv, det ni matrix_rank en el motor."),
             p("El determinante es (-1)^s multiplicado por los pivotes de U, con s intercambios. Las sumas de filas no lo alteran. Si falta un pivote, det(A)=0. El rango de A cuenta pivotes; una fila [0,...,0|c] con c distinto de 0 aumenta en 1 el rango de [A|B]."),
             p("Si ambos rangos son n hay una solución; si son iguales y menores que n hay variables libres; si difieren el sistema es incompatible. Para el caso indeterminado se construye X = Xp + suma ti*vi, con A Xp = B y A vi = 0 [3]."),
             heading("IV. Arquitectura y entradas"),
             p("El agente aplica el ciclo validar, diagnosticar, resolver, verificar y explicar. agent.py contiene los algoritmos, exercise_parser.py convierte de forma segura ecuaciones, JSON o bloques A/B, scenarios.py conserva los datos, main.py expone la CLI y api/solve.py atiende la web React. El Tutor IA de OpenAI es opcional: el servidor recalcula el contexto y el motor exacto sigue siendo la única fuente de cifras."),
             p("La interfaz y el motor admiten dimensiones de 1 x 1 a 12 x 12. Se aceptan vectores planos o columna, enteros, decimales, notación científica y fracciones. Se rechazan dimensiones incorrectas, expresiones no lineales, código, valores vacíos, NaN, infinitos y división por cero. No existe un límite artificial de palabras; permanece un límite técnico de 2 MB por solicitud."),
             p("Fraction opera exactamente sobre los racionales introducidos; los decimales JSON se leen con Decimal. La presentación decimal es aproximada y no interviene en las pruebas. Esta elección favorece sistemas educativos pequeños: las operaciones de eliminación son O(n^3), pero el costo de las fracciones crece con sus dígitos. El historial completo puede ocupar O(n^4) celdas."),
             heading("V. Validación y resultados"),
             table([["Escenario", "Rangos", "Estado"]]+[[key, f"{r.rank_A}/{r.rank_augmented}", {"unique":"Única","infinite":"Infinitas","inconsistent":"Incompatible"}[r.status]] for key,r in reports.items()], [column*.30,column*.20,column*.50-12]),
             p("Los escenarios original, compatible y escasez tienen det(A)=-83. Cada método produce exactamente el mismo X y el error E=|AX-B| es el vector cero; cada componente cumple E<10^-6. Se comprueban además pivotes nulos, matrices cero, signos de determinante, entradas inválidas y determinantes pequeños no nulos."),
             p("Las pruebas reproducen cada operación de fila y contrastan determinantes pequeños con la definición por permutaciones, independiente del algoritmo. Se verifican A*A^-1=I y A^-1*A=I, así como sistemas de tamaños 1,2,3,6,12 construidos con soluciones conocidas. Los recorridos web prueban edición, JSON, cambio de método y eliminación de resultados obsoletos."),
             heading("VI. Interpretación operacional"),
             p("Con B original: X=(-105,345,2430,1170,1130,2010)/83. En particular x1=-1.265060 miles: no existe un plan no negativo que agote simultáneamente las seis capacidades. Redondear o reemplazar ese valor por cero destruiría el balance."),
             p("Con B compatible: X=(15,20,25,10,15,20), un total de 105 mil módulos. Las seis capacidades se consumen al 100% dentro del modelo continuo; esta disponibilidad es una variante, no el dato original."),
             p("Con resina B3=100 y las demás capacidades originales: X=(-26355,-6780,18555,3170,3505,6510)/83. Las líneas 1 y 2 son negativas: plan inalcanzable por la restricción de materias primas bajo el balance de igualdades. Esto no prueba que sea imposible producir dejando recursos ociosos."),
             p("Al fijar F6=2F1 y conservar B6=175 aparece la contradicción B6 != 2B1=310: rangos 5 y 6, cero soluciones. Si también se fija B6=310, los rangos son 5 y 5 y existe una familia con una variable libre. La aplicación no inventa una solución única ni una inversa."),
             heading("VII. Alcance y uso empresarial"),
             p("El valor del prototipo es la trazabilidad: entradas visibles, escenarios comparables, cálculo reproducible e informes auditables. Resolver igualdades no optimiza beneficios, costos o tiempos. No hay datos suficientes para una función objetivo; llamar 'óptima' a toda solución positiva sería incorrecto."),
             p("Una implantación empresarial exigiría validar unidades y datos reales, decidir si se permite capacidad ociosa, modelar costos/demanda, conectar fuentes de datos y acordar controles de acceso, persistencia y operación. Estas extensiones no se presentan como implementadas. El proyecto actual es una demostración funcional y una base para un piloto."),
             heading("VIII. Reproducción y entrega"),
             p("python main.py --validate ejecuta la batería. python -m unittest discover -s tests -v ejecuta las 60 pruebas Python; npm test, npm run lint y npm run build validan el frontend. python scripts/build_deliverables.py regenera ejemplos, bitácora, procedimientos y este PDF (requiere reportlab)."),
             p("Los anexos contienen el desarrollo algebraico completo por Gauss y Gauss-Jordan del sistema original mediante operaciones verificables a mano. Son trazas generadas y comprobadas por software, no evidencia de escritura manuscrita independiente. Si la rúbrica exige hojas manuscritas físicas, deben elaborarse y contrastarse con estas trazas."),
             heading("Referencias")]
    for i,(name,url) in enumerate(REFERENCES,1):
        story.append(p(f"[{i}] {name}. Material docente, 18.06SC Linear Algebra, MIT OpenCourseWare. Consulta: 19/09/2026."))
        story.append(Paragraph(f'<link href="{escape(url, quote=True)}" color="#087968">Consultar fuente primaria en MIT OpenCourseWare</link>', styles["Paper"]))
    story += [NextPageTemplate("appendix"), PageBreak(), p("Anexo A. Diagnóstico y determinante del caso original", "AppendixHeading"), p("Cada matriz se muestra después de la operación indicada. Las barras separan coeficientes y términos independientes. Los valores son racionales exactos.")]
    sequences = [("Diagnóstico", original.diagnostic_steps),
                 (original.methods["gauss"].name, original.methods["gauss"].steps),
                 (original.methods["gauss_jordan"].name, original.methods["gauss_jordan"].steps)]
    for section,(name,steps) in enumerate(sequences):
        if section:
            story += [PageBreak(), p(f"Anexo {chr(65+section)}. {name}: desarrollo completo", "AppendixHeading")]
        for i, step in enumerate(steps,1):
            story.append(KeepTogether([p(f"Paso {i}. {step.operation}", "PaperHeading"), p(step.explanation), matrix(step.matrix,step.split,width-2*margin-12)]))
    story += [PageBreak(), p("Anexo D. Sustitución y comparación de escenarios", "AppendixHeading")]
    for key, report in reports.items():
        story.append(heading(SCENARIOS[key][0]))
        for item in report.interpretation:
            story.append(p(item))
        if report.solution is not None:
            story.append(p("X = (" + ", ".join(map(str,report.solution)) + ")"))
            for substitution in report.substitution:
                story.append(p(substitution))
        if report.particular is not None:
            story.append(p("Xp = ("+", ".join(map(str,report.particular))+")"))
            for i,v in enumerate(report.nullspace):
                story.append(p(f"v{i+1} = ("+", ".join(map(str,v))+")"))
            story.append(p("X = Xp + t1*v1; t1 real."))
    doc.build(story)


def main():
    for directory in ["examples", "docs", "docs/logs"]:
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    reports = {}
    for key in SCENARIOS:
        A, B = get_scenario(key)
        (ROOT / f"examples/{key}.json").write_text(json.dumps({"A": A, "B": B}, indent=2)+"\n", encoding="utf-8")
        reports[key] = TechChipAgent().analyze(A, B, production=key!="example")
        (ROOT / f"docs/logs/{key}.md").write_text(markdown_report(reports[key], title=SCENARIOS[key][0], note=SCENARIOS[key][1]+(" "+GUIDE_NOTE if key!="example" else "")), encoding="utf-8")
    battery = validation_battery()
    (ROOT / "docs/logs/validation.json").write_text(json.dumps(battery, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    lines = ["# Interpretación de operaciones — TechChip Systems", "", GUIDE_NOTE, ""]
    for key, report in reports.items():
        if key == "example":
            continue
        lines += ["## " + SCENARIOS[key][0], "", *report.interpretation, ""]
        if report.solution:
            lines += ["| Producto | Miles de módulos (exacto) | Aproximación |", "|---|---:|---:|"]
            lines += [f"| {name} | {v} | {decimal_text(v)} |" for name,v in zip(PRODUCTS, report.solution)]
            lines += ["", f"E = ({', '.join(map(str, report.residual))}); error máximo = {report.max_error}.", ""]
    lines += ["## Decisión recomendada", "", "Usar las disponibilidades originales B = (155, 160, 225, 140, 215, 175) como caso principal y registrar como incorrecto el vector indicado en la guía. En un contexto industrial, si se permiten capacidades ociosas, modelar AX ≤ B con X ≥ 0 e incorporar demanda y una función objetivo. No sustituir producciones negativas por cero: se perderían las igualdades. Las cantidades continuas en miles tampoco garantizan una solución en unidades enteras.", ""]
    (ROOT / "docs/interpretacion_operaciones.md").write_text("\n".join(lines), encoding="utf-8")
    try:
        technical_pdf(reports)
        print("PDF generado: docs/informe_tecnico.pdf")
    except ImportError:
        print("PDF omitido: instala reportlab para generarlo.", file=sys.stderr)
    print("Ejemplos, bitácoras y conclusiones regenerados. Escenarios verificados:", battery["all_passed"])


if __name__ == "__main__":
    main()
