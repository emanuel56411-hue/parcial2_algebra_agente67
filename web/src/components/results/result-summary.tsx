import { useState } from "react"
import { motion, useReducedMotion } from "framer-motion"
import { AlertTriangle, Check, CheckCircle2, CircleX, Copy, Infinity as InfinityIcon } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ExactValue, MathFormula } from "@/components/math-value"
import { numeric } from "@/lib/format"
import type { Analysis } from "@/types/analysis"

const labels = { unique: "Solución única", infinite: "Infinitas soluciones", inconsistent: "Sin solución" }

export function StatusBadge({ report }: { report: Analysis }) {
  const Icon = report.status === "unique" ? CheckCircle2 : report.status === "infinite" ? InfinityIcon : CircleX
  const style = report.status === "unique" ? "border-emerald-400/40 bg-emerald-400/15 text-emerald-200" : report.status === "infinite" ? "border-amber-400/40 bg-amber-400/15 text-amber-200" : "border-rose-400/40 bg-rose-400/15 text-rose-200"
  return <Badge variant="outline" className={`gap-1.5 ${style}`}><Icon className="size-3.5" />{labels[report.status]}</Badge>
}

export function ResultSummary({ report }: { report: Analysis }) {
  const [copied, setCopied] = useState(false)
  const reduced = useReducedMotion()
  const negative = Boolean(report.solution?.some((value) => numeric(value) < 0) && report.production)
  const Icon = negative ? AlertTriangle : report.status === "unique" ? CheckCircle2 : report.status === "infinite" ? InfinityIcon : CircleX
  async function copy() {
    const content = report.solution ? `X = (${report.solution.join(", ")})` : report.particular ? `X = (${report.particular.join(", ")}) + ${report.nullspace.map((v, i) => `t${i + 1}·(${v.join(", ")})`).join(" + ")}` : "Sin solución"
    await navigator.clipboard.writeText(content)
    setCopied(true)
    window.setTimeout(() => setCopied(false), 2200)
  }
  return <motion.div initial={reduced ? false : { opacity: 0, scale: .985 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: reduced ? 0 : .35 }}>
    <Card className={report.status === "inconsistent" ? "border-rose-400/40" : negative ? "border-amber-400/40" : "border-primary/30"}>
      <CardHeader className="border-b bg-primary/5"><div className="flex flex-wrap items-center justify-between gap-3"><div className="flex items-center gap-3"><Icon className={negative ? "text-amber-300" : report.status === "inconsistent" ? "text-rose-300" : "text-primary"} /><CardTitle>Resultado final</CardTitle></div><StatusBadge report={report} /></div></CardHeader>
      <CardContent className="space-y-6 pt-6">
        {report.solution ? <>
          <div className="flex flex-wrap items-center justify-between gap-3"><p className="text-xl font-semibold sm:text-3xl"><MathFormula source="X =" /></p><Button variant="outline" size="sm" onClick={() => void copy()}>{copied ? <Check /> : <Copy />}{copied ? "Copiado" : "Copiar resultado"}</Button></div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{report.solution.map((value, index) => <div key={index} className="rounded-xl border border-primary/20 bg-background/60 p-4 shadow-sm"><p className="mb-2 text-xs font-semibold uppercase tracking-wider text-primary"><MathFormula source={`x${index + 1}`} /></p><ExactValue value={value} showDecimal className="text-lg sm:text-xl" /></div>)}</div>
        </> : <div className="flex flex-wrap items-start justify-between gap-3"><div className="min-w-0 flex-1">{report.particular ? <div className="overflow-x-auto rounded-lg bg-muted p-4 text-sm"><span className="inline-flex min-w-max items-center gap-2"><MathFormula source="X =" /><span>(</span>{report.particular.map((value, index) => <span key={index}><ExactValue value={value} />{index < report.particular!.length - 1 ? ", " : ""}</span>)}<span>)</span>{report.nullspace.map((vector, index) => <span key={index}> + <MathFormula source={`t${index + 1}`} /> · ({vector.map((value, item) => <span key={item}><ExactValue value={value} />{item < vector.length - 1 ? ", " : ""}</span>)})</span>)}</span></div> : <p className="rounded-lg bg-rose-400/10 p-4 text-sm">Una fila 0 = c, con c ≠ 0, demuestra que ninguna X satisface todas las ecuaciones.</p>}</div><Button variant="outline" size="sm" onClick={() => void copy()}>{copied ? <Check /> : <Copy />}{copied ? "Copiado" : "Copiar resultado"}</Button></div>}
        <div className="rounded-xl border bg-muted/25 p-5"><p className="text-xs font-bold uppercase tracking-[.16em] text-primary">Conclusión</p><p className="mt-2 text-base leading-relaxed">{report.interpretation[0]}</p>{report.interpretation.length > 1 && <ul className="mt-4 space-y-2 text-sm text-muted-foreground">{report.interpretation.slice(1).map((item, index) => <li key={index} className="flex gap-3"><span className="mt-2 size-1.5 shrink-0 rounded-full bg-primary" />{item}</li>)}</ul>}</div>
      </CardContent>
    </Card>
  </motion.div>
}
