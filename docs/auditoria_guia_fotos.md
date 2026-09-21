# Auditoría de las seis fotos de la guía del Parcial 2

Esta revisión compara lo legible de las fotos enviadas con `scenarios.py`, `web/src/data/scenarios.ts`, la salida exacta de `TechChipAgent` y los documentos de entrega. `scripts/verify_photo_matrix.py` comprueba el determinante por la definición de Leibniz y la solución por Cramer, sin llamar al motor. Se preservan por separado los **datos impresos** y la **variante que reproduce la respuesta esperada**. Ningún resultado se ajustó por redondeo.

## Lectura de cada foto y cumplimiento

| Foto | Indicación comprobada | Evidencia y estado |
|---|---|---|
| 1 | Caso TechChip, seis líneas, seis recursos, modelo `AX=B`, producción diaria y balance de capacidad | `scenarios.py` y el informe IEEE modelan exactamente seis variables y seis restricciones. **Cumple**, con la aclaración de unidades indicada abajo. |
| 2 | Nombres de `x₁…x₆` y seis ecuaciones con disponibilidades | La matriz `A` y el vector `B` del escenario `original` **coinciden fila por fila** con la foto. Se detallan abajo. |
| 3 | Gauss con sustitución hacia atrás, Gauss-Jordan hasta `[I₆|X]`, inversa; entrada editable, validación dimensional/rango/determinante, traza explícita y diagnóstico | `agent.py`, `main.py`, la web y las pruebas cubren estos apartados. El informe incluye las tres trazas completas. **Cumple como desarrollo computacional reproducible**; una resolución manuscrita independiente sigue pendiente si el docente la exige literalmente. |
| 4 | Prueba base con `X=(15,20,25,10,15,20)`, sustitución `E=|AX-B|<10⁻⁶`, escasez `B₃=100`, singularidad `F₆=2F₁` | Escasez y singularidad están implementadas. La prueba base **no puede pasar con el `B` impreso**: la propia guía contiene una contradicción numérica. La variante `compatible` reproduce `X` y da `E=0`; está rotulada como variante, no como dato original. |
| 5 | Cuatro entregables y rúbrica: dominio, modelación, agente, rigor, extremos, interpretación, presentación | Se empaquetan informe PDF y fuente, código portable, bitácora con logs/capturas e interpretación. **Falta confirmación** de si el desarrollo “manual” debe ser manuscrito. |
| 6 | Redacción y estructura de la entrega, total de 100 puntos | El informe IEEEtran tiene 48 páginas y apéndices. Revisar con el docente si requiere una plantilla ACM, portada institucional o longitud máxima. |

## Matriz transcrita de la foto 2

Las filas son recursos y las columnas son líneas de módulos, en el mismo orden de la foto:

| Recurso | x₁ | x₂ | x₃ | x₄ | x₅ | x₆ | B impreso |
|---|---:|---:|---:|---:|---:|---:|---:|
| Litografía EUV | 2 | 1 | 3 | 1 | 2 | 1 | 155 |
| Pruebas ATE | 1 | 3 | 2 | 2 | 1 | 2 | 160 |
| Resina de encapsulado | 3 | 2 | 4 | 1 | 3 | 2 | 225 |
| Sustrato de silicio | 1 | 1 | 1 | 4 | 2 | 1 | 140 |
| Energía eléctrica para cortado láser | 2 | 1 | 2 | 1 | 5 | 3 | 215 |
| Inspección de control de calidad óptico | 1 | 2 | 1 | 2 | 1 | 4 | 175 |

`A` y `B` son idénticos en `scenarios.py`, `web/src/data/scenarios.ts` y los JSON `original`. Las etiquetas abreviadas del informe (“Energía láser”, “Inspección óptica”) nombran los mismos recursos; conviene conservar los nombres completos de la foto en la presentación final.

## Contradicción numérica de la foto 4

La foto pide comprobar `X_esperado=(15,20,25,10,15,20)`. La sustitución directa en las filas impresas da:

