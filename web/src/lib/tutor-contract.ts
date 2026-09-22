import type { Analysis, Matrix, Step } from "../types/analysis"

export type TutorStep = { titulo: string; que: string; por_que: string; ref_paso: number | null }
export type TutorAnswer = { resumen: string; pasos: TutorStep[]; conclusion: string; fuera_de_tema: boolean }
export type TutorSource = "model" | "engine"
export type TutorAction = "step" | "pivot" | "verify" | "method"
export type TutorToken =
  | { kind: "text"; text: string }
  | { kind: "value"; label: string; value: string; approximate: boolean }
  | { kind: "matrix"; matrix: Matrix; split: number }

const markerPattern = /\{\{([^{}]+)\}\}/g
const maxSteps = 96

export function methodSteps(report: Analysis, method: string): Step[] {
  return method === "diagnosis" ? report.diagnostic_steps : report.methods[method]?.steps || report.diagnostic_steps
}

export function resolveTutorMarker(marker: string, report: Analysis, method: string): TutorToken | null {
  if (marker === "det") return { kind: "value", label: "det(A)", value: report.determinant, approximate: true }
  if (marker === "rango_A") return { kind: "value", label: "rango(A)", value: String(report.rank_A), approximate: false }
  if (marker === "rango_aug") return { kind: "value", label: "rango([A|B])", value: String(report.rank_augmented), approximate: false }
  const variable = /^x([1-9]\d*)$/.exec(marker)
  if (variable) {
    const value = report.solution?.[Number(variable[1]) - 1]
    return value === undefined ? null : { kind: "value", label: `x${variable[1]}`, value, approximate: true }
  }
  const stepMatch = /^(pivote|factor|matriz):paso([1-9]\d*)$/.exec(marker)
  const rowMatch = /^fila:paso([1-9]\d*):([1-9]\d*)$/.exec(marker)
  const steps = methodSteps(report, method)
  if (stepMatch) {
    const step = steps[Number(stepMatch[2]) - 1]
    if (!step) return null
    if (stepMatch[1] === "matriz") return { kind: "matrix", matrix: step.matrix, split: step.split }
    if (stepMatch[1] === "factor") return step.factor === null ? null : { kind: "value", label: "factor", value: step.factor, approximate: true }
    const pivot = step.pivot
    if (!pivot || step.matrix[pivot[0]]?.[pivot[1]] === undefined) return null
    return { kind: "value", label: "pivote", value: step.matrix[pivot[0]][pivot[1]], approximate: true }
  }
  if (rowMatch) {
    const step = steps[Number(rowMatch[1]) - 1]
    const row = step?.matrix[Number(rowMatch[2]) - 1]
    return row ? { kind: "matrix", matrix: [row], split: step.split } : null
  }
  return null
}

export function tokenizeTutorText(text: string, report: Analysis, method: string, warn: (message: string) => void = console.warn): TutorToken[] {
  const tokens: TutorToken[] = []
  let cursor = 0
  for (const match of text.matchAll(markerPattern)) {
    if (match.index > cursor) tokens.push({ kind: "text", text: text.slice(cursor, match.index) })
    const resolved = resolveTutorMarker(match[1], report, method)
    if (resolved) tokens.push(resolved)
    else warn(`Marcador del tutor desconocido: ${match[1]}`)
    cursor = match.index + match[0].length
  }
  if (cursor < text.length) tokens.push({ kind: "text", text: text.slice(cursor) })
  return tokens
}

function validText(text: unknown, limit: number, report: Analysis, method: string) {
  if (typeof text !== "string" || text.length > limit) return false
  for (const match of text.matchAll(markerPattern)) if (!resolveTutorMarker(match[1], report, method)) return false
  let clean = text.replace(markerPattern, "")
  if (clean.includes("{{") || clean.includes("}}")) return false
  const steps = methodSteps(report, method)
  for (const match of clean.matchAll(/\bpaso\s+([1-9]\d*)\b/gi)) if (Number(match[1]) > steps.length) return false
  clean = clean.replace(/\bpaso\s+[1-9]\d*\b/gi, "")
  return !/[\d\\$=^+*<>×÷·±≈√∑]/.test(clean) && !clean.includes("/")
}

