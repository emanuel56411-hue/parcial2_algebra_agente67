# Escasez · resina a 100 kg

TechChip Matrix Studio · procedimiento reproducible

Parte de B original y modifica únicamente B₃ = 100. La guía contiene una inconsistencia: el vector esperado (15, 20, 25, 10, 15, 20) requiere B = (185, 200, 280, 150, 245, 195). No resuelve el B original (155, 160, 225, 140, 215, 175). Ambos casos se conservan por separado.

## 1. Sistema de entrada

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  100 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

## 2. Diagnóstico

- Estado: Solución única
- det(A) = -83
- rango(A) = 6; rango([A|B]) = 6

## 3. Interpretación

- Plan de producción inalcanzable por restricción de materias primas.
- La solución de AX = B exige cantidades negativas: x1 = -26355/83 (≈ -317.530120); x2 = -6780/83 (≈ -81.686747).
- No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa.
- La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

## 4. Solución y verificación

| Variable | Valor exacto | Aproximación |
|---|---:|---:|
| x1 | -26355/83 | -317.530120 |
| x2 | -6780/83 | -81.686747 |
| x3 | 18555/83 | 223.554217 |
| x4 | 3170/83 | 38.192771 |
| x5 | 3505/83 | 42.228916 |
| x6 | 6510/83 | 78.433735 |

Los tres métodos coinciden: sí.
Error máximo por componente: 0; criterio exigido: < 10⁻⁶.

Fila 1: (2)·(-26355/83) + (1)·(-6780/83) + (3)·(18555/83) + (1)·(3170/83) + (2)·(3505/83) + (1)·(6510/83) = 155; B1 = 155; |AX − B| = 0
Fila 2: (1)·(-26355/83) + (3)·(-6780/83) + (2)·(18555/83) + (2)·(3170/83) + (1)·(3505/83) + (2)·(6510/83) = 160; B2 = 160; |AX − B| = 0
Fila 3: (3)·(-26355/83) + (2)·(-6780/83) + (4)·(18555/83) + (1)·(3170/83) + (3)·(3505/83) + (2)·(6510/83) = 100; B3 = 100; |AX − B| = 0
Fila 4: (1)·(-26355/83) + (1)·(-6780/83) + (1)·(18555/83) + (4)·(3170/83) + (2)·(3505/83) + (1)·(6510/83) = 140; B4 = 140; |AX − B| = 0
Fila 5: (2)·(-26355/83) + (1)·(-6780/83) + (2)·(18555/83) + (1)·(3170/83) + (5)·(3505/83) + (3)·(6510/83) = 215; B5 = 215; |AX − B| = 0
Fila 6: (1)·(-26355/83) + (2)·(-6780/83) + (1)·(18555/83) + (2)·(3170/83) + (1)·(3505/83) + (4)·(6510/83) = 175; B6 = 175; |AX − B| = 0


## Procedimiento — Diagnóstico: determinante y rangos

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  100 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ 3  2  4  1  3  2  |  100 ]
[ 1  3  2  2  1  2  |  160 ]
[ 2  1  3  1  2  1  |  155 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

### Paso 3. F2 ← F2 + (-1/3) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 3    2    4    1  3    2  |    100 ]
[ 0  7/3  2/3  5/3  0  4/3  |  380/3 ]
[ 2    1    3    1  2    1  |    155 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 1    2    1    2  1    4  |    175 ]
```

### Paso 4. F3 ← F3 + (-2/3) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2    4    1  3     2  |    100 ]
[ 0   7/3  2/3  5/3  0   4/3  |  380/3 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |  265/3 ]
[ 1     1    1    4  2     1  |    140 ]
[ 2     1    2    1  5     3  |    215 ]
[ 1     2    1    2  1     4  |    175 ]
```

### Paso 5. F4 ← F4 + (-1/3) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 2     1     2     1  5     3  |    215 ]
[ 1     2     1     2  1     4  |    175 ]
```

### Paso 6. F5 ← F5 + (-2/3) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 1     2     1     2  1     4  |    175 ]
```

### Paso 7. F6 ← F6 + (-1/3) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 8. F3 ← F3 + (1/7) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0     0   3/7   4/7  0  -1/7  |  745/7 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 9. F4 ← F4 + (-1/7) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0     0   3/7   4/7  0  -1/7  |  745/7 ]
[ 0     0  -3/7  24/7  1   1/7  |  620/7 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 10. F5 ← F5 + (1/7) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3    2     4     1  3     2  |     100 ]
[ 0  7/3   2/3   5/3  0   4/3  |   380/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0  4/3  -1/3   5/3  0  10/3  |   425/3 ]
```

### Paso 11. F6 ← F6 + (-4/7) · F2

Se anula la entrada 4/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3    2     4     1  3     2  |     100 ]
[ 0  7/3   2/3   5/3  0   4/3  |   380/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0    0  -5/7   5/7  0  18/7  |   485/7 ]
```

### Paso 12. F3 ↔ F6

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 3.

```text
[ 3    2     4     1  3     2  |     100 ]
[ 0  7/3   2/3   5/3  0   4/3  |   380/3 ]
[ 0    0  -5/7   5/7  0  18/7  |   485/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
```

### Paso 13. F4 ← F4 + (-3/5) · F3

Se anula la entrada -3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 3    2     4    1  3     2  |     100 ]
[ 0  7/3   2/3  5/3  0   4/3  |   380/3 ]
[ 0    0  -5/7  5/7  0  18/7  |   485/7 ]
[ 0    0     0    3  1  -7/5  |      47 ]
[ 0    0  -4/7  4/7  3  13/7  |  1165/7 ]
[ 0    0   3/7  4/7  0  -1/7  |   745/7 ]
```

### Paso 14. F5 ← F5 + (-4/5) · F3

Se anula la entrada -4/7 en la columna 3; se opera sobre la fila completa.

```text
[ 3    2     4    1  3     2  |    100 ]
[ 0  7/3   2/3  5/3  0   4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  485/7 ]
[ 0    0     0    3  1  -7/5  |     47 ]
[ 0    0     0    0  3  -1/5  |    111 ]
[ 0    0   3/7  4/7  0  -1/7  |  745/7 ]
```

### Paso 15. F6 ← F6 + (3/5) · F3

Se anula la entrada 3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 3    2     4    1  3     2  |    100 ]
[ 0  7/3   2/3  5/3  0   4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  485/7 ]
[ 0    0     0    3  1  -7/5  |     47 ]
[ 0    0     0    0  3  -1/5  |    111 ]
[ 0    0     0    1  0   7/5  |    148 ]
```

