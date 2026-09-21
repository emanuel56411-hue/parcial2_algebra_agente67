import { useEffect, useRef, useState } from "react"
import { useReducedMotion } from "framer-motion"
import { LoaderCircle, Send, ShieldCheck, Sparkles, X } from "lucide-react"
import { TutorAnswerView } from "@/components/tutor/tutor-answer"
import { TutorAvatar } from "@/components/tutor/tutor-avatar"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetClose, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Textarea } from "@/components/ui/textarea"
import { askTutor } from "@/lib/api"
import { actionTutorAnswer, engineTutorAnswer, validateModelAnswer } from "@/lib/tutor-contract"
import type { TutorAction, TutorAnswer, TutorSource } from "@/lib/tutor-contract"
import type { Analysis, SolveInput } from "@/types/analysis"

type StepContext = { method: string; stepIndex: number } | null
type ChatItem = { kind: "user"; text: string } | { kind: "answer"; answer: TutorAnswer; source: TutorSource; method: string; action?: TutorAction }

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
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const latestAnswerRef = useRef<HTMLDivElement>(null)
  const reducedMotion = useReducedMotion()
  const method = stepContext?.method || (report && !report.methods[preferredMethod] ? "diagnosis" : preferredMethod)
  const stepIndex = stepContext?.stepIndex ?? 0

  useEffect(() => {
    if (!open) return
    const viewport = document.querySelector<HTMLElement>(".tutor-sheet [data-radix-scroll-area-viewport]")
    if (!viewport) return
    const latest = messages[messages.length - 1]
    if (latest?.kind === "answer" && latestAnswerRef.current) {
      const distance = latestAnswerRef.current.getBoundingClientRect().top - viewport.getBoundingClientRect().top
      viewport.scrollTo({ top: viewport.scrollTop + distance - 8, behavior: reducedMotion ? "instant" : "smooth" })
    } else if (latest?.kind === "user" || loading) {
      bottomRef.current?.scrollIntoView({ behavior: reducedMotion ? "instant" : "smooth", block: "end" })
    } else {
      viewport.scrollTop = 0
    }
  }, [open, messages, loading, reducedMotion])

  function runAction(action: TutorAction, label: string) {
    if (!report) return
    setError("")
    setMessages((current) => [...current, { kind: "user", text: label }, { kind: "answer", answer: actionTutorAnswer(report, method, action, stepIndex), source: "engine", method, action }])
  }

  async function submit() {
    const text = question.trim()
    if (!text || loading) return
    if (!input || !report) { setError("Resuelve el sistema antes de preguntar al tutor."); return }
    if (text.length > 500) { setError("La pregunta puede tener hasta 500 caracteres."); return }
    if (sensitive.test(text)) { setError("No compartas claves ni datos personales. Reformula tu pregunta."); return }
    setError("")
    setMessages((current) => [...current, { kind: "user", text }])
    setQuestion("")
    setLoading(true)
    try {
      const result = await askTutor({ ...input, question: text, method, step_index: stepIndex })
      const valid = result.source === "model" && validateModelAnswer(result.answer, report, method)
      const serverEngine = result.source === "engine" && result.answer && typeof result.answer.resumen === "string" && typeof result.answer.conclusion === "string" && typeof result.answer.fuera_de_tema === "boolean" && Array.isArray(result.answer.pasos) && result.answer.pasos.every((step) => step && typeof step.titulo === "string" && typeof step.que === "string" && typeof step.por_que === "string" && (step.ref_paso === null || Number.isInteger(step.ref_paso)))
      const answer = valid || serverEngine ? result.answer : engineTutorAnswer(report, method, stepContext?.stepIndex)
      setMessages((current) => [...current, { kind: "answer", answer, source: valid ? "model" : "engine", method }])
    } catch {
      setMessages((current) => [...current, { kind: "answer", answer: engineTutorAnswer(report, method, stepContext?.stepIndex), source: "engine", method }])
    } finally {
      setLoading(false)
    }
  }

  return <Sheet open={open} onOpenChange={onOpenChange}>
    <SheetContent className="tutor-sheet flex flex-col gap-0 bg-[#10201c] p-0 text-foreground shadow-[0_30px_90px_#0009]" showCloseButton={false}>
      <SheetHeader className="relative flex-row items-center gap-3 border-b border-cyan-300/20 p-4 pr-14">
        <TutorAvatar className="size-12 border-2 border-[#5fd4ff] shadow-[0_0_18px_#5fd4ff55]" />
        <div className="min-w-0"><SheetTitle className="text-base font-semibold">Tutor de IA · Matrices</SheetTitle><SheetDescription className="text-xs">Explicaciones con valores exactos del motor.</SheetDescription></div>
        <SheetClose asChild><Button type="button" variant="ghost" size="icon" className="absolute right-3 top-4" aria-label="Cerrar tutor"><X /></Button></SheetClose>
      </SheetHeader>
      <Alert className="mx-4 mt-3 w-auto shrink-0 border-primary/20 bg-primary/5 text-xs"><ShieldCheck className="size-4" /><AlertDescription>Las preguntas escritas usan OpenAI y consumen la cuota configurada. No compartas secretos ni datos personales.</AlertDescription></Alert>
      <ScrollArea className="min-h-0 flex-1 px-4 py-4" aria-label="Conversación con el tutor">
        <div className="space-y-4 pb-3">
          <div className="flex items-start gap-2.5"><TutorAvatar className="mt-0.5 size-8 border border-[#5fd4ff]" /><div className="max-w-[85%] rounded-2xl rounded-tl-sm border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-sm leading-relaxed"><p>¡Hola! Elige una ayuda rápida o pregúntame sobre tu sistema. Las cifras vienen de la calculadora.</p>{stepContext && <p className="mt-2 text-xs text-cyan-200">Estoy viendo el paso {stepContext.stepIndex + 1} contigo.</p>}</div></div>
          {report && stepContext && messages.length === 0 && <TutorAnswerView answer={actionTutorAnswer(report, method, "step", stepIndex)} source="engine" report={report} method={method} action="step" />}
          {messages.map((message, index) => message.kind === "user" ? <div key={index} className="ml-auto max-w-[85%] rounded-2xl rounded-tr-sm bg-primary px-4 py-3 text-sm text-primary-foreground whitespace-pre-wrap">{message.text}</div> : report ? <div key={index} ref={index === messages.length - 1 ? latestAnswerRef : undefined}><TutorAnswerView answer={message.answer} source={message.source} report={report} method={message.method} action={message.action} /></div> : null)}
          {loading && <div className="flex items-center gap-2 text-sm text-muted-foreground" role="status"><LoaderCircle className="size-4 animate-spin motion-reduce:animate-none" />Estoy preparando una explicación clara…</div>}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>
      <form className="shrink-0 border-t border-cyan-300/20 bg-[#0d1715] px-4 pt-3 pb-[max(1rem,env(safe-area-inset-bottom))]" onSubmit={(event) => { event.preventDefault(); void submit() }}>
        <div className="mb-3 flex flex-wrap gap-2" aria-label="Ayudas rápidas del motor">{actions.map(({ label, action }) => <button key={action} type="button" disabled={!report} onClick={() => runAction(action, label)} className="inline-flex items-center gap-1.5 rounded-full border border-cyan-300/30 bg-cyan-300/10 px-3 py-1.5 text-xs text-cyan-100 transition-colors hover:bg-cyan-300/20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#5fd4ff] disabled:cursor-not-allowed disabled:opacity-45"><Sparkles className="size-3.5" />{label}</button>)}</div>
        {error && <p className="mb-2 text-sm text-rose-300" role="alert">{error}</p>}
        {!report && <p className="mb-2 text-xs text-amber-200">Resuelve un sistema para activar el tutor contextual.</p>}
        <Textarea ref={textareaRef} value={question} onChange={(event) => setQuestion(event.target.value)} maxLength={500} rows={3} placeholder="Escribe tu pregunta sobre el sistema actual…" aria-label="Pregunta para el Tutor IA" />
        <div className="mt-2 flex items-center justify-between gap-3"><small className="text-muted-foreground">{question.length}/500 · Hasta cinco preguntas por minuto</small><Button type="submit" disabled={loading || !question.trim() || !input || !report}>{loading ? <LoaderCircle className="animate-spin motion-reduce:animate-none" /> : <Send />}Enviar</Button></div>
      </form>
    </SheetContent>
  </Sheet>
}
