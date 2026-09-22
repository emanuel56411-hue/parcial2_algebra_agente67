# Informe de interpretación de operaciones — TechChip Systems

## Conclusión principal

Con las disponibilidades originales **B = (155, 160, 225, 140, 215, 175)**, los tres métodos obtienen exactamente `X = (-105, 345, 2430, 1170, 1130, 2010)/83`, con determinante `-83` y residuo cero. Como `x1=-105/83≈-1.265060`, el balance algebraico existe pero no constituye un plan de producción físicamente viable bajo `X≥0`.

El vector `(15,20,25,10,15,20)` de la guía es incorrecto para el B original. Solo aparece al reemplazar B por `(185,200,280,150,245,195)`; ese segundo caso se conserva exclusivamente como comparación didáctica.

## Resultado por línea para el B original

| Línea | Valor exacto | Aproximación (miles de módulos) |
|---|---:|---:|
| AI-Edge 1 | -105/83 | -1.265060 |
| AI-Server Pro | 345/83 | 4.156627 |
| AI-Autonomous Car | 2430/83 | 29.277108 |
| AI-IoT LowPower | 1170/83 | 14.096386 |
| AI-Robotics Heavy | 1130/83 | 13.614458 |
| AI-Medical Vision | 2010/83 | 24.216867 |

## Balance cuantitativo

La sustitución exacta devuelve `AX=B` en las seis restricciones: el error máximo es cero. Esto comprueba el cálculo, pero la componente negativa invalida la interpretación productiva no negativa. No debe reemplazarse por cero porque se romperían las igualdades.

## Comparación didáctica con B alternativo

Con el B alternativo, el agente obtiene `X = (15, 20, 25, 10, 15, 20)` y residuo cero. Este escenario consume el 100 % de ese B alternativo, pero no representa las disponibilidades originales de TechChip Systems.

## Escasez de resina

Al sustituir únicamente `B3=225` por `B3=100`, el agente obtiene `X = (-26355/83, -6780/83, 18555/83, 3170/83, 3505/83, 6510/83)`. Las producciones `x1=-26355/83` y `x2=-6780/83` son negativas. El problema es de factibilidad empresarial, no de cálculo.

## Dependencia y contradicción

Si `F6=2F1` pero se conserva `B6=175`, se exige simultáneamente `2B1=310` y `B6=175`: `rango(A)=5`, `rango([A|B])=6` y no existe solución. Si también se establece `B6=310`, ambos rangos son 5 y aparece una familia con una variable libre.

## Recomendaciones

1. Usar el B original como caso principal y registrar el vector indicado como resultado erróneo de la guía.
2. No redondear ni reemplazar producciones negativas por cero.
3. Si se permite capacidad ociosa, reformular como `AX≤B`, `X≥0` e incorporar demanda.
4. Para hablar de un plan óptimo, añadir una función objetivo con costos, márgenes o tiempos.
5. Validar la escala: si X está en miles, A debe representar consumo por cada mil módulos.
