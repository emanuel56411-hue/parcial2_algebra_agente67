import { useEffect, useState } from "react"
import { Bot, LoaderCircle, Send, ShieldCheck, Sparkles } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Textarea } from "@/components/ui/textarea"
import { askTutor } from "@/lib/api"
import { cn } from "@/lib/utils"
import type { SolveInput, TutorMessage } from "@/types/analysis"

type StepContext = { method: string; stepIndex: number } | null

type Props = {
  open: boolean
  onOpenChange: (open: boolean) => void
  input: SolveInput
  title: string
  note: string
  initialQuestion?: string
  stepContext?: StepContext
}

const suggestions = [
  "¿Por qué este sistema tiene este diagnóstico?",
  "Explica la interpretación empresarial sin cambiar los resultados.",
  "Compara los tres métodos y explica por qué coinciden.",
]

export function TutorSheet({ open, onOpenChange, input, title, note, initialQuestion = "", stepContext }: Props) {
  const [question, setQuestion] = useState(initialQuestion)
  const [messages, setMessages] = useState<TutorMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => { if (initialQuestion) setQuestion(initialQuestion) }, [initialQuestion, stepContext])

  async function submit(raw: string) {
    const text = raw.trim()
    if (!text || text.length > 1500 || loading) return
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
      setError(caught instanceof Error ? caught.message : "El tutor no pudo responder.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="flex w-full flex-col gap-0 p-0 sm:max-w-xl">
        <SheetHeader className="border-b p-5">
          <div className="mb-2 flex size-10 items-center justify-center rounded-xl bg-primary text-primary-foreground"><Bot className="size-5" /></div>
          <SheetTitle>Tutor IA contextual</SheetTitle>
          <SheetDescription>Explica el cálculo actual; el motor racional sigue siendo la fuente de verdad.</SheetDescription>
        </SheetHeader>
        <Alert className="mx-5 mt-4 w-auto border-primary/20 bg-primary/5"><ShieldCheck /><AlertDescription>La consulta usa OpenAI y consume la cuota configurada. No escribas secretos ni datos personales.</AlertDescription></Alert>
        <ScrollArea className="min-h-0 flex-1 px-5 py-4">
          {!messages.length ? (
            <div className="grid gap-2">
              <p className="mb-2 text-xs font-bold uppercase tracking-widest text-muted-foreground">Preguntas sugeridas</p>
              {suggestions.map((suggestion) => <Button key={suggestion} variant="outline" className="h-auto justify-start whitespace-normal py-3 text-left" onClick={() => setQuestion(suggestion)}><Sparkles className="size-4 shrink-0" />{suggestion}</Button>)}
            </div>
          ) : (
            <div className="space-y-3">{messages.map((message, index) => <div key={index} className={cn("max-w-[88%] rounded-xl px-4 py-3 text-sm whitespace-pre-wrap", message.role === "user" ? "ml-auto bg-primary text-primary-foreground" : "border bg-muted")}><p>{message.content}</p>{message.meta && <small className="mt-2 block opacity-65">{message.meta}</small>}</div>)}{loading && <div className="flex items-center gap-2 text-sm text-muted-foreground"><LoaderCircle className="size-4 animate-spin" />El tutor está preparando la explicación…</div>}</div>
          )}
        </ScrollArea>
        <form className="border-t p-4" onSubmit={(event) => { event.preventDefault(); void submit(question) }}>
          {error && <p className="mb-3 text-sm text-destructive" role="alert">{error}</p>}
          <Textarea value={question} onChange={(event) => setQuestion(event.target.value)} maxLength={1500} rows={4} placeholder="Pregunta sobre la solución o el paso seleccionado…" aria-label="Pregunta para el Tutor IA" />
          <div className="mt-3 flex items-center justify-between gap-3"><small className="text-muted-foreground">{question.length}/1500</small><Button type="submit" disabled={loading || !question.trim()}>{loading ? <LoaderCircle className="animate-spin" /> : <Send />}Enviar</Button></div>
        </form>
      </SheetContent>
    </Sheet>
  )
}