### Paso 16. F6 ← F6 + (-1/3) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 3    2     4    1     3      2  |    100 ]
[ 0  7/3   2/3  5/3     0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7     0   18/7  |  485/7 ]
[ 0    0     0    3     1   -7/5  |     47 ]
[ 0    0     0    0     3   -1/5  |    111 ]
[ 0    0     0    0  -1/3  28/15  |  397/3 ]
```

### Paso 17. F6 ← F6 + (1/9) · F5

Se anula la entrada -1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 18. det(A) = -83

2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (3) · (7/3) · (-5/7) · (3) · (3) · (83/45) = -83.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```


## Procedimiento — Eliminación de Gauss

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  100 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ 3  2  4  1  3  2  |  100 ]
[ 1  3  2  2  1  2  |  160 ]
[ 2  1  3  1  2  1  |  155 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

### Paso 3. F2 ← F2 + (-1/3) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 3    2    4    1  3    2  |    100 ]
[ 0  7/3  2/3  5/3  0  4/3  |  380/3 ]
[ 2    1    3    1  2    1  |    155 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 1    2    1    2  1    4  |    175 ]
```

### Paso 4. F3 ← F3 + (-2/3) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2    4    1  3     2  |    100 ]
[ 0   7/3  2/3  5/3  0   4/3  |  380/3 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |  265/3 ]
[ 1     1    1    4  2     1  |    140 ]
[ 2     1    2    1  5     3  |    215 ]
[ 1     2    1    2  1     4  |    175 ]
```

### Paso 5. F4 ← F4 + (-1/3) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 2     1     2     1  5     3  |    215 ]
[ 1     2     1     2  1     4  |    175 ]
```

### Paso 6. F5 ← F5 + (-2/3) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 1     2     1     2  1     4  |    175 ]
```

### Paso 7. F6 ← F6 + (-1/3) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 8. F3 ← F3 + (1/7) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0     0   3/7   4/7  0  -1/7  |  745/7 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 9. F4 ← F4 + (-1/7) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3     2     4     1  3     2  |    100 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0     0   3/7   4/7  0  -1/7  |  745/7 ]
[ 0     0  -3/7  24/7  1   1/7  |  620/7 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 10. F5 ← F5 + (1/7) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3    2     4     1  3     2  |     100 ]
[ 0  7/3   2/3   5/3  0   4/3  |   380/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0  4/3  -1/3   5/3  0  10/3  |   425/3 ]
```

### Paso 11. F6 ← F6 + (-4/7) · F2

Se anula la entrada 4/3 en la columna 2; se opera sobre la fila completa.

```text
[ 3    2     4     1  3     2  |     100 ]
[ 0  7/3   2/3   5/3  0   4/3  |   380/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0    0  -5/7   5/7  0  18/7  |   485/7 ]
```

### Paso 12. F3 ↔ F6

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 3.

```text
[ 3    2     4     1  3     2  |     100 ]
[ 0  7/3   2/3   5/3  0   4/3  |   380/3 ]
[ 0    0  -5/7   5/7  0  18/7  |   485/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
```

### Paso 13. F4 ← F4 + (-3/5) · F3

Se anula la entrada -3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 3    2     4    1  3     2  |     100 ]
[ 0  7/3   2/3  5/3  0   4/3  |   380/3 ]
[ 0    0  -5/7  5/7  0  18/7  |   485/7 ]
[ 0    0     0    3  1  -7/5  |      47 ]
[ 0    0  -4/7  4/7  3  13/7  |  1165/7 ]
[ 0    0   3/7  4/7  0  -1/7  |   745/7 ]
```

### Paso 14. F5 ← F5 + (-4/5) · F3

Se anula la entrada -4/7 en la columna 3; se opera sobre la fila completa.

```text
[ 3    2     4    1  3     2  |    100 ]
[ 0  7/3   2/3  5/3  0   4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  485/7 ]
[ 0    0     0    3  1  -7/5  |     47 ]
[ 0    0     0    0  3  -1/5  |    111 ]
[ 0    0   3/7  4/7  0  -1/7  |  745/7 ]
```

### Paso 15. F6 ← F6 + (3/5) · F3

Se anula la entrada 3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 3    2     4    1  3     2  |    100 ]
[ 0  7/3   2/3  5/3  0   4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  485/7 ]
[ 0    0     0    3  1  -7/5  |     47 ]
[ 0    0     0    0  3  -1/5  |    111 ]
[ 0    0     0    1  0   7/5  |    148 ]
```

### Paso 16. F6 ← F6 + (-1/3) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 3    2     4    1     3      2  |    100 ]
[ 0  7/3   2/3  5/3     0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7     0   18/7  |  485/7 ]
[ 0    0     0    3     1   -7/5  |     47 ]
[ 0    0     0    0     3   -1/5  |    111 ]
[ 0    0     0    0  -1/3  28/15  |  397/3 ]
```

### Paso 17. F6 ← F6 + (1/9) · F5

Se anula la entrada -1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 18. det(A) = -83

2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (3) · (7/3) · (-5/7) · (3) · (3) · (83/45) = -83.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 19. Matriz triangular superior U

Se resuelve U·X = C desde la última fila hacia la primera.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 20. x6 = (434/3 − (0)) / (83/45) = 6510/83

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 21. x5 = (111 − ((-1/5)·(6510/83))) / (3) = 3505/83

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 22. x4 = (47 − ((1)·(3505/83) + (-7/5)·(6510/83))) / (3) = 3170/83

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 23. x3 = (485/7 − ((5/7)·(3170/83) + (0)·(3505/83) + (18/7)·(6510/83))) / (-5/7) = 18555/83

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 24. x2 = (380/3 − ((2/3)·(18555/83) + (5/3)·(3170/83) + (0)·(3505/83) + (4/3)·(6510/83))) / (7/3) = -6780/83

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```

### Paso 25. x1 = (100 − ((2)·(-6780/83) + (4)·(18555/83) + (1)·(3170/83) + (3)·(3505/83) + (2)·(6510/83))) / (3) = -26355/83

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ 3    2     4    1  3      2  |    100 ]
[ 0  7/3   2/3  5/3  0    4/3  |  380/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  485/7 ]
[ 0    0     0    3  1   -7/5  |     47 ]
[ 0    0     0    0  3   -1/5  |    111 ]
[ 0    0     0    0  0  83/45  |  434/3 ]
```


## Procedimiento — Gauss-Jordan

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  100 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ 3  2  4  1  3  2  |  100 ]
[ 1  3  2  2  1  2  |  160 ]
[ 2  1  3  1  2  1  |  155 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 1  2  1  2  1  4  |  175 ]
```

### Paso 3. F1 ← (1/3) · F1

Se convierte el pivote 3 en 1.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  100/3 ]
[ 1    3    2    2  1    2  |    160 ]
[ 2    1    3    1  2    1  |    155 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 1    2    1    2  1    4  |    175 ]
```

