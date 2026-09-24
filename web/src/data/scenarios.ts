export type Scenario = {
  title: string
  shortTitle: string
  note: string
  A: number[][]
  B: number[]
  production: boolean
  variables: string[]
}

const PRODUCTS = ["AI-Edge 1", "AI-Server Pro", "AI-Autonomous Car", "AI-IoT LowPower", "AI-Robotics Heavy", "AI-Medical Vision"]

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
    shortTitle: "Auditoría · Datos originales",
    note: "Caso de control con el B impreso. Permite demostrar que el vector esperado de la guía no corresponde a estos datos.",
    A: A_BASE,
    B: B_GUIDE,
    production: true,
    variables: PRODUCTS,
  },
  compatible: {
    title: "Variante didáctica · B alternativo",
    shortTitle: "1 · Prueba Base",
    note: "Verifica exactamente X = (15, 20, 25, 10, 15, 20). Requiere B = A·X; este B alternativo no es el impreso en la guía.",
    A: A_BASE,
    B: [185, 200, 280, 150, 245, 195],
    production: true,
    variables: PRODUCTS,
  },
  scarcity: {
    title: "Escasez · resina a 100 kg",
    shortTitle: "3 · Escenario de Escasez (Datos Modificados)",
    note: "Reduce únicamente la resina a B₃ = 100 kg y comprueba si aparecen producciones negativas.",
    A: A_BASE,
    B: [155, 160, 100, 140, 215, 175],
    production: true,
    variables: PRODUCTS,
  },
  singular: {
    title: "Singular · sin solución",
    shortTitle: "4A · Escenario Degenerado (Singularidad) · cero soluciones",
    note: "Hace F₆ = 2F₁ y conserva B₆ = 175: det(A) = 0 y aparece una contradicción.",
    A: [...A_BASE.slice(0, 5), A_BASE[0].map((value) => 2 * value)],
    B: B_GUIDE,
    production: true,
    variables: PRODUCTS,
  },
  infinite: {
    title: "Singular · infinitas soluciones",
    shortTitle: "4B · Escenario Degenerado (Singularidad) · infinitas soluciones",
    note: "Hace F₆ = 2F₁ y también B₆ = 2B₁: det(A) = 0 y una variable queda libre.",
    A: [...A_BASE.slice(0, 5), A_BASE[0].map((value) => 2 * value)],
    B: [155, 160, 225, 140, 215, 310],
    production: true,
    variables: PRODUCTS,
  },
  example: {
    title: "Ejemplo guiado · 3 × 3",
    shortTitle: "Ejemplo extra · 3 × 3",
    note: "Sistema pequeño con solución X = (2, 3, −1).",
    A: [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
    B: [8, -11, -3],
    production: false,
    variables: ["x1", "x2", "x3"],
  },
}

export function cloneScenario(key: string) {
  const item = scenarios[key]
  return {
    A: item.A.map((row) => row.map(String)),
    B: item.B.map(String),
    production: item.production,
    variables: [...item.variables],
  }
}
