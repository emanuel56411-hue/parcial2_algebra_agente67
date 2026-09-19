import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

type Props = {
  A: string[][]
  B: string[]
  onChange: (A: string[][], B: string[]) => void
}

export function MatrixEditor({ A, B, onChange }: Props) {
  const n = A.length
  const updateA = (row: number, column: number, value: string) => {
    const next = A.map((values) => [...values])
    next[row][column] = value
    onChange(next, B)
  }
  const updateB = (row: number, value: string) => {
    const next = [...B]
    next[row] = value
    onChange(A, next)
  }

  return (
    <div className="max-w-full overflow-x-auto rounded-xl border bg-muted/20 p-3 sm:p-5" tabIndex={0} aria-label={`Editor de matriz ${n} por ${n}`}>
      <div className="grid min-w-max gap-2" style={{ gridTemplateColumns: `2.5rem repeat(${n}, minmax(3.75rem, 1fr)) minmax(4.25rem, 1fr)` }}>
        <span />
        {A[0].map((_, column) => <span key={column} className="pb-1 text-center font-mono text-xs font-semibold text-muted-foreground">x{column + 1}</span>)}
        <span className="pb-1 text-center font-mono text-xs font-semibold text-primary">B</span>
        {A.map((row, rowIndex) => (
          <div className="contents" key={rowIndex}>
            <span className="flex items-center font-mono text-xs font-semibold text-muted-foreground">F{rowIndex + 1}</span>
            {row.map((value, columnIndex) => (
              <div key={columnIndex}>
                <Label className="sr-only" htmlFor={`a-${rowIndex}-${columnIndex}`}>A fila {rowIndex + 1}, columna {columnIndex + 1}</Label>
                <Input id={`a-${rowIndex}-${columnIndex}`} className="h-10 min-w-15 px-2 text-center font-mono" value={value} onChange={(event) => updateA(rowIndex, columnIndex, event.target.value)} />
              </div>
            ))}
            <div className="border-l-2 border-primary/50 pl-2">
              <Label className="sr-only" htmlFor={`b-${rowIndex}`}>B fila {rowIndex + 1}</Label>
              <Input id={`b-${rowIndex}`} className="h-10 min-w-17 bg-primary/5 px-2 text-center font-mono" value={B[rowIndex]} onChange={(event) => updateB(rowIndex, event.target.value)} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
