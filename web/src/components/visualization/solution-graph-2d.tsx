import { Coordinates, Mafs, Plot, Point } from "mafs"
import "mafs/core.css"
import { numeric } from "@/lib/format"
import type { Analysis } from "@/types/analysis"

const colors = ["#62d6a3", "#fbbf24"]

export function SolutionGraph2D({ report }: { report: Analysis }) {
  const rows = report.A.map((row, i) => ({ a: numeric(row[0]), b: numeric(row[1]), c: numeric(report.B[i]) }))
  const solution = report.solution?.map(numeric)
  const extent = Math.max(5, ...rows.map(({ a, b, c }) => Math.abs(c / (Math.abs(a) > Math.abs(b) ? a || 1 : b || 1))), ...(solution || []).map(Math.abs)) * 1.5
  return <div className="overflow-hidden rounded-xl border bg-[#101e1b] p-2">
    <Mafs viewBox={{ x: [-extent, extent], y: [-extent, extent] }} height={320} pan={false} zoom={false}>
      <Coordinates.Cartesian />
      {rows.map(({ a, b, c }, i) => Math.abs(b) > 1e-12
        ? <Plot.OfX key={i} y={(x) => (c - a * x) / b} color={colors[i]} weight={3} />
        : Math.abs(a) > 1e-12 ? <Plot.OfY key={i} x={() => c / a} color={colors[i]} weight={3} /> : null)}
      {solution && <Point x={solution[0]} y={solution[1]} color="#fff" />}
    </Mafs>
    <div className="flex flex-wrap gap-4 px-3 py-2 text-xs text-muted-foreground"><span><i className="mr-1 inline-block size-2 rounded-full bg-emerald-300" />Ecuación 1</span><span><i className="mr-1 inline-block size-2 rounded-full bg-amber-300" />Ecuación 2</span><span>{report.status === "unique" ? "Punto blanco: intersección" : report.status === "infinite" ? "Rectas coincidentes" : "Sin intersección común"}</span></div>
  </div>
}