### Paso 4. F2 ← F2 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  100/3 ]
[ 0  7/3  2/3  5/3  0  4/3  |  380/3 ]
[ 2    1    3    1  2    1  |    155 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 1    2    1    2  1    4  |    175 ]
```

### Paso 5. F3 ← F3 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3  4/3  1/3  1   2/3  |  100/3 ]
[ 0   7/3  2/3  5/3  0   4/3  |  380/3 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |  265/3 ]
[ 1     1    1    4  2     1  |    140 ]
[ 2     1    2    1  5     3  |    215 ]
[ 1     2    1    2  1     4  |    175 ]
```

### Paso 6. F4 ← F4 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  100/3 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 2     1     2     1  5     3  |    215 ]
[ 1     2     1     2  1     4  |    175 ]
```

### Paso 7. F5 ← F5 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  100/3 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 1     2     1     2  1     4  |    175 ]
```

### Paso 8. F6 ← F6 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  100/3 ]
[ 0   7/3   2/3   5/3  0   4/3  |  380/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 9. F2 ← (3/7) · F2

Se convierte el pivote 7/3 en 1.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  100/3 ]
[ 0     1   2/7   5/7  0   4/7  |  380/7 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 10. F1 ← F1 + (-2/3) · F2

Se anula la entrada 2/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1     0   8/7  -1/7  1   2/7  |  -20/7 ]
[ 0     1   2/7   5/7  0   4/7  |  380/7 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  265/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 11. F3 ← F3 + (1/3) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1     0   8/7  -1/7  1   2/7  |  -20/7 ]
[ 0     1   2/7   5/7  0   4/7  |  380/7 ]
[ 0     0   3/7   4/7  0  -1/7  |  745/7 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  320/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 12. F4 ← F4 + (-1/3) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1     0   8/7  -1/7  1   2/7  |  -20/7 ]
[ 0     1   2/7   5/7  0   4/7  |  380/7 ]
[ 0     0   3/7   4/7  0  -1/7  |  745/7 ]
[ 0     0  -3/7  24/7  1   1/7  |  620/7 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  445/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  425/3 ]
```

### Paso 13. F5 ← F5 + (1/3) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1    0   8/7  -1/7  1   2/7  |   -20/7 ]
[ 0    1   2/7   5/7  0   4/7  |   380/7 ]
[ 0    0   3/7   4/7  0  -1/7  |   745/7 ]
[ 0    0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0  4/3  -1/3   5/3  0  10/3  |   425/3 ]
```

### Paso 14. F6 ← F6 + (-4/3) · F2

Se anula la entrada 4/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1  0   8/7  -1/7  1   2/7  |   -20/7 ]
[ 0  1   2/7   5/7  0   4/7  |   380/7 ]
[ 0  0   3/7   4/7  0  -1/7  |   745/7 ]
[ 0  0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0  0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0  0  -5/7   5/7  0  18/7  |   485/7 ]
```

### Paso 15. F3 ↔ F6

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 3.

```text
[ 1  0   8/7  -1/7  1   2/7  |   -20/7 ]
[ 0  1   2/7   5/7  0   4/7  |   380/7 ]
[ 0  0  -5/7   5/7  0  18/7  |   485/7 ]
[ 0  0  -3/7  24/7  1   1/7  |   620/7 ]
[ 0  0  -4/7   4/7  3  13/7  |  1165/7 ]
[ 0  0   3/7   4/7  0  -1/7  |   745/7 ]
```

### Paso 16. F3 ← (-7/5) · F3

Se convierte el pivote -5/7 en 1.

```text
[ 1  0   8/7  -1/7  1    2/7  |   -20/7 ]
[ 0  1   2/7   5/7  0    4/7  |   380/7 ]
[ 0  0     1    -1  0  -18/5  |     -97 ]
[ 0  0  -3/7  24/7  1    1/7  |   620/7 ]
[ 0  0  -4/7   4/7  3   13/7  |  1165/7 ]
[ 0  0   3/7   4/7  0   -1/7  |   745/7 ]
```

### Paso 17. F1 ← F1 + (-8/7) · F3

Se anula la entrada 8/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0     1  1   22/5  |     108 ]
[ 0  1   2/7   5/7  0    4/7  |   380/7 ]
[ 0  0     1    -1  0  -18/5  |     -97 ]
[ 0  0  -3/7  24/7  1    1/7  |   620/7 ]
[ 0  0  -4/7   4/7  3   13/7  |  1165/7 ]
[ 0  0   3/7   4/7  0   -1/7  |   745/7 ]
```

