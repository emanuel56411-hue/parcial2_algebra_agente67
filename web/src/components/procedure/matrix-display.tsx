import { cn } from "@/lib/utils"
import type { Matrix, Step } from "@/types/analysis"

type Props = {
  matrix: Matrix
  split: number
  step?: Step
  previous?: Matrix | null
  label?: string
}

export function MatrixDisplay({ matrix, split, step, previous, label = "Matriz resultante" }: Props) {
  return (
    <div className="max-w-full overflow-x-auto rounded-lg border bg-muted/20 p-3" tabIndex={0} aria-label={label}>
      <table className="mx-auto min-w-max border-separate border-spacing-1 font-mono text-xs sm:text-sm">
        <tbody>
          {matrix.map((row, rowIndex) => (
            <tr key={rowIndex} className={cn(
              step?.target === rowIndex && "bg-primary/10",
              step?.source === rowIndex && "outline outline-1 outline-amber-500/60",
            )}>
              {row.map((value, columnIndex) => {
                const changed = previous?.[rowIndex] && String(previous[rowIndex][columnIndex]) !== String(value)
                return (
                  <td key={columnIndex} className={cn(
                    "min-w-12 rounded px-2 py-1.5 text-right",
                    columnIndex === split && "border-l-2 border-primary pl-3",
                    changed && "bg-primary/15 font-bold text-primary",
                  )}>{value}</td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
