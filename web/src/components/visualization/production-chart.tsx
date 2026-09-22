import { BarChart3 } from "lucide-react"
import { Bar, BarChart, Cell, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { numeric } from "@/lib/format"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Analysis } from "@/types/analysis"

export function ProductionChart({ report }: { report: Analysis }) {
  if (!report.production || !report.solution) return null
  const data = report.A.map((row, index) => {
    const consumed = row.reduce((sum, value, column) => sum + numeric(value) * numeric(report.solution![column]), 0)
    const available = numeric(report.B[index])
    return { name: `R${index + 1}`, consumed, available, excess: consumed > available + 1e-8 }
  })
  return <Card><CardHeader><CardTitle className="flex items-center gap-2"><BarChart3 className="size-5 text-primary" /> Consumo y disponibilidad</CardTitle></CardHeader><CardContent><div className="h-64 w-full" role="img" aria-label="Barras de consumo y disponibilidad por recurso"><ResponsiveContainer width="100%" height="100%"><BarChart data={data} margin={{ top: 8, right: 8, bottom: 8, left: 0 }}><CartesianGrid stroke="var(--border)" strokeDasharray="3 3" vertical={false} /><XAxis dataKey="name" stroke="var(--muted-foreground)" /><YAxis stroke="var(--muted-foreground)" width={45} /><Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 12, color: "var(--popover-foreground)" }} /><Legend /><Bar dataKey="available" name="Disponible" fill="#c4b5fd" radius={[6, 6, 0, 0]} /><Bar dataKey="consumed" name="Consumo" radius={[6, 6, 0, 0]} isAnimationActive={false}>{data.map((item) => <Cell key={item.name} fill={item.excess ? "#f9a8d4" : "#86efac"} />)}</Bar></BarChart></ResponsiveContainer></div><div className="mt-3 flex flex-wrap gap-2 text-xs">{data.filter((item) => item.excess).map((item) => <span key={item.name} className="rounded-full bg-rose-100 px-2 py-1 text-rose-700 dark:bg-rose-950/30 dark:text-rose-200">{item.name}: excede disponibilidad</span>)}{!data.some((item) => item.excess) && <span className="text-muted-foreground">Ningún recurso excede su disponibilidad.</span>}</div></CardContent></Card>
}