### Paso 18. F2 ← F2 + (-2/7) · F3

Se anula la entrada 2/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0     1  1   22/5  |     108 ]
[ 0  1     0     1  0    8/5  |      82 ]
[ 0  0     1    -1  0  -18/5  |     -97 ]
[ 0  0  -3/7  24/7  1    1/7  |   620/7 ]
[ 0  0  -4/7   4/7  3   13/7  |  1165/7 ]
[ 0  0   3/7   4/7  0   -1/7  |   745/7 ]
```

### Paso 19. F4 ← F4 + (3/7) · F3

Se anula la entrada -3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0    1  1   22/5  |     108 ]
[ 0  1     0    1  0    8/5  |      82 ]
[ 0  0     1   -1  0  -18/5  |     -97 ]
[ 0  0     0    3  1   -7/5  |      47 ]
[ 0  0  -4/7  4/7  3   13/7  |  1165/7 ]
[ 0  0   3/7  4/7  0   -1/7  |   745/7 ]
```

### Paso 20. F5 ← F5 + (4/7) · F3

Se anula la entrada -4/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0    0    1  1   22/5  |    108 ]
[ 0  1    0    1  0    8/5  |     82 ]
[ 0  0    1   -1  0  -18/5  |    -97 ]
[ 0  0    0    3  1   -7/5  |     47 ]
[ 0  0    0    0  3   -1/5  |    111 ]
[ 0  0  3/7  4/7  0   -1/7  |  745/7 ]
```

### Paso 21. F6 ← F6 + (-3/7) · F3

Se anula la entrada 3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0  0   1  1   22/5  |  108 ]
[ 0  1  0   1  0    8/5  |   82 ]
[ 0  0  1  -1  0  -18/5  |  -97 ]
[ 0  0  0   3  1   -7/5  |   47 ]
[ 0  0  0   0  3   -1/5  |  111 ]
[ 0  0  0   1  0    7/5  |  148 ]
```

### Paso 22. F4 ← (1/3) · F4

Se convierte el pivote 3 en 1.

```text
[ 1  0  0   1    1   22/5  |   108 ]
[ 0  1  0   1    0    8/5  |    82 ]
[ 0  0  1  -1    0  -18/5  |   -97 ]
[ 0  0  0   1  1/3  -7/15  |  47/3 ]
[ 0  0  0   0    3   -1/5  |   111 ]
[ 0  0  0   1    0    7/5  |   148 ]
```

### Paso 23. F1 ← F1 + (-1) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0   0  2/3  73/15  |  277/3 ]
[ 0  1  0   1    0    8/5  |     82 ]
[ 0  0  1  -1    0  -18/5  |    -97 ]
[ 0  0  0   1  1/3  -7/15  |   47/3 ]
[ 0  0  0   0    3   -1/5  |    111 ]
[ 0  0  0   1    0    7/5  |    148 ]
```

### Paso 24. F2 ← F2 + (-1) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0   0   2/3  73/15  |  277/3 ]
[ 0  1  0   0  -1/3  31/15  |  199/3 ]
[ 0  0  1  -1     0  -18/5  |    -97 ]
[ 0  0  0   1   1/3  -7/15  |   47/3 ]
[ 0  0  0   0     3   -1/5  |    111 ]
[ 0  0  0   1     0    7/5  |    148 ]
```

### Paso 25. F3 ← F3 + (1) · F4

Se anula la entrada -1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0  0   2/3   73/15  |   277/3 ]
[ 0  1  0  0  -1/3   31/15  |   199/3 ]
[ 0  0  1  0   1/3  -61/15  |  -244/3 ]
[ 0  0  0  1   1/3   -7/15  |    47/3 ]
[ 0  0  0  0     3    -1/5  |     111 ]
[ 0  0  0  1     0     7/5  |     148 ]
```

### Paso 26. F6 ← F6 + (-1) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0  0   2/3   73/15  |   277/3 ]
[ 0  1  0  0  -1/3   31/15  |   199/3 ]
[ 0  0  1  0   1/3  -61/15  |  -244/3 ]
[ 0  0  0  1   1/3   -7/15  |    47/3 ]
[ 0  0  0  0     3    -1/5  |     111 ]
[ 0  0  0  0  -1/3   28/15  |   397/3 ]
```

### Paso 27. F5 ← (1/3) · F5

Se convierte el pivote 3 en 1.

```text
[ 1  0  0  0   2/3   73/15  |   277/3 ]
[ 0  1  0  0  -1/3   31/15  |   199/3 ]
[ 0  0  1  0   1/3  -61/15  |  -244/3 ]
[ 0  0  0  1   1/3   -7/15  |    47/3 ]
[ 0  0  0  0     1   -1/15  |      37 ]
[ 0  0  0  0  -1/3   28/15  |   397/3 ]
```

### Paso 28. F1 ← F1 + (-2/3) · F5

Se anula la entrada 2/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  221/45  |   203/3 ]
[ 0  1  0  0  -1/3   31/15  |   199/3 ]
[ 0  0  1  0   1/3  -61/15  |  -244/3 ]
[ 0  0  0  1   1/3   -7/15  |    47/3 ]
[ 0  0  0  0     1   -1/15  |      37 ]
[ 0  0  0  0  -1/3   28/15  |   397/3 ]
```

### Paso 29. F2 ← F2 + (1/3) · F5

Se anula la entrada -1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  221/45  |   203/3 ]
[ 0  1  0  0     0   92/45  |   236/3 ]
[ 0  0  1  0   1/3  -61/15  |  -244/3 ]
[ 0  0  0  1   1/3   -7/15  |    47/3 ]
[ 0  0  0  0     1   -1/15  |      37 ]
[ 0  0  0  0  -1/3   28/15  |   397/3 ]
```

