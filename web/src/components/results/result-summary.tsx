import { AlertTriangle, CheckCircle2, CircleX } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { decimal, numeric } from "@/lib/format"
import type { Analysis } from "@/types/analysis"

const labels = { unique: "Solución única", infinite: "Infinitas soluciones", inconsistent: "Sin solución" }

export function StatusBadge({ report }: { report: Analysis }) {
  const variant = report.status === "unique" ? "default" : report.status === "infinite" ? "secondary" : "destructive"
  return <Badge variant={variant}>{labels[report.status]}</Badge>
}

export function ResultSummary({ report }: { report: Analysis }) {
  const negative = Boolean(report.solution?.some((value) => numeric(value) < 0) && report.production)
  const Icon = report.status === "inconsistent" ? CircleX : negative ? AlertTriangle : CheckCircle2
  return (
    <div className="space-y-5">
      <Alert variant={report.status === "inconsistent" ? "destructive" : "default"} className={negative ? "border-amber-500/50 bg-amber-500/5" : ""}>
        <Icon />
        <AlertTitle>{report.status === "unique" ? negative ? "Solución matemática, plan no viable" : "Análisis completado" : labels[report.status]}</AlertTitle>
        <AlertDescription>{report.interpretation[0]}</AlertDescription>
      </Alert>

      {report.solution ? (
        <div className="grid gap-5 lg:grid-cols-[1.1fr_.9fr]">
          <Card>
            <CardHeader><CardTitle>Solución por variable</CardTitle></CardHeader>
            <CardContent className="overflow-x-auto">
              <Table>
                <TableHeader><TableRow><TableHead>Variable</TableHead><TableHead>Exacto</TableHead><TableHead>Aproximación</TableHead>{report.production && <TableHead>Producción</TableHead>}</TableRow></TableHeader>
                <TableBody>{report.solution.map((value, index) => <TableRow key={index}><TableCell className="font-semibold">x{index + 1}</TableCell><TableCell className="font-mono">{value}</TableCell><TableCell>≈ {decimal(value)}</TableCell>{report.production && <TableCell><Badge variant={numeric(value) < 0 ? "destructive" : "outline"}>{numeric(value) < 0 ? "No viable" : "No negativa"}</Badge></TableCell>}</TableRow>)}</TableBody>
              </Table>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Interpretación operacional</CardTitle></CardHeader>
            <CardContent><ul className="space-y-3 text-sm text-muted-foreground">{report.interpretation.slice(1).map((item, index) => <li key={index} className="flex gap-3"><span className="mt-2 size-1.5 shrink-0 rounded-full bg-primary" />{item}</li>)}</ul></CardContent>
          </Card>
        </div>
      ) : report.particular ? (
        <Card><CardHeader><CardTitle>Familia de soluciones</CardTitle></CardHeader><CardContent className="space-y-3"><code className="block overflow-x-auto rounded-lg bg-muted p-4 font-mono text-sm">X = ({report.particular.join(", ")}) {report.nullspace.map((vector, index) => `+ t${index + 1}·(${vector.join(", ")})`).join(" ")}</code><p className="text-sm text-muted-foreground">Los parámetros t₁, t₂, … pueden tomar cualquier valor real.</p></CardContent></Card>
      ) : (
        <Card><CardHeader><CardTitle>El sistema es incompatible</CardTitle></CardHeader><CardContent><p className="text-sm text-muted-foreground">Una fila de la forma 0 = c, con c ≠ 0, demuestra que ninguna X satisface todas las ecuaciones.</p></CardContent></Card>
      )}
    </div>
  )
}
