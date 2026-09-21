import { useEffect, useState } from "react"
import { AnimatePresence, motion, useReducedMotion } from "framer-motion"
import { Bot, Calculator, CheckCircle2, ChevronLeft, ChevronRight, List, Pause, Play, Rows3 } from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { MathFormula, MathLine, MathText } from "@/components/math-value"
import { MatrixDisplay } from "@/components/procedure/matrix-display"
import type { Analysis, Step } from "@/types/analysis"

const methodLabels: Record<string, string> = {
  diagnosis: "Diagnóstico",
  gauss: "Eliminación de Gauss",
  gauss_jordan: "Gauss-Jordan",
  inverse: "Matriz inversa",
}

const methodGoals: Record<string, string> = {
  diagnosis: "Pivotes, determinante y rangos.",
  gauss: "Construir U y resolver desde la última ecuación.",
  gauss_jordan: "Convertir A en I y leer X.",
  inverse: "Construir A⁻¹ y calcular X = A⁻¹B.",
}

function phase(step: Step) {
  if (step.kind === "swap") return "Intercambio"
  if (step.kind === "scale") return "Normalización"
  if (step.kind === "add") return "Eliminación"
  if (step.kind === "substitution") return "Sustitución"
  if (step.kind === "multiplication") return "A⁻¹·B"
  return "Control"
}

