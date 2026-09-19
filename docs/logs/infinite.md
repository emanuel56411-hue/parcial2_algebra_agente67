# Singular · infinitas soluciones

TechChip Matrix Studio · procedimiento reproducible

F₆ = 2F₁ y B₆ = 2B₁ = 310. Se conserva la dependencia en ambos lados. La guía contiene una inconsistencia: el vector esperado (15, 20, 25, 10, 15, 20) requiere B = (185, 200, 280, 150, 245, 195). No resuelve el B original (155, 160, 225, 140, 215, 175). Ambos casos se conservan por separado.

## 1. Sistema de entrada

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 4  2  6  2  4  2  |  310 ]
```

## 2. Diagnóstico

- Estado: Infinitas soluciones
- det(A) = 0
- rango(A) = 5; rango([A|B]) = 5

## 3. Interpretación

- Hay 1 variable(s) libre(s): los datos no determinan una solución única.
- La familia X = Xₚ + t₁v₁ + … describe todas las soluciones reales; hacen falta restricciones independientes para reducir la ambigüedad.
- La viabilidad de esta familia bajo X ≥ 0 requiere un análisis adicional; no se declara un plan de producción viable.

## 4. Familia de soluciones

Xₚ = (-105/16, 345/16, 105/4, 165/16, 115/4, 0)
v1 = (7/32, -23/32, 1/8, 5/32, -5/8, 1)
X = Xₚ + t1·v1
Los parámetros t son números reales libres.


## Procedimiento — Diagnóstico: determinante y rangos

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 4  2  6  2  4  2  |  310 ]
```

### Paso 2. F1 ↔ F6

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ 4  2  6  2  4  2  |  310 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 2  1  3  1  2  1  |  155 ]
```

### Paso 3. F2 ← F2 + (-1/4) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 4    2    6    2  4    2  |    310 ]
[ 0  5/2  1/2  3/2  0  3/2  |  165/2 ]
[ 3    2    4    1  3    2  |    225 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 2    1    3    1  2    1  |    155 ]
```

### Paso 4. F3 ← F3 + (-3/4) · F1

