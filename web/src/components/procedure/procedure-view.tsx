import { useMemo, useState } from "react"
import { ArrowLeft, ArrowRight, Bot, CheckCircle2 } from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MatrixDisplay } from "@/components/procedure/matrix-display"
import type { Analysis, Step } from "@/types/analysis"

const methodLabels: Record<string, string> = {
  diagnosis: "Diagnóstico",
  gauss: "Eliminación de Gauss",
  gauss_jordan: "Gauss-Jordan",
  inverse: "Matriz inversa",
}

const methodGoals: Record<string, string> = {
  diagnosis: "Determinar si existe una solución y si es única.",
  gauss: "Construir U y resolver desde la última ecuación.",
  gauss_jordan: "Convertir A en I para leer X directamente.",
  inverse: "Construir A⁻¹ y calcular X = A⁻¹B.",
}

function phase(step: Step) {
  if (step.kind === "swap") return "Elección de pivote"
  if (step.kind === "scale") return "Normalización"
  if (step.kind === "add") return "Eliminación"
  if (step.kind === "substitution") return "Sustitución hacia atrás"
  if (step.kind === "multiplication") return "Producto A⁻¹B"
  if (step.operation.includes("det(A)")) return "Diagnóstico"
  if (step.operation.includes("lectura") || step.operation.includes("inversa obtenida")) return "Resultado"
  return "Punto de control"
}

function reason(step: Step) {
  if (step.kind === "swap") return "Solo cambia el orden de las ecuaciones."
  if (step.kind === "scale") return "El factor no es cero, por lo que la operación es reversible."
  if (step.kind === "add") return "Sumar un múltiplo de otra fila es una operación reversible."
  if (step.kind === "substitution") return "Se despeja usando igualdades ya demostradas."
  if (step.kind === "multiplication") return "Se aplica X = A⁻¹B fila por columna."
  return "El estado queda registrado para poder auditar el procedimiento."
}

function RowChange({ step, previous }: { step: Step; previous?: string[][] }) {
  if (!previous || step.target == null || !previous[step.target]) return null
  const before = `[ ${previous[step.target].join("   ")} ]`
  const after = `[ ${step.matrix[step.target].join("   ")} ]`
  return (
    <div className="grid gap-3 rounded-lg border bg-muted/30 p-4 lg:grid-cols-[1fr_auto_1fr] lg:items-center">
      <div><span className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Fila F{step.target + 1} antes</span><code className="mt-2 block overflow-x-auto whitespace-nowrap font-mono text-xs">{before}</code></div>
      <ArrowRight className="hidden size-4 text-primary lg:block" aria-hidden="true" />
      <div><span className="text-[10px] font-bold uppercase tracking-widest text-primary">Fila F{step.target + 1} después</span><code className="mt-2 block overflow-x-auto whitespace-nowrap font-mono text-xs">{after}</code></div>
    </div>
  )
}

type Props = {
  report: Analysis
  preferredMethod: string
  onExplain: (method: string, stepIndex: number) => void
}

