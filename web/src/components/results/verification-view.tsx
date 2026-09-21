import { Check, CheckCircle2 } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MathLine } from "@/components/math-value"
import type { Analysis } from "@/types/analysis"

export function VerificationView({ report }: { report: Analysis }) {
  if (!report.solution) return (
    <Card>
      <CardHeader><CardTitle>Verificación por rangos</CardTitle></CardHeader>
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
          <div className="flex items-center gap-2"><CheckCircle2 className="size-5 text-primary" /><CardTitle>Verificación: A·X = B</CardTitle></div>
          {report.methods_agree && <Badge className="gap-1.5"><Check className="size-3.5" />Los 3 métodos coinciden</Badge>}
        </div>
      </CardHeader>
      <CardContent className="space-y-3 pt-6">
        {report.substitution.map((line, index) => {
          const exact = report.residual[index] === "0"
          return (
            <div key={index} className="flex min-w-0 items-center gap-3 rounded-lg border bg-muted/20 p-3">
              <span className={exact ? "grid size-6 shrink-0 place-items-center rounded-full bg-primary text-primary-foreground" : "grid size-6 shrink-0 place-items-center rounded-full bg-destructive text-white"} aria-label={exact ? "Residuo cero" : "Residuo distinto de cero"}>{exact ? <Check className="size-4" /> : "!"}</span>
              <div className="min-w-0 flex-1 overflow-x-auto"><MathLine>{line}</MathLine></div>
            </div>
          )
        })}
        <p className="pt-2 text-sm text-muted-foreground">Residuo máximo exacto: <span className="font-mono font-semibold text-foreground">{report.max_error}</span>.</p>
      </CardContent>
    </Card>
  )
}
