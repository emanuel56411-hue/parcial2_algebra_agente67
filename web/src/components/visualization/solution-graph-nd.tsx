import { Bar, BarChart, CartesianGrid, Cell, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { numeric } from "@/lib/format"
import type { Analysis } from "@/types/analysis"

export function SolutionGraphND({ report }: { report: Analysis }) {
  if (!report.solution) {
    const ranks = [
      { name: "Variables", value: report.A.length, color: "#c4b5fd" },
      { name: "rango(A)", value: report.rank_A, color: "#93c5fd" },
      { name: "rango([A|B])", value: report.rank_augmented, color: "#f9a8d4" },
    ]
    return <div className="rounded-2xl border border-violet-200/70 bg-violet-50/55 p-3 dark:border-violet-900/60 dark:bg-violet-950/20">
      <div className="h-72" role="img" aria-label="Comparación de variables y rangos del sistema"><ResponsiveContainer width="100%" height="100%"><BarChart data={ranks} margin={{ top: 12, right: 12, bottom: 8, left: 0 }}><CartesianGrid stroke="var(--border)" strokeDasharray="4 4" vertical={false} /><XAxis dataKey="name" stroke="var(--muted-foreground)" /><YAxis allowDecimals={false} stroke="var(--muted-foreground)" width={38} /><Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 12, color: "var(--popover-foreground)" }} /><Bar dataKey="value" radius={[8, 8, 0, 0]}>{ranks.map((item) => <Cell key={item.name} fill={item.color} />)}</Bar></BarChart></ResponsiveContainer></div>
      <p className="px-2 pb-1 text-xs text-muted-foreground">En dimensiones mayores se representa el diagnóstico por rangos; no existe una intersección geométrica dibujable en una pantalla tridimensional.</p>
    </div>
  }

  const data = report.solution.map((value, index) => ({ name: report.variables?.[index] || `x${index + 1}`, exact: value, value: numeric(value) }))
  return <div className="rounded-2xl border border-violet-200/70 bg-violet-50/55 p-3 dark:border-violet-900/60 dark:bg-violet-950/20">
    <div className="h-72" role="img" aria-label={`Gráfica del vector solución de ${report.A.length} variables`}><ResponsiveContainer width="100%" height="100%"><BarChart data={data} margin={{ top: 12, right: 12, bottom: 8, left: 0 }}><CartesianGrid stroke="var(--border)" strokeDasharray="4 4" vertical={false} /><XAxis dataKey="name" stroke="var(--muted-foreground)" /><YAxis stroke="var(--muted-foreground)" width={52} /><ReferenceLine y={0} stroke="var(--foreground)" strokeOpacity={0.45} /><Tooltip formatter={(value, _name, item) => [String(item.payload.exact), "Valor exacto"]} contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 12, color: "var(--popover-foreground)" }} /><Bar dataKey="value" name="Valor" radius={[8, 8, 4, 4]}>{data.map((item) => <Cell key={item.name} fill={item.value < 0 ? "#f9a8d4" : "#86efac"} />)}</Bar></BarChart></ResponsiveContainer></div>
    <p className="px-2 pb-1 text-xs text-muted-foreground">Representación del vector solución en {report.A.length} dimensiones. Rosa identifica componentes negativas; los valores exactos aparecen al pasar el cursor.</p>
  </div>
}