function StepCard({ step, index, previous, detailed, method, onExplain }: {
  step: Step
  index: number
  previous?: string[][]
  detailed: boolean
  method: string
  onExplain: (method: string, stepIndex: number) => void
}) {
  const reduced = useReducedMotion()
  const calculations = step.calc?.length ? step.calc : [step.operation]
  return <motion.div initial={reduced ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={reduced ? undefined : { opacity: 0, y: -8 }} transition={{ duration: reduced ? 0 : 0.22 }}>
    <Card className="overflow-hidden border-border/80 shadow-[0_12px_36px_-26px_#65e2ad]">
      <CardHeader className="border-b bg-muted/20 pb-4">
        <div className="flex flex-wrap items-center justify-between gap-2"><Badge variant="outline" className="font-mono">Paso {index + 1}</Badge>{detailed && <Badge variant="secondary">{phase(step)}</Badge>}</div>
        <CardTitle className="text-base leading-snug sm:text-lg">{step.title || step.operation}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-5 pt-5">
        {detailed && <>
          <div className="grid gap-3 md:grid-cols-2">
            <div className="rounded-lg border-l-4 border-primary bg-primary/5 p-4"><p className="text-[10px] font-bold uppercase tracking-[.16em] text-primary">Qué hice</p><p className="mt-1.5 text-sm leading-relaxed"><MathText>{step.what || step.operation}</MathText></p></div>
            <div className="rounded-lg border-l-4 border-amber-400 bg-amber-400/5 p-4"><p className="text-[10px] font-bold uppercase tracking-[.16em] text-amber-300">Por qué</p><p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">{step.why || step.explanation}</p></div>
          </div>
          {step.kind !== "note" && <div className="flex flex-wrap items-center gap-2 rounded-lg border border-primary/25 bg-primary/5 px-3 py-2 text-sm"><Rows3 className="size-4 shrink-0 text-primary" /><span className="overflow-x-auto"><MathFormula source={step.operation} /></span></div>}
          <div><p className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[.14em] text-muted-foreground"><Calculator className="size-3.5" /> Cálculo</p><div className="max-w-full overflow-x-auto rounded-lg border bg-background px-4 py-3"><div className="table border-separate border-spacing-x-1">{calculations.map((line, lineIndex) => <MathLine key={lineIndex} align>{line}</MathLine>)}</div></div></div>
        </>}
        <div>{detailed && <p className="mb-2 text-xs font-bold uppercase tracking-[.14em] text-muted-foreground">Matriz resultante</p>}<MatrixDisplay matrix={step.matrix} split={step.split} step={step} previous={previous} /></div>
        {detailed && Object.keys(step.decimals || {}).length > 0 && <div className="flex flex-wrap gap-2" aria-label="Aproximaciones decimales">{Object.entries(step.decimals).map(([name, value]) => <Badge key={name} variant="outline" className="font-mono font-normal tabular-nums">{name} ≈ {value}</Badge>)}</div>}
        {detailed && <div className="flex justify-end border-t pt-4"><Button size="sm" variant="outline" onClick={() => onExplain(method, index)}><Bot /> Consultar este paso</Button></div>}
      </CardContent>
    </Card>
  </motion.div>
}

function StepSequence({ steps, detailed, method, onExplain }: { steps: Step[]; detailed: boolean; method: string; onExplain: (method: string, stepIndex: number) => void }) {
  const [index, setIndex] = useState(0)
  const [all, setAll] = useState(false)
  const [playing, setPlaying] = useState(false)
  const reduced = useReducedMotion()
  useEffect(() => {
    if (!playing || all) return
    const timer = window.setInterval(() => setIndex((current) => {
      if (current >= steps.length - 1) { setPlaying(false); return current }
      return current + 1
    }), reduced ? 2000 : 1600)
    return () => window.clearInterval(timer)
  }, [playing, all, steps.length, reduced])
  const selected = Math.min(index, Math.max(0, steps.length - 1))
  if (!steps.length) return <p className="py-4 text-sm text-muted-foreground">Sin pasos registrados.</p>
  return <div className="space-y-5 py-2">
    <div className="rounded-xl border bg-background/70 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-sm font-semibold">Reproductor de pasos</p><p className="text-xs text-muted-foreground" aria-live="polite">Paso {selected + 1} de {steps.length}</p></div><label className="flex items-center gap-2 text-xs"><List className="size-4" /> Ver todos los pasos <Switch checked={all} onCheckedChange={(value) => { setAll(value); setPlaying(false) }} aria-label="Ver todos los pasos" /></label></div>
      {!all && <>
        <input className="mt-4 w-full accent-emerald-400" type="range" min={0} max={steps.length - 1} value={selected} onChange={(event) => { setIndex(Number(event.target.value)); setPlaying(false) }} aria-label="Elegir paso" />
        <div className="mt-3 flex flex-wrap items-center gap-2"><Button variant="outline" size="sm" disabled={selected === 0} onClick={() => { setIndex(selected - 1); setPlaying(false) }}><ChevronLeft /> Anterior</Button><Button variant="outline" size="sm" disabled={selected === steps.length - 1} onClick={() => { setIndex(selected + 1); setPlaying(false) }}>Siguiente <ChevronRight /></Button><Tooltip><TooltipTrigger asChild><Button variant="secondary" size="sm" onClick={() => { if (selected === steps.length - 1) setIndex(0); setPlaying(!playing) }}>{playing ? <Pause /> : <Play />}{playing ? "Pausa" : "Play"}</Button></TooltipTrigger><TooltipContent>Avanza automáticamente por el procedimiento</TooltipContent></Tooltip></div>
        <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow={selected + 1} aria-valuemin={1} aria-valuemax={steps.length} aria-label="Progreso de pasos"><div className="h-full rounded-full bg-primary transition-[width]" style={{ width: `${((selected + 1) / steps.length) * 100}%` }} /></div>
      </>}
    </div>
    {all ? <div className="grid gap-5">{steps.map((step, current) => <StepCard key={`${method}-${current}`} step={step} index={current} previous={current ? steps[current - 1].matrix : undefined} detailed={detailed} method={method} onExplain={onExplain} />)}</div> : <AnimatePresence mode="wait"><StepCard key={`${method}-${selected}`} step={steps[selected]} index={selected} previous={selected ? steps[selected - 1].matrix : undefined} detailed={detailed} method={method} onExplain={onExplain} /></AnimatePresence>}
  </div>
}

export function ProcedureView({ report, preferredMethod, onExplain }: { report: Analysis; preferredMethod: string; onExplain: (method: string, stepIndex: number) => void }) {
  const [view, setView] = useState<"summary" | "detailed">("summary")
  const reduced = useReducedMotion()
  const sections = [{ key: "diagnosis", name: methodLabels.diagnosis, steps: report.diagnostic_steps }, ...Object.entries(report.methods).map(([key, method]) => ({ key, name: method.name, steps: method.steps }))]
  return <div className="space-y-5">
    <div className="flex flex-col gap-3 rounded-xl border bg-card p-4 sm:flex-row sm:items-center sm:justify-between"><div><h3 className="font-semibold">Métodos paso a paso</h3><p className="mt-1 text-xs text-muted-foreground">Cada paso conserva su matriz y sus valores exactos.</p></div><Tabs value={view} onValueChange={(value) => setView(value as "summary" | "detailed")}><TabsList aria-label="Nivel de detalle"><TabsTrigger value="summary">Vista resumen</TabsTrigger><TabsTrigger value="detailed">Vista detallada</TabsTrigger></TabsList></Tabs></div>
    <Accordion type="multiple" defaultValue={["diagnosis"]} className="gap-4">{sections.map((section) => <AccordionItem key={section.key} value={section.key} className="rounded-xl border bg-card px-4 data-[state=open]:shadow-sm"><AccordionTrigger className="py-5 hover:no-underline"><span className="min-w-0 pr-3"><span className="flex flex-wrap items-center gap-2 text-base font-semibold">{section.name}{section.key === preferredMethod && <Badge>Principal</Badge>}</span><span className="mt-1 block text-xs font-normal text-muted-foreground">{methodGoals[section.key]} · {section.steps.length} pasos</span></span></AccordionTrigger><AccordionContent className="pb-5"><motion.div initial={reduced ? false : { opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduced ? 0 : 0.2 }}><StepSequence steps={section.steps} detailed={view === "detailed"} method={section.key} onExplain={onExplain} /></motion.div></AccordionContent></AccordionItem>)}</Accordion>
    {report.methods_agree && <div className="flex items-center gap-2 rounded-lg border border-primary/30 bg-primary/5 p-3 text-sm"><CheckCircle2 className="size-4 text-primary" /> Los procedimientos llegan exactamente al mismo resultado.</div>}
  </div>
}