### Paso 30. F3 ← F3 + (-1/3) · F5

Se anula la entrada 1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0   221/45  |   203/3 ]
[ 0  1  0  0     0    92/45  |   236/3 ]
[ 0  0  1  0     0  -182/45  |  -281/3 ]
[ 0  0  0  1   1/3    -7/15  |    47/3 ]
[ 0  0  0  0     1    -1/15  |      37 ]
[ 0  0  0  0  -1/3    28/15  |   397/3 ]
```

### Paso 31. F4 ← F4 + (-1/3) · F5

Se anula la entrada 1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0   221/45  |   203/3 ]
[ 0  1  0  0     0    92/45  |   236/3 ]
[ 0  0  1  0     0  -182/45  |  -281/3 ]
[ 0  0  0  1     0     -4/9  |    10/3 ]
[ 0  0  0  0     1    -1/15  |      37 ]
[ 0  0  0  0  -1/3    28/15  |   397/3 ]
```

### Paso 32. F6 ← F6 + (1/3) · F5

Se anula la entrada -1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0  0   221/45  |   203/3 ]
[ 0  1  0  0  0    92/45  |   236/3 ]
[ 0  0  1  0  0  -182/45  |  -281/3 ]
[ 0  0  0  1  0     -4/9  |    10/3 ]
[ 0  0  0  0  1    -1/15  |      37 ]
[ 0  0  0  0  0    83/45  |   434/3 ]
```

### Paso 33. F6 ← (45/83) · F6

Se convierte el pivote 83/45 en 1.

```text
[ 1  0  0  0  0   221/45  |    203/3 ]
[ 0  1  0  0  0    92/45  |    236/3 ]
[ 0  0  1  0  0  -182/45  |   -281/3 ]
[ 0  0  0  1  0     -4/9  |     10/3 ]
[ 0  0  0  0  1    -1/15  |       37 ]
[ 0  0  0  0  0        1  |  6510/83 ]
```

### Paso 34. F1 ← F1 + (-221/45) · F6

Se anula la entrada 221/45 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0        0  |  -26355/83 ]
[ 0  1  0  0  0    92/45  |      236/3 ]
[ 0  0  1  0  0  -182/45  |     -281/3 ]
[ 0  0  0  1  0     -4/9  |       10/3 ]
[ 0  0  0  0  1    -1/15  |         37 ]
[ 0  0  0  0  0        1  |    6510/83 ]
```

### Paso 35. F2 ← F2 + (-92/45) · F6

Se anula la entrada 92/45 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0        0  |  -26355/83 ]
[ 0  1  0  0  0        0  |   -6780/83 ]
[ 0  0  1  0  0  -182/45  |     -281/3 ]
[ 0  0  0  1  0     -4/9  |       10/3 ]
[ 0  0  0  0  1    -1/15  |         37 ]
[ 0  0  0  0  0        1  |    6510/83 ]
```

### Paso 36. F3 ← F3 + (182/45) · F6

Se anula la entrada -182/45 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0      0  |  -26355/83 ]
[ 0  1  0  0  0      0  |   -6780/83 ]
[ 0  0  1  0  0      0  |   18555/83 ]
[ 0  0  0  1  0   -4/9  |       10/3 ]
[ 0  0  0  0  1  -1/15  |         37 ]
[ 0  0  0  0  0      1  |    6510/83 ]
```

### Paso 37. F4 ← F4 + (4/9) · F6

Se anula la entrada -4/9 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0      0  |  -26355/83 ]
[ 0  1  0  0  0      0  |   -6780/83 ]
[ 0  0  1  0  0      0  |   18555/83 ]
[ 0  0  0  1  0      0  |    3170/83 ]
[ 0  0  0  0  1  -1/15  |         37 ]
[ 0  0  0  0  0      1  |    6510/83 ]
```

### Paso 38. F5 ← F5 + (1/15) · F6

Se anula la entrada -1/15 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0  0  |  -26355/83 ]
[ 0  1  0  0  0  0  |   -6780/83 ]
[ 0  0  1  0  0  0  |   18555/83 ]
[ 0  0  0  1  0  0  |    3170/83 ]
[ 0  0  0  0  1  0  |    3505/83 ]
[ 0  0  0  0  0  1  |    6510/83 ]
```

### Paso 39. [I | X]: lectura de la solución

Cada fila contiene una incógnita con coeficiente 1; la última columna es X.

```text
[ 1  0  0  0  0  0  |  -26355/83 ]
[ 0  1  0  0  0  0  |   -6780/83 ]
[ 0  0  1  0  0  0  |   18555/83 ]
[ 0  0  0  1  0  0  |    3170/83 ]
[ 0  0  0  0  1  0  |    3505/83 ]
[ 0  0  0  0  0  1  |    6510/83 ]
```


## Procedimiento — Matriz inversa

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[ 2  1  3  1  2  1  |  1  0  0  0  0  0 ]
[ 1  3  2  2  1  2  |  0  1  0  0  0  0 ]
[ 3  2  4  1  3  2  |  0  0  1  0  0  0 ]
[ 1  1  1  4  2  1  |  0  0  0  1  0  0 ]
[ 2  1  2  1  5  3  |  0  0  0  0  1  0 ]
[ 1  2  1  2  1  4  |  0  0  0  0  0  1 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ 3  2  4  1  3  2  |  0  0  1  0  0  0 ]
[ 1  3  2  2  1  2  |  0  1  0  0  0  0 ]
[ 2  1  3  1  2  1  |  1  0  0  0  0  0 ]
[ 1  1  1  4  2  1  |  0  0  0  1  0  0 ]
[ 2  1  2  1  5  3  |  0  0  0  0  1  0 ]
[ 1  2  1  2  1  4  |  0  0  0  0  0  1 ]
```

### Paso 3. F1 ← (1/3) · F1

Se convierte el pivote 3 en 1.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  0  0  1/3  0  0  0 ]
[ 1    3    2    2  1    2  |  0  1    0  0  0  0 ]
[ 2    1    3    1  2    1  |  1  0    0  0  0  0 ]
[ 1    1    1    4  2    1  |  0  0    0  1  0  0 ]
[ 2    1    2    1  5    3  |  0  0    0  0  1  0 ]
[ 1    2    1    2  1    4  |  0  0    0  0  0  1 ]
```