Se anula la entrada 3 en la columna 1; se opera sobre la fila completa.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 1    1     1     4  2    1  |    140 ]
[ 2    1     2     1  5    3  |    215 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 5. F4 ← F4 + (-1/4) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 2    1     2     1  5    3  |    215 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 6. F5 ← F5 + (-1/2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 7. F6 ← F6 + (-1/2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 8. F3 ← F3 + (-1/5) · F2

Se anula la entrada 1/2 en la columna 2; se opera sobre la fila completa.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0    0  -3/5  -4/5  0  1/5  |    -24 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 9. F4 ← F4 + (-1/5) · F2

Se anula la entrada 1/2 en la columna 2; se opera sobre la fila completa.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0    0  -3/5  -4/5  0  1/5  |    -24 ]
[ 0    0  -3/5  16/5  1  1/5  |     46 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 10. F3 ↔ F5

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 3.

```text
[ 4    2     6     2  4    2  |    310 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0  -3/5  16/5  1  1/5  |     46 ]
[ 0    0  -3/5  -4/5  0  1/5  |    -24 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 11. F4 ← F4 + (-3/5) · F3

Se anula la entrada -3/5 en la columna 3; se opera sobre la fila completa.

```text
[ 4    2     6     2     4    2  |    310 ]
[ 0  5/2   1/2   3/2     0  3/2  |  165/2 ]
[ 0    0    -1     0     3    2  |     60 ]
[ 0    0     0  16/5  -4/5   -1  |     10 ]
[ 0    0  -3/5  -4/5     0  1/5  |    -24 ]
[ 0    0     0     0     0    0  |      0 ]
```

### Paso 12. F5 ← F5 + (-3/5) · F3

Se anula la entrada -3/5 en la columna 3; se opera sobre la fila completa.

```text
[ 4    2    6     2     4    2  |    310 ]
[ 0  5/2  1/2   3/2     0  3/2  |  165/2 ]
[ 0    0   -1     0     3    2  |     60 ]
[ 0    0    0  16/5  -4/5   -1  |     10 ]
[ 0    0    0  -4/5  -9/5   -1  |    -60 ]
[ 0    0    0     0     0    0  |      0 ]
```

### Paso 13. F5 ← F5 + (1/4) · F4

Se anula la entrada -4/5 en la columna 4; se opera sobre la fila completa.

```text
[ 4    2    6     2     4     2  |     310 ]
[ 0  5/2  1/2   3/2     0   3/2  |   165/2 ]
[ 0    0   -1     0     3     2  |      60 ]
[ 0    0    0  16/5  -4/5    -1  |      10 ]
[ 0    0    0     0    -2  -5/4  |  -115/2 ]
[ 0    0    0     0     0     0  |       0 ]
```

### Paso 14. Columna 6: sin pivote

Todas las entradas disponibles son cero. Se continúa en la siguiente columna.

```text
[ 4    2    6     2     4     2  |     310 ]
[ 0  5/2  1/2   3/2     0   3/2  |   165/2 ]
[ 0    0   -1     0     3     2  |      60 ]
[ 0    0    0  16/5  -4/5    -1  |      10 ]
[ 0    0    0     0    -2  -5/4  |  -115/2 ]
[ 0    0    0     0     0     0  |       0 ]
```

### Paso 15. det(A) = 0

No hay n pivotes independientes; det(A) = 0. No existe A⁻¹.

```text
[ 4    2    6     2     4     2  |     310 ]
[ 0  5/2  1/2   3/2     0   3/2  |   165/2 ]
[ 0    0   -1     0     3     2  |      60 ]
[ 0    0    0  16/5  -4/5    -1  |      10 ]
[ 0    0    0     0    -2  -5/4  |  -115/2 ]
[ 0    0    0     0     0     0  |       0 ]
```

### Paso 16. Diagnóstico de variables libres

Se reduce el sistema para describir la familia de soluciones; no se intenta invertir A.

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 4  2  6  2  4  2  |  310 ]
```

### Paso 17. F1 ↔ F6

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ 4  2  6  2  4  2  |  310 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 2  1  3  1  2  1  |  155 ]
```

### Paso 18. F1 ← (1/4) · F1

Se convierte el pivote 4 en 1.

```text
[ 1  1/2  3/2  1/2  1  1/2  |  155/2 ]
[ 1    3    2    2  1    2  |    160 ]
[ 3    2    4    1  3    2  |    225 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 2    1    3    1  2    1  |    155 ]
```

### Paso 19. F2 ← F2 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/2  3/2  1/2  1  1/2  |  155/2 ]
[ 0  5/2  1/2  3/2  0  3/2  |  165/2 ]
[ 3    2    4    1  3    2  |    225 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 2    1    3    1  2    1  |    155 ]
```

### Paso 20. F3 ← F3 + (-3) · F1

Se anula la entrada 3 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/2   3/2   1/2  1  1/2  |  155/2 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 1    1     1     4  2    1  |    140 ]
[ 2    1     2     1  5    3  |    215 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 21. F4 ← F4 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/2   3/2   1/2  1  1/2  |  155/2 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 2    1     2     1  5    3  |    215 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 22. F5 ← F5 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/2   3/2   1/2  1  1/2  |  155/2 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 23. F6 ← F6 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/2   3/2   1/2  1  1/2  |  155/2 ]
[ 0  5/2   1/2   3/2  0  3/2  |  165/2 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 24. F2 ← (2/5) · F2

Se convierte el pivote 5/2 en 1.

```text
[ 1  1/2   3/2   1/2  1  1/2  |  155/2 ]
[ 0    1   1/5   3/5  0  3/5  |     33 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 25. F1 ← F1 + (-1/2) · F2

Se anula la entrada 1/2 en la columna 2; se opera sobre la fila completa.

```text
[ 1    0   7/5   1/5  1  1/5  |     61 ]
[ 0    1   1/5   3/5  0  3/5  |     33 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  -15/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 26. F3 ← F3 + (-1/2) · F2

Se anula la entrada 1/2 en la columna 2; se opera sobre la fila completa.

```text
[ 1    0   7/5   1/5  1  1/5  |     61 ]
[ 0    1   1/5   3/5  0  3/5  |     33 ]
[ 0    0  -3/5  -4/5  0  1/5  |    -24 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  125/2 ]
[ 0    0    -1     0  3    2  |     60 ]
[ 0    0     0     0  0    0  |      0 ]
```

### Paso 27. F4 ← F4 + (-1/2) · F2

Se anula la entrada 1/2 en la columna 2; se opera sobre la fila completa.

```text
[ 1  0   7/5   1/5  1  1/5  |   61 ]
[ 0  1   1/5   3/5  0  3/5  |   33 ]
[ 0  0  -3/5  -4/5  0  1/5  |  -24 ]
[ 0  0  -3/5  16/5  1  1/5  |   46 ]
[ 0  0    -1     0  3    2  |   60 ]
[ 0  0     0     0  0    0  |    0 ]
```

### Paso 28. F3 ↔ F5

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 3.

```text
[ 1  0   7/5   1/5  1  1/5  |   61 ]
[ 0  1   1/5   3/5  0  3/5  |   33 ]
[ 0  0    -1     0  3    2  |   60 ]
[ 0  0  -3/5  16/5  1  1/5  |   46 ]
[ 0  0  -3/5  -4/5  0  1/5  |  -24 ]
[ 0  0     0     0  0    0  |    0 ]
```

### Paso 29. F3 ← (-1) · F3

Se convierte el pivote -1 en 1.

```text
[ 1  0   7/5   1/5   1  1/5  |   61 ]
[ 0  1   1/5   3/5   0  3/5  |   33 ]
[ 0  0     1     0  -3   -2  |  -60 ]
[ 0  0  -3/5  16/5   1  1/5  |   46 ]
[ 0  0  -3/5  -4/5   0  1/5  |  -24 ]
[ 0  0     0     0   0    0  |    0 ]
```

### Paso 30. F1 ← F1 + (-7/5) · F3

Se anula la entrada 7/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0   1/5  26/5    3  |  145 ]
[ 0  1   1/5   3/5     0  3/5  |   33 ]
[ 0  0     1     0    -3   -2  |  -60 ]
[ 0  0  -3/5  16/5     1  1/5  |   46 ]
[ 0  0  -3/5  -4/5     0  1/5  |  -24 ]
[ 0  0     0     0     0    0  |    0 ]
```

### Paso 31. F2 ← F2 + (-1/5) · F3

Se anula la entrada 1/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0   1/5  26/5    3  |  145 ]
[ 0  1     0   3/5   3/5    1  |   45 ]
[ 0  0     1     0    -3   -2  |  -60 ]
[ 0  0  -3/5  16/5     1  1/5  |   46 ]
[ 0  0  -3/5  -4/5     0  1/5  |  -24 ]
[ 0  0     0     0     0    0  |    0 ]
```

### Paso 32. F4 ← F4 + (3/5) · F3

Se anula la entrada -3/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0   1/5  26/5    3  |  145 ]
[ 0  1     0   3/5   3/5    1  |   45 ]
[ 0  0     1     0    -3   -2  |  -60 ]
[ 0  0     0  16/5  -4/5   -1  |   10 ]
[ 0  0  -3/5  -4/5     0  1/5  |  -24 ]
[ 0  0     0     0     0    0  |    0 ]
```

### Paso 33. F5 ← F5 + (3/5) · F3

Se anula la entrada -3/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0  0   1/5  26/5   3  |  145 ]
[ 0  1  0   3/5   3/5   1  |   45 ]
[ 0  0  1     0    -3  -2  |  -60 ]
[ 0  0  0  16/5  -4/5  -1  |   10 ]
[ 0  0  0  -4/5  -9/5  -1  |  -60 ]
[ 0  0  0     0     0   0  |    0 ]
```

### Paso 34. F4 ← (5/16) · F4

Se convierte el pivote 16/5 en 1.

```text
[ 1  0  0   1/5  26/5      3  |   145 ]
[ 0  1  0   3/5   3/5      1  |    45 ]
[ 0  0  1     0    -3     -2  |   -60 ]
[ 0  0  0     1  -1/4  -5/16  |  25/8 ]
[ 0  0  0  -4/5  -9/5     -1  |   -60 ]
[ 0  0  0     0     0      0  |     0 ]
```

### Paso 35. F1 ← F1 + (-1/5) · F4

Se anula la entrada 1/5 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0     0  21/4  49/16  |  1155/8 ]
[ 0  1  0   3/5   3/5      1  |      45 ]
[ 0  0  1     0    -3     -2  |     -60 ]
[ 0  0  0     1  -1/4  -5/16  |    25/8 ]
[ 0  0  0  -4/5  -9/5     -1  |     -60 ]
[ 0  0  0     0     0      0  |       0 ]
```

### Paso 36. F2 ← F2 + (-3/5) · F4

Se anula la entrada 3/5 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0     0  21/4  49/16  |  1155/8 ]
[ 0  1  0     0   3/4  19/16  |   345/8 ]
[ 0  0  1     0    -3     -2  |     -60 ]
[ 0  0  0     1  -1/4  -5/16  |    25/8 ]
[ 0  0  0  -4/5  -9/5     -1  |     -60 ]
[ 0  0  0     0     0      0  |       0 ]
```

