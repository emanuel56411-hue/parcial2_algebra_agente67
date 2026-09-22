export type Scenario = {
  title: string
  shortTitle: string
  note: string
  A: number[][]
  B: number[]
  production: boolean
}

export const A_BASE = [
  [2, 1, 3, 1, 2, 1],
  [1, 3, 2, 2, 1, 2],
  [3, 2, 4, 1, 3, 2],
  [1, 1, 1, 4, 2, 1],
  [2, 1, 2, 1, 5, 3],
  [1, 2, 1, 2, 1, 4],
]

export const B_GUIDE = [155, 160, 225, 140, 215, 175]

export const scenarios: Record<string, Scenario> = {
  original: {
    title: "TechChip · datos originales",
    shortTitle: "Datos originales",
    note: "Disponibilidades transcritas de la guía, sin correcciones ocultas.",
    A: A_BASE,
    B: B_GUIDE,
    production: true,
  },
  compatible: {
    title: "Variante didáctica · B alternativo",
    shortTitle: "Vector esperado",
    note: "Comparación con B = A·X indicado; no es la disponibilidad original de la guía ni el caso principal.",
    A: A_BASE,
    B: [185, 200, 280, 150, 245, 195],
    production: true,
  },
  scarcity: {
    title: "Escasez · resina a 100 kg",
    shortTitle: "Escasez de resina",
    note: "Parte de B original y modifica únicamente B₃ = 100.",
    A: A_BASE,
    B: [155, 160, 100, 140, 215, 175],
    production: true,
  },
  singular: {
    title: "Singular · sin solución",
    shortTitle: "Singular incompatible",
    note: "F₆ = 2F₁, conservando B₆ = 175; aparece una contradicción.",
    A: [...A_BASE.slice(0, 5), A_BASE[0].map((value) => 2 * value)],
    B: B_GUIDE,
    production: true,
  },
  infinite: {
    title: "Singular · infinitas soluciones",
    shortTitle: "Infinitas soluciones",
    note: "F₆ = 2F₁ y B₆ = 2B₁; una variable queda libre.",
    A: [...A_BASE.slice(0, 5), A_BASE[0].map((value) => 2 * value)],
    B: [155, 160, 225, 140, 215, 310],
    production: true,
  },
  example: {
    title: "Ejemplo guiado · 3 × 3",
    shortTitle: "Ejemplo 3 × 3",
    note: "Sistema pequeño con solución X = (2, 3, −1).",
    A: [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
    B: [8, -11, -3],
    production: false,
  },
}

export function cloneScenario(key: string) {
  const item = scenarios[key]
  return {
    A: item.A.map((row) => row.map(String)),
    B: item.B.map(String),
    production: item.production,
  }
}
