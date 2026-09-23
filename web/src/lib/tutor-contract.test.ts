import { describe, expect, it, vi } from "vitest"
import { actionTutorAnswer, engineTutorAnswer, plainTutorText, resolveTutorMarker, tokenizeTutorText, validateModelAnswer } from "./tutor-contract"
import type { Analysis, Step } from "../types/analysis"

const first: Step = {
  operation: "F2 ← F2 − F1", explanation: "Conserva la equivalencia.",
  title: "Eliminar en la fila", what: "Resté las filas.", why: "Conserva el sistema.",
  matrix: [["1", "1", "3"], ["0", "-1/2", "-1/2"]], split: 2,
  kind: "add", target: 1, source: 0, factor: "-1", pivot: [0, 0],
  changed_rows: [1], calc: ["1 − 1 = 0"], decimals: {},
}
const report = {
  A: [["1", "1"], ["1", "1/2"]], B: ["3", "5/2"], determinant: "-1/2",
  rank_A: 2, rank_augmented: 2, status: "unique", diagnostic_steps: [first],
  methods: { gauss: { name: "Gauss", steps: [first], solution: ["2", "1"], inverse: null } },
  solution: ["2", "1"], residual: ["0", "0"], substitution: ["1·2 + 1·1 = 3"],
  particular: null, nullspace: [], free_columns: [], interpretation: ["Solución única."],
  production: false, variables: ["Producto A", "Producto B"], methods_agree: true, max_error: "0", format: "fraction",
} as Analysis
const good = { resumen: "La solución es {{x1}} y el determinante {{det}}.", pasos: [{ titulo: "Paso actual", que: "La matriz es {{matriz:paso1}}.", por_que: "El pivote es {{pivote:paso1}}.", ref_paso: 1 }], conclusion: "El rango es {{rango_A}}.", fuera_de_tema: false }

describe("marcadores del tutor", () => {
  it("resuelve cada valor exacto desde el motor", () => {
    expect(resolveTutorMarker("x1", report, "gauss")).toMatchObject({ kind: "value", value: "2" })
    expect(resolveTutorMarker("det", report, "gauss")).toMatchObject({ kind: "value", value: "-1/2" })
    expect(resolveTutorMarker("rango_A", report, "gauss")).toMatchObject({ value: "2" })
    expect(resolveTutorMarker("rango_aug", report, "gauss")).toMatchObject({ value: "2" })
    expect(resolveTutorMarker("factor:paso1", report, "gauss")).toMatchObject({ value: "-1" })
    expect(resolveTutorMarker("pivote:paso1", report, "gauss")).toMatchObject({ value: "1" })
    expect(resolveTutorMarker("matriz:paso1", report, "gauss")).toMatchObject({ kind: "matrix", matrix: first.matrix })
    expect(resolveTutorMarker("fila:paso1:2", report, "gauss")).toMatchObject({ kind: "matrix", matrix: [first.matrix[1]] })
  })
  it("elimina y registra un marcador desconocido", () => {
    const warn = vi.fn()
    expect(tokenizeTutorText("Antes {{inventado}} después", report, "gauss", warn)).toEqual([{ kind: "text", text: "Antes " }, { kind: "text", text: " después" }])
    expect(warn).toHaveBeenCalledOnce()
    expect(plainTutorText("{{det}}", report, "gauss")).toContain("-1/2")
  })
})

describe("validador y respaldo", () => {
  it("acepta texto breve con referencias existentes", () => expect(validateModelAnswer(good, report, "gauss")).toBe(true))
  it("descarta respuestas malformadas y conserva una explicación del motor", () => {
    const malformed: unknown[] = ["{bad json", { ...good, resumen: "Valor {{fantasma}}" }, { ...good, resumen: "La solución es 999" }, { ...good, resumen: "a".repeat(1601) }, { ...good, pasos: [{ ...good.pasos[0], ref_paso: 99 }] }, { ...good, resumen: "x = 2" }]
    for (const answer of malformed) {
      expect(validateModelAnswer(answer, report, "gauss")).toBe(false)
      expect(engineTutorAnswer(report, "gauss", 0).pasos[0].que).toBe(first.what)
    }
  })
  it("responde las cuatro acciones sin llamar al modelo", () => {
    for (const action of ["step", "pivot", "verify", "method"] as const) {
      const answer = actionTutorAnswer(report, "gauss", action, 0)
      expect(answer.fuera_de_tema).toBe(false)
      expect(answer.resumen.length).toBeGreaterThan(0)
    }
    expect(actionTutorAnswer(report, "gauss", "method").pasos).toHaveLength(report.methods.gauss.steps.length)
  })
})