export function ProcedureView({ report, preferredMethod, onExplain }: Props) {
  const methods = useMemo(() => ["diagnosis", ...Object.keys(report.methods)], [report])
  const [method, setMethod] = useState(methods.includes(preferredMethod) ? preferredMethod : "diagnosis")
  const [view, setView] = useState("summary")
  const [index, setIndex] = useState(0)
  const steps = method === "diagnosis" ? report.diagnostic_steps : report.methods[method].steps

  const step = steps[index]
  const previous = index > 0 ? steps[index - 1].matrix : undefined

  return (
    <div className="space-y-4">
      <div className="grid gap-3 rounded-xl border bg-card p-4 md:grid-cols-[minmax(15rem,1fr)_auto] md:items-end">
        <div className="space-y-2">
          <label className="text-xs font-semibold" htmlFor="procedure-method">Método de resolución</label>
          <Select value={method} onValueChange={(nextMethod) => { setMethod(nextMethod); setIndex(0) }}>
            <SelectTrigger id="procedure-method" className="w-full md:max-w-sm" aria-label="Método del procedimiento"><SelectValue /></SelectTrigger>
            <SelectContent>{methods.map((key) => <SelectItem key={key} value={key}>{methodLabels[key]}</SelectItem>)}</SelectContent>
          </Select>
          <p className="text-xs text-muted-foreground">{methodGoals[method]}</p>
        </div>
        <Tabs value={view} onValueChange={setView}>
          <TabsList aria-label="Modo del procedimiento">
            <TabsTrigger value="summary">Paso a paso</TabsTrigger>
            <TabsTrigger value="complete">Completo</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {view === "summary" ? (
        <Card className="overflow-hidden border-primary/20">
          <CardHeader className="border-b bg-muted/20">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <Badge variant="outline">Paso {index + 1} de {steps.length}</Badge>
              <Badge>{phase(step)}</Badge>
            </div>
            <CardTitle className="font-mono text-base sm:text-lg">{step.operation}</CardTitle>
            <CardDescription className="text-sm leading-relaxed">{step.explanation}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 pt-5">
            <div className="flex gap-3 rounded-lg border-l-4 border-primary bg-primary/5 p-4 text-sm">
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-primary" />
              <div><strong>Por qué es válido</strong><p className="mt-1 text-muted-foreground">{reason(step)}</p></div>
            </div>
            <MatrixDisplay matrix={step.matrix} split={step.split} step={step} previous={previous} />
            <RowChange step={step} previous={previous} />
            <div className="flex flex-wrap items-center justify-between gap-3 border-t pt-4">
              <Button variant="outline" onClick={() => setIndex((value) => Math.max(0, value - 1))} disabled={index === 0}><ArrowLeft /> Anterior</Button>
              <Button variant="ghost" onClick={() => onExplain(method, index)}><Bot /> Explicar con Tutor IA</Button>
              <Button variant="outline" onClick={() => setIndex((value) => Math.min(steps.length - 1, value + 1))} disabled={index === steps.length - 1}>Siguiente <ArrowRight /></Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader><CardTitle>Procedimiento completo</CardTitle><CardDescription>{steps.length} estados auditables. Abre cada operación para ver el antes y el después.</CardDescription></CardHeader>
          <CardContent>
            <Accordion type="multiple" defaultValue={["step-0", `step-${steps.length - 1}`]}>
              {steps.map((item, itemIndex) => {
                const before = itemIndex > 0 ? steps[itemIndex - 1].matrix : undefined
                return (
                  <AccordionItem key={itemIndex} value={`step-${itemIndex}`}>
                    <AccordionTrigger className="gap-3 py-4 hover:no-underline">
                      <span className="grid min-w-0 gap-1">
                        <span className="text-[10px] font-bold uppercase tracking-widest text-primary">Paso {itemIndex + 1} · {phase(item)}</span>
                        <span className="truncate font-mono text-sm">{item.operation}</span>
                      </span>
                    </AccordionTrigger>
                    <AccordionContent className="space-y-4 pb-5">
                      <p className="leading-relaxed text-muted-foreground">{item.explanation}</p>
                      <p className="rounded-md bg-muted p-3 text-xs"><strong>Validez:</strong> {reason(item)}</p>
                      {before && <div><p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Antes</p><MatrixDisplay matrix={before} split={item.split} label="Matriz anterior" /></div>}
                      <div><p className="mb-2 text-xs font-semibold uppercase tracking-wider text-primary">Después</p><MatrixDisplay matrix={item.matrix} split={item.split} step={item} previous={before} /></div>
                      <RowChange step={item} previous={before} />
                      <Button size="sm" variant="outline" onClick={() => onExplain(method, itemIndex)}><Bot /> Consultar este paso</Button>
                    </AccordionContent>
                  </AccordionItem>
                )
              })}
            </Accordion>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
