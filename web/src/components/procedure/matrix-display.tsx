import { motion, useReducedMotion } from "framer-motion"
import { cn } from "@/lib/utils"
import { numeric } from "@/lib/format"
import { ExactValue } from "@/components/math-value"
import type { Matrix, Step } from "@/types/analysis"

type Props = { matrix: Matrix; split: number; step?: Step; previous?: Matrix | null; label?: string }

export function MatrixDisplay({ matrix, split, step, previous, label = "Matriz resultante" }: Props) {
  const reduced = useReducedMotion()
  const maximum = Math.max(1, ...matrix.flat().map((value) => Math.abs(numeric(value))).filter(Number.isFinite))
  return <div>
    <div className="matrix-scroll max-w-full overflow-x-auto rounded-xl border bg-muted/20 p-3 sm:p-4" tabIndex={0} aria-label={label}>
      <div className="mx-auto flex w-max min-w-full items-stretch justify-center">
        <span className="matrix-bracket" aria-hidden="true">[</span>
        <table className="min-w-max border-separate border-spacing-x-1 border-spacing-y-1 text-xs tabular-nums sm:text-sm"><tbody>
          {matrix.map((row, rowIndex) => <motion.tr key={rowIndex} layout={!reduced && step?.kind === "swap"} transition={{ duration: reduced ? 0 : 0.35 }} className={cn(step?.changed_rows?.includes(rowIndex) && "bg-primary/10", step?.source === rowIndex && "outline outline-1 outline-amber-400/60")}>
            {row.map((value, columnIndex) => {
              const amount = numeric(value)
              const strength = Math.min(0.24, 0.06 + 0.18 * Math.abs(amount) / maximum)
              const changed = previous?.[rowIndex] && String(previous[rowIndex][columnIndex]) !== String(value)
              const pivotColumn = step?.pivot?.[1] === columnIndex
              const pivotCell = step?.pivot?.[0] === rowIndex && pivotColumn
              return <td key={columnIndex} className={cn("matrix-cell min-w-14 rounded px-2 py-2 text-center align-middle", columnIndex === split && "border-l-[3px] border-primary/80 pl-4", pivotColumn && "outline outline-1 outline-amber-400/25", changed && "font-bold", pivotCell && "ring-2 ring-amber-300 ring-inset shadow-[0_0_14px_#fcd34d55]")} style={{ backgroundColor: amount === 0 ? "rgba(148,163,184,.05)" : amount > 0 ? `rgba(52,211,153,${strength})` : `rgba(251,113,133,${strength})` }}><ExactValue value={value} showDecimal={String(value).includes("/")} /></td>
            })}
          </motion.tr>)}
        </tbody></table>
        <span className="matrix-bracket" aria-hidden="true">]</span>
      </div>
    </div>
    <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-muted-foreground" aria-label="Leyenda de la matriz"><span><i className="mr-1 inline-block size-2.5 rounded bg-emerald-400/50" />positivo</span><span><i className="mr-1 inline-block size-2.5 rounded bg-rose-400/50" />negativo</span><span><i className="mr-1 inline-block size-2.5 rounded bg-slate-400/20" />cero</span><span><i className="mr-1 inline-block size-2.5 rounded border-2 border-amber-300" />pivote</span></div>
  </div>
}