### Paso 37. F5 ← F5 + (4/5) · F4

Se anula la entrada -4/5 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0  0  21/4  49/16  |  1155/8 ]
[ 0  1  0  0   3/4  19/16  |   345/8 ]
[ 0  0  1  0    -3     -2  |     -60 ]
[ 0  0  0  1  -1/4  -5/16  |    25/8 ]
[ 0  0  0  0    -2   -5/4  |  -115/2 ]
[ 0  0  0  0     0      0  |       0 ]
```

### Paso 38. F5 ← (-1/2) · F5

Se convierte el pivote -2 en 1.

```text
[ 1  0  0  0  21/4  49/16  |  1155/8 ]
[ 0  1  0  0   3/4  19/16  |   345/8 ]
[ 0  0  1  0    -3     -2  |     -60 ]
[ 0  0  0  1  -1/4  -5/16  |    25/8 ]
[ 0  0  0  0     1    5/8  |   115/4 ]
[ 0  0  0  0     0      0  |       0 ]
```

### Paso 39. F1 ← F1 + (-21/4) · F5

Se anula la entrada 21/4 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  -7/32  |  -105/16 ]
[ 0  1  0  0   3/4  19/16  |    345/8 ]
[ 0  0  1  0    -3     -2  |      -60 ]
[ 0  0  0  1  -1/4  -5/16  |     25/8 ]
[ 0  0  0  0     1    5/8  |    115/4 ]
[ 0  0  0  0     0      0  |        0 ]
```

