import type { Analysis, SolveInput } from "@/types/analysis"
import type { TutorAnswer, TutorSource } from "@/lib/tutor-contract"

async function readResponse<T>(response: Response): Promise<T> {
  const body = await response.json().catch(() => ({ error: "El servidor no devolvió JSON válido." }))
  if (!response.ok) throw new Error(body.error || "No se pudo completar la solicitud.")
  return body as T
}

export async function solveSystem(input: SolveInput): Promise<Analysis> {
  const response = await fetch("/api/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  return readResponse<Analysis>(response)
}

type TutorPayload = SolveInput & {
  question: string
  method?: string
  step_index?: number
}

export type TutorResponse = {
  answer: TutorAnswer
  source: TutorSource
  model: string | null
  input_tokens: number
  output_tokens: number
  incomplete: boolean
}

export async function askTutor(payload: TutorPayload): Promise<TutorResponse> {
  const response = await fetch("/api/tutor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(16000),
  })
  return readResponse<TutorResponse>(response)
}
