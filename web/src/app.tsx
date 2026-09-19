import { useMemo, useState } from "react"
import {
  ArrowDown,
  Bot,
  Braces,
  Calculator,
  CheckCircle2,
  Code2,
  Download,
  FileDown,
  FlaskConical,
  LoaderCircle,
  Menu,
  Printer,
  RotateCcw,
  ShieldAlert,
} from "lucide-react"
import { ModeToggle } from "@/components/mode-toggle"
import { MatrixEditor } from "@/components/calculator/matrix-editor"
import { ProcedureView } from "@/components/procedure/procedure-view"
import { ResultSummary, StatusBadge } from "@/components/results/result-summary"
import { VerificationView } from "@/components/results/verification-view"
import { TutorSheet } from "@/components/tutor/tutor-sheet"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Skeleton } from "@/components/ui/skeleton"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { cloneScenario, scenarios } from "@/data/scenarios"
import { solveSystem } from "@/lib/api"
import { downloadJson } from "@/lib/format"
import type { Analysis, SolveInput } from "@/types/analysis"

type Source = "scenario" | "custom" | "json"
type StepContext = { method: string; stepIndex: number } | null

const initial = cloneScenario("compatible")

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
  const [scenarioKey, setScenarioKey] = useState("compatible")
  const [A, setA] = useState(initial.A)
  const [B, setB] = useState(initial.B)
  const [production, setProduction] = useState(initial.production)
  const [dimension, setDimension] = useState(3)
  const [jsonInput, setJsonInput] = useState('{"A":[[2,1],[1,-1]],"B":[5,1]}')
  const [preferredMethod, setPreferredMethod] = useState("gauss")
  const [report, setReport] = useState<Analysis | null>(null)
  const [analysisVersion, setAnalysisVersion] = useState(0)
  const [currentInput, setCurrentInput] = useState<SolveInput>({ A, B, production })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [tutorOpen, setTutorOpen] = useState(false)
  const [stepContext, setStepContext] = useState<StepContext>(null)
  const [tutorPrompt, setTutorPrompt] = useState("")

  const currentScenario = scenarios[scenarioKey]
  const title = source === "scenario" ? currentScenario.title : source === "json" ? "Sistema importado" : "Sistema personalizado"
  const note = source === "scenario" ? currentScenario.note : "Datos proporcionados por el usuario."

  function chooseScenario(key: string) {
    const next = cloneScenario(key)
    setScenarioKey(key); setA(next.A); setB(next.B); setProduction(next.production); setReport(null); setError("")
  }

  function chooseSource(next: Source) {
    setSource(next); setReport(null); setError("")
    if (next === "scenario") chooseScenario(scenarioKey)
    if (next === "custom") resizeCustom(dimension)
    if (next === "json") setProduction(false)
  }

  function resizeCustom(raw: number) {
    const size = Math.max(1, Math.min(12, raw || 3))
    setDimension(size)
    setA(Array.from({ length: size }, (_, row) => Array.from({ length: size }, (_, column) => row === column ? "1" : "0")))
    setB(Array(size).fill("1")); setProduction(false); setReport(null)
  }

  async function solve() {
    setError(""); setReport(null); setLoading(true)
    try {
      let input: SolveInput
      if (source === "json") {
        const parsed = JSON.parse(jsonInput)
        if (!parsed || !Array.isArray(parsed.A) || !Array.isArray(parsed.B)) throw new Error("El JSON debe contener A y B como arreglos.")
        input = { A: parsed.A, B: parsed.B, production }
      } else input = { A, B, production }
      const result = await solveSystem(input)
      setCurrentInput(input); setReport(result); setAnalysisVersion((value) => value + 1)
      window.setTimeout(() => document.getElementById("results")?.scrollIntoView({ behavior: "smooth" }), 50)
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "No se pudo resolver el sistema.")
    } finally { setLoading(false) }
  }

  function explainStep(method: string, stepIndex: number) {
    setStepContext({ method, stepIndex })
    setTutorPrompt("Explica este paso completo: identifica la operación, justifica por qué conserva las soluciones y muestra cómo cambia la fila afectada.")
    setTutorOpen(true)
  }

  function openTutor() {
    setStepContext(null); setTutorPrompt(""); setTutorOpen(true)
  }

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
            <Card className="self-end border-primary/20 bg-card/85 shadow-xl shadow-primary/5"><CardHeader><div className="flex items-center justify-between"><Badge>Caso base listo</Badge><span className="font-mono text-xs text-muted-foreground">6 × 6</span></div><CardTitle>Vector esperado de la guía</CardTitle><CardDescription>Precargado con el B compatible y claramente separado de las disponibilidades originales.</CardDescription></CardHeader><CardContent><div className="grid grid-cols-3 gap-2 font-mono text-sm">{[15, 20, 25, 10, 15, 20].map((value, index) => <div key={index} className="rounded-lg border bg-muted/30 p-3"><span className="block text-[10px] text-muted-foreground">x{index + 1}</span><strong>{value}</strong></div>)}</div></CardContent></Card>
          </div>
        </section>

        <section id="calculator" className="scroll-mt-20 border-b py-14 sm:py-20">
          <div className="mx-auto max-w-7xl px-4 sm:px-6">
            <div className="mb-8 max-w-2xl"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">Laboratorio</p><h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Define y resuelve el sistema</h2><p className="mt-3 text-muted-foreground">El caso compatible está cargado desde el inicio. Puedes editar cualquier celda antes de calcular.</p></div>
            <div className="grid gap-5 xl:grid-cols-[19rem_minmax(0,1fr)]">
              <Card className="h-fit"><CardHeader><CardTitle className="text-lg">Configuración</CardTitle><CardDescription>Origen, escenario y método principal.</CardDescription></CardHeader><CardContent className="space-y-5">
                <div className="space-y-2"><Label>Origen de los datos</Label><Select value={source} onValueChange={(value) => chooseSource(value as Source)}><SelectTrigger className="w-full" aria-label="Origen de los datos"><SelectValue /></SelectTrigger><SelectContent><SelectItem value="scenario">Escenario preparado</SelectItem><SelectItem value="custom">Matriz propia</SelectItem><SelectItem value="json">Importar JSON</SelectItem></SelectContent></Select></div>
                {source === "scenario" && <div className="space-y-2"><Label>Escenario</Label><Select value={scenarioKey} onValueChange={chooseScenario}><SelectTrigger className="w-full" aria-label="Escenario preparado"><SelectValue /></SelectTrigger><SelectContent>{scenarioEntries.map(([key, item]) => <SelectItem key={key} value={key}>{item.shortTitle}</SelectItem>)}</SelectContent></Select><p className="text-xs leading-relaxed text-muted-foreground">{currentScenario.note}</p></div>}
                {source === "custom" && <div className="space-y-2"><Label htmlFor="dimension">Dimensión cuadrada</Label><Input id="dimension" type="number" min={1} max={12} value={dimension} onChange={(event) => resizeCustom(Number(event.target.value))} /></div>}
                <div className="space-y-2"><Label>Método principal</Label><Select value={preferredMethod} onValueChange={setPreferredMethod}><SelectTrigger className="w-full" aria-label="Método principal"><SelectValue /></SelectTrigger><SelectContent><SelectItem value="gauss">Eliminación de Gauss</SelectItem><SelectItem value="gauss_jordan">Gauss-Jordan</SelectItem><SelectItem value="inverse">Matriz inversa</SelectItem></SelectContent></Select><p className="text-xs text-muted-foreground">Los otros métodos también se calculan para comprobar la coincidencia.</p></div>
                <Separator />
                <div className="flex items-center justify-between gap-4"><div><Label htmlFor="production">Interpretación productiva</Label><p className="mt-1 text-xs text-muted-foreground">Exige X ≥ 0 para declarar el plan viable.</p></div><Switch id="production" checked={production} onCheckedChange={(checked) => { setProduction(checked); setReport(null) }} /></div>
              </CardContent></Card>
              <Card className="min-w-0"><CardHeader><div className="flex flex-wrap items-center justify-between gap-3"><div><CardTitle>Matriz aumentada A · X = B</CardTitle><CardDescription>Acepta enteros, decimales, notación científica y fracciones.</CardDescription></div><Badge variant="outline">{A.length} × {A.length}</Badge></div></CardHeader><CardContent className="min-w-0 space-y-5">
                {source === "json" ? <div className="space-y-2"><Label htmlFor="json-input">Datos JSON</Label><Textarea id="json-input" className="min-h-60 font-mono text-xs" value={jsonInput} onChange={(event) => { setJsonInput(event.target.value); setReport(null) }} spellCheck={false} /><p className="text-xs text-muted-foreground">B puede ser vector o columna; escribe las fracciones como &quot;2/3&quot;.</p></div> : <div id="matrix-editor"><MatrixEditor A={A} B={B} onChange={(nextA, nextB) => { setA(nextA); setB(nextB); setReport(null) }} /></div>}
                {source === "scenario" && scenarioKey !== "example" && <Alert className="border-amber-500/40 bg-amber-500/5"><ShieldAlert className="text-amber-600" /><AlertTitle>Discrepancia documentada</AlertTitle><AlertDescription>El vector esperado requiere un B diferente. El escenario original y la variante compatible permanecen separados.</AlertDescription></Alert>}
                {error && <Alert variant="destructive" role="alert"><ShieldAlert /><AlertTitle>No se pudo resolver</AlertTitle><AlertDescription>{error}</AlertDescription></Alert>}
                <div className="flex flex-wrap items-center justify-between gap-3 border-t pt-5"><p className="text-xs text-muted-foreground">El servidor valida dimensiones y vuelve a calcular todo desde A y B.</p><Button id="solve" size="lg" onClick={() => void solve()} disabled={loading}>{loading ? <LoaderCircle className="animate-spin" /> : <Calculator />}{loading ? "Analizando…" : "Resolver sistema"}</Button></div>
              </CardContent></Card>
            </div>
          </div>
        </section>

        {(loading || report) && <section id="results" className="scroll-mt-20 border-b py-14 sm:py-20" aria-live="polite"><div className="mx-auto max-w-7xl px-4 sm:px-6"><div className="mb-8 flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">Resultado</p><h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Evidencia matemática</h2></div>{report && <div className="flex gap-2"><Button variant="outline" onClick={() => document.getElementById("calculator")?.scrollIntoView({ behavior: "smooth" })}><RotateCcw />Editar datos</Button><Button onClick={openTutor}><Bot />Tutor IA</Button></div>}</div>{loading ? <LoadingResults /> : report && <><Card className="mb-6"><CardContent className="grid gap-5 pt-6 sm:grid-cols-2 lg:grid-cols-4"><Metric label="Estado"><StatusBadge report={report} /></Metric><Metric label="Determinante">{report.determinant}</Metric><Metric label="Rangos A / [A|B]">{report.rank_A} / {report.rank_augmented}</Metric><Metric label="Error máximo">{report.max_error ?? "No aplica"}</Metric></CardContent></Card><Tabs defaultValue="summary"><div className="max-w-full overflow-x-auto pb-1"><TabsList variant="line" className="min-w-max"><TabsTrigger value="summary">Resumen</TabsTrigger><TabsTrigger value="procedure">Procedimiento</TabsTrigger><TabsTrigger value="verification">Verificación</TabsTrigger><TabsTrigger value="export">Exportar</TabsTrigger></TabsList></div><TabsContent value="summary" className="pt-5"><ResultSummary report={report} /></TabsContent><TabsContent value="procedure" className="pt-5"><ProcedureView report={report} preferredMethod={preferredMethod} onExplain={explainStep} /></TabsContent><TabsContent value="verification" className="pt-5"><VerificationView report={report} /></TabsContent><TabsContent value="export" className="pt-5"><Card><CardHeader><CardTitle>Comparte un análisis reproducible</CardTitle><CardDescription>Descarga los datos exactos o guarda esta página como PDF desde el navegador.</CardDescription></CardHeader><CardContent className="flex flex-wrap gap-3"><Button onClick={() => downloadJson("resultado-techchip.json", report)}><Download />Resultado JSON</Button><Button variant="outline" onClick={() => downloadJson("sistema-techchip.json", currentInput)}><Braces />Datos de entrada</Button><Button variant="outline" onClick={() => window.print()}><Printer />Imprimir / PDF</Button><Button asChild variant="outline"><a href="https://raw.githubusercontent.com/emanuel56411-hue/parcial2_algebra_agente67/main/docs/informe_tecnico_ieee.pdf" target="_blank" rel="noreferrer"><FileDown />Informe IEEE</a></Button></CardContent></Card></TabsContent></Tabs></>}</div></section>}

        <section id="methodology" className="scroll-mt-20 py-14 sm:py-20"><div className="mx-auto max-w-7xl px-4 sm:px-6"><div className="mb-8 max-w-2xl"><p className="text-xs font-bold uppercase tracking-[.18em] text-primary">Tres rutas, una respuesta</p><h2 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Métodos que puedes defender</h2><p className="mt-3 text-muted-foreground">Cada recorrido parte de los datos originales, registra sus transformaciones y se contrasta con los demás.</p></div><div className="grid gap-4 md:grid-cols-3">{[["01", "Eliminación de Gauss", "Lleva [A|B] a [U|C] y aplica sustitución hacia atrás."], ["02", "Gauss-Jordan", "Normaliza pivotes y elimina arriba y abajo hasta [I|X]."], ["03", "Matriz inversa", "Construye A⁻¹ con [A|I] y calcula el producto A⁻¹B."]].map(([number, method, description]) => <Card key={number}><CardHeader><span className="font-mono text-xs text-primary">{number}</span><CardTitle>{method}</CardTitle><CardDescription className="leading-relaxed">{description}</CardDescription></CardHeader></Card>)}</div><div className="mt-6 grid gap-4 lg:grid-cols-2"><Alert><CheckCircle2 /><AlertTitle>Residual exacto</AlertTitle><AlertDescription>Las fracciones racionales permiten comprobar E = max|AX−B| sin introducir redondeos binarios.</AlertDescription></Alert><Alert className="border-amber-500/40"><ShieldAlert className="text-amber-600" /><AlertTitle>Balance no es optimización</AlertTitle><AlertDescription>AX=B consume capacidades; sin función objetivo no demuestra un máximo de beneficios ni un mínimo de costos.</AlertDescription></Alert></div></div></section>
      </main>
      <footer className="border-t bg-card"><div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 text-sm text-muted-foreground sm:flex-row sm:items-center sm:px-6"><strong className="text-foreground">TechChip Matrix Studio</strong><span className="sm:mr-auto">Universidad Francisco Gavidia · Álgebra lineal explicable</span><a className="inline-flex items-center gap-2 hover:text-foreground" href="https://github.com/emanuel56411-hue/parcial2_algebra_agente67" target="_blank" rel="noreferrer"><Code2 className="size-4" />Código fuente</a></div></footer>
      {report && <TutorSheet key={analysisVersion} open={tutorOpen} onOpenChange={setTutorOpen} input={currentInput} title={title} note={note} initialQuestion={tutorPrompt} stepContext={stepContext} />}
    </div>
  )
}