### Paso 4. F2 ← F2 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  0  0   1/3  0  0  0 ]
[ 0  7/3  2/3  5/3  0  4/3  |  0  1  -1/3  0  0  0 ]
[ 2    1    3    1  2    1  |  1  0     0  0  0  0 ]
[ 1    1    1    4  2    1  |  0  0     0  1  0  0 ]
[ 2    1    2    1  5    3  |  0  0     0  0  1  0 ]
[ 1    2    1    2  1    4  |  0  0     0  0  0  1 ]
```

### Paso 5. F3 ← F3 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3  4/3  1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3  2/3  5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 1     1    1    4  2     1  |  0  0     0  1  0  0 ]
[ 2     1    2    1  5     3  |  0  0     0  0  1  0 ]
[ 1     2    1    2  1     4  |  0  0     0  0  0  1 ]
```

### Paso 6. F4 ← F4 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3   2/3   5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0  0  -1/3  1  0  0 ]
[ 2     1     2     1  5     3  |  0  0     0  0  1  0 ]
[ 1     2     1     2  1     4  |  0  0     0  0  0  1 ]
```

### Paso 7. F5 ← F5 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3   2/3   5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0  0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0  0  -2/3  0  1  0 ]
[ 1     2     1     2  1     4  |  0  0     0  0  0  1 ]
```

### Paso 8. F6 ← F6 + (-1) · F1

Se anula la entrada 1 en la columna 1; se opera sobre la fila completa.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3   2/3   5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0  0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0  0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0  0  -1/3  0  0  1 ]
```

### Paso 9. F2 ← (3/7) · F2

Se convierte el pivote 7/3 en 1.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0    0   1/3  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0  3/7  -1/7  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1    0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0    0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0    0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0    0  -1/3  0  0  1 ]
```

### Paso 10. F1 ← F1 + (-2/3) · F2

Se anula la entrada 2/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1     0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1     0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0     0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0     0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 11. F3 ← F3 + (1/3) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1     0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0     0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0     0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0     0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 12. F4 ← F4 + (-1/3) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1     0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0     0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0     0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0     0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 13. F5 ← F5 + (1/3) · F2

