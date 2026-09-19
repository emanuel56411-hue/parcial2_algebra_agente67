# Informe de interpretación de operaciones

## Resumen ejecutivo

Con el vector compatible **X = (15, 20, 25, 10, 15, 20)** miles de módulos, el modelo de igualdades consume exactamente **B = (185, 200, 280, 150, 245, 195)**. No queda capacidad ociosa dentro de este escenario matemático. Esta conclusión no aplica al B impreso en la guía, cuya solución exige `x1 = -105/83`.

## Producción por línea

| Línea | Producción por turno |
|---|---:|
| AI-Edge 1 | 15 mil módulos |
| AI-Server Pro | 20 mil módulos |
| AI-Autonomous Car | 25 mil módulos |
| AI-IoT LowPower | 10 mil módulos |
| AI-Robotics Heavy | 15 mil módulos |
| AI-Medical Vision | 20 mil módulos |

Producción total: **105 mil módulos por turno**.

## Aporte de cada línea al consumo de recursos

Cada celda es el producto exacto `aᵢⱼxⱼ`. La suma horizontal reproduce la disponibilidad del recurso.

| Recurso | x1 | x2 | x3 | x4 | x5 | x6 | Total / disponible | Unidad |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Litografía EUV | 30 | 20 | 75 | 10 | 30 | 20 | 185 / 185 | horas-máquina |
| Pruebas ATE | 15 | 60 | 50 | 20 | 15 | 40 | 200 / 200 | horas-máquina |
| Resina de encapsulado | 45 | 40 | 100 | 10 | 45 | 40 | 280 / 280 | kg |
| Sustrato de silicio | 15 | 20 | 25 | 40 | 30 | 20 | 150 / 150 | m² |
| Energía láser | 30 | 20 | 50 | 10 | 75 | 60 | 245 / 245 | MWh |
| Inspección óptica | 15 | 40 | 25 | 20 | 15 | 80 | 195 / 195 | horas-hombre |

En los seis recursos se verifica `consumo = disponibilidad`; por tanto, el uso es del **100 %** y la holgura es exactamente **0**. Esto describe el caso compatible y no constituye por sí solo una optimización económica.

## Escasez de resina

Al sustituir únicamente `B3=225` por `B3=100`, el agente obtiene `X = (-26355/83, -6780/83, 18555/83, 3170/83, 3505/83, 6510/83)`. Las producciones `x1=-26355/83` y `x2=-6780/83` son negativas. Por tanto, no existe un plan físicamente realizable con `X≥0` que agote simultáneamente todas las capacidades bajo `AX=B`. El error algebraico continúa siendo cero: el problema es de factibilidad empresarial, no de cálculo.

## Dependencia y contradicción

Si `F6=2F1` pero se conserva `B6=175`, la sexta ecuación exige simultáneamente `2B1=310` y `B6=175`: `rango(A)=5`, `rango([A|B])=6` y no existe solución. Si también se establece `B6=310`, ambos rangos son 5 y aparece una familia con una variable libre. Operacionalmente, una restricción redundante no aporta información nueva; una restricción proporcional con disponibilidad incompatible revela datos o políticas contradictorias.

## Recomendaciones

1. Validar con la fuente del caso si el B oficial es `(155,160,225,140,215,175)` o el compatible `(185,200,280,150,245,195)`.
2. No redondear ni reemplazar producciones negativas por cero: se destruiría `AX=B`.
3. Si se permite capacidad ociosa, reformular como `AX≤B`, `X≥0` e incorporar demanda.
4. Para hablar de un plan óptimo, añadir costos, márgenes o tiempos como función objetivo; el sistema actual determina balance, no optimalidad.
5. Auditar filas proporcionales antes de planificar para distinguir redundancia válida de datos contradictorios.
