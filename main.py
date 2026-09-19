"""CLI portable: python main.py --help. No necesita paquetes externos."""
import argparse
import json
from pathlib import Path
import sys
from agent import InputError, MAX_JSON_BYTES, MAX_SIZE, TechChipAgent, json_ready, matvec, parse_json, validate_input
from reporting import html_report, markdown_report
from scenarios import GUIDE_NOTE, SCENARIOS, X_TARGET, get_scenario


def validation_battery() -> dict:
    agent = TechChipAgent()
    results = {}
    for key in SCENARIOS:
        A, B = get_scenario(key)
        report = agent.analyze(A, B, production=key != "example")
        expected_status = "inconsistent" if key == "singular" else "infinite" if key == "infinite" else "unique"
        passed = report.status == expected_status
        if report.solution is not None:
            passed = passed and report.methods_agree and report.max_error == 0
        if key == "compatible":
            passed = passed and report.solution == X_TARGET
        if key in ("original", "scarcity"):
            passed = passed and any(x < 0 for x in report.solution)
        if key == "infinite":
            passed = passed and matvec(report.A, report.particular) == report.B
            passed = passed and all(not any(matvec(report.A, v)) for v in report.nullspace)
        results[key] = {"passed": passed, "status": report.status, "determinant": str(report.determinant),
                        "rank_A": report.rank_A, "rank_augmented": report.rank_augmented,
                        "solution": json_ready(report.solution), "error_max": json_ready(report.max_error)}
    return {"all_passed": all(r["passed"] for r in results.values()), "guide_note": GUIDE_NOTE, "scenarios": results}


def interactive_input():
    try:
        n = int(input(f"Número de incógnitas (1–{MAX_SIZE}): "))
        if not 1 <= n <= MAX_SIZE:
            raise InputError(f"El tamaño debe estar entre 1 y {MAX_SIZE}.")
        print("Escribe cada fila separando valores con espacios; se admiten fracciones como 1/3.")
        A = [input(f"Fila {i + 1} de A: ").split() for i in range(n)]
        B = input(f"Vector B ({n} valores): ").split()
        return validate_input(A, B)
    except (EOFError, ValueError) as exc:
        raise InputError(f"Entrada incompleta o inválida: {exc}") from exc


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="TechChip Matrix Studio — Gauss, Gauss-Jordan e inversa con pasos exactos.")
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--scenario", choices=SCENARIOS, default=None, help="Caso de ejemplo; por defecto: original.")
    sources.add_argument("--input", metavar="ARCHIVO", help="JSON con A y B; usa - para entrada estándar.")
    sources.add_argument("--interactive", action="store_true", help="Introducir el sistema por consola.")
    sources.add_argument("--validate", action="store_true", help="Ejecutar la batería de escenarios de la guía.")
    parser.add_argument("--production", action="store_true", help="Interpretar una entrada propia como producción en miles de unidades.")
    parser.add_argument("--format", choices=["markdown", "json", "html"], default="markdown")
    parser.add_argument("--summary", action="store_true", help="Omitir los pasos en la salida Markdown.")
    parser.add_argument("--output", type=Path, help="Guardar el resultado en un archivo UTF-8.")
    args = parser.parse_args(argv)
    try:
        if args.validate:
            battery = validation_battery()
            output = json.dumps(battery, ensure_ascii=False, indent=2)
            code = 0 if battery["all_passed"] else 1
        else:
            note, title = "", "Sistema personalizado"
            production = args.production
            if args.input:
                if args.input == "-":
                    text = sys.stdin.read(MAX_JSON_BYTES + 1)
                else:
                    with Path(args.input).open(encoding="utf-8") as handle:
                        text = handle.read(MAX_JSON_BYTES + 1)
                A, B = parse_json(text)
            elif args.interactive:
                A, B = interactive_input()
            else:
                key = args.scenario or "original"
                A, B = get_scenario(key)
                title, scenario_note = SCENARIOS[key]
                note = scenario_note + (" " + GUIDE_NOTE if key != "example" else "")
                production = key != "example"
            report = TechChipAgent().analyze(A, B, production=production)
            if args.format == "json":
                output = json.dumps({"title": title, "note": note, **report.to_dict()}, ensure_ascii=False, indent=2)
            elif args.format == "html":
                output = html_report(report, title=title, note=note)
            else:
                output = markdown_report(report, title=title, note=note, full=not args.summary)
            code = 0
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output + "\n", encoding="utf-8")
            print(f"Informe guardado: {args.output}", file=sys.stderr)
        else:
            print(output)
        return code
    except (InputError, OSError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