export function validateModelAnswer(raw: unknown, report: Analysis, method: string): raw is TutorAnswer {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return false
  const answer = raw as Record<string, unknown>
  if (Object.keys(answer).sort().join() !== "conclusion,fuera_de_tema,pasos,resumen") return false
  if (typeof answer.fuera_de_tema !== "boolean" || !Array.isArray(answer.pasos) || answer.pasos.length > maxSteps) return false
  if (!validText(answer.resumen, 1600, report, method) || !validText(answer.conclusion, 1600, report, method)) return false
  if (answer.fuera_de_tema && answer.pasos.length) return false
  return answer.pasos.every((item: unknown) => {
    if (!item || typeof item !== "object" || Array.isArray(item)) return false
    const step = item as Record<string, unknown>
    if (Object.keys(step).sort().join() !== "por_que,que,ref_paso,titulo") return false
    const ref = step.ref_paso
    if (ref !== null && (typeof ref !== "number" || !Number.isInteger(ref) || ref < 1 || ref > methodSteps(report, method).length)) return false
    return validText(step.titulo, 200, report, method) && validText(step.que, 2400, report, method) && validText(step.por_que, 2400, report, method)
  })
}

function stepAnswer(step: Step, number: number): TutorStep {
  return { titulo: step.title || step.operation, que: step.what || step.operation, por_que: step.why || step.explanation, ref_paso: number }
}

export function engineTutorAnswer(report: Analysis, method: string, stepIndex?: number): TutorAnswer {
  const steps = methodSteps(report, method)
  if (stepIndex !== undefined && steps[stepIndex]) return {
    resumen: "Revisemos juntos la operación seleccionada.", pasos: [stepAnswer(steps[stepIndex], stepIndex + 1)],
    conclusion: "La matriz mostrada es el resultado exacto de este paso.", fuera_de_tema: false,
  }
  const resumen = report.status === "unique" ? "El sistema tiene solución única." : report.status === "infinite" ? "El sistema tiene infinitas soluciones." : "El sistema no tiene solución."
  return { resumen, pasos: steps.map((step, index) => stepAnswer(step, index + 1)), conclusion: report.interpretation[0] || resumen, fuera_de_tema: false }
}

export function actionTutorAnswer(report: Analysis, method: string, action: TutorAction, stepIndex = 0): TutorAnswer {
  const steps = methodSteps(report, method)
  const current = steps[Math.min(stepIndex, steps.length - 1)]
  if (action === "step" && current) return engineTutorAnswer(report, method, stepIndex)
  if (action === "pivot" && current) {
    const marker = current.pivot ? `{{pivote:paso${stepIndex + 1}}}` : ""
    return { resumen: marker ? `El pivote de este paso es ${marker}.` : "Este paso no necesita un pivote nuevo.", pasos: [stepAnswer(current, stepIndex + 1)], conclusion: current.why || "La operación conserva el procedimiento exacto.", fuera_de_tema: false }
  }
  if (action === "verify") return {
    resumen: report.solution ? "Comprueba cada fila del producto con el término independiente." : "El diagnóstico se comprueba comparando los rangos.",
    pasos: [], conclusion: report.solution && report.residual.every((value) => value === "0") ? "Todos los residuos exactos son cero." : report.interpretation[0] || "Consulta el diagnóstico del sistema.", fuera_de_tema: false,
  }
  return { resumen: `Procedimiento completo del método ${method === "diagnosis" ? "de diagnóstico" : report.methods[method]?.name || method}. Cada operación aparece en el orden en que fue ejecutada.`, pasos: steps.map((step, index) => stepAnswer(step, index + 1)), conclusion: report.interpretation[0] || "Revisa el resultado exacto.", fuera_de_tema: false }
}

export function plainTutorText(text: string, report: Analysis, method: string): string {
  return tokenizeTutorText(text, report, method).map((token) => token.kind === "text" ? token.text : token.kind === "value" ? `${token.label} = ${token.value}` : token.matrix.map((row) => `[${row.join(", ")}]`).join(" ")).join("")
}
