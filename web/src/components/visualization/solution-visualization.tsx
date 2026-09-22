import { lazy, Suspense } from "react"
import { ChartNoAxesCombined } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

import type { Analysis } from "@/types/analysis"

const SolutionGraph2D = lazy(() => import("@/components/visualization/solution-graph-2d").then((module) => ({ default: module.SolutionGraph2D })))
const SolutionGraph3D = lazy(() => import("@/components/visualization/solution-graph-3d"))
const SolutionGraphND = lazy(() => import("@/components/visualization/solution-graph-nd").then((module) => ({ default: module.SolutionGraphND })))

export function SolutionVisualization({ report }: { report: Analysis }) {
  const size = report.A.length
  return <Card><CardHeader><CardTitle className="flex items-center gap-2"><ChartNoAxesCombined className="size-5 text-primary" /> Gráfica de la solución</CardTitle></CardHeader><CardContent>{size === 2 ? <Suspense fallback={<div className="grid h-80 place-items-center rounded-xl border text-sm text-muted-foreground">Cargando rectas…</div>}><SolutionGraph2D report={report} /></Suspense> : size === 3 ? <Suspense fallback={<div className="grid h-80 place-items-center rounded-xl border text-sm text-muted-foreground">Cargando planos…</div>}><SolutionGraph3D report={report} /></Suspense> : <Suspense fallback={<div className="grid h-72 place-items-center rounded-xl border text-sm text-muted-foreground">Cargando vector n-dimensional…</div>}><SolutionGraphND report={report} /></Suspense>}</CardContent></Card>
}
