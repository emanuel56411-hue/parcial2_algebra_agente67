import { useState } from "react"
import { Check, Copy } from "lucide-react"
import { ExactValue, MathFormula, MathLine } from "@/components/math-value"
import { MatrixDisplay } from "@/components/procedure/matrix-display"
import { TutorAvatar } from "@/components/tutor/tutor-avatar"
import { Button } from "@/components/ui/button"
import { methodSteps, plainTutorText, tokenizeTutorText } from "@/lib/tutor-contract"
import type { TutorAction, TutorAnswer, TutorSource } from "@/lib/tutor-contract"
import type { Analysis } from "@/types/analysis"

function TutorText({ value, report, method }: { value: string; report: Analysis; method: string }) {
  return <div className="leading-relaxed">{tokenizeTutorText(value, report, method).map((token, index) => {
    if (token.kind === "text") return <span key={index}>{token.text}</span>
    if (token.kind === "matrix") return <div key={index} className="my-3 min-w-0"><MatrixDisplay matrix={token.matrix} split={token.split} label="Matriz exacta del motor" /></div>
    return <span key={index} className="mx-1 inline-flex flex-wrap items-center gap-1 rounded-md bg-primary/10 px-1.5 py-0.5 align-middle"><MathFormula source={`${token.label} =`} /><ExactValue value={token.value} showDecimal={token.approximate} /></span>
  })}</div>
}

export function TutorAnswerView({ answer, source, report, method, action }: { answer: TutorAnswer; source: TutorSource; report: Analysis; method: string; action?: TutorAction }) {
  const [copied, setCopied] = useState(false)
  const steps = methodSteps(report, method)
  async function copy() {
    const lines = [answer.resumen, ...answer.pasos.flatMap((step) => [step.titulo, step.que, step.por_que]), answer.conclusion]
    const text = lines.map((line) => plainTutorText(line, report, method)).join("\n")
    try { await navigator.clipboard.writeText(text); setCopied(true); window.setTimeout(() => setCopied(false), 2000) } catch { setCopied(false) }
  }
  return <div className="flex min-w-0 items-start gap-2.5">
    <TutorAvatar className="mt-0.5 size-8 border border-violet-300" />
    <article className="min-w-0 flex-1 space-y-3 rounded-2xl rounded-tl-sm border border-violet-300/40 bg-violet-100/55 p-3 text-sm dark:bg-violet-950/25">
      {answer.fuera_de_tema ? <p>Con gusto te ayudo con el sistema actual. Pregúntame sobre sus pasos, sus matrices o su resultado.</p> : <>
        <TutorText value={answer.resumen} report={report} method={method} />
        {answer.pasos.map((item, index) => {
          const step = item.ref_paso === null ? null : steps[item.ref_paso - 1]
          return <section key={index} className="space-y-2 rounded-xl border border-violet-300/30 bg-white/55 p-3 dark:bg-slate-950/25">
            <h3 className="font-semibold text-violet-800 dark:text-violet-100"><TutorText value={item.titulo} report={report} method={method} /></h3>
            <p className="text-[11px] font-bold uppercase tracking-wider text-sky-700 dark:text-sky-200">Qué hice</p><TutorText value={item.que} report={report} method={method} />
            <p className="text-[11px] font-bold uppercase tracking-wider text-amber-700 dark:text-amber-200">Por qué</p><TutorText value={item.por_que} report={report} method={method} />
            {step && ![item.titulo, item.que, item.por_que].some((text) => text.includes(`{{matriz:paso${item.ref_paso}}}`)) && <div className="pt-2"><MatrixDisplay matrix={step.matrix} split={step.split} step={step} label={`Matriz del paso ${item.ref_paso}`} /></div>}
            {step && source === "engine" && action !== "verify" && step.calc.length > 0 && <div className="max-w-full overflow-x-auto rounded-lg border border-border bg-background/60 px-3 py-2">{step.calc.map((line, lineIndex) => <MathLine key={lineIndex}>{line}</MathLine>)}</div>}
          </section>
        })}
        {action === "verify" && (report.solution ? <div className="space-y-2">{report.substitution.map((line, index) => <div key={index} className="flex items-start gap-2 rounded-lg border border-border bg-background/60 p-2"><span className="text-emerald-600 dark:text-emerald-300">{report.residual[index] === "0" ? "✓" : "!"}</span><div className="min-w-0 overflow-x-auto"><MathLine>{line}</MathLine></div></div>)}</div> : <div className="flex flex-wrap gap-3 rounded-lg border border-border bg-background/60 p-2"><span>rango(A): <ExactValue value={report.rank_A} /></span><span>rango([A|B]): <ExactValue value={report.rank_augmented} /></span></div>)}
        <TutorText value={answer.conclusion} report={report} method={method} />
      </>}
      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-violet-300/30 pt-2">{source === "engine" ? <small className="text-muted-foreground">Explicación generada por el motor</small> : <small className="text-muted-foreground">Texto revisado con valores exactos del motor</small>}<Button type="button" size="sm" variant="outline" onClick={() => void copy()} className="h-7 gap-1.5 text-xs">{copied ? <Check className="size-3.5" /> : <Copy className="size-3.5" />}Copiar</Button></div>
    </article>
  </div>
}