### Paso 40. F2 ← F2 + (-3/4) · F5

Se anula la entrada 3/4 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  -7/32  |  -105/16 ]
[ 0  1  0  0     0  23/32  |   345/16 ]
[ 0  0  1  0    -3     -2  |      -60 ]
[ 0  0  0  1  -1/4  -5/16  |     25/8 ]
[ 0  0  0  0     1    5/8  |    115/4 ]
[ 0  0  0  0     0      0  |        0 ]
```

### Paso 41. F3 ← F3 + (3) · F5

Se anula la entrada -3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  -7/32  |  -105/16 ]
[ 0  1  0  0     0  23/32  |   345/16 ]
[ 0  0  1  0     0   -1/8  |    105/4 ]
[ 0  0  0  1  -1/4  -5/16  |     25/8 ]
[ 0  0  0  0     1    5/8  |    115/4 ]
[ 0  0  0  0     0      0  |        0 ]
```

### Paso 42. F4 ← F4 + (1/4) · F5

Se anula la entrada -1/4 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0  0  -7/32  |  -105/16 ]
[ 0  1  0  0  0  23/32  |   345/16 ]
[ 0  0  1  0  0   -1/8  |    105/4 ]
[ 0  0  0  1  0  -5/32  |   165/16 ]
[ 0  0  0  0  1    5/8  |    115/4 ]
[ 0  0  0  0  0      0  |        0 ]
```

### Paso 43. Columna 6: sin pivote

Todas las entradas disponibles son cero. Se continúa en la siguiente columna.

```text
[ 1  0  0  0  0  -7/32  |  -105/16 ]
[ 0  1  0  0  0  23/32  |   345/16 ]
[ 0  0  1  0  0   -1/8  |    105/4 ]
[ 0  0  0  1  0  -5/32  |   165/16 ]
[ 0  0  0  0  1    5/8  |    115/4 ]
[ 0  0  0  0  0      0  |        0 ]
```

## Referencias

- [MIT OpenCourseWare · Eliminación con matrices](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/0903b4b404284cd14b66ecccea103fd4_MIT18_06SCF11_Ses1.2sum.pdf)
- [MIT OpenCourseWare · Multiplicación, Gauss-Jordan e inversa](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf)
- [MIT OpenCourseWare · AX = B y variables libres](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/solving-ax-b-row-reduced-form-r/)

Cálculo racional exacto respecto de los datos introducidos. Los decimales de presentación son aproximados.
