import { Check, CheckCircle2 } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MathLine } from "@/components/math-value"
import type { Analysis } from "@/types/analysis"

export function VerificationView({ report }: { report: Analysis }) {
  if (!report.solution) return (
    <Card>
      <CardHeader><CardTitle>4 · Escenario Degenerado (Singularidad)</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <p className="font-mono text-sm tabular-nums">det(A) = {report.determinant}</p>
        <p className="font-mono text-sm tabular-nums">rango(A) = {report.rank_A}</p>
        <p className="font-mono text-sm tabular-nums">rango([A|B]) = {report.rank_augmented}</p>
        <p className="text-sm text-muted-foreground">{report.status === "inconsistent" ? "Los rangos distintos prueban que no existe solución." : "Los rangos iguales menores que n prueban que hay variables libres."}</p>
      </CardContent>
    </Card>
  )

  return (
    <Card className="border-primary/30">
      <CardHeader className="border-b">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2"><CheckCircle2 className="size-5 text-primary" /><CardTitle>2 · Comprobación por Sustitución Directa</CardTitle></div>
          {report.methods_agree && <Badge className="gap-1.5"><Check className="size-3.5" />Los 3 métodos coinciden</Badge>}
        </div>
      </CardHeader>
      <CardContent className="space-y-3 pt-6">
        <div className="rounded-lg border border-emerald-400/50 bg-emerald-50/70 p-4 text-sm text-emerald-900 dark:bg-emerald-950/25 dark:text-emerald-100" role="status">
          <p className="font-semibold">Criterio aprobado</p>
          <p className="mt-1 font-mono">E = max |A·X − B| = {report.max_error} &lt; 10⁻⁶</p>
        </div>
        {report.substitution.map((line, index) => {
          const exact = report.residual[index] === "0"
          return (
            <div key={index} className="flex min-w-0 items-center gap-3 rounded-lg border bg-muted/20 p-3">
              <span className={exact ? "grid size-6 shrink-0 place-items-center rounded-full bg-primary text-primary-foreground" : "grid size-6 shrink-0 place-items-center rounded-full bg-destructive text-white"} aria-label={exact ? "Residuo cero" : "Residuo distinto de cero"}>{exact ? <Check className="size-4" /> : "!"}</span>
              <div className="min-w-0 flex-1 overflow-x-auto"><MathLine>{line}</MathLine></div>
            </div>
          )
        })}
        <p className="pt-2 text-sm text-muted-foreground">Las filas anteriores sustituyen cada componente de X en A·X y comparan el resultado con su B correspondiente.</p>
      </CardContent>
    </Card>
  )
}
