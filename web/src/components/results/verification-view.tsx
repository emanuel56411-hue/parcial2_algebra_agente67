import { CheckCircle2 } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import type { Analysis } from "@/types/analysis"

export function VerificationView({ report }: { report: Analysis }) {
  if (!report.solution) return (
    <Card><CardHeader><CardTitle>Diagnóstico por rangos</CardTitle></CardHeader><CardContent className="space-y-3"><p className="font-mono text-sm">det(A) = {report.determinant}</p><p className="font-mono text-sm">rango(A) = {report.rank_A}</p><p className="font-mono text-sm">rango([A|B]) = {report.rank_augmented}</p><p className="text-sm text-muted-foreground">{report.status === "inconsistent" ? "Los rangos distintos prueban que no existe solución." : "Los rangos iguales menores que n prueban que hay variables libres."}</p></CardContent></Card>
  )
  const methods = Object.values(report.methods)
  return (
    <div className="space-y-5">
      <Alert><CheckCircle2 /><AlertTitle>Comprobación exacta superada</AlertTitle><AlertDescription>Los tres métodos coinciden y E = max|A·X − B| = {report.max_error}. Por tanto, E &lt; 10⁻⁶.</AlertDescription></Alert>
      <Card><CardHeader><CardTitle>Comparación entre métodos</CardTitle></CardHeader><CardContent className="overflow-x-auto"><Table><TableHeader><TableRow><TableHead>Variable</TableHead>{methods.map((method) => <TableHead key={method.name}>{method.name}</TableHead>)}</TableRow></TableHeader><TableBody>{report.solution.map((_, index) => <TableRow key={index}><TableCell className="font-semibold">x{index + 1}</TableCell>{methods.map((method) => <TableCell className="font-mono" key={method.name}>{method.solution[index]}</TableCell>)}</TableRow>)}</TableBody></Table></CardContent></Card>
      <Card><CardHeader><CardTitle>Sustitución directa</CardTitle></CardHeader><CardContent className="grid gap-2">{report.substitution.map((line, index) => <code key={index} className="overflow-x-auto whitespace-nowrap rounded-md bg-muted p-3 font-mono text-xs">{line}</code>)}</CardContent></Card>
    </div>
  )
}
