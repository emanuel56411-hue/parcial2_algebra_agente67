# Interpretación de operaciones — TechChip Systems

La guía contiene una inconsistencia: el vector esperado (15, 20, 25, 10, 15, 20) requiere B = (185, 200, 280, 150, 245, 195). No resuelve el B original (155, 160, 225, 140, 215, 175). Ambos casos se conservan por separado.

## TechChip · datos originales

Plan de producción inalcanzable por restricción de materias primas.
La solución de AX = B exige cantidades negativas: x1 = -105/83 (≈ -1.265060).
No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa.
La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

| Producto | Miles de módulos (exacto) | Aproximación |
|---|---:|---:|
| AI-Edge 1 | -105/83 | -1.265060 |
| AI-Server Pro | 345/83 | 4.156627 |
| AI-Autonomous Car | 2430/83 | 29.277108 |
| AI-IoT LowPower | 1170/83 | 14.096386 |
| AI-Robotics Heavy | 1130/83 | 13.614458 |
| AI-Medical Vision | 2010/83 | 24.216867 |

E = (0, 0, 0, 0, 0, 0); error máximo = 0.

## TechChip · vector esperado

Plan factible para el modelo continuo: todas las cantidades son no negativas y AX = B consume el 100 % de cada disponibilidad.
X se expresa en miles de unidades; X·1000 se informa como cantidad continua, sin redondear a unidades enteras.
La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

| Producto | Miles de módulos (exacto) | Aproximación |
|---|---:|---:|
| AI-Edge 1 | 15 | 15.000000 |
| AI-Server Pro | 20 | 20.000000 |
| AI-Autonomous Car | 25 | 25.000000 |
| AI-IoT LowPower | 10 | 10.000000 |
| AI-Robotics Heavy | 15 | 15.000000 |
| AI-Medical Vision | 20 | 20.000000 |

E = (0, 0, 0, 0, 0, 0); error máximo = 0.

## Escasez · resina a 100 kg

Plan de producción inalcanzable por restricción de materias primas.
La solución de AX = B exige cantidades negativas: x1 = -26355/83 (≈ -317.530120); x2 = -6780/83 (≈ -81.686747).
No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa.
La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

| Producto | Miles de módulos (exacto) | Aproximación |
|---|---:|---:|
| AI-Edge 1 | -26355/83 | -317.530120 |
| AI-Server Pro | -6780/83 | -81.686747 |
| AI-Autonomous Car | 18555/83 | 223.554217 |
| AI-IoT LowPower | 3170/83 | 38.192771 |
| AI-Robotics Heavy | 3505/83 | 42.228916 |
| AI-Medical Vision | 6510/83 | 78.433735 |

E = (0, 0, 0, 0, 0, 0); error máximo = 0.

## Singular · sin solución

Las restricciones se contradicen: no existe un vector X que cumpla todas las igualdades.
Revisa las ecuaciones dependientes y sus disponibilidades antes de proponer un plan.

## Singular · infinitas soluciones

Hay 1 variable(s) libre(s): los datos no determinan una solución única.
La familia X = Xₚ + t₁v₁ + … describe todas las soluciones reales; hacen falta restricciones independientes para reducir la ambigüedad.
La viabilidad de esta familia bajo X ≥ 0 requiere un análisis adicional; no se declara un plan de producción viable.

## Decisión recomendada

Aclarar con el docente o propietario de los datos cuál disponibilidad es válida. En un contexto industrial, si se permiten capacidades ociosas, modelar AX ≤ B con X ≥ 0 e incorporar demanda y una función objetivo. No sustituir producciones negativas por cero: se perderían las igualdades. Las cantidades continuas en miles tampoco garantizan una solución en unidades enteras.