| Fila | Suma exacta de `A·X_esperado` | B impreso | Diferencia |
|---|---|---:|---:|
| 1 | `30+20+75+10+30+20 = 185` | 155 | 30 |
| 2 | `15+60+50+20+15+40 = 200` | 160 | 40 |
| 3 | `45+40+100+10+45+40 = 280` | 225 | 55 |
| 4 | `15+20+25+40+30+20 = 150` | 140 | 10 |
| 5 | `30+20+50+10+75+60 = 245` | 215 | 30 |
| 6 | `15+40+25+20+15+80 = 195` | 175 | 20 |

Por tanto, `A·X_esperado=(185,200,280,150,245,195)` y `|A·X_esperado−B_foto|=(30,40,55,10,30,20)`. El error máximo es **55**, así que **no cumple** el umbral `10⁻⁶` con los datos impresos. Los tres métodos del motor dan, para ese `B_foto`, la única solución exacta

`X_foto=(-105,345,2430,1170,1130,2010)/83`,

con `det(A)=-83`, ambos rangos iguales a 6 y residuo exacto cero. Como `x₁=-105/83<0`, es una solución algebraica correcta pero **no** un plan de producción no negativo que agote todas las capacidades. Para el `B_compatible=A·X_esperado`, los tres métodos dan el vector esperado y residuo cero. **No debe presentarse `B_compatible` como si fuese el de la foto.**

## Pruebas extremas de la foto 4

| Prueba | Cambio respecto a la foto | Resultado exacto | Interpretación |
|---|---|---|---|
| Escasez | Solo `B₃: 225→100` | `X=(-26355,-6780,18555,3170,3505,6510)/83`; `det=-83`, rango 6/6, residuo 0 | `x₁` y `x₂` negativos: no hay plan no negativo que consuma exactamente todos los recursos bajo `AX=B`. Esto no excluye un plan con holguras. |
| Singular incompatible | Solo `F₆(A)=2F₁(A)`; `B₆` sigue en 175 | `det=0`, rango(A)=5, rango([A|B])=6 | No hay solución: la fila 6 exigiría `B₆=2·155=310`, distinto de 175. |
| Singular indeterminado | Además `B₆=310` | `det=0`, ambos rangos 5 | Infinitas soluciones; hay una variable libre. Esta segunda modificación se identifica explícitamente. |

## Alcance y comprobaciones pendientes

- **Desarrollo manual:** el PDF contiene todas las operaciones y matrices, calculadas por software y verificables a mano. Las fotos piden un “desarrollo manual paso a paso”; si significa hojas resueltas a mano, todavía deben elaborarse y adjuntarse. No se presentan las trazas generadas como manuscrito.
- **Dato oficial contradictorio:** pedir al docente que confirme si manda el `B` impreso o el vector esperado. Con los dos a la vez, la prueba base es imposible.
- **Unidades:** la foto dice que `x` está en *miles de unidades* y que `A` es consumo “por unidad”. Para que `AX=B` tenga las horas, kg, m² y MWh impresos, el informe interpreta los coeficientes como consumo **por mil módulos**. Confirmar esta escala con el docente.
- **Alcance empresarial:** `AX=B` y `X≥0` comprueban un balance exacto. No prueban optimización de costos o beneficios: faltan función objetivo, demanda y reglas sobre capacidad ociosa.
- **Metadatos de entrega:** autores, carnés, docente, grupo y fecha figuran en el PDF, pero no aparecen en estas seis fotos; deben ser confirmados por el equipo antes de entregarlo. Confirmar también si IEEEtran `conference` satisface el formato solicitado.
- **Dependencia propietaria:** el núcleo Python y la CLI funcionan sin OpenAI ni Vercel; el tutor generativo y el hosting son opcionales. Si la evaluación exige independencia total incluso de estas funciones opcionales, demostrar la CLI local y el respaldo determinista.
