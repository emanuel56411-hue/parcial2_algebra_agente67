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
  return <Card><CardHeader><CardTitle className="flex items-center gap-2"><BarChart3 className="size-5 text-primary" /> Consumo y disponibilidad</CardTitle></CardHeader><CardContent><div className="h-64 w-full" role="img" aria-label="Barras de consumo y disponibilidad por recurso"><ResponsiveContainer width="100%" height="100%"><BarChart data={data} margin={{ top: 8, right: 8, bottom: 8, left: 0 }}><CartesianGrid stroke="#36534a" strokeDasharray="3 3" vertical={false} /><XAxis dataKey="name" stroke="#b5c7be" /><YAxis stroke="#b5c7be" width={45} /><Tooltip contentStyle={{ background: "#172823", border: "1px solid #557568", color: "#fff" }} /><Legend /><Bar dataKey="available" name="Disponible" fill="#849e94" radius={[4, 4, 0, 0]} /><Bar dataKey="consumed" name="Consumo" radius={[4, 4, 0, 0]} isAnimationActive={false}>{data.map((item) => <Cell key={item.name} fill={item.excess ? "#fb7185" : "#52d5a5"} />)}</Bar></BarChart></ResponsiveContainer></div><div className="mt-3 flex flex-wrap gap-2 text-xs">{data.filter((item) => item.excess).map((item) => <span key={item.name} className="rounded-full bg-red-500/15 px-2 py-1 text-red-300">{item.name}: excede disponibilidad</span>)}{!data.some((item) => item.excess) && <span className="text-muted-foreground">Ningún recurso excede su disponibilidad.</span>}</div></CardContent></Card>
}
