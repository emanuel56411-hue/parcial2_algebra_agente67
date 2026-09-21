import { useEffect, useRef, useState } from "react"
import { useReducedMotion } from "framer-motion"
import { LoaderCircle, Send, ShieldCheck, Sparkles, X } from "lucide-react"
import { TutorAvatar } from "@/components/tutor/tutor-avatar"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetClose, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Textarea } from "@/components/ui/textarea"
import { askTutor } from "@/lib/api"
import { cn } from "@/lib/utils"
import type { SolveInput, TutorMessage } from "@/types/analysis"

type StepContext = { method: string; stepIndex: number } | null

type Props = {
  open: boolean
  onOpenChange: (open: boolean) => void
  input: SolveInput | null
  title: string
  note: string
  initialQuestion?: string
  stepContext?: StepContext
}

export function TutorSheet({ open, onOpenChange, input, title, note, initialQuestion = "", stepContext }: Props) {
  const questionSource = `${initialQuestion}:${stepContext?.method ?? "general"}:${stepContext?.stepIndex ?? -1}`
  const [draft, setDraft] = useState({ source: questionSource, value: initialQuestion })
  const question = draft.source === questionSource ? draft.value : initialQuestion
  const setQuestion = (value: string) => setDraft({ source: questionSource, value })
  const [messages, setMessages] = useState<TutorMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const reducedMotion = useReducedMotion()

  useEffect(() => {
    if (open) bottomRef.current?.scrollIntoView({ behavior: reducedMotion ? "instant" : "smooth", block: "end" })
  }, [open, messages, loading, reducedMotion])

  const suggestions = [
    { label: "Explícame este paso", prompt: stepContext ? "Explícame con palabras sencillas el paso seleccionado y por qué funciona." : "Explícame cómo empezar a resolver esta matriz." },
    { label: "¿Por qué el resultado?", prompt: "¿Por qué el sistema tiene este resultado? Explícamelo con un ejemplo sencillo." },
    { label: "Compara los métodos", prompt: "Compara Gauss, Gauss-Jordan y la inversa para este sistema con palabras sencillas." },
  ]

  async function submit(raw: string) {
    const text = raw.trim()
    if (!text || text.length > 1500 || loading) return
    if (!input) { setError("Corrige el JSON de entrada antes de preguntar al tutor."); return }
    setError("")
    const userMessage: TutorMessage = { role: "user", content: text }
    setMessages((current) => [...current, userMessage])
    setQuestion("")
    setLoading(true)
    try {
      const result = await askTutor({
        ...input,
        question: text,
        history: messages.slice(-6),
        title,
        note,
        ...(stepContext ? { method: stepContext.method, step_index: stepContext.stepIndex } : {}),
      })
      setMessages((current) => [...current, { role: "assistant", content: result.answer, meta: `${result.model} · ${result.input_tokens} entrada / ${result.output_tokens} salida` }])
    } catch (caught) {
      setMessages((current) => current.slice(0, -1))
      setError(caught instanceof Error ? caught.message : "No pude responder esta vez. Inténtalo de nuevo.")
    } finally {
      setLoading(false)
    }
  }

  function chooseSuggestion(prompt: string) {
    setQuestion(prompt)
    setError("")
    textareaRef.current?.focus()
  }

  return <Sheet open={open} onOpenChange={onOpenChange}>
    <SheetContent className="tutor-sheet flex flex-col gap-0 bg-[#10201c] p-0 text-foreground shadow-[0_30px_90px_#0009]" showCloseButton={false}>
      <SheetHeader className="relative flex-row items-center gap-3 border-b border-cyan-300/20 p-4 pr-14">
        <TutorAvatar className="size-12 border-2 border-[#5fd4ff] shadow-[0_0_18px_#5fd4ff55]" />
        <div className="min-w-0"><SheetTitle className="text-base font-semibold">Tutor de IA · Matrices</SheetTitle><SheetDescription className="text-xs">Estoy aquí para ayudarte paso a paso.</SheetDescription></div>
        <SheetClose asChild><Button type="button" variant="ghost" size="icon" className="absolute right-3 top-4" aria-label="Cerrar tutor"><X /></Button></SheetClose>
      </SheetHeader>
      <Alert className="mx-4 mt-3 w-auto shrink-0 border-primary/20 bg-primary/5 text-xs"><ShieldCheck className="size-4" /><AlertDescription>Las preguntas usan OpenAI y consumen la cuota configurada. No compartas datos personales.</AlertDescription></Alert>
      <ScrollArea className="min-h-0 flex-1 px-4 py-4" aria-label="Conversación con el tutor">
        <div className="space-y-4 pb-3">
          <div className="flex items-start gap-2.5"><TutorAvatar className="mt-0.5 size-8 border border-[#5fd4ff]" /><div className="max-w-[85%] rounded-2xl rounded-tl-sm border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-sm leading-relaxed"><p>¡Hola! Soy tu tutor de matrices. Dime qué parte quieres entender y la vemos juntos.</p>{stepContext && <p className="mt-2 text-xs text-cyan-200">Estoy viendo el paso {stepContext.stepIndex + 1} contigo.</p>}</div></div>
          {messages.map((message, index) => <div key={index} className={cn("flex items-start gap-2.5", message.role === "user" && "justify-end")}>{message.role === "assistant" && <TutorAvatar className="mt-0.5 size-8 border border-[#5fd4ff]" />}<div className={cn("max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap", message.role === "user" ? "rounded-tr-sm bg-primary text-primary-foreground" : "rounded-tl-sm border border-cyan-300/20 bg-cyan-300/10")}><p>{message.content}</p>{message.meta && <small className="mt-2 block opacity-65">{message.meta}</small>}</div></div>)}
          {loading && <div className="flex items-center gap-2 text-sm text-muted-foreground" role="status"><LoaderCircle className="size-4 animate-spin motion-reduce:animate-none" />Estoy preparando una explicación clara…</div>}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>
      <form className="shrink-0 border-t border-cyan-300/20 bg-[#0d1715] px-4 pt-3 pb-[max(1rem,env(safe-area-inset-bottom))]" onSubmit={(event) => { event.preventDefault(); void submit(question) }}>
        <div className="mb-3 flex flex-wrap gap-2" aria-label="Preguntas sugeridas">{suggestions.map(({ label, prompt }) => <button key={label} type="button" onClick={() => chooseSuggestion(prompt)} className="inline-flex items-center gap-1.5 rounded-full border border-cyan-300/30 bg-cyan-300/10 px-3 py-1.5 text-xs text-cyan-100 transition-colors hover:bg-cyan-300/20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#5fd4ff]"><Sparkles className="size-3.5" />{label}</button>)}</div>
        {error && <p className="mb-2 text-sm text-rose-300" role="alert">{error}</p>}
        {!input && <p className="mb-2 text-xs text-amber-200">Corrige el JSON para activar las preguntas.</p>}
        <Textarea ref={textareaRef} value={question} onChange={(event) => setQuestion(event.target.value)} maxLength={1500} rows={3} placeholder="Pregúntame sobre tu matriz o el paso actual…" aria-label="Pregunta para el Tutor IA" />
        <div className="mt-2 flex items-center justify-between gap-3"><small className="text-muted-foreground">{question.length}/1500</small><Button type="submit" disabled={loading || !question.trim() || !input}>{loading ? <LoaderCircle className="animate-spin motion-reduce:animate-none" /> : <Send />}Enviar</Button></div>
      </form>
    </SheetContent>
  </Sheet>
}
