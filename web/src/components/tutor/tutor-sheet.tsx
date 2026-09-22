import { useEffect, useRef, useState } from "react"
import { useReducedMotion } from "framer-motion"
import { FileJson, LoaderCircle, Maximize2, Minimize2, Send, ShieldCheck, Sparkles, X } from "lucide-react"
import { TutorAnswerView } from "@/components/tutor/tutor-answer"
import { TutorAvatar } from "@/components/tutor/tutor-avatar"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetClose, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Textarea } from "@/components/ui/textarea"
import { askTutor, solveSystem } from "@/lib/api"
import { actionTutorAnswer, engineTutorAnswer, validateModelAnswer } from "@/lib/tutor-contract"
import type { TutorAction, TutorAnswer, TutorSource } from "@/lib/tutor-contract"
import type { Analysis, SolveInput } from "@/types/analysis"

type StepContext = { method: string; stepIndex: number } | null
type ChatItem = { kind: "user"; text: string } | { kind: "welcome" } | { kind: "attachment"; name: string; size: number } | { kind: "answer"; answer: TutorAnswer; source: TutorSource; method: string; action?: TutorAction }

type Props = {
  open: boolean
  onOpenChange: (open: boolean) => void
  input: SolveInput | null
  report: Analysis | null
  preferredMethod: string
  stepContext?: StepContext
}

const actions: { label: string; action: TutorAction }[] = [
  { label: "Explícame este paso", action: "step" },
  { label: "¿Por qué este pivote?", action: "pivot" },
  { label: "Verifica el resultado", action: "verify" },
  { label: "Resume el método", action: "method" },
]
const sensitive = /(?:\bsk-[A-Za-z0-9_-]{8,}\b|\bBearer\s+\S+|\b(?:password|contraseña|clave\s+api)\b|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b\+?\d[\d .-]{8,}\d\b)/i

