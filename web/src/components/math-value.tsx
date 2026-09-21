import katex from "katex"
import { cn } from "@/lib/utils"
import { decimal } from "@/lib/format"

const fraction = /(-?\d+)\/(\d+)/g

export function toTex(source: string) {
  return source
    .replace(fraction, (_match, top: string, bottom: string) => `${top.startsWith("-") ? "-" : ""}\\frac{${top.replace("-", "")}}{${bottom}}`)
    .replace(/A⁻¹/g, "A^{-1}")
    .replace(/([xFt])(\d+)/g, "$1_{$2}")
    .replace(/−/g, "-")
    .replace(/·/g, "\\cdot ")
    .replace(/←/g, "\\leftarrow ")
    .replace(/↔/g, "\\leftrightarrow ")
    .replace(/≥/g, "\\geq ")
    .replace(/≤/g, "\\leq ")
    .replace(/≠/g, "\\ne ")
    .replace(/→/g, "\\longrightarrow ")
    .replace(/ᵢ/g, "_i")
    .replace(/\bResultado:/g, "\\text{Resultado: }\\quad ")
    .replace(/\bfactor\b/g, "\\text{factor}")
    .replace(/\brango\b/g, "\\operatorname{rango}")
    .replace(/\bdet\b/g, "\\det")
    .replace(/\bpara\b/g, "\\text{ para }")
}

export function MathFormula({ source, className }: { source: string; className?: string }) {
  const html = katex.renderToString(toTex(source), { throwOnError: false, output: "html", strict: "ignore" })
  return <span className={cn("math-formula", className)} aria-label={source} dangerouslySetInnerHTML={{ __html: html }} />
}

export function ExactValue({ value, showDecimal = false, className }: {
  value: string | number
  showDecimal?: boolean
  className?: string
}) {
  const raw = String(value)
  return <span className={cn("inline-flex items-center gap-1.5 whitespace-nowrap tabular-nums", raw.startsWith("-") && "text-rose-300", className)}>
    <MathFormula source={raw} />
    {showDecimal && <span className="font-sans text-[0.78em] font-normal text-muted-foreground">(≈ {decimal(raw)})</span>}
  </span>
}

export function MathText({ children }: { children: string }) {
  const pieces = children.split(/(-?\d+\/\d+|(?:x|F|t)\d+|A⁻¹)/g)
  return <>{pieces.map((piece, index) => /^-?\d+\/\d+$|^(?:x|F|t)\d+$|^A⁻¹$/.test(piece)
    ? <span key={index} className="mx-0.5"><MathFormula source={piece} />{/^-?\d+\/\d+$/.test(piece) && <span className="ml-1 text-xs text-muted-foreground">(≈ {decimal(piece)})</span>}</span>
    : <span key={index}>{piece}</span>)}</>
}

export function MathLine({ children, align = false }: { children: string; align?: boolean }) {
  if (align && children.includes("=")) {
    const offset = children.indexOf("=")
    return <div className="table-row whitespace-nowrap text-xs leading-7 tabular-nums sm:text-sm"><span className="table-cell py-1 pr-3 text-right"><MathFormula source={children.slice(0, offset).trim()} /></span><span className="table-cell py-1 pr-3"><MathFormula source="=" /></span><span className="table-cell py-1"><MathFormula source={children.slice(offset + 1).trim()} /></span></div>
  }
  return <div className={align ? "table-row whitespace-nowrap text-xs leading-7 tabular-nums sm:text-sm" : "min-w-max whitespace-nowrap py-1 text-xs leading-7 tabular-nums sm:text-sm"}><span className={align ? "table-cell py-1" : ""}><MathFormula source={children} /></span></div>
}
