export function numeric(value: string | number) {
  const [numerator, denominator = "1"] = String(value).split("/")
  return Number(numerator) / Number(denominator)
}

export function decimal(value: string | number) {
  const number = numeric(value)
  if (!Number.isFinite(number)) return "—"
  if (number !== 0 && (Math.abs(number) >= 1e9 || Math.abs(number) < 1e-5)) return number.toExponential(5)
  return number.toLocaleString("es-SV", { maximumFractionDigits: 6 })
}

export function downloadJson(filename: string, data: unknown) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement("a")
  anchor.href = url
  anchor.download = filename
  anchor.click()
  window.setTimeout(() => URL.revokeObjectURL(url), 1000)
}
