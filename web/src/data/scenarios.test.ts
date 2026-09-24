import { describe, expect, it } from "vitest"
import { A_BASE, B_GUIDE, scenarios } from "./scenarios"

const EXPECTED_X = [15, 20, 25, 10, 15, 20]

function matvec(A: number[][], x: number[]) {
  return A.map((row) => row.reduce((total, value, column) => total + value * x[column], 0))
}

describe("las cuatro pruebas de la guía", () => {
  it("usa los nombres de la fotografía en el selector", () => {
    expect(scenarios.compatible.shortTitle).toBe("1 · Prueba Base")
    expect(scenarios.scarcity.shortTitle).toBe("3 · Escenario de Escasez (Datos Modificados)")
    expect(scenarios.singular.shortTitle).toContain("Escenario Degenerado (Singularidad)")
    expect(scenarios.infinite.shortTitle).toContain("Escenario Degenerado (Singularidad)")
  })

  it("prueba 1 carga el B que produce exactamente el vector esperado", () => {
    expect(matvec(scenarios.compatible.A, EXPECTED_X)).toEqual(scenarios.compatible.B)
  })

  it("prueba 2 por sustitución directa obtiene E menor que 10^-6", () => {
    const ax = matvec(scenarios.compatible.A, EXPECTED_X)
    const error = Math.max(...ax.map((value, index) => Math.abs(value - scenarios.compatible.B[index])))
    expect(error).toBe(0)
    expect(error).toBeLessThan(1e-6)
  })

  it("prueba 3 solo reduce la resina B3 a 100 kg", () => {
    expect(scenarios.scarcity.A).toEqual(A_BASE)
    expect(scenarios.scarcity.B).toEqual(B_GUIDE.map((value, index) => index === 2 ? 100 : value))
  })

  it("prueba 4 cubre los diagnósticos singular incompatible e indeterminado", () => {
    const doubledFirstRow = A_BASE[0].map((value) => 2 * value)
    expect(scenarios.singular.A[5]).toEqual(doubledFirstRow)
    expect(scenarios.singular.B[5]).toBe(175)
    expect(scenarios.infinite.A[5]).toEqual(doubledFirstRow)
    expect(scenarios.infinite.B[5]).toBe(2 * B_GUIDE[0])
  })
})
