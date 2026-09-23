export type Matrix = string[][]

export type Step = {
  operation: string
  explanation: string
  matrix: Matrix
  split: number
  kind: "note" | "swap" | "scale" | "add" | "substitution" | "multiplication"
  target: number | null
  source: number | null
  factor: string | null
  title: string | null
  what: string | null
  why: string | null
  calc: string[]
  pivot: [number, number] | null
  changed_rows: number[]
  decimals: Record<string, string>
}

export type MethodResult = {
  name: string
  solution: string[]
  steps: Step[]
  inverse: Matrix | null
}

export type Analysis = {
  A: Matrix
  B: string[]
  determinant: string
  rank_A: number
  rank_augmented: number
  status: "unique" | "infinite" | "inconsistent"
  diagnostic_steps: Step[]
  methods: Record<string, MethodResult>
  solution: string[] | null
  residual: string[]
  substitution: string[]
  particular: string[] | null
  nullspace: string[][]
  free_columns: number[]
  interpretation: string[]
  production: boolean
  variables: string[]
  methods_agree: boolean
  max_error: string | null
  format: string
}

export type SolveInput = {
  A: (string | number)[][]
  B: (string | number)[]
  production: boolean
  variables?: string[]
}

export type TutorMessage = {
  role: "user" | "assistant"
  content: string
  meta?: string
}
