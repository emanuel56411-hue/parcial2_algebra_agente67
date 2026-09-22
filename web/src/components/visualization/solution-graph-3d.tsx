import { Canvas } from "@react-three/fiber"
import { OrbitControls } from "@react-three/drei"
import { DoubleSide } from "three"
import { numeric } from "@/lib/format"
import type { Analysis } from "@/types/analysis"

const colors = ["#86efac", "#fde68a", "#f9a8d4"]

function Plane({ row, right, color, scale }: { row: number[]; right: number; color: string; scale: number }) {
  const axis = row.reduce((best, value, index) => Math.abs(value) > Math.abs(row[best]) ? index : best, 0)
  if (Math.abs(row[axis]) < 1e-12) return null
  const other = [0, 1, 2].filter((i) => i !== axis)
  const corners = [[-scale, -scale], [scale, -scale], [scale, scale], [-scale, scale]].map(([u, v]) => {
    const point = [0, 0, 0]
    point[other[0]] = u; point[other[1]] = v
    point[axis] = (right - row[other[0]] * u - row[other[1]] * v) / row[axis]
    return point as [number, number, number]
  })
  const positions = new Float32Array([...corners[0], ...corners[1], ...corners[2], ...corners[0], ...corners[2], ...corners[3]])
  return <mesh><bufferGeometry><bufferAttribute attach="attributes-position" args={[positions, 3]} /></bufferGeometry><meshStandardMaterial color={color} transparent opacity={0.38} side={DoubleSide} depthWrite={false} /></mesh>
}

export default function SolutionGraph3D({ report }: { report: Analysis }) {
  const solution = report.solution?.map(numeric)
  const scale = Math.max(4, ...(solution || []).map(Math.abs)) * 1.4
  return <div className="overflow-hidden rounded-xl border bg-violet-50/60 dark:bg-violet-950/20">
    <div className="h-80"><Canvas camera={{ position: [scale * 1.6, scale * 1.4, scale * 1.6], fov: 50 }}><ambientLight intensity={1.8} /><directionalLight position={[5, 8, 5]} intensity={2} /><gridHelper args={[scale * 2, 10, "#4b7568", "#244239"]} /><axesHelper args={[scale]} />{report.A.map((row, i) => <Plane key={i} row={row.map(numeric)} right={numeric(report.B[i])} color={colors[i]} scale={scale} />)}{solution && <mesh position={solution as [number, number, number]}><sphereGeometry args={[scale * 0.055, 20, 20]} /><meshStandardMaterial color="white" emissive="white" emissiveIntensity={0.4} /></mesh>}<OrbitControls enablePan={false} /></Canvas></div>
    <p className="px-4 py-3 text-xs text-muted-foreground">Arrastra para rotar · verde, ámbar y rosa: planos 1–3{solution ? " · punto claro: intersección" : " · sin punto de intersección única"}.</p>
  </div>
}
