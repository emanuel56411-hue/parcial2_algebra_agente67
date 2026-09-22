# Autoevaluación detallada de la rúbrica

Esta revisión contrasta los entregables ejecutables con la rúbrica recibida. Es una autoauditoría técnica, no sustituye la nota del docente.

## Resultado global

| Criterio | Valor | Evidencia comprobada | Estado |
|---|---:|---|---|
| Dominio de Álgebra Lineal | 20 | Modelo 6×6, determinante, rangos, Gauss, Gauss-Jordan, inversa y residuos exactos | Cumple |
| Modelación empresarial | 15 | Variables, recursos, restricciones, unidades, factibilidad y diferencia entre balance y optimización | Cumple con observación de escala |
| Implementación del Agente IA | 20 | Motor exacto, API, tutor OpenAI con respaldo local, JSON y conversor seguro de ecuaciones | Cumple |
| Rigor matemático | 15 | Fracciones exactas, tres métodos coincidentes, reproducción de operaciones y validación `AX=B` | Cumple |
| Pruebas y extremos | 10 | Caso original, B alternativo, escasez, incompatible, infinitas soluciones, 2×2–6×6 y entradas adversarias | Cumple |
| Interpretación | 10 | Conclusiones cuantitativas, inviabilidad por valores negativos, dependencia y recomendaciones | Cumple |
| Documentación y presentación | 10 | PDF a dos columnas estilo IEEE, fuente IEEEtran, código portable, bitácora, capturas y logs | Cumple con condición indicada abajo |

## Comprobación por criterio

### 1. Dominio de Álgebra Lineal

- Se define `AX=B` y la matriz aumentada `[A|B]`.
- Se justifican operaciones elementales, pivoteo parcial, determinante y rangos.
- El desarrollo completo del caso original contiene Gauss con sustitución hacia atrás y Gauss-Jordan.
- La inversa se calcula y se usa como tercera comprobación automática.
- Para el B original se obtiene exactamente `X=(-105,345,2430,1170,1130,2010)/83` y residuo cero.

**Conclusión:** cumple completamente.

### 2. Modelación empresarial

- Las seis variables representan líneas de producto y se justifican individualmente.
- Las seis filas representan litografía, pruebas ATE, resina, sustrato, energía e inspección.
- Se distingue solución algebraica de factibilidad con `X≥0`.
- Se aclara que `AX=B` es balance, no optimización, porque falta una función objetivo.

**Observación:** si `X` está en miles de módulos, los coeficientes deben interpretarse como consumo por mil módulos. La guía usa “por unidad”, por lo que la escala debe mantenerse explícita en la exposición.

### 3. Implementación del agente

- Resuelve por Gauss, Gauss-Jordan y matriz inversa.
- Admite dimensiones seleccionables de 2×2 a 6×6.
- Acepta JSON adjunto o pegado, `A=[[...]], B=[...]` y ecuaciones escritas como prompt.
- Acepta enteros, decimales, fracciones y notación científica.
- Rechaza código, expresiones no lineales y dimensiones inválidas.
- El tutor puede expandirse, ofrece procedimientos completos y usa el motor exacto como fuente de cifras.
- Se eliminó el límite artificial anterior de 500 caracteres; permanece únicamente el límite técnico de 100 kB.

**Conclusión:** cumple completamente.

### 4. Rigor matemático

- Los cálculos utilizan `Fraction`, sin redondeo binario en la solución.
- Los tres métodos coinciden para matrices invertibles.
- Se verifican `AX=B`, `AA⁻¹=I`, determinante y reproducción de cada operación elemental.
- El error de la guía queda demostrado mediante `A·(15,20,25,10,15,20)=(185,200,280,150,245,195)`, distinto del B original.

**Conclusión:** cumple completamente.

### 5. Pruebas normales, modificadas y degeneradas

- Normal principal: B original, solución única algebraica y plan productivo inviable.
- Comparación didáctica: B alternativo que reproduce el vector incorrectamente atribuido al original.
- Modificado: escasez de resina con `B3=100`.
- Degenerado incompatible: `F6=2F1` con `B6=175`.
- Degenerado indeterminado: `F6=2F1` con `B6=310`.
- Pruebas automatizadas: 60 Python, 5 frontend, ESLint y build de producción.

**Conclusión:** cumple completamente.

### 6. Interpretación cuantitativa

- El B original produce `x1=-105/83≈-1.265060`; por tanto, no existe un plan no negativo que agote exactamente las seis capacidades.
- La escasez produce dos componentes negativas.
- Una fila proporcional con término independiente incompatible produce cero soluciones; con término proporcional produce infinitas.
- Se recomienda usar desigualdades y función objetivo si se desea permitir holgura u optimizar.

**Conclusión:** cumple completamente.

### 7. Documentación y presentación

- El PDF presenta diseño académico a dos columnas tipo IEEE y se incluye también la fuente `IEEEtran`.
- Se incluyen código fuente ejecutable, instrucciones, bitácora, capturas, logs, datos originales y checksums.
- El desarrollo de Gauss y Gauss-Jordan es exhaustivo y reproducible a mano.

**Condición:** si “desarrollo manual” significa obligatoriamente hojas escritas a mano y escaneadas, esa evidencia física debe producirla el equipo. El paquete contiene desarrollo algebraico paso a paso generado y verificado, pero no pretende falsificar escritura manuscrita.

## Dictamen

La implementación y los cuatro entregables solicitados están completos y trazables. No se detecta una carencia de software o cálculo. Antes de entregar solo debe cuidarse la explicación de la escala “por mil módulos” y, si el docente lo exige literalmente, añadir hojas manuscritas reales. El resultado `(15,20,25,10,15,20)` no debe presentarse como solución del B original.