Se anula la entrada -1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1    0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0    1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0    0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0    0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0    0  -4/7   4/7  3  13/7  |  0   1/7  -5/7  0  1  0 ]
[ 0  4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 14. F6 ← F6 + (-4/3) · F2

Se anula la entrada 4/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1  0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0  1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0  0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0  0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0  0  -4/7   4/7  3  13/7  |  0   1/7  -5/7  0  1  0 ]
[ 0  0  -5/7   5/7  0  18/7  |  0  -4/7  -1/7  0  0  1 ]
```

### Paso 15. F3 ↔ F6

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 3.

```text
[ 1  0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0  1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0  0  -5/7   5/7  0  18/7  |  0  -4/7  -1/7  0  0  1 ]
[ 0  0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0  0  -4/7   4/7  3  13/7  |  0   1/7  -5/7  0  1  0 ]
[ 0  0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
```

### Paso 16. F3 ← (-7/5) · F3

Se convierte el pivote -5/7 en 1.

```text
[ 1  0   8/7  -1/7  1    2/7  |  0  -2/7   3/7  0  0     0 ]
[ 0  1   2/7   5/7  0    4/7  |  0   3/7  -1/7  0  0     0 ]
[ 0  0     1    -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  -3/7  24/7  1    1/7  |  0  -1/7  -2/7  1  0     0 ]
[ 0  0  -4/7   4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7   4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 17. F1 ← F1 + (-8/7) · F3

Se anula la entrada 8/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0     1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1   2/7   5/7  0    4/7  |  0   3/7  -1/7  0  0     0 ]
[ 0  0     1    -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  -3/7  24/7  1    1/7  |  0  -1/7  -2/7  1  0     0 ]
[ 0  0  -4/7   4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7   4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 18. F2 ← F2 + (-2/7) · F3

Se anula la entrada 2/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0     1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1     0     1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0     1    -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  -3/7  24/7  1    1/7  |  0  -1/7  -2/7  1  0     0 ]
[ 0  0  -4/7   4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7   4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 19. F4 ← F4 + (3/7) · F3

Se anula la entrada -3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0     0    1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1     0    1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0     1   -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0     0    3  1   -7/5  |  0   1/5  -1/5  1  0  -3/5 ]
[ 0  0  -4/7  4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7  4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 20. F5 ← F5 + (4/7) · F3

Se anula la entrada -4/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0    0    1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1    0    1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0    1   -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0    0    3  1   -7/5  |  0   1/5  -1/5  1  0  -3/5 ]
[ 0  0    0    0  3   -1/5  |  0   3/5  -3/5  0  1  -4/5 ]
[ 0  0  3/7  4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 21. F6 ← F6 + (-3/7) · F3

Se anula la entrada 3/7 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0  0   1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1  0   1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0  1  -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  0   3  1   -7/5  |  0   1/5  -1/5  1  0  -3/5 ]
[ 0  0  0   0  3   -1/5  |  0   3/5  -3/5  0  1  -4/5 ]
[ 0  0  0   1  0    7/5  |  1  -1/5  -4/5  0  0   3/5 ]
```

### Paso 22. F4 ← (1/3) · F4

Se convierte el pivote 3 en 1.

```text
[ 1  0  0   1    1   22/5  |  0  -6/5    1/5    0  0   8/5 ]
[ 0  1  0   1    0    8/5  |  0   1/5   -1/5    0  0   2/5 ]
[ 0  0  1  -1    0  -18/5  |  0   4/5    1/5    0  0  -7/5 ]
[ 0  0  0   1  1/3  -7/15  |  0  1/15  -1/15  1/3  0  -1/5 ]
[ 0  0  0   0    3   -1/5  |  0   3/5   -3/5    0  1  -4/5 ]
[ 0  0  0   1    0    7/5  |  1  -1/5   -4/5    0  0   3/5 ]
```

### Paso 23. F1 ← F1 + (-1) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0   0  2/3  73/15  |  0  -19/15   4/15  -1/3  0   9/5 ]
[ 0  1  0   1    0    8/5  |  0     1/5   -1/5     0  0   2/5 ]
[ 0  0  1  -1    0  -18/5  |  0     4/5    1/5     0  0  -7/5 ]
[ 0  0  0   1  1/3  -7/15  |  0    1/15  -1/15   1/3  0  -1/5 ]
[ 0  0  0   0    3   -1/5  |  0     3/5   -3/5     0  1  -4/5 ]
[ 0  0  0   1    0    7/5  |  1    -1/5   -4/5     0  0   3/5 ]
```

### Paso 24. F2 ← F2 + (-1) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0   0   2/3  73/15  |  0  -19/15   4/15  -1/3  0   9/5 ]
[ 0  1  0   0  -1/3  31/15  |  0    2/15  -2/15  -1/3  0   3/5 ]
[ 0  0  1  -1     0  -18/5  |  0     4/5    1/5     0  0  -7/5 ]
[ 0  0  0   1   1/3  -7/15  |  0    1/15  -1/15   1/3  0  -1/5 ]
[ 0  0  0   0     3   -1/5  |  0     3/5   -3/5     0  1  -4/5 ]
[ 0  0  0   1     0    7/5  |  1    -1/5   -4/5     0  0   3/5 ]
```

### Paso 25. F3 ← F3 + (1) · F4

Se anula la entrada -1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0  0   2/3   73/15  |  0  -19/15   4/15  -1/3  0   9/5 ]
[ 0  1  0  0  -1/3   31/15  |  0    2/15  -2/15  -1/3  0   3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0   13/15   2/15   1/3  0  -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0    1/15  -1/15   1/3  0  -1/5 ]
[ 0  0  0  0     3    -1/5  |  0     3/5   -3/5     0  1  -4/5 ]
[ 0  0  0  1     0     7/5  |  1    -1/5   -4/5     0  0   3/5 ]
```

### Paso 26. F6 ← F6 + (-1) · F4

Se anula la entrada 1 en la columna 4; se opera sobre la fila completa.

```text
[ 1  0  0  0   2/3   73/15  |  0  -19/15    4/15  -1/3  0   9/5 ]
[ 0  1  0  0  -1/3   31/15  |  0    2/15   -2/15  -1/3  0   3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0   13/15    2/15   1/3  0  -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0    1/15   -1/15   1/3  0  -1/5 ]
[ 0  0  0  0     3    -1/5  |  0     3/5    -3/5     0  1  -4/5 ]
[ 0  0  0  0  -1/3   28/15  |  1   -4/15  -11/15  -1/3  0   4/5 ]
```

### Paso 27. F5 ← (1/3) · F5

Se convierte el pivote 3 en 1.

```text
[ 1  0  0  0   2/3   73/15  |  0  -19/15    4/15  -1/3    0    9/5 ]
[ 0  1  0  0  -1/3   31/15  |  0    2/15   -2/15  -1/3    0    3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0   13/15    2/15   1/3    0   -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0    1/15   -1/15   1/3    0   -1/5 ]
[ 0  0  0  0     1   -1/15  |  0     1/5    -1/5     0  1/3  -4/15 ]
[ 0  0  0  0  -1/3   28/15  |  1   -4/15  -11/15  -1/3    0    4/5 ]
```

### Paso 28. F1 ← F1 + (-2/3) · F5

Se anula la entrada 2/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  221/45  |  0   -7/5     2/5  -1/3  -2/9  89/45 ]
[ 0  1  0  0  -1/3   31/15  |  0   2/15   -2/15  -1/3     0    3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0  13/15    2/15   1/3     0   -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0   1/15   -1/15   1/3     0   -1/5 ]
[ 0  0  0  0     1   -1/15  |  0    1/5    -1/5     0   1/3  -4/15 ]
[ 0  0  0  0  -1/3   28/15  |  1  -4/15  -11/15  -1/3     0    4/5 ]
```

### Paso 29. F2 ← F2 + (1/3) · F5

Se anula la entrada -1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0  221/45  |  0   -7/5     2/5  -1/3  -2/9  89/45 ]
[ 0  1  0  0     0   92/45  |  0    1/5    -1/5  -1/3   1/9  23/45 ]
[ 0  0  1  0   1/3  -61/15  |  0  13/15    2/15   1/3     0   -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0   1/15   -1/15   1/3     0   -1/5 ]
[ 0  0  0  0     1   -1/15  |  0    1/5    -1/5     0   1/3  -4/15 ]
[ 0  0  0  0  -1/3   28/15  |  1  -4/15  -11/15  -1/3     0    4/5 ]
```

### Paso 30. F3 ← F3 + (-1/3) · F5

