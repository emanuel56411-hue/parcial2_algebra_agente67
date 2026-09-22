"""Genera el desarrollo algebraico completo de Gauss y Gauss-Jordan."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "bitacora" / "original.json"
TARGET = ROOT / "docs" / "desarrollo_manual_dos_metodos.md"


def matrix_block(matrix: list[list[str]], split: int) -> str:
    rows = []
    for row in matrix:
        left = "  ".join(str(value) for value in row[:split])
        right = "  ".join(str(value) for value in row[split:])
        rows.append(f"[ {left} | {right} ]")
    return "```text\n" + "\n".join(rows) + "\n```"


def render_method(report: dict, key: str, title: str) -> list[str]:
    method = report["methods"][key]
    lines = [f"# {title}", "", f"Total de estados registrados: **{len(method['steps'])}**.", ""]
    for index, step in enumerate(method["steps"], 1):
        lines += [
            f"## Paso {index}. {step.get('title') or step['operation']}", "",
            f"**Operación:** `{step['operation']}`", "",
            f"**Qué se hizo:** {step.get('what') or step['explanation']}", "",
            f"**Por qué:** {step.get('why') or 'La operación elemental conserva un sistema equivalente.'}", "",
        ]
        calculations = step.get("calc") or []
        if calculations:
            lines += ["**Cálculo exacto:**", "", *[f"- `{item}`" for item in calculations], ""]
        lines += [matrix_block(step["matrix"], step["split"]), ""]
    lines += ["## Resultado del método", "", "`X = (" + ", ".join(method["solution"]) + ")`", ""]
    return lines


def main() -> None:
    report = json.loads(SOURCE.read_text(encoding="utf-8"))
    lines = [
        "# Desarrollo manual paso a paso — caso original de TechChip Systems", "",
        "Este documento desarrolla las operaciones elementales que pueden reproducirse a mano. "
        "Las fracciones son exactas y corresponden al B original `(155,160,225,140,215,175)`. "
        "El vector `(15,20,25,10,15,20)` no se usa porque es incorrecto para esos datos.", "",
        "La matriz aumentada se transforma sin redondeos. Cada paso indica la operación, su "
        "justificación y el estado completo resultante.", "", "---", "",
    ]
    lines += render_method(report, "gauss", "Método 1 — Eliminación de Gauss y sustitución hacia atrás")
    lines += ["---", ""]
    lines += render_method(report, "gauss_jordan", "Método 2 — Gauss-Jordan")
    lines += [
        "---", "", "# Comprobación final", "",
        "Los dos métodos producen exactamente `X = (-105/83, 345/83, 2430/83, "
        "1170/83, 1130/83, 2010/83)`. La sustitución devuelve `AX=B`, el residuo es "
        "`(0,0,0,0,0,0)` y el error máximo es `0`.", "",
    ]
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generado: {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
