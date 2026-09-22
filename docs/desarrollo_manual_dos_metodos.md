# Desarrollo manual paso a paso — caso original de TechChip Systems

Este documento desarrolla las operaciones elementales que pueden reproducirse a mano. Las fracciones son exactas y corresponden al B original `(155,160,225,140,215,175)`. El vector `(15,20,25,10,15,20)` no se usa porque es incorrecto para esos datos.

La matriz aumentada se transforma sin redondeos. Cada paso indica la operación, su justificación y el estado completo resultante.

---

# Método 1 — Eliminación de Gauss y sustitución hacia atrás

Total de estados registrados: **25**.

## Paso 1. Matriz aumentada inicial

**Operación:** `Matriz aumentada inicial`

**Qué se hizo:** Punto de partida: [A | B]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 2  1  3  1  2  1 | 155 ]
[ 1  3  2  2  1  2 | 160 ]
[ 3  2  4  1  3  2 | 225 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 2. F1 ↔ F3

**Operación:** `F1 ↔ F3`

**Qué se hizo:** Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 1  3  2  2  1  2 | 160 ]
[ 2  1  3  1  2  1 | 155 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 3. F2 ← F2 + (-1/3) · F1

**Operación:** `F2 ← F2 + (-1/3) · F1`

**Qué se hizo:** El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 2  1  3  1  2  1 | 155 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 4. F3 ← F3 + (-2/3) · F1

**Operación:** `F3 ← F3 + (-2/3) · F1`

**Qué se hizo:** El multiplicador es −(2)/(3) = -2/3; así, 2 + (-2/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 5. F4 ← F4 + (-1/3) · F1

**Operación:** `F4 ← F4 + (-1/3) · F1`

**Qué se hizo:** El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 6. F5 ← F5 + (-2/3) · F1

**Operación:** `F5 ← F5 + (-2/3) · F1`

**Qué se hizo:** El multiplicador es −(2)/(3) = -2/3; así, 2 + (-2/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 7. F6 ← F6 + (-1/3) · F1

**Operación:** `F6 ← F6 + (-1/3) · F1`

**Qué se hizo:** El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 8. F3 ← F3 + (1/7) · F2

**Operación:** `F3 ← F3 + (1/7) · F2`

**Qué se hizo:** El multiplicador es −(-1/3)/(7/3) = 1/7; así, -1/3 + (1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 9. F4 ← F4 + (-1/7) · F2

**Operación:** `F4 ← F4 + (-1/7) · F2`

**Qué se hizo:** El multiplicador es −(1/3)/(7/3) = -1/7; así, 1/3 + (-1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 10. F5 ← F5 + (1/7) · F2

**Operación:** `F5 ← F5 + (1/7) · F2`

**Qué se hizo:** El multiplicador es −(-1/3)/(7/3) = 1/7; así, -1/3 + (1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 11. F6 ← F6 + (-4/7) · F2

**Operación:** `F6 ← F6 + (-4/7) · F2`

**Qué se hizo:** El multiplicador es −(4/3)/(7/3) = -4/7; así, 4/3 + (-4/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
```

## Paso 12. F3 ↔ F6

**Operación:** `F3 ↔ F6`

**Qué se hizo:** Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 13. F4 ← F4 + (-3/5) · F3

**Operación:** `F4 ← F4 + (-3/5) · F3`

**Qué se hizo:** El multiplicador es −(-3/7)/(-5/7) = -3/5; así, -3/7 + (-3/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 14. F5 ← F5 + (-4/5) · F3

**Operación:** `F5 ← F5 + (-4/5) · F3`

**Qué se hizo:** El multiplicador es −(-4/7)/(-5/7) = -4/5; así, -4/7 + (-4/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 15. F6 ← F6 + (3/5) · F3

**Operación:** `F6 ← F6 + (3/5) · F3`

**Qué se hizo:** El multiplicador es −(3/7)/(-5/7) = 3/5; así, 3/7 + (3/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  1  0  7/5 | 48 ]
```

## Paso 16. F6 ← F6 + (-1/3) · F4

**Operación:** `F6 ← F6 + (-1/3) · F4`

**Qué se hizo:** El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 17. F6 ← F6 + (1/9) · F5

**Operación:** `F6 ← F6 + (1/9) · F5`

**Qué se hizo:** El multiplicador es −(-1/3)/(3) = 1/9; así, -1/3 + (1/9)·(3) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 18. det(A) = -83

**Operación:** `det(A) = -83`

**Qué se hizo:** 2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (3) · (7/3) · (-5/7) · (3) · (3) · (83/45) = -83.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 19. Matriz triangular superior U

**Operación:** `Matriz triangular superior U`

**Qué se hizo:** La eliminación terminó: debajo de cada pivote hay ceros. Ahora se resuelve U·X = C desde la última ecuación hacia la primera, porque cada fila solo depende de variables ya conocidas.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 20. x6 = (134/3 − (0)) / (83/45) = 2010/83

**Operación:** `x6 = (134/3 − (0)) / (83/45) = 2010/83`

**Qué se hizo:** En la fila 6 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x6. El valor se conserva como fracción exacta.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 21. x5 = (36 − ((-1/5)·(2010/83))) / (3) = 1130/83

**Operación:** `x5 = (36 − ((-1/5)·(2010/83))) / (3) = 1130/83`

**Qué se hizo:** En la fila 5 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x5. El valor se conserva como fracción exacta.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 22. x4 = (22 − ((1)·(1130/83) + (-7/5)·(2010/83))) / (3) = 1170/83

**Operación:** `x4 = (22 − ((1)·(1130/83) + (-7/5)·(2010/83))) / (3) = 1170/83`

**Qué se hizo:** En la fila 4 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x4. El valor se conserva como fracción exacta.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 23. x3 = (360/7 − ((5/7)·(1170/83) + (0)·(1130/83) + (18/7)·(2010/83))) / (-5/7) = 2430/83

**Operación:** `x3 = (360/7 − ((5/7)·(1170/83) + (0)·(1130/83) + (18/7)·(2010/83))) / (-5/7) = 2430/83`

**Qué se hizo:** En la fila 3 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x3. El valor se conserva como fracción exacta.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 24. x2 = (85 − ((2/3)·(2430/83) + (5/3)·(1170/83) + (0)·(1130/83) + (4/3)·(2010/83))) / (7/3) = 345/83

**Operación:** `x2 = (85 − ((2/3)·(2430/83) + (5/3)·(1170/83) + (0)·(1130/83) + (4/3)·(2010/83))) / (7/3) = 345/83`

**Qué se hizo:** En la fila 2 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x2. El valor se conserva como fracción exacta.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 25. x1 = (225 − ((2)·(345/83) + (4)·(2430/83) + (1)·(1170/83) + (3)·(1130/83) + (2)·(2010/83))) / (3) = -105/83

**Operación:** `x1 = (225 − ((2)·(345/83) + (4)·(2430/83) + (1)·(1170/83) + (3)·(1130/83) + (2)·(2010/83))) / (3) = -105/83`

**Qué se hizo:** En la fila 1 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x1. El valor se conserva como fracción exacta.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Resultado del método

`X = (-105/83, 345/83, 2430/83, 1170/83, 1130/83, 2010/83)`

---

# Método 2 — Gauss-Jordan

Total de estados registrados: **39**.

## Paso 1. Matriz aumentada inicial

**Operación:** `Matriz aumentada inicial`

**Qué se hizo:** Punto de partida: [A | B]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 2  1  3  1  2  1 | 155 ]
[ 1  3  2  2  1  2 | 160 ]
[ 3  2  4  1  3  2 | 225 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 2. F1 ↔ F3

**Operación:** `F1 ↔ F3`

**Qué se hizo:** Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 3  2  4  1  3  2 | 225 ]
[ 1  3  2  2  1  2 | 160 ]
[ 2  1  3  1  2  1 | 155 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 3. F1 ← (1/3) · F1

**Operación:** `F1 ← (1/3) · F1`

**Qué se hizo:** Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 1  3  2  2  1  2 | 160 ]
[ 2  1  3  1  2  1 | 155 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 4. F2 ← F2 + (-1) · F1

**Operación:** `F2 ← F2 + (-1) · F1`

**Qué se hizo:** El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 2  1  3  1  2  1 | 155 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 5. F3 ← F3 + (-2) · F1

**Operación:** `F3 ← F3 + (-2) · F1`

**Qué se hizo:** El multiplicador es −(2)/(1) = -2; así, 2 + (-2)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 1  1  1  4  2  1 | 140 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 6. F4 ← F4 + (-1) · F1

**Operación:** `F4 ← F4 + (-1) · F1`

**Qué se hizo:** El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 2  1  2  1  5  3 | 215 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 7. F5 ← F5 + (-2) · F1

**Operación:** `F5 ← F5 + (-2) · F1`

**Qué se hizo:** El multiplicador es −(2)/(1) = -2; así, 2 + (-2)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 1  2  1  2  1  4 | 175 ]
```

## Paso 8. F6 ← F6 + (-1) · F1

**Operación:** `F6 ← F6 + (-1) · F1`

**Qué se hizo:** El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 0  7/3  2/3  5/3  0  4/3 | 85 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 9. F2 ← (3/7) · F2

**Operación:** `F2 ← (3/7) · F2`

**Qué se hizo:** Se divide toda la fila entre el pivote 7/3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3 | 75 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 10. F1 ← F1 + (-2/3) · F2

**Operación:** `F1 ← F1 + (-2/3) · F2`

**Qué se hizo:** El multiplicador es −(2/3)/(1) = -2/3; así, 2/3 + (-2/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  -1/3  1/3  1/3  0  -1/3 | 5 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 11. F3 ← F3 + (1/3) · F2

**Operación:** `F3 ← F3 + (1/3) · F2`

**Qué se hizo:** El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  1/3  -1/3  11/3  1  1/3 | 65 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 12. F4 ← F4 + (-1/3) · F2

**Operación:** `F4 ← F4 + (-1/3) · F2`

**Qué se hizo:** El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  -1/3  -2/3  1/3  3  5/3 | 65 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 13. F5 ← F5 + (1/3) · F2

**Operación:** `F5 ← F5 + (1/3) · F2`

**Qué se hizo:** El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  4/3  -1/3  5/3  0  10/3 | 100 ]
```

## Paso 14. F6 ← F6 + (-4/3) · F2

**Operación:** `F6 ← F6 + (-4/3) · F2`

**Qué se hizo:** El multiplicador es −(4/3)/(1) = -4/3; así, 4/3 + (-4/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
```

## Paso 15. F3 ↔ F6

**Operación:** `F3 ↔ F6`

**Qué se hizo:** Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  -5/7  5/7  0  18/7 | 360/7 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 16. F3 ← (-7/5) · F3

**Operación:** `F3 ← (-7/5) · F3`

**Qué se hizo:** Se divide toda la fila entre el pivote -5/7, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  8/7  -1/7  1  2/7 | 355/7 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 17. F1 ← F1 + (-8/7) · F3

**Operación:** `F1 ← F1 + (-8/7) · F3`

**Qué se hizo:** El multiplicador es −(8/7)/(1) = -8/7; así, 8/7 + (-8/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  1  1  22/5 | 133 ]
[ 0  1  2/7  5/7  0  4/7 | 255/7 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 18. F2 ← F2 + (-2/7) · F3

**Operación:** `F2 ← F2 + (-2/7) · F3`

**Qué se hizo:** El multiplicador es −(2/7)/(1) = -2/7; así, 2/7 + (-2/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  1  1  22/5 | 133 ]
[ 0  1  0  1  0  8/5 | 57 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  -3/7  24/7  1  1/7 | 370/7 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 19. F4 ← F4 + (3/7) · F3

**Operación:** `F4 ← F4 + (3/7) · F3`

**Qué se hizo:** El multiplicador es −(-3/7)/(1) = 3/7; así, -3/7 + (3/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  1  1  22/5 | 133 ]
[ 0  1  0  1  0  8/5 | 57 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  -4/7  4/7  3  13/7 | 540/7 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 20. F5 ← F5 + (4/7) · F3

**Operación:** `F5 ← F5 + (4/7) · F3`

**Qué se hizo:** El multiplicador es −(-4/7)/(1) = 4/7; así, -4/7 + (4/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  1  1  22/5 | 133 ]
[ 0  1  0  1  0  8/5 | 57 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  3/7  4/7  0  -1/7 | 120/7 ]
```

## Paso 21. F6 ← F6 + (-3/7) · F3

**Operación:** `F6 ← F6 + (-3/7) · F3`

**Qué se hizo:** El multiplicador es −(3/7)/(1) = -3/7; así, 3/7 + (-3/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  1  1  22/5 | 133 ]
[ 0  1  0  1  0  8/5 | 57 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  0  3  1  -7/5 | 22 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  1  0  7/5 | 48 ]
```

## Paso 22. F4 ← (1/3) · F4

**Operación:** `F4 ← (1/3) · F4`

**Qué se hizo:** Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  1  1  22/5 | 133 ]
[ 0  1  0  1  0  8/5 | 57 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  1  0  7/5 | 48 ]
```

## Paso 23. F1 ← F1 + (-1) · F4

**Operación:** `F1 ← F1 + (-1) · F4`

**Qué se hizo:** El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  2/3  73/15 | 377/3 ]
[ 0  1  0  1  0  8/5 | 57 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  1  0  7/5 | 48 ]
```

## Paso 24. F2 ← F2 + (-1) · F4

**Operación:** `F2 ← F2 + (-1) · F4`

**Qué se hizo:** El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  2/3  73/15 | 377/3 ]
[ 0  1  0  0  -1/3  31/15 | 149/3 ]
[ 0  0  1  -1  0  -18/5 | -72 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  1  0  7/5 | 48 ]
```

## Paso 25. F3 ← F3 + (1) · F4

**Operación:** `F3 ← F3 + (1) · F4`

**Qué se hizo:** El multiplicador es −(-1)/(1) = 1; así, -1 + (1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  2/3  73/15 | 377/3 ]
[ 0  1  0  0  -1/3  31/15 | 149/3 ]
[ 0  0  1  0  1/3  -61/15 | -194/3 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  1  0  7/5 | 48 ]
```

## Paso 26. F6 ← F6 + (-1) · F4

**Operación:** `F6 ← F6 + (-1) · F4`

**Qué se hizo:** El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  2/3  73/15 | 377/3 ]
[ 0  1  0  0  -1/3  31/15 | 149/3 ]
[ 0  0  1  0  1/3  -61/15 | -194/3 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  3  -1/5 | 36 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 27. F5 ← (1/3) · F5

**Operación:** `F5 ← (1/3) · F5`

**Qué se hizo:** Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  2/3  73/15 | 377/3 ]
[ 0  1  0  0  -1/3  31/15 | 149/3 ]
[ 0  0  1  0  1/3  -61/15 | -194/3 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 28. F1 ← F1 + (-2/3) · F5

**Operación:** `F1 ← F1 + (-2/3) · F5`

**Qué se hizo:** El multiplicador es −(2/3)/(1) = -2/3; así, 2/3 + (-2/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  221/45 | 353/3 ]
[ 0  1  0  0  -1/3  31/15 | 149/3 ]
[ 0  0  1  0  1/3  -61/15 | -194/3 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 29. F2 ← F2 + (1/3) · F5

**Operación:** `F2 ← F2 + (1/3) · F5`

**Qué se hizo:** El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  221/45 | 353/3 ]
[ 0  1  0  0  0  92/45 | 161/3 ]
[ 0  0  1  0  1/3  -61/15 | -194/3 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 30. F3 ← F3 + (-1/3) · F5

**Operación:** `F3 ← F3 + (-1/3) · F5`

**Qué se hizo:** El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  221/45 | 353/3 ]
[ 0  1  0  0  0  92/45 | 161/3 ]
[ 0  0  1  0  0  -182/45 | -206/3 ]
[ 0  0  0  1  1/3  -7/15 | 22/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 31. F4 ← F4 + (-1/3) · F5

**Operación:** `F4 ← F4 + (-1/3) · F5`

**Qué se hizo:** El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  221/45 | 353/3 ]
[ 0  1  0  0  0  92/45 | 161/3 ]
[ 0  0  1  0  0  -182/45 | -206/3 ]
[ 0  0  0  1  0  -4/9 | 10/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  -1/3  28/15 | 122/3 ]
```

## Paso 32. F6 ← F6 + (1/3) · F5

**Operación:** `F6 ← F6 + (1/3) · F5`

**Qué se hizo:** El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  221/45 | 353/3 ]
[ 0  1  0  0  0  92/45 | 161/3 ]
[ 0  0  1  0  0  -182/45 | -206/3 ]
[ 0  0  0  1  0  -4/9 | 10/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  0  83/45 | 134/3 ]
```

## Paso 33. F6 ← (45/83) · F6

**Operación:** `F6 ← (45/83) · F6`

**Qué se hizo:** Se divide toda la fila entre el pivote 83/45, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  221/45 | 353/3 ]
[ 0  1  0  0  0  92/45 | 161/3 ]
[ 0  0  1  0  0  -182/45 | -206/3 ]
[ 0  0  0  1  0  -4/9 | 10/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Paso 34. F1 ← F1 + (-221/45) · F6

**Operación:** `F1 ← F1 + (-221/45) · F6`

**Qué se hizo:** El multiplicador es −(221/45)/(1) = -221/45; así, 221/45 + (-221/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  0 | -105/83 ]
[ 0  1  0  0  0  92/45 | 161/3 ]
[ 0  0  1  0  0  -182/45 | -206/3 ]
[ 0  0  0  1  0  -4/9 | 10/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Paso 35. F2 ← F2 + (-92/45) · F6

**Operación:** `F2 ← F2 + (-92/45) · F6`

**Qué se hizo:** El multiplicador es −(92/45)/(1) = -92/45; así, 92/45 + (-92/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  0 | -105/83 ]
[ 0  1  0  0  0  0 | 345/83 ]
[ 0  0  1  0  0  -182/45 | -206/3 ]
[ 0  0  0  1  0  -4/9 | 10/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Paso 36. F3 ← F3 + (182/45) · F6

**Operación:** `F3 ← F3 + (182/45) · F6`

**Qué se hizo:** El multiplicador es −(-182/45)/(1) = 182/45; así, -182/45 + (182/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  0 | -105/83 ]
[ 0  1  0  0  0  0 | 345/83 ]
[ 0  0  1  0  0  0 | 2430/83 ]
[ 0  0  0  1  0  -4/9 | 10/3 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Paso 37. F4 ← F4 + (4/9) · F6

**Operación:** `F4 ← F4 + (4/9) · F6`

**Qué se hizo:** El multiplicador es −(-4/9)/(1) = 4/9; así, -4/9 + (4/9)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  0 | -105/83 ]
[ 0  1  0  0  0  0 | 345/83 ]
[ 0  0  1  0  0  0 | 2430/83 ]
[ 0  0  0  1  0  0 | 1170/83 ]
[ 0  0  0  0  1  -1/15 | 12 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Paso 38. F5 ← F5 + (1/15) · F6

**Operación:** `F5 ← F5 + (1/15) · F6`

**Qué se hizo:** El multiplicador es −(-1/15)/(1) = 1/15; así, -1/15 + (1/15)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  0 | -105/83 ]
[ 0  1  0  0  0  0 | 345/83 ]
[ 0  0  1  0  0  0 | 2430/83 ]
[ 0  0  0  1  0  0 | 1170/83 ]
[ 0  0  0  0  1  0 | 1130/83 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Paso 39. [I | X]: lectura directa de la solución

**Operación:** `[I | X]: lectura directa de la solución`

**Qué se hizo:** El bloque izquierdo es la identidad: la fila i representa 1·xᵢ = Xᵢ. Por eso la última columna se lee directamente, sin sustitución hacia atrás.

**Por qué:** La operación elemental conserva un sistema equivalente.

```text
[ 1  0  0  0  0  0 | -105/83 ]
[ 0  1  0  0  0  0 | 345/83 ]
[ 0  0  1  0  0  0 | 2430/83 ]
[ 0  0  0  1  0  0 | 1170/83 ]
[ 0  0  0  0  1  0 | 1130/83 ]
[ 0  0  0  0  0  1 | 2010/83 ]
```

## Resultado del método

`X = (-105/83, 345/83, 2430/83, 1170/83, 1130/83, 2010/83)`

---

# Comprobación final

Los dos métodos producen exactamente `X = (-105/83, 345/83, 2430/83, 1170/83, 1130/83, 2010/83)`. La sustitución devuelve `AX=B`, el residuo es `(0,0,0,0,0,0)` y el error máximo es `0`.
