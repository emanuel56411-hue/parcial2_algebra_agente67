import { lazy, Suspense, useMemo, useRef, useState } from "react"
import { motion, useReducedMotion } from "framer-motion"
import {
  ArrowDown,
  Bot,
  Braces,
  Calculator,
  CheckCircle2,
  Code2,
  Download,
  FileDown,
  FileJson,
  FlaskConical,
  LoaderCircle,
  Menu,
  Printer,
  RotateCcw,
  ShieldAlert,
} from "lucide-react"
import { ModeToggle } from "@/components/mode-toggle"
import { MatrixEditor } from "@/components/calculator/matrix-editor"
import { ExactValue } from "@/components/math-value"
import { ProcedureView } from "@/components/procedure/procedure-view"
import { ResultSummary, StatusBadge } from "@/components/results/result-summary"
import { VerificationView } from "@/components/results/verification-view"
import { SolutionVisualization } from "@/components/visualization/solution-visualization"
const ProductionChart = lazy(() => import("@/components/visualization/production-chart").then((module) => ({ default: module.ProductionChart })))
import { TutorSheet } from "@/components/tutor/tutor-sheet"
import { TutorAvatar } from "@/components/tutor/tutor-avatar"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Skeleton } from "@/components/ui/skeleton"
import { Switch } from "@/components/ui/switch"
import { Textarea } from "@/components/ui/textarea"
import { cloneScenario, scenarios } from "@/data/scenarios"
import { solveExercise, solveSystem } from "@/lib/api"
import { downloadJson } from "@/lib/format"
import type { Analysis, SolveInput } from "@/types/analysis"

type Source = "scenario" | "custom" | "json"
type StepContext = { method: string; stepIndex: number } | null

const initial = cloneScenario("original")

function methodFromJson(value: unknown): "gauss" | "gauss_jordan" | "inverse" | null {
  if (!value || typeof value !== "object") return null
  const candidate = (value as { method?: unknown; metodo?: unknown }).method ?? (value as { metodo?: unknown }).metodo
  if (typeof candidate !== "string") return null
  const normalized = candidate.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[_-]+/g, " ")
  if (normalized.includes("jordan")) return "gauss_jordan"
  if (normalized.includes("inversa") || normalized.includes("inverse")) return "inverse"
  if (normalized.includes("gauss")) return "gauss"
  return null
}

function Metric({ label, children, id }: { label: string; children: React.ReactNode; id?: string }) {
  return <div className="space-y-1 border-l-2 border-primary/30 pl-4"><span className="text-[10px] font-bold uppercase tracking-[.16em] text-muted-foreground">{label}</span><div id={id} className="font-mono text-lg font-semibold">{children}</div></div>
}

function LoadingResults() {
  return <div className="grid gap-4 md:grid-cols-4" aria-label="Calculando resultados"><Skeleton className="h-24" /><Skeleton className="h-24" /><Skeleton className="h-24" /><Skeleton className="h-24" /></div>
}

function Header() {
  const links = <><a className="text-sm font-medium text-muted-foreground transition hover:text-foreground" href="#calculator">Calculadora</a><a className="text-sm font-medium text-muted-foreground transition hover:text-foreground" href="#results">Resultados</a><a className="text-sm font-medium text-muted-foreground transition hover:text-foreground" href="#methodology">Métodos</a></>
  return <header className="sticky top-0 z-40 border-b bg-background/90 backdrop-blur-xl"><div className="mx-auto flex h-16 max-w-7xl items-center gap-4 px-4 sm:px-6"><a href="#top" className="flex items-center gap-3"><span className="grid size-9 place-items-center rounded-lg bg-primary font-mono font-bold text-primary-foreground">M</span><span className="leading-none"><strong className="block text-sm">TechChip</strong><small className="text-[9px] font-bold uppercase tracking-[.2em] text-muted-foreground">Matrix Studio</small></span></a><nav className="ml-auto hidden items-center gap-7 md:flex" aria-label="Navegación principal">{links}</nav><ModeToggle /><Sheet><SheetTrigger asChild><Button variant="outline" size="icon" className="md:hidden" aria-label="Abrir navegación"><Menu /></Button></SheetTrigger><SheetContent><SheetHeader><SheetTitle>Navegación</SheetTitle></SheetHeader><nav className="grid gap-5 p-5">{links}</nav></SheetContent></Sheet></div></header>
}