Se anula la entrada 1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0   221/45  |  0   -7/5     2/5  -1/3  -2/9   89/45 ]
[ 0  1  0  0     0    92/45  |  0    1/5    -1/5  -1/3   1/9   23/45 ]
[ 0  0  1  0     0  -182/45  |  0    4/5     1/5   1/3  -1/9  -68/45 ]
[ 0  0  0  1   1/3    -7/15  |  0   1/15   -1/15   1/3     0    -1/5 ]
[ 0  0  0  0     1    -1/15  |  0    1/5    -1/5     0   1/3   -4/15 ]
[ 0  0  0  0  -1/3    28/15  |  1  -4/15  -11/15  -1/3     0     4/5 ]
```

### Paso 31. F4 ← F4 + (-1/3) · F5

Se anula la entrada 1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0     0   221/45  |  0   -7/5     2/5  -1/3  -2/9   89/45 ]
[ 0  1  0  0     0    92/45  |  0    1/5    -1/5  -1/3   1/9   23/45 ]
[ 0  0  1  0     0  -182/45  |  0    4/5     1/5   1/3  -1/9  -68/45 ]
[ 0  0  0  1     0     -4/9  |  0      0       0   1/3  -1/9    -1/9 ]
[ 0  0  0  0     1    -1/15  |  0    1/5    -1/5     0   1/3   -4/15 ]
[ 0  0  0  0  -1/3    28/15  |  1  -4/15  -11/15  -1/3     0     4/5 ]
```

### Paso 32. F6 ← F6 + (1/3) · F5

Se anula la entrada -1/3 en la columna 5; se opera sobre la fila completa.

```text
[ 1  0  0  0  0   221/45  |  0  -7/5   2/5  -1/3  -2/9   89/45 ]
[ 0  1  0  0  0    92/45  |  0   1/5  -1/5  -1/3   1/9   23/45 ]
[ 0  0  1  0  0  -182/45  |  0   4/5   1/5   1/3  -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |  0     0     0   1/3  -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |  0   1/5  -1/5     0   1/3   -4/15 ]
[ 0  0  0  0  0    83/45  |  1  -1/5  -4/5  -1/3   1/9   32/45 ]
```

### Paso 33. F6 ← (45/83) · F6

Se convierte el pivote 83/45 en 1.

```text
[ 1  0  0  0  0   221/45  |      0   -7/5     2/5    -1/3  -2/9   89/45 ]
[ 0  1  0  0  0    92/45  |      0    1/5    -1/5    -1/3   1/9   23/45 ]
[ 0  0  1  0  0  -182/45  |      0    4/5     1/5     1/3  -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |      0      0       0     1/3  -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |      0    1/5    -1/5       0   1/3   -4/15 ]
[ 0  0  0  0  0        1  |  45/83  -9/83  -36/83  -15/83  5/83   32/83 ]
```

### Paso 34. F1 ← F1 + (-221/45) · F6

Se anula la entrada 221/45 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0        0  |  -221/83  -72/83  210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0    92/45  |        0     1/5    -1/5    -1/3     1/9   23/45 ]
[ 0  0  1  0  0  -182/45  |        0     4/5     1/5     1/3    -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |        0       0       0     1/3    -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |        0     1/5    -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0        1  |    45/83   -9/83  -36/83  -15/83    5/83   32/83 ]
```

### Paso 35. F2 ← F2 + (-92/45) · F6

Se anula la entrada 92/45 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0        0  |  -221/83  -72/83  210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0        0  |   -92/83   35/83   57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  -182/45  |        0     4/5     1/5     1/3    -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |        0       0       0     1/3    -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |        0     1/5    -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0        1  |    45/83   -9/83  -36/83  -15/83    5/83   32/83 ]
```

### Paso 36. F3 ← F3 + (182/45) · F6

Se anula la entrada -182/45 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0      0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0      0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0      0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0   -4/9  |        0       0        0     1/3    -1/9    -1/9 ]
[ 0  0  0  0  1  -1/15  |        0     1/5     -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0      1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 37. F4 ← F4 + (4/9) · F6

Se anula la entrada -4/9 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0      0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0      0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0      0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0      0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  -1/15  |        0     1/5     -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0      1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 38. F5 ← F5 + (1/15) · F6

Se anula la entrada -1/15 en la columna 6; se opera sobre la fila completa.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 39. [I | A⁻¹]: inversa obtenida

Las operaciones que convierten A en I convierten I en A⁻¹.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 40. x1 = (-221/83)·(155) + (-72/83)·(160) + (210/83)·(100) + (46/83)·(140) + (-43/83)·(215) + (7/83)·(175) = -26355/83

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 41. x2 = (-92/83)·(155) + (35/83)·(160) + (57/83)·(100) + (3/83)·(140) + (-1/83)·(215) + (-23/83)·(175) = -6780/83

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 42. x3 = (182/83)·(155) + (30/83)·(160) + (-129/83)·(100) + (-33/83)·(140) + (11/83)·(215) + (4/83)·(175) = 18555/83

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 43. x4 = (20/83)·(155) + (-4/83)·(160) + (-16/83)·(100) + (21/83)·(140) + (-7/83)·(215) + (5/83)·(175) = 3170/83

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 44. x5 = (3/83)·(155) + (16/83)·(160) + (-19/83)·(100) + (-1/83)·(140) + (28/83)·(215) + (-20/83)·(175) = 3505/83

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 45. x6 = (45/83)·(155) + (-9/83)·(160) + (-36/83)·(100) + (-15/83)·(140) + (5/83)·(215) + (32/83)·(175) = 6510/83

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

## Referencias

- [MIT OpenCourseWare · Eliminación con matrices](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/0903b4b404284cd14b66ecccea103fd4_MIT18_06SCF11_Ses1.2sum.pdf)
- [MIT OpenCourseWare · Multiplicación, Gauss-Jordan e inversa](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf)
- [MIT OpenCourseWare · AX = B y variables libres](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/solving-ax-b-row-reduced-form-r/)

Cálculo racional exacto respecto de los datos introducidos. Los decimales de presentación son aproximados.