export function TutorSheet({ open, onOpenChange, input, report, preferredMethod, stepContext }: Props) {
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState<ChatItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [expanded, setExpanded] = useState(false)
  const [selectedMethod, setSelectedMethod] = useState(preferredMethod)
  const [attached, setAttached] = useState<{ name: string; input: SolveInput; report: Analysis } | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const fileRef = useRef<HTMLInputElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const latestAnswerRef = useRef<HTMLDivElement>(null)
  const reducedMotion = useReducedMotion()
  const activeReport = attached?.report ?? report
  const activeInput = attached?.input ?? input
  const requestedMethod = attached ? selectedMethod : stepContext?.method || selectedMethod
  const method = activeReport && !activeReport.methods[requestedMethod] ? "diagnosis" : requestedMethod
  const stepIndex = attached ? 0 : stepContext?.stepIndex ?? 0

  useEffect(() => {
    if (!open) return
    const viewport = document.querySelector<HTMLElement>(".tutor-sheet [data-radix-scroll-area-viewport]")
    if (!viewport) return
    const latest = messages[messages.length - 1]
    if ((latest?.kind === "answer" || latest?.kind === "welcome") && latestAnswerRef.current) {
      const distance = latestAnswerRef.current.getBoundingClientRect().top - viewport.getBoundingClientRect().top
      viewport.scrollTo({ top: viewport.scrollTop + distance - 8, behavior: reducedMotion ? "instant" : "smooth" })
    } else if (latest?.kind === "user" || loading) {
      bottomRef.current?.scrollIntoView({ behavior: reducedMotion ? "instant" : "smooth", block: "end" })
    } else {
      viewport.scrollTop = 0
    }
  }, [open, messages, loading, reducedMotion])

  function runAction(action: TutorAction, label: string) {
    if (!activeReport) return
    setError("")
    setMessages((current) => [...current, { kind: "user", text: label }, { kind: "answer", answer: actionTutorAnswer(activeReport, method, action, stepIndex), source: "engine", method, action }])
  }

  async function attachJson(file: File) {
    setError("")
    setLoading(true)
    try {
      const parsed = JSON.parse(await file.text()) as { A?: unknown; B?: unknown; production?: unknown }
      if (!Array.isArray(parsed.A) || !Array.isArray(parsed.B)) throw new Error('El archivo debe contener {"A":[[...]],"B":[...]}.')
      const rawB = parsed.B.length > 0 && Array.isArray(parsed.B[0]) ? parsed.B.map((row) => Array.isArray(row) ? row[0] : row) : parsed.B
      const nextInput = { A: parsed.A, B: rawB, production: typeof parsed.production === "boolean" ? parsed.production : false } as SolveInput
      const nextReport = await solveSystem(nextInput)
      setAttached({ name: file.name, input: nextInput, report: nextReport })
      setSelectedMethod("gauss")
      setMessages((current) => [...current, { kind: "attachment", name: file.name, size: nextReport.A.length }])
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "No se pudo leer el archivo JSON.")
    } finally {
      setLoading(false)
      if (fileRef.current) fileRef.current.value = ""
    }
  }

  async function submit() {
    const text = question.trim()
    if (!text || loading) return
    if (sensitive.test(text)) { setError("No compartas claves ni datos personales. Reformula tu pregunta."); return }
    setError("")
    if (!activeReport) {
      setMessages((current) => [...current, { kind: "user", text }, { kind: "welcome" }])
      setQuestion("")
      return
    }
    if (!activeInput) { setError("Revisa los datos de la matriz antes de continuar."); return }
    setMessages((current) => [...current, { kind: "user", text }])
    setQuestion("")
    setLoading(true)
    try {
      const result = await askTutor({ ...activeInput, question: text, method, ...(!attached && stepContext ? { step_index: stepIndex } : {}) })
      const valid = result.source === "model" && validateModelAnswer(result.answer, activeReport, method)
      const serverEngine = result.source === "engine" && result.answer && typeof result.answer.resumen === "string" && typeof result.answer.conclusion === "string" && typeof result.answer.fuera_de_tema === "boolean" && Array.isArray(result.answer.pasos) && result.answer.pasos.every((step) => step && typeof step.titulo === "string" && typeof step.que === "string" && typeof step.por_que === "string" && (step.ref_paso === null || Number.isInteger(step.ref_paso)))
      const answer = valid || serverEngine ? result.answer : engineTutorAnswer(activeReport, method, attached ? undefined : stepContext?.stepIndex)
      setMessages((current) => [...current, { kind: "answer", answer, source: valid ? "model" : "engine", method }])
    } catch {
      setMessages((current) => [...current, { kind: "answer", answer: engineTutorAnswer(activeReport, method, attached ? undefined : stepContext?.stepIndex), source: "engine", method }])
    } finally {
      setLoading(false)
    }
  }

  return <Sheet open={open} onOpenChange={onOpenChange}>
    <SheetContent className="tutor-sheet flex flex-col gap-0 p-0 text-foreground shadow-[0_30px_90px_#4c3b6b33]" style={expanded ? { width: "min(92rem, calc(100vw - 1rem))" } : undefined} showCloseButton={false}>
      <SheetHeader className="relative flex-row items-center gap-3 border-b border-violet-300/35 p-4 pr-24">
        <TutorAvatar className="size-12 border-2 border-violet-300 shadow-[0_0_18px_#c4b5fd88]" />
        <div className="min-w-0"><SheetTitle className="text-base font-semibold">Tutor de IA · Matrices</SheetTitle><SheetDescription className="text-xs">Explicaciones con valores exactos del motor.</SheetDescription></div>
        <Button type="button" variant="ghost" size="icon" className="absolute right-12 top-4" onClick={() => setExpanded((value) => !value)} aria-label={expanded ? "Restaurar tamaño del tutor" : "Expandir tutor"}>{expanded ? <Minimize2 /> : <Maximize2 />}</Button>
        <SheetClose asChild><Button type="button" variant="ghost" size="icon" className="absolute right-3 top-4" aria-label="Cerrar tutor"><X /></Button></SheetClose>
      </SheetHeader>
      <Alert className="mx-4 mt-3 w-auto shrink-0 border-violet-300/40 bg-violet-100/45 text-xs dark:bg-violet-950/25"><ShieldCheck className="size-4" /><AlertDescription>Puedes escribir un prompt completo o adjuntar un JSON. El cálculo exacto siempre lo realiza el motor antes de que el tutor explique.</AlertDescription></Alert>
      <div className="mx-4 mt-3 flex flex-wrap items-center gap-2" aria-label="Método que explicará el tutor">
        {([['gauss', 'Gauss'], ['gauss_jordan', 'Gauss-Jordan'], ['inverse', 'Matriz inversa']] as const).map(([key, label]) => <Button key={key} type="button" size="sm" variant={method === key ? "default" : "outline"} disabled={Boolean(activeReport && !activeReport.methods[key])} onClick={() => setSelectedMethod(key)}>{label}</Button>)}
        {method === "diagnosis" && <span className="text-xs text-amber-700 dark:text-amber-200">Sistema singular: se muestra el diagnóstico; la inversa no existe.</span>}
      </div>
      <ScrollArea className="min-h-0 flex-1 px-4 py-4" aria-label="Conversación con el tutor">
        <div className="space-y-4 pb-3" role="log" aria-live="polite" aria-relevant="additions">
          <div className="flex items-start gap-2.5"><TutorAvatar className="mt-0.5 size-8 border border-violet-300" /><div className="max-w-[85%] rounded-2xl rounded-tl-sm border border-violet-300/35 bg-violet-100/50 px-4 py-3 text-sm leading-relaxed dark:bg-violet-950/25"><p>¡Hola! Elige uno de los tres métodos, adjunta un JSON o pregúntame sobre tu sistema. Las cifras vienen de la calculadora exacta.</p>{stepContext && !attached && <p className="mt-2 text-xs text-violet-700 dark:text-violet-200">Estoy viendo el paso {stepContext.stepIndex + 1} contigo.</p>}</div></div>
          {activeReport && stepContext && !attached && messages.length === 0 && <TutorAnswerView answer={actionTutorAnswer(activeReport, method, "step", stepIndex)} source="engine" report={activeReport} method={method} action="step" />}
          {messages.map((message, index) => message.kind === "user" ? <div key={index} className="ml-auto max-w-[85%] rounded-2xl rounded-tr-sm bg-primary px-4 py-3 text-sm text-primary-foreground whitespace-pre-wrap">{message.text}</div> : message.kind === "attachment" ? <div key={index} className="ml-auto flex max-w-[85%] items-center gap-3 rounded-2xl rounded-tr-sm border border-violet-300/40 bg-violet-100/60 px-4 py-3 text-sm dark:bg-violet-950/30"><FileJson className="size-5 text-violet-600 dark:text-violet-300" /><div><strong className="block">{message.name}</strong><small>Sistema {message.size}×{message.size} validado y listo.</small></div></div> : message.kind === "welcome" ? <div key={index} ref={index === messages.length - 1 ? latestAnswerRef : undefined} className="flex items-start gap-2.5"><TutorAvatar className="mt-0.5 size-8 border border-violet-300" /><div className="max-w-[85%] space-y-2 rounded-2xl rounded-tl-sm border border-violet-300/35 bg-violet-100/50 px-4 py-3 text-sm leading-relaxed dark:bg-violet-950/25"><p>¡Hola! Puedes adjuntar aquí el JSON del ejercicio o resolver la matriz de la página.</p><Button type="button" size="sm" variant="outline" onClick={() => fileRef.current?.click()}><FileJson />Adjuntar JSON</Button></div></div> : activeReport ? <div key={index} ref={index === messages.length - 1 ? latestAnswerRef : undefined}><TutorAnswerView answer={message.answer} source={message.source} report={activeReport} method={message.method} action={message.action} /></div> : null)}
          {loading && <div className="flex items-center gap-2 text-sm text-muted-foreground" role="status"><LoaderCircle className="size-4 animate-spin motion-reduce:animate-none" />Estoy preparando una explicación clara…</div>}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>
      <form className="shrink-0 border-t border-violet-300/35 bg-white/55 px-4 pt-3 pb-[max(1rem,env(safe-area-inset-bottom))] backdrop-blur dark:bg-slate-950/35" onSubmit={(event) => { event.preventDefault(); void submit() }}>
        <div className="mb-3 flex flex-wrap gap-2" aria-label="Ayudas rápidas del motor">{actions.map(({ label, action }) => <button key={action} type="button" disabled={!activeReport} onClick={() => runAction(action, label)} className="inline-flex items-center gap-1.5 rounded-full border border-violet-300/50 bg-violet-100/60 px-3 py-1.5 text-xs text-violet-800 transition-colors hover:bg-violet-200/70 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400 disabled:cursor-not-allowed disabled:opacity-45 dark:bg-violet-950/30 dark:text-violet-100"><Sparkles className="size-3.5" />{label}</button>)}</div>
        {error && <p className="mb-2 text-sm text-rose-300" role="alert">{error}</p>}
        {!activeReport && <p className="mb-2 text-xs text-amber-700 dark:text-amber-200">Adjunta un JSON o resuelve una matriz para hablar de cifras y pasos.</p>}
        <Textarea ref={textareaRef} value={question} onChange={(event) => setQuestion(event.target.value)} rows={expanded ? 5 : 3} placeholder={activeReport ? "Escribe un prompt completo sobre el sistema actual…" : "Adjunta un JSON o pregunta cómo comenzar…"} aria-label="Pregunta para el Tutor IA" />
        <div className="mt-2 flex flex-wrap items-center justify-between gap-3"><div className="flex items-center gap-2"><input ref={fileRef} type="file" accept="application/json,.json" className="sr-only" onChange={(event) => { const file = event.target.files?.[0]; if (file) void attachJson(file) }} /><Button type="button" variant="outline" size="sm" onClick={() => fileRef.current?.click()}><FileJson />Adjuntar JSON</Button><small className="text-muted-foreground">Prompt sin límite artificial de palabras</small></div><Button type="submit" disabled={loading || !question.trim()}>{loading ? <LoaderCircle className="animate-spin motion-reduce:animate-none" /> : <Send />}Enviar</Button></div>
      </form>
    </SheetContent>
  </Sheet>
}