export default function App() {
  const [source, setSource] = useState<Source>("scenario")
  const [scenarioKey, setScenarioKey] = useState("original")
  const [A, setA] = useState(initial.A)
  const [B, setB] = useState(initial.B)
  const [production, setProduction] = useState(initial.production)
  const [dimension, setDimension] = useState(3)
  const [jsonInput, setJsonInput] = useState('{"A":[[2,1],[1,-1]],"B":[5,1]}')
  const [inputNotice, setInputNotice] = useState("")
  const [preferredMethod, setPreferredMethod] = useState("gauss")
  const [report, setReport] = useState<Analysis | null>(null)
  const [analysisVersion, setAnalysisVersion] = useState(0)
  const [currentInput, setCurrentInput] = useState<SolveInput>({ A, B, production })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [tutorOpen, setTutorOpen] = useState(false)
  const [stepContext, setStepContext] = useState<StepContext>(null)
  const jsonFileRef = useRef<HTMLInputElement>(null)
  const reducedMotion = useReducedMotion()

  const currentScenario = scenarios[scenarioKey]

  function chooseScenario(key: string) {
    const next = cloneScenario(key)
    setScenarioKey(key); setA(next.A); setB(next.B); setProduction(next.production); setReport(null); setError("")
  }

  function chooseSource(next: Source) {
    setSource(next); setReport(null); setError(""); setInputNotice("")
    if (next === "scenario") chooseScenario(scenarioKey)
    if (next === "custom") resizeCustom(dimension)
    if (next === "json") setProduction(false)
  }

  function resizeCustom(raw: number) {
    const size = Math.max(2, Math.min(10, raw || 3))
    setDimension(size)
    setA(Array.from({ length: size }, (_, row) => Array.from({ length: size }, (_, column) => row === column ? "1" : "0")))
    setB(Array(size).fill("1")); setProduction(false); setReport(null)
  }

  async function loadJsonFile(file: File) {
    setError(""); setInputNotice("")
    try {
      const text = await file.text()
      if (!text.trim()) throw new Error("El archivo está vacío.")
      if (new Blob([text]).size > 100_000) throw new Error("El archivo no puede superar 100 kB.")
      setJsonInput(text)
      setReport(null)
      setInputNotice(`Archivo cargado: ${file.name}. Puedes revisarlo antes de resolver.`)
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "No se pudo leer el archivo JSON.")
    } finally {
      if (jsonFileRef.current) jsonFileRef.current.value = ""
    }
  }

  async function solve() {
    setError(""); setInputNotice(""); setReport(null); setLoading(true)
    try {
      let input: SolveInput
      let result: Analysis
      if (source === "json") {
        let parsed: unknown = null
        try { parsed = JSON.parse(jsonInput) } catch { /* El servidor interpretará el texto libre. */ }
        const direct = parsed && typeof parsed === "object" && Array.isArray((parsed as { A?: unknown }).A) && Array.isArray((parsed as { B?: unknown }).B)
        if (direct) {
          const system = parsed as { A: SolveInput["A"]; B: SolveInput["B"] }
          input = { A: system.A, B: system.B, production }
          result = await solveSystem(input)
          const requestedMethod = methodFromJson(parsed)
          if (requestedMethod) setPreferredMethod(requestedMethod)
          setInputNotice("Entrada detectada como JSON A/B y validada directamente.")
        } else {
          const interpreted = await solveExercise(jsonInput, production)
          input = interpreted.input
          result = interpreted.analysis
          setA(input.A.map((row) => row.map(String))); setB(input.B.map(String)); setDimension(input.A.length)
          if (interpreted.preferred_method) setPreferredMethod(interpreted.preferred_method)
          const labels = { llm: "lenguaje natural con IA", equations: "ecuaciones escritas", matrix_notation: "notación A/B", json: "JSON flexible" }
          setInputNotice(`Entrada interpretada como ${labels[interpreted.source]}. Se extrajo y validó un sistema ${input.A.length}×${input.A.length}.`)
        }
      } else {
        input = { A, B, production }
        result = await solveSystem(input)
      }
      setCurrentInput(input); setReport(result); setAnalysisVersion((value) => value + 1)
      window.setTimeout(() => document.getElementById("results")?.scrollIntoView({ behavior: "smooth" }), 50)
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "No se pudo resolver el sistema.")
    } finally { setLoading(false) }
  }

  function explainStep(method: string, stepIndex: number) {
    setStepContext({ method, stepIndex })
    setTutorOpen(true)
  }

  function openTutor() {
    setStepContext(null); setTutorOpen(true)
  }

  const tutorInput = useMemo<SolveInput | null>(() => {
    if (report) return currentInput
    if (source !== "json") return { A, B, production }
    try {
      const parsed = JSON.parse(jsonInput)
      if (Array.isArray(parsed?.A) && Array.isArray(parsed?.B)) return { A: parsed.A, B: parsed.B, production }
    } catch { /* El tutor pedirá corregir el JSON antes de enviarlo. */ }
    return null
  }, [report, currentInput, source, jsonInput, A, B, production])

  const scenarioEntries = useMemo(() => Object.entries(scenarios), [])

  return (
    <div id="top" className="min-h-svh bg-background text-foreground">
      <a href="#calculator" className="sr-only z-50 rounded-md bg-background p-3 focus:not-sr-only focus:fixed focus:left-3 focus:top-3">Saltar a la calculadora</a>
      <Header />
      <main>
        <section className="relative overflow-hidden border-b" aria-labelledby="hero-title">
          <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_75%_25%,color-mix(in_oklab,var(--primary)_12%,transparent),transparent_38%)]" />
          <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:px-6 lg:grid-cols-[1fr_.8fr] lg:py-20">
            <div className="max-w-3xl"><Badge variant="outline" className="mb-5"><FlaskConical /> Álgebra lineal explicable</Badge><h1 id="hero-title" className="text-balance text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">Del sistema matricial a una decisión defendible.</h1><p className="mt-5 max-w-2xl text-pretty text-base leading-relaxed text-muted-foreground sm:text-lg">Resuelve balances de capacidad con aritmética racional, tres métodos auditables y una explicación clara de cada operación.</p><div className="mt-7 flex flex-wrap gap-3"><Button asChild size="lg"><a href="#calculator">Abrir laboratorio <ArrowDown /></a></Button><Button asChild size="lg" variant="outline"><a href="#methodology">Ver metodología</a></Button></div></div>
            <Card className="self-end border-primary/20 bg-card/85 shadow-xl shadow-primary/5"><CardHeader><div className="flex items-center justify-between"><Badge>Datos originales</Badge><span className="font-mono text-xs text-muted-foreground">6 × 6</span></div><CardTitle>Disponibilidades de la guía</CardTitle><CardDescription>El sistema usa el B impreso y calcula su solución real, sin forzar el vector incorrecto del enunciado.</CardDescription></CardHeader><CardContent><div className="grid grid-cols-3 gap-2 font-mono text-sm">{[155, 160, 225, 140, 215, 175].map((value, index) => <div key={index} className="rounded-lg border bg-muted/30 p-3"><span className="block text-[10px] text-muted-foreground">B{index + 1}</span><strong>{value}</strong></div>)}</div></CardContent></Card>
          </div>
        </section>

        <section id="calculator" className="scroll-mt-20 border-b py-14 sm:py-20">
          <div className="mx-auto max-w-7xl px-4 sm:px-6">
            <div className="mb-8 max-w-2xl"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">01 · Entrada</p><h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Define y resuelve el sistema</h2><p className="mt-3 text-muted-foreground">Los datos originales de la guía están cargados desde el inicio. Puedes editar cualquier celda antes de calcular.</p></div>
            <div className="grid gap-5 xl:grid-cols-[19rem_minmax(0,1fr)]">
              <Card className="h-fit"><CardHeader><CardTitle className="text-lg">Configuración</CardTitle><CardDescription>Origen, escenario y método principal.</CardDescription></CardHeader><CardContent className="space-y-5">
                <div className="space-y-2"><Label>Origen de los datos</Label><Select value={source} onValueChange={(value) => chooseSource(value as Source)}><SelectTrigger className="w-full" aria-label="Origen de los datos"><SelectValue /></SelectTrigger><SelectContent><SelectItem value="scenario">Escenario preparado</SelectItem><SelectItem value="custom">Matriz propia</SelectItem><SelectItem value="json">Texto o JSON</SelectItem></SelectContent></Select></div>
                {source === "scenario" && <div className="space-y-2"><Label>Escenario</Label><Select value={scenarioKey} onValueChange={chooseScenario}><SelectTrigger className="w-full" aria-label="Escenario preparado"><SelectValue /></SelectTrigger><SelectContent>{scenarioEntries.map(([key, item]) => <SelectItem key={key} value={key}>{item.shortTitle}</SelectItem>)}</SelectContent></Select><p className="text-xs leading-relaxed text-muted-foreground">{currentScenario.note}</p></div>}
                {source === "custom" && <div className="space-y-2"><Label>Dimensión cuadrada</Label><Select value={String(dimension)} onValueChange={(value) => resizeCustom(Number(value))}><SelectTrigger className="w-full" aria-label="Dimensión de la matriz"><SelectValue /></SelectTrigger><SelectContent>{[2, 3, 4, 5, 6, 7, 8, 9, 10].map((size) => <SelectItem key={size} value={String(size)}>{size} × {size}</SelectItem>)}</SelectContent></Select><p className="text-xs text-muted-foreground">Elige directamente entre 2×2 y 10×10.</p></div>}
                <div className="space-y-2"><Label>Método principal</Label><Select value={preferredMethod} onValueChange={setPreferredMethod}><SelectTrigger className="w-full" aria-label="Método principal"><SelectValue /></SelectTrigger><SelectContent><SelectItem value="gauss">Eliminación de Gauss</SelectItem><SelectItem value="gauss_jordan">Gauss-Jordan</SelectItem><SelectItem value="inverse">Matriz inversa</SelectItem></SelectContent></Select><p className="text-xs text-muted-foreground">Los otros métodos también se calculan para comprobar la coincidencia.</p></div>
                <Separator />
                <div className="flex items-center justify-between gap-4"><div><Label htmlFor="production">Interpretación productiva</Label><p className="mt-1 text-xs text-muted-foreground">Exige X ≥ 0. Si X está en miles, A se interpreta por cada mil módulos.</p></div><Switch id="production" checked={production} onCheckedChange={(checked) => { setProduction(checked); setReport(null) }} /></div>
              </CardContent></Card>
              <Card className="min-w-0 shadow-sm"><CardHeader><div className="flex flex-wrap items-center justify-between gap-3"><div><CardTitle>{source === "json" ? "Describe o pega tu sistema" : "Matriz aumentada A · X = B"}</CardTitle><CardDescription>{source === "json" ? "Detectamos automáticamente texto libre, ecuaciones y JSON." : "Acepta enteros, decimales, notación científica y fracciones."}</CardDescription></div><Badge variant="outline">{source === "json" ? "Hasta 10 × 10" : `${A.length} × ${A.length}`}</Badge></div></CardHeader><CardContent className="min-w-0 space-y-5">
                {source === "json" ? <div className="space-y-3"><div className="flex flex-wrap items-center justify-between gap-2"><Label htmlFor="json-input">Problema en palabras, ecuaciones o JSON</Label><input ref={jsonFileRef} type="file" accept="application/json,text/plain,.json,.txt,.md" className="sr-only" onChange={(event) => { const file = event.target.files?.[0]; if (file) void loadJsonFile(file) }} /><Button type="button" size="sm" variant="outline" onClick={() => jsonFileRef.current?.click()}><FileJson />Subir JSON o texto</Button></div><Textarea id="json-input" className="min-h-72 resize-y text-sm leading-relaxed" value={jsonInput} onChange={(event) => { setJsonInput(event.target.value); setReport(null); setInputNotice("") }} placeholder={'Ejemplo en palabras:\nEl producto x usa 7 kg de A y 4 kg de B; el producto y usa 3 kg de A y 5 kg de B. Hay 579 kg de A y 643 kg de B. Resuelve por Gauss-Jordan.\n\nO pega JSON:\n{"A":[[7,3],[4,5]],"B":[579,643]}'} spellCheck /><div className="grid gap-2 text-xs text-muted-foreground sm:grid-cols-2"><p>En texto libre, incluye el consumo de cada producto y la disponibilidad de cada recurso.</p><p className="sm:text-right">En JSON, B puede ser vector o columna y las fracciones pueden escribirse como &quot;2/3&quot;.</p></div></div> : <div id="matrix-editor"><MatrixEditor A={A} B={B} onChange={(nextA, nextB) => { setA(nextA); setB(nextB); setReport(null) }} /></div>}
                {source === "scenario" && scenarioKey !== "example" && <Alert className="border-amber-500/40 bg-amber-500/5"><ShieldAlert className="text-amber-600" /><AlertTitle>{scenarioKey === "original" ? "Resultado incorrecto documentado" : "Variante solo comparativa"}</AlertTitle><AlertDescription>{scenarioKey === "original" ? "El vector indicado en el enunciado no resuelve este B. Aquí se calcula la respuesta real de los datos originales." : "Este B alternativo produce el vector indicado, pero no pertenece a los datos originales de la guía."}</AlertDescription></Alert>}
                {error && <Alert variant="destructive" role="alert"><ShieldAlert /><AlertTitle>No se pudo resolver</AlertTitle><AlertDescription>{error}</AlertDescription></Alert>}
                {inputNotice && <Alert><CheckCircle2 /><AlertTitle>Entrada reconocida</AlertTitle><AlertDescription>{inputNotice}</AlertDescription></Alert>}
                <div className="flex flex-wrap items-center justify-between gap-3 border-t pt-5"><p className="text-xs text-muted-foreground">El intérprete solo extrae A y B; el servidor valida y calcula los tres métodos con aritmética exacta.</p><Button id="solve" size="lg" onClick={() => void solve()} disabled={loading}>{loading ? <LoaderCircle className="animate-spin" /> : <Calculator />}{loading ? "Interpretando y resolviendo…" : "Resolver sistema"}</Button></div>
              </CardContent></Card>
            </div>
          </div>
        </section>

        {(loading || report) && (
          <section id="results" className="scroll-mt-20 border-b py-14 sm:py-20" aria-live="polite">
            <div className="mx-auto max-w-7xl px-4 sm:px-6">
              <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
                <div><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">Análisis</p><h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Evidencia matemática</h2></div>
                {report && <div className="flex gap-2"><Button variant="outline" onClick={() => document.getElementById("calculator")?.scrollIntoView({ behavior: "smooth" })}><RotateCcw />Editar datos</Button><Button onClick={openTutor}><Bot />Tutor IA</Button></div>}
              </div>

              {loading ? <LoadingResults /> : report && (
                <div className="space-y-12">
                  <section aria-labelledby="diagnosis-title">
                    <div className="mb-4"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">02 · Diagnóstico</p><h3 id="diagnosis-title" className="mt-1 text-2xl font-semibold">Determinante y rangos</h3></div>
                    <Card>
                      <CardContent className="grid gap-5 pt-6 sm:grid-cols-2 lg:grid-cols-4">
                        <Metric label="Estado"><StatusBadge report={report} /></Metric>
                        <Metric label="Determinante"><ExactValue value={report.determinant} showDecimal /></Metric>
                        <Metric label="Rangos A / [A|B]">{report.rank_A} / {report.rank_augmented}</Metric>
                        <Metric label="Error máximo">{report.max_error ?? "No aplica"}</Metric>
                      </CardContent>
                    </Card>
                  </section>

                  <section aria-labelledby="method-title">
                    <div className="mb-4"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">03 · Método</p><h3 id="method-title" className="mt-1 text-2xl font-semibold">Procedimiento estructurado</h3></div>
                    <ProcedureView report={report} preferredMethod={preferredMethod} onExplain={explainStep} />
                  </section>

                  <section aria-labelledby="final-title">
                    <div className="mb-4"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">04 · Resultado</p><h3 id="final-title" className="mt-1 text-2xl font-semibold">Conclusión del sistema</h3></div>
                    <div className="space-y-5"><ResultSummary report={report} /><SolutionVisualization report={report} /><Suspense fallback={null}><ProductionChart report={report} /></Suspense></div>
                  </section>

                  <section aria-labelledby="verification-title">
                    <div className="mb-4"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">05 · Verificación</p><h3 id="verification-title" className="mt-1 text-2xl font-semibold">Comprobación exacta</h3></div>
                    <VerificationView report={report} />
                  </section>

                  <Card>
                    <CardHeader><CardTitle>Comparte un análisis reproducible</CardTitle><CardDescription>Descarga los datos exactos o guarda esta página como PDF desde el navegador.</CardDescription></CardHeader>
                    <CardContent className="flex flex-wrap gap-3"><Button onClick={() => downloadJson("resultado-techchip.json", report)}><Download />Resultado JSON</Button><Button variant="outline" onClick={() => downloadJson("sistema-techchip.json", currentInput)}><Braces />Datos de entrada</Button><Button variant="outline" onClick={() => window.print()}><Printer />Imprimir / PDF</Button><Button asChild variant="outline"><a href="https://raw.githubusercontent.com/emanuel56411-hue/parcial2_algebra_agente67/main/docs/informe_tecnico_ieee.pdf" target="_blank" rel="noreferrer"><FileDown />Informe IEEE</a></Button></CardContent>
                  </Card>
                </div>
              )}
            </div>
          </section>
        )}

        <section id="methodology" className="scroll-mt-20 py-14 sm:py-20"><div className="mx-auto max-w-7xl px-4 sm:px-6"><div className="mb-8 max-w-2xl"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">Tres rutas, una respuesta</p><h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Métodos que puedes defender</h2><p className="mt-3 text-muted-foreground">Cada recorrido parte de los datos originales, registra sus transformaciones y se contrasta con los demás.</p></div><div className="grid gap-4 md:grid-cols-3">{[["01", "Eliminación de Gauss", "Lleva [A|B] a [U|C] y aplica sustitución hacia atrás.", "from-violet-100/75 to-pink-50/60 dark:from-violet-950/30 dark:to-pink-950/10"], ["02", "Gauss-Jordan", "Normaliza pivotes y elimina arriba y abajo hasta [I|X].", "from-sky-100/75 to-violet-50/60 dark:from-sky-950/30 dark:to-violet-950/10"], ["03", "Matriz inversa", "Construye A⁻¹ con [A|I] y calcula el producto A⁻¹B.", "from-emerald-100/75 to-sky-50/60 dark:from-emerald-950/30 dark:to-sky-950/10"]].map(([number, method, description, color]) => <Card key={number} className={`bg-gradient-to-br ${color}`}><CardHeader><span className="font-mono text-xs text-primary">{number}</span><CardTitle>{method}</CardTitle><CardDescription className="leading-relaxed">{description}</CardDescription></CardHeader></Card>)}</div><div className="mt-6 grid gap-4 lg:grid-cols-2"><Alert className="bg-emerald-50/60 dark:bg-emerald-950/15"><CheckCircle2 /><AlertTitle>Residual exacto</AlertTitle><AlertDescription>Las fracciones racionales permiten comprobar E = max|AX−B| sin introducir redondeos binarios.</AlertDescription></Alert><Alert className="border-amber-500/40 bg-amber-50/60 dark:bg-amber-950/15"><ShieldAlert className="text-amber-600" /><AlertTitle>Balance no es optimización</AlertTitle><AlertDescription>AX=B consume capacidades; sin función objetivo no demuestra un máximo de beneficios ni un mínimo de costos.</AlertDescription></Alert></div></div></section>
      </main>
      <footer className="border-t bg-card"><div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 text-sm text-muted-foreground sm:flex-row sm:items-center sm:px-6"><strong className="text-foreground">TechChip Matrix Studio</strong><span className="sm:mr-auto">Universidad Francisco Gavidia · Álgebra lineal explicable</span><a className="inline-flex items-center gap-2 hover:text-foreground" href="https://github.com/emanuel56411-hue/parcial2_algebra_agente67" target="_blank" rel="noreferrer"><Code2 className="size-4" />Código fuente</a></div></footer>
      <motion.button
        type="button"
        aria-label="Abrir tutor de IA"
        aria-haspopup="dialog"
        aria-expanded={tutorOpen}
        onClick={openTutor}
        whileHover={reducedMotion ? undefined : { scale: 1.06 }}
        whileTap={reducedMotion ? undefined : { scale: 0.96 }}
        className="fixed bottom-[max(1rem,env(safe-area-inset-bottom))] right-4 z-40 grid size-16 place-items-center rounded-full border-2 border-violet-300 bg-violet-100 shadow-[0_0_0_4px_#faf7ff,0_0_30px_#a78bfa88] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-violet-400 dark:bg-violet-950 dark:shadow-[0_0_0_4px_#211d34,0_0_30px_#a78bfa77] sm:right-6"
      ><TutorAvatar eager className="size-14" /></motion.button>
      <TutorSheet key={analysisVersion} open={tutorOpen} onOpenChange={setTutorOpen} input={tutorInput} report={report} preferredMethod={preferredMethod} stepContext={stepContext} />
    </div>
  )
}
