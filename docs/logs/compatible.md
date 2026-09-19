# TechChip · vector esperado

TechChip Matrix Studio · procedimiento reproducible

Variante didáctica con B = A·X esperado. Esta disponibilidad no es la de la guía. La guía contiene una inconsistencia: el vector esperado (15, 20, 25, 10, 15, 20) requiere B = (185, 200, 280, 150, 245, 195). No resuelve el B original (155, 160, 225, 140, 215, 175). Ambos casos se conservan por separado.

## 1. Sistema de entrada

```text
[ 2  1  3  1  2  1  |  185 ]
[ 1  3  2  2  1  2  |  200 ]
[ 3  2  4  1  3  2  |  280 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

## 2. Diagnóstico

- Estado: Solución única
- det(A) = -83
- rango(A) = 6; rango([A|B]) = 6

## 3. Interpretación

- Plan factible para el modelo continuo: todas las cantidades son no negativas y AX = B consume el 100 % de cada disponibilidad.
- X se expresa en miles de unidades; X·1000 se informa como cantidad continua, sin redondear a unidades enteras.
- La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

## 4. Solución y verificación

| Variable | Valor exacto | Aproximación |
|---|---:|---:|
| x1 | 15 | 15.000000 |
| x2 | 20 | 20.000000 |
| x3 | 25 | 25.000000 |
| x4 | 10 | 10.000000 |
| x5 | 15 | 15.000000 |
| x6 | 20 | 20.000000 |

Los tres métodos coinciden: sí.
Error máximo por componente: 0; criterio exigido: < 10⁻⁶.

Fila 1: (2)·(15) + (1)·(20) + (3)·(25) + (1)·(10) + (2)·(15) + (1)·(20) = 185; B1 = 185; |AX − B| = 0
Fila 2: (1)·(15) + (3)·(20) + (2)·(25) + (2)·(10) + (1)·(15) + (2)·(20) = 200; B2 = 200; |AX − B| = 0
Fila 3: (3)·(15) + (2)·(20) + (4)·(25) + (1)·(10) + (3)·(15) + (2)·(20) = 280; B3 = 280; |AX − B| = 0
Fila 4: (1)·(15) + (1)·(20) + (1)·(25) + (4)·(10) + (2)·(15) + (1)·(20) = 150; B4 = 150; |AX − B| = 0
Fila 5: (2)·(15) + (1)·(20) + (2)·(25) + (1)·(10) + (5)·(15) + (3)·(20) = 245; B5 = 245; |AX − B| = 0
Fila 6: (1)·(15) + (2)·(20) + (1)·(25) + (2)·(10) + (1)·(15) + (4)·(20) = 195; B6 = 195; |AX − B| = 0


## Procedimiento — Diagnóstico: determinante y rangos

### Paso 1. Matriz aumentada inicial

Punto de partida: [A | B]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

```text
[ 2  1  3  1  2  1  |  185 ]
[ 1  3  2  2  1  2  |  200 ]
[ 3  2  4  1  3  2  |  280 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 3  2  4  1  3  2  |  280 ]
[ 1  3  2  2  1  2  |  200 ]
[ 2  1  3  1  2  1  |  185 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

### Paso 3. F2 ← F2 + (-1/3) · F1

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2    4    1  3    2  |    280 ]
[ 0  7/3  2/3  5/3  0  4/3  |  320/3 ]
[ 2    1    3    1  2    1  |    185 ]
[ 1    1    1    4  2    1  |    150 ]
[ 2    1    2    1  5    3  |    245 ]
[ 1    2    1    2  1    4  |    195 ]
```

### Paso 4. F3 ← F3 + (-2/3) · F1

El multiplicador es −(2)/(3) = -2/3; así, 2 + (-2/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2    4    1  3     2  |    280 ]
[ 0   7/3  2/3  5/3  0   4/3  |  320/3 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |   -5/3 ]
[ 1     1    1    4  2     1  |    150 ]
[ 2     1    2    1  5     3  |    245 ]
[ 1     2    1    2  1     4  |    195 ]
```

### Paso 5. F4 ← F4 + (-1/3) · F1

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 2     1     2     1  5     3  |    245 ]
[ 1     2     1     2  1     4  |    195 ]
```

### Paso 6. F5 ← F5 + (-2/3) · F1

El multiplicador es −(2)/(3) = -2/3; así, 2 + (-2/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 1     2     1     2  1     4  |    195 ]
```

### Paso 7. F6 ← F6 + (-1/3) · F1

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 8. F3 ← F3 + (1/7) · F2

El multiplicador es −(-1/3)/(7/3) = 1/7; así, -1/3 + (1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0     0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 9. F4 ← F4 + (-1/7) · F2

El multiplicador es −(1/3)/(7/3) = -1/7; así, 1/3 + (-1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0     0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0     0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 10. F5 ← F5 + (1/7) · F2

El multiplicador es −(-1/3)/(7/3) = 1/7; así, -1/3 + (1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4     1  3     2  |    280 ]
[ 0  7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0  4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 11. F6 ← F6 + (-4/7) · F2

El multiplicador es −(4/3)/(7/3) = -4/7; así, 4/3 + (-4/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4     1  3     2  |    280 ]
[ 0  7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0    0  -5/7   5/7  0  18/7  |  285/7 ]
```

### Paso 12. F3 ↔ F6

Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 3    2     4     1  3     2  |    280 ]
[ 0  7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7   5/7  0  18/7  |  285/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
```

### Paso 13. F4 ← F4 + (-3/5) · F3

El multiplicador es −(-3/7)/(-5/7) = -3/5; así, -3/7 + (-3/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3     2  |    280 ]
[ 0  7/3   2/3  5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  285/7 ]
[ 0    0     0    3  1  -7/5  |     17 ]
[ 0    0  -4/7  4/7  3  13/7  |  515/7 ]
[ 0    0   3/7  4/7  0  -1/7  |   95/7 ]
```

### Paso 14. F5 ← F5 + (-4/5) · F3

El multiplicador es −(-4/7)/(-5/7) = -4/5; así, -4/7 + (-4/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3     2  |    280 ]
[ 0  7/3   2/3  5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  285/7 ]
[ 0    0     0    3  1  -7/5  |     17 ]
[ 0    0     0    0  3  -1/5  |     41 ]
[ 0    0   3/7  4/7  0  -1/7  |   95/7 ]
```

### Paso 15. F6 ← F6 + (3/5) · F3

El multiplicador es −(3/7)/(-5/7) = 3/5; así, 3/7 + (3/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3     2  |    280 ]
[ 0  7/3   2/3  5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  285/7 ]
[ 0    0     0    3  1  -7/5  |     17 ]
[ 0    0     0    0  3  -1/5  |     41 ]
[ 0    0     0    1  0   7/5  |     38 ]
```

### Paso 16. F6 ← F6 + (-1/3) · F4

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1     3      2  |    280 ]
[ 0  7/3   2/3  5/3     0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7     0   18/7  |  285/7 ]
[ 0    0     0    3     1   -7/5  |     17 ]
[ 0    0     0    0     3   -1/5  |     41 ]
[ 0    0     0    0  -1/3  28/15  |   97/3 ]
```

### Paso 17. F6 ← F6 + (1/9) · F5

El multiplicador es −(-1/3)/(3) = 1/9; así, -1/3 + (1/9)·(3) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 18. det(A) = -83

2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (3) · (7/3) · (-5/7) · (3) · (3) · (83/45) = -83.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```


## Procedimiento — Eliminación de Gauss

### Paso 1. Matriz aumentada inicial

Punto de partida: [A | B]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

```text
[ 2  1  3  1  2  1  |  185 ]
[ 1  3  2  2  1  2  |  200 ]
[ 3  2  4  1  3  2  |  280 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 3  2  4  1  3  2  |  280 ]
[ 1  3  2  2  1  2  |  200 ]
[ 2  1  3  1  2  1  |  185 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

### Paso 3. F2 ← F2 + (-1/3) · F1

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2    4    1  3    2  |    280 ]
[ 0  7/3  2/3  5/3  0  4/3  |  320/3 ]
[ 2    1    3    1  2    1  |    185 ]
[ 1    1    1    4  2    1  |    150 ]
[ 2    1    2    1  5    3  |    245 ]
[ 1    2    1    2  1    4  |    195 ]
```

### Paso 4. F3 ← F3 + (-2/3) · F1

El multiplicador es −(2)/(3) = -2/3; así, 2 + (-2/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2    4    1  3     2  |    280 ]
[ 0   7/3  2/3  5/3  0   4/3  |  320/3 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |   -5/3 ]
[ 1     1    1    4  2     1  |    150 ]
[ 2     1    2    1  5     3  |    245 ]
[ 1     2    1    2  1     4  |    195 ]
```

### Paso 5. F4 ← F4 + (-1/3) · F1

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 2     1     2     1  5     3  |    245 ]
[ 1     2     1     2  1     4  |    195 ]
```

### Paso 6. F5 ← F5 + (-2/3) · F1

El multiplicador es −(2)/(3) = -2/3; así, 2 + (-2/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 1     2     1     2  1     4  |    195 ]
```

### Paso 7. F6 ← F6 + (-1/3) · F1

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 8. F3 ← F3 + (1/7) · F2

El multiplicador es −(-1/3)/(7/3) = 1/7; así, -1/3 + (1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0     0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 9. F4 ← F4 + (-1/7) · F2

El multiplicador es −(1/3)/(7/3) = -1/7; así, 1/3 + (-1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3     2     4     1  3     2  |    280 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0     0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0     0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 10. F5 ← F5 + (1/7) · F2

El multiplicador es −(-1/3)/(7/3) = 1/7; así, -1/3 + (1/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4     1  3     2  |    280 ]
[ 0  7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0  4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 11. F6 ← F6 + (-4/7) · F2

El multiplicador es −(4/3)/(7/3) = -4/7; así, 4/3 + (-4/7)·(7/3) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4     1  3     2  |    280 ]
[ 0  7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0    0  -5/7   5/7  0  18/7  |  285/7 ]
```

### Paso 12. F3 ↔ F6

Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 3    2     4     1  3     2  |    280 ]
[ 0  7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7   5/7  0  18/7  |  285/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
```

### Paso 13. F4 ← F4 + (-3/5) · F3

El multiplicador es −(-3/7)/(-5/7) = -3/5; así, -3/7 + (-3/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3     2  |    280 ]
[ 0  7/3   2/3  5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  285/7 ]
[ 0    0     0    3  1  -7/5  |     17 ]
[ 0    0  -4/7  4/7  3  13/7  |  515/7 ]
[ 0    0   3/7  4/7  0  -1/7  |   95/7 ]
```

### Paso 14. F5 ← F5 + (-4/5) · F3

El multiplicador es −(-4/7)/(-5/7) = -4/5; así, -4/7 + (-4/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3     2  |    280 ]
[ 0  7/3   2/3  5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  285/7 ]
[ 0    0     0    3  1  -7/5  |     17 ]
[ 0    0     0    0  3  -1/5  |     41 ]
[ 0    0   3/7  4/7  0  -1/7  |   95/7 ]
```

### Paso 15. F6 ← F6 + (3/5) · F3

El multiplicador es −(3/7)/(-5/7) = 3/5; así, 3/7 + (3/5)·(-5/7) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3     2  |    280 ]
[ 0  7/3   2/3  5/3  0   4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0  18/7  |  285/7 ]
[ 0    0     0    3  1  -7/5  |     17 ]
[ 0    0     0    0  3  -1/5  |     41 ]
[ 0    0     0    1  0   7/5  |     38 ]
```

### Paso 16. F6 ← F6 + (-1/3) · F4

El multiplicador es −(1)/(3) = -1/3; así, 1 + (-1/3)·(3) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1     3      2  |    280 ]
[ 0  7/3   2/3  5/3     0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7     0   18/7  |  285/7 ]
[ 0    0     0    3     1   -7/5  |     17 ]
[ 0    0     0    0     3   -1/5  |     41 ]
[ 0    0     0    0  -1/3  28/15  |   97/3 ]
```

### Paso 17. F6 ← F6 + (1/9) · F5

El multiplicador es −(-1/3)/(3) = 1/9; así, -1/3 + (1/9)·(3) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 18. det(A) = -83

2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (3) · (7/3) · (-5/7) · (3) · (3) · (83/45) = -83.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 19. Matriz triangular superior U

La eliminación terminó: debajo de cada pivote hay ceros. Ahora se resuelve U·X = C desde la última ecuación hacia la primera, porque cada fila solo depende de variables ya conocidas.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 20. x6 = (332/9 − (0)) / (83/45) = 20

En la fila 6 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x6. El valor se conserva como fracción exacta.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 21. x5 = (41 − ((-1/5)·(20))) / (3) = 15

En la fila 5 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x5. El valor se conserva como fracción exacta.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 22. x4 = (17 − ((1)·(15) + (-7/5)·(20))) / (3) = 10

En la fila 4 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x4. El valor se conserva como fracción exacta.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 23. x3 = (285/7 − ((5/7)·(10) + (0)·(15) + (18/7)·(20))) / (-5/7) = 25

En la fila 3 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x3. El valor se conserva como fracción exacta.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 24. x2 = (320/3 − ((2/3)·(25) + (5/3)·(10) + (0)·(15) + (4/3)·(20))) / (7/3) = 20

En la fila 2 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x2. El valor se conserva como fracción exacta.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```

### Paso 25. x1 = (280 − ((2)·(20) + (4)·(25) + (1)·(10) + (3)·(15) + (2)·(20))) / (3) = 15

En la fila 1 se pasan al lado derecho los términos ya conocidos y se divide entre el coeficiente de x1. El valor se conserva como fracción exacta.

```text
[ 3    2     4    1  3      2  |    280 ]
[ 0  7/3   2/3  5/3  0    4/3  |  320/3 ]
[ 0    0  -5/7  5/7  0   18/7  |  285/7 ]
[ 0    0     0    3  1   -7/5  |     17 ]
[ 0    0     0    0  3   -1/5  |     41 ]
[ 0    0     0    0  0  83/45  |  332/9 ]
```


## Procedimiento — Gauss-Jordan

### Paso 1. Matriz aumentada inicial

Punto de partida: [A | B]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

```text
[ 2  1  3  1  2  1  |  185 ]
[ 1  3  2  2  1  2  |  200 ]
[ 3  2  4  1  3  2  |  280 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 3  2  4  1  3  2  |  280 ]
[ 1  3  2  2  1  2  |  200 ]
[ 2  1  3  1  2  1  |  185 ]
[ 1  1  1  4  2  1  |  150 ]
[ 2  1  2  1  5  3  |  245 ]
[ 1  2  1  2  1  4  |  195 ]
```

### Paso 3. F1 ← (1/3) · F1

Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  280/3 ]
[ 1    3    2    2  1    2  |    200 ]
[ 2    1    3    1  2    1  |    185 ]
[ 1    1    1    4  2    1  |    150 ]
[ 2    1    2    1  5    3  |    245 ]
[ 1    2    1    2  1    4  |    195 ]
```

### Paso 4. F2 ← F2 + (-1) · F1

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  280/3 ]
[ 0  7/3  2/3  5/3  0  4/3  |  320/3 ]
[ 2    1    3    1  2    1  |    185 ]
[ 1    1    1    4  2    1  |    150 ]
[ 2    1    2    1  5    3  |    245 ]
[ 1    2    1    2  1    4  |    195 ]
```

### Paso 5. F3 ← F3 + (-2) · F1

El multiplicador es −(2)/(1) = -2; así, 2 + (-2)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3  4/3  1/3  1   2/3  |  280/3 ]
[ 0   7/3  2/3  5/3  0   4/3  |  320/3 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |   -5/3 ]
[ 1     1    1    4  2     1  |    150 ]
[ 2     1    2    1  5     3  |    245 ]
[ 1     2    1    2  1     4  |    195 ]
```

### Paso 6. F4 ← F4 + (-1) · F1

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  280/3 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 2     1     2     1  5     3  |    245 ]
[ 1     2     1     2  1     4  |    195 ]
```

### Paso 7. F5 ← F5 + (-2) · F1

El multiplicador es −(2)/(1) = -2; así, 2 + (-2)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  280/3 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 1     2     1     2  1     4  |    195 ]
```

### Paso 8. F6 ← F6 + (-1) · F1

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  280/3 ]
[ 0   7/3   2/3   5/3  0   4/3  |  320/3 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 9. F2 ← (3/7) · F2

Se divide toda la fila entre el pivote 7/3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  280/3 ]
[ 0     1   2/7   5/7  0   4/7  |  320/7 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 10. F1 ← F1 + (-2/3) · F2

El multiplicador es −(2/3)/(1) = -2/3; así, 2/3 + (-2/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1     0   8/7  -1/7  1   2/7  |  440/7 ]
[ 0     1   2/7   5/7  0   4/7  |  320/7 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |   -5/3 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 11. F3 ← F3 + (1/3) · F2

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1     0   8/7  -1/7  1   2/7  |  440/7 ]
[ 0     1   2/7   5/7  0   4/7  |  320/7 ]
[ 0     0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  170/3 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 12. F4 ← F4 + (-1/3) · F2

El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1     0   8/7  -1/7  1   2/7  |  440/7 ]
[ 0     1   2/7   5/7  0   4/7  |  320/7 ]
[ 0     0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0     0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  175/3 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 13. F5 ← F5 + (1/3) · F2

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1    0   8/7  -1/7  1   2/7  |  440/7 ]
[ 0    1   2/7   5/7  0   4/7  |  320/7 ]
[ 0    0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0    0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0    0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0  4/3  -1/3   5/3  0  10/3  |  305/3 ]
```

### Paso 14. F6 ← F6 + (-4/3) · F2

El multiplicador es −(4/3)/(1) = -4/3; así, 4/3 + (-4/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0   8/7  -1/7  1   2/7  |  440/7 ]
[ 0  1   2/7   5/7  0   4/7  |  320/7 ]
[ 0  0   3/7   4/7  0  -1/7  |   95/7 ]
[ 0  0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0  0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0  0  -5/7   5/7  0  18/7  |  285/7 ]
```

### Paso 15. F3 ↔ F6

Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 1  0   8/7  -1/7  1   2/7  |  440/7 ]
[ 0  1   2/7   5/7  0   4/7  |  320/7 ]
[ 0  0  -5/7   5/7  0  18/7  |  285/7 ]
[ 0  0  -3/7  24/7  1   1/7  |  290/7 ]
[ 0  0  -4/7   4/7  3  13/7  |  515/7 ]
[ 0  0   3/7   4/7  0  -1/7  |   95/7 ]
```

### Paso 16. F3 ← (-7/5) · F3

Se divide toda la fila entre el pivote -5/7, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0   8/7  -1/7  1    2/7  |  440/7 ]
[ 0  1   2/7   5/7  0    4/7  |  320/7 ]
[ 0  0     1    -1  0  -18/5  |    -57 ]
[ 0  0  -3/7  24/7  1    1/7  |  290/7 ]
[ 0  0  -4/7   4/7  3   13/7  |  515/7 ]
[ 0  0   3/7   4/7  0   -1/7  |   95/7 ]
```

### Paso 17. F1 ← F1 + (-8/7) · F3

El multiplicador es −(8/7)/(1) = -8/7; así, 8/7 + (-8/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0     0     1  1   22/5  |    128 ]
[ 0  1   2/7   5/7  0    4/7  |  320/7 ]
[ 0  0     1    -1  0  -18/5  |    -57 ]
[ 0  0  -3/7  24/7  1    1/7  |  290/7 ]
[ 0  0  -4/7   4/7  3   13/7  |  515/7 ]
[ 0  0   3/7   4/7  0   -1/7  |   95/7 ]
```

### Paso 18. F2 ← F2 + (-2/7) · F3

El multiplicador es −(2/7)/(1) = -2/7; así, 2/7 + (-2/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0     0     1  1   22/5  |    128 ]
[ 0  1     0     1  0    8/5  |     62 ]
[ 0  0     1    -1  0  -18/5  |    -57 ]
[ 0  0  -3/7  24/7  1    1/7  |  290/7 ]
[ 0  0  -4/7   4/7  3   13/7  |  515/7 ]
[ 0  0   3/7   4/7  0   -1/7  |   95/7 ]
```

### Paso 19. F4 ← F4 + (3/7) · F3

El multiplicador es −(-3/7)/(1) = 3/7; así, -3/7 + (3/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0     0    1  1   22/5  |    128 ]
[ 0  1     0    1  0    8/5  |     62 ]
[ 0  0     1   -1  0  -18/5  |    -57 ]
[ 0  0     0    3  1   -7/5  |     17 ]
[ 0  0  -4/7  4/7  3   13/7  |  515/7 ]
[ 0  0   3/7  4/7  0   -1/7  |   95/7 ]
```

### Paso 20. F5 ← F5 + (4/7) · F3

El multiplicador es −(-4/7)/(1) = 4/7; así, -4/7 + (4/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0    0    1  1   22/5  |   128 ]
[ 0  1    0    1  0    8/5  |    62 ]
[ 0  0    1   -1  0  -18/5  |   -57 ]
[ 0  0    0    3  1   -7/5  |    17 ]
[ 0  0    0    0  3   -1/5  |    41 ]
[ 0  0  3/7  4/7  0   -1/7  |  95/7 ]
```

### Paso 21. F6 ← F6 + (-3/7) · F3

El multiplicador es −(3/7)/(1) = -3/7; así, 3/7 + (-3/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0   1  1   22/5  |  128 ]
[ 0  1  0   1  0    8/5  |   62 ]
[ 0  0  1  -1  0  -18/5  |  -57 ]
[ 0  0  0   3  1   -7/5  |   17 ]
[ 0  0  0   0  3   -1/5  |   41 ]
[ 0  0  0   1  0    7/5  |   38 ]
```

### Paso 22. F4 ← (1/3) · F4

Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0  0   1    1   22/5  |   128 ]
[ 0  1  0   1    0    8/5  |    62 ]
[ 0  0  1  -1    0  -18/5  |   -57 ]
[ 0  0  0   1  1/3  -7/15  |  17/3 ]
[ 0  0  0   0    3   -1/5  |    41 ]
[ 0  0  0   1    0    7/5  |    38 ]
```

### Paso 23. F1 ← F1 + (-1) · F4

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0   0  2/3  73/15  |  367/3 ]
[ 0  1  0   1    0    8/5  |     62 ]
[ 0  0  1  -1    0  -18/5  |    -57 ]
[ 0  0  0   1  1/3  -7/15  |   17/3 ]
[ 0  0  0   0    3   -1/5  |     41 ]
[ 0  0  0   1    0    7/5  |     38 ]
```

### Paso 24. F2 ← F2 + (-1) · F4

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0   0   2/3  73/15  |  367/3 ]
[ 0  1  0   0  -1/3  31/15  |  169/3 ]
[ 0  0  1  -1     0  -18/5  |    -57 ]
[ 0  0  0   1   1/3  -7/15  |   17/3 ]
[ 0  0  0   0     3   -1/5  |     41 ]
[ 0  0  0   1     0    7/5  |     38 ]
```

### Paso 25. F3 ← F3 + (1) · F4

El multiplicador es −(-1)/(1) = 1; así, -1 + (1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0   2/3   73/15  |   367/3 ]
[ 0  1  0  0  -1/3   31/15  |   169/3 ]
[ 0  0  1  0   1/3  -61/15  |  -154/3 ]
[ 0  0  0  1   1/3   -7/15  |    17/3 ]
[ 0  0  0  0     3    -1/5  |      41 ]
[ 0  0  0  1     0     7/5  |      38 ]
```

### Paso 26. F6 ← F6 + (-1) · F4

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0   2/3   73/15  |   367/3 ]
[ 0  1  0  0  -1/3   31/15  |   169/3 ]
[ 0  0  1  0   1/3  -61/15  |  -154/3 ]
[ 0  0  0  1   1/3   -7/15  |    17/3 ]
[ 0  0  0  0     3    -1/5  |      41 ]
[ 0  0  0  0  -1/3   28/15  |    97/3 ]
```

### Paso 27. F5 ← (1/3) · F5

Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0  0  0   2/3   73/15  |   367/3 ]
[ 0  1  0  0  -1/3   31/15  |   169/3 ]
[ 0  0  1  0   1/3  -61/15  |  -154/3 ]
[ 0  0  0  1   1/3   -7/15  |    17/3 ]
[ 0  0  0  0     1   -1/15  |    41/3 ]
[ 0  0  0  0  -1/3   28/15  |    97/3 ]
```

### Paso 28. F1 ← F1 + (-2/3) · F5

El multiplicador es −(2/3)/(1) = -2/3; así, 2/3 + (-2/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0  221/45  |  1019/9 ]
[ 0  1  0  0  -1/3   31/15  |   169/3 ]
[ 0  0  1  0   1/3  -61/15  |  -154/3 ]
[ 0  0  0  1   1/3   -7/15  |    17/3 ]
[ 0  0  0  0     1   -1/15  |    41/3 ]
[ 0  0  0  0  -1/3   28/15  |    97/3 ]
```

### Paso 29. F2 ← F2 + (1/3) · F5

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0  221/45  |  1019/9 ]
[ 0  1  0  0     0   92/45  |   548/9 ]
[ 0  0  1  0   1/3  -61/15  |  -154/3 ]
[ 0  0  0  1   1/3   -7/15  |    17/3 ]
[ 0  0  0  0     1   -1/15  |    41/3 ]
[ 0  0  0  0  -1/3   28/15  |    97/3 ]
```

### Paso 30. F3 ← F3 + (-1/3) · F5

El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0   221/45  |  1019/9 ]
[ 0  1  0  0     0    92/45  |   548/9 ]
[ 0  0  1  0     0  -182/45  |  -503/9 ]
[ 0  0  0  1   1/3    -7/15  |    17/3 ]
[ 0  0  0  0     1    -1/15  |    41/3 ]
[ 0  0  0  0  -1/3    28/15  |    97/3 ]
```

### Paso 31. F4 ← F4 + (-1/3) · F5

El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0   221/45  |  1019/9 ]
[ 0  1  0  0     0    92/45  |   548/9 ]
[ 0  0  1  0     0  -182/45  |  -503/9 ]
[ 0  0  0  1     0     -4/9  |    10/9 ]
[ 0  0  0  0     1    -1/15  |    41/3 ]
[ 0  0  0  0  -1/3    28/15  |    97/3 ]
```

### Paso 32. F6 ← F6 + (1/3) · F5

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0   221/45  |  1019/9 ]
[ 0  1  0  0  0    92/45  |   548/9 ]
[ 0  0  1  0  0  -182/45  |  -503/9 ]
[ 0  0  0  1  0     -4/9  |    10/9 ]
[ 0  0  0  0  1    -1/15  |    41/3 ]
[ 0  0  0  0  0    83/45  |   332/9 ]
```

### Paso 33. F6 ← (45/83) · F6

Se divide toda la fila entre el pivote 83/45, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0  0  0  0   221/45  |  1019/9 ]
[ 0  1  0  0  0    92/45  |   548/9 ]
[ 0  0  1  0  0  -182/45  |  -503/9 ]
[ 0  0  0  1  0     -4/9  |    10/9 ]
[ 0  0  0  0  1    -1/15  |    41/3 ]
[ 0  0  0  0  0        1  |      20 ]
```

### Paso 34. F1 ← F1 + (-221/45) · F6

El multiplicador es −(221/45)/(1) = -221/45; así, 221/45 + (-221/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0        0  |      15 ]
[ 0  1  0  0  0    92/45  |   548/9 ]
[ 0  0  1  0  0  -182/45  |  -503/9 ]
[ 0  0  0  1  0     -4/9  |    10/9 ]
[ 0  0  0  0  1    -1/15  |    41/3 ]
[ 0  0  0  0  0        1  |      20 ]
```

### Paso 35. F2 ← F2 + (-92/45) · F6

El multiplicador es −(92/45)/(1) = -92/45; así, 92/45 + (-92/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0        0  |      15 ]
[ 0  1  0  0  0        0  |      20 ]
[ 0  0  1  0  0  -182/45  |  -503/9 ]
[ 0  0  0  1  0     -4/9  |    10/9 ]
[ 0  0  0  0  1    -1/15  |    41/3 ]
[ 0  0  0  0  0        1  |      20 ]
```

### Paso 36. F3 ← F3 + (182/45) · F6

El multiplicador es −(-182/45)/(1) = 182/45; así, -182/45 + (182/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0      0  |    15 ]
[ 0  1  0  0  0      0  |    20 ]
[ 0  0  1  0  0      0  |    25 ]
[ 0  0  0  1  0   -4/9  |  10/9 ]
[ 0  0  0  0  1  -1/15  |  41/3 ]
[ 0  0  0  0  0      1  |    20 ]
```

### Paso 37. F4 ← F4 + (4/9) · F6

El multiplicador es −(-4/9)/(1) = 4/9; así, -4/9 + (4/9)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0      0  |    15 ]
[ 0  1  0  0  0      0  |    20 ]
[ 0  0  1  0  0      0  |    25 ]
[ 0  0  0  1  0      0  |    10 ]
[ 0  0  0  0  1  -1/15  |  41/3 ]
[ 0  0  0  0  0      1  |    20 ]
```

### Paso 38. F5 ← F5 + (1/15) · F6

El multiplicador es −(-1/15)/(1) = 1/15; así, -1/15 + (1/15)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0  0  |  15 ]
[ 0  1  0  0  0  0  |  20 ]
[ 0  0  1  0  0  0  |  25 ]
[ 0  0  0  1  0  0  |  10 ]
[ 0  0  0  0  1  0  |  15 ]
[ 0  0  0  0  0  1  |  20 ]
```

### Paso 39. [I | X]: lectura directa de la solución

El bloque izquierdo es la identidad: la fila i representa 1·xᵢ = Xᵢ. Por eso la última columna se lee directamente, sin sustitución hacia atrás.

```text
[ 1  0  0  0  0  0  |  15 ]
[ 0  1  0  0  0  0  |  20 ]
[ 0  0  1  0  0  0  |  25 ]
[ 0  0  0  1  0  0  |  10 ]
[ 0  0  0  0  1  0  |  15 ]
[ 0  0  0  0  0  1  |  20 ]
```


## Procedimiento — Matriz inversa

### Paso 1. Matriz aumentada inicial

Punto de partida: [A | I]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

```text
[ 2  1  3  1  2  1  |  1  0  0  0  0  0 ]
[ 1  3  2  2  1  2  |  0  1  0  0  0  0 ]
[ 3  2  4  1  3  2  |  0  0  1  0  0  0 ]
[ 1  1  1  4  2  1  |  0  0  0  1  0  0 ]
[ 2  1  2  1  5  3  |  0  0  0  0  1  0 ]
[ 1  2  1  2  1  4  |  0  0  0  0  0  1 ]
```

### Paso 2. F1 ↔ F3

Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 3  2  4  1  3  2  |  0  0  1  0  0  0 ]
[ 1  3  2  2  1  2  |  0  1  0  0  0  0 ]
[ 2  1  3  1  2  1  |  1  0  0  0  0  0 ]
[ 1  1  1  4  2  1  |  0  0  0  1  0  0 ]
[ 2  1  2  1  5  3  |  0  0  0  0  1  0 ]
[ 1  2  1  2  1  4  |  0  0  0  0  0  1 ]
```

### Paso 3. F1 ← (1/3) · F1

Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  0  0  1/3  0  0  0 ]
[ 1    3    2    2  1    2  |  0  1    0  0  0  0 ]
[ 2    1    3    1  2    1  |  1  0    0  0  0  0 ]
[ 1    1    1    4  2    1  |  0  0    0  1  0  0 ]
[ 2    1    2    1  5    3  |  0  0    0  0  1  0 ]
[ 1    2    1    2  1    4  |  0  0    0  0  0  1 ]
```

### Paso 4. F2 ← F2 + (-1) · F1

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  2/3  4/3  1/3  1  2/3  |  0  0   1/3  0  0  0 ]
[ 0  7/3  2/3  5/3  0  4/3  |  0  1  -1/3  0  0  0 ]
[ 2    1    3    1  2    1  |  1  0     0  0  0  0 ]
[ 1    1    1    4  2    1  |  0  0     0  1  0  0 ]
[ 2    1    2    1  5    3  |  0  0     0  0  1  0 ]
[ 1    2    1    2  1    4  |  0  0     0  0  0  1 ]
```

### Paso 5. F3 ← F3 + (-2) · F1

El multiplicador es −(2)/(1) = -2; así, 2 + (-2)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3  4/3  1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3  2/3  5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3  1/3  1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 1     1    1    4  2     1  |  0  0     0  1  0  0 ]
[ 2     1    2    1  5     3  |  0  0     0  0  1  0 ]
[ 1     2    1    2  1     4  |  0  0     0  0  0  1 ]
```

### Paso 6. F4 ← F4 + (-1) · F1

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3   2/3   5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0  0  -1/3  1  0  0 ]
[ 2     1     2     1  5     3  |  0  0     0  0  1  0 ]
[ 1     2     1     2  1     4  |  0  0     0  0  0  1 ]
```

### Paso 7. F5 ← F5 + (-2) · F1

El multiplicador es −(2)/(1) = -2; así, 2 + (-2)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3   2/3   5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0  0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0  0  -2/3  0  1  0 ]
[ 1     2     1     2  1     4  |  0  0     0  0  0  1 ]
```

### Paso 8. F6 ← F6 + (-1) · F1

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0  0   1/3  0  0  0 ]
[ 0   7/3   2/3   5/3  0   4/3  |  0  1  -1/3  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1  0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0  0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0  0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0  0  -1/3  0  0  1 ]
```

### Paso 9. F2 ← (3/7) · F2

Se divide toda la fila entre el pivote 7/3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1   2/3   4/3   1/3  1   2/3  |  0    0   1/3  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0  3/7  -1/7  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1    0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0    0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0    0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0    0  -1/3  0  0  1 ]
```

### Paso 10. F1 ← F1 + (-2/3) · F2

El multiplicador es −(2/3)/(1) = -2/3; así, 2/3 + (-2/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1     0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0  -1/3   1/3   1/3  0  -1/3  |  1     0  -2/3  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0     0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0     0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 11. F3 ← F3 + (1/3) · F2

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1     0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0     0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0   1/3  -1/3  11/3  1   1/3  |  0     0  -1/3  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0     0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 12. F4 ← F4 + (-1/3) · F2

El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1     0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0     1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0     0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0     0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0  -1/3  -2/3   1/3  3   5/3  |  0     0  -2/3  0  1  0 ]
[ 0   4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 13. F5 ← F5 + (1/3) · F2

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1    0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0    1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0    0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0    0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0    0  -4/7   4/7  3  13/7  |  0   1/7  -5/7  0  1  0 ]
[ 0  4/3  -1/3   5/3  0  10/3  |  0     0  -1/3  0  0  1 ]
```

### Paso 14. F6 ← F6 + (-4/3) · F2

El multiplicador es −(4/3)/(1) = -4/3; así, 4/3 + (-4/3)·(1) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0  1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0  0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
[ 0  0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0  0  -4/7   4/7  3  13/7  |  0   1/7  -5/7  0  1  0 ]
[ 0  0  -5/7   5/7  0  18/7  |  0  -4/7  -1/7  0  0  1 ]
```

### Paso 15. F3 ↔ F6

Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 1  0   8/7  -1/7  1   2/7  |  0  -2/7   3/7  0  0  0 ]
[ 0  1   2/7   5/7  0   4/7  |  0   3/7  -1/7  0  0  0 ]
[ 0  0  -5/7   5/7  0  18/7  |  0  -4/7  -1/7  0  0  1 ]
[ 0  0  -3/7  24/7  1   1/7  |  0  -1/7  -2/7  1  0  0 ]
[ 0  0  -4/7   4/7  3  13/7  |  0   1/7  -5/7  0  1  0 ]
[ 0  0   3/7   4/7  0  -1/7  |  1   1/7  -5/7  0  0  0 ]
```

### Paso 16. F3 ← (-7/5) · F3

Se divide toda la fila entre el pivote -5/7, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0   8/7  -1/7  1    2/7  |  0  -2/7   3/7  0  0     0 ]
[ 0  1   2/7   5/7  0    4/7  |  0   3/7  -1/7  0  0     0 ]
[ 0  0     1    -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  -3/7  24/7  1    1/7  |  0  -1/7  -2/7  1  0     0 ]
[ 0  0  -4/7   4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7   4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 17. F1 ← F1 + (-8/7) · F3

El multiplicador es −(8/7)/(1) = -8/7; así, 8/7 + (-8/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0     0     1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1   2/7   5/7  0    4/7  |  0   3/7  -1/7  0  0     0 ]
[ 0  0     1    -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  -3/7  24/7  1    1/7  |  0  -1/7  -2/7  1  0     0 ]
[ 0  0  -4/7   4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7   4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 18. F2 ← F2 + (-2/7) · F3

El multiplicador es −(2/7)/(1) = -2/7; así, 2/7 + (-2/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0     0     1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1     0     1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0     1    -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  -3/7  24/7  1    1/7  |  0  -1/7  -2/7  1  0     0 ]
[ 0  0  -4/7   4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7   4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 19. F4 ← F4 + (3/7) · F3

El multiplicador es −(-3/7)/(1) = 3/7; así, -3/7 + (3/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0     0    1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1     0    1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0     1   -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0     0    3  1   -7/5  |  0   1/5  -1/5  1  0  -3/5 ]
[ 0  0  -4/7  4/7  3   13/7  |  0   1/7  -5/7  0  1     0 ]
[ 0  0   3/7  4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 20. F5 ← F5 + (4/7) · F3

El multiplicador es −(-4/7)/(1) = 4/7; así, -4/7 + (4/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0    0    1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1    0    1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0    1   -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0    0    3  1   -7/5  |  0   1/5  -1/5  1  0  -3/5 ]
[ 0  0    0    0  3   -1/5  |  0   3/5  -3/5  0  1  -4/5 ]
[ 0  0  3/7  4/7  0   -1/7  |  1   1/7  -5/7  0  0     0 ]
```

### Paso 21. F6 ← F6 + (-3/7) · F3

El multiplicador es −(3/7)/(1) = -3/7; así, 3/7 + (-3/7)·(1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0   1  1   22/5  |  0  -6/5   1/5  0  0   8/5 ]
[ 0  1  0   1  0    8/5  |  0   1/5  -1/5  0  0   2/5 ]
[ 0  0  1  -1  0  -18/5  |  0   4/5   1/5  0  0  -7/5 ]
[ 0  0  0   3  1   -7/5  |  0   1/5  -1/5  1  0  -3/5 ]
[ 0  0  0   0  3   -1/5  |  0   3/5  -3/5  0  1  -4/5 ]
[ 0  0  0   1  0    7/5  |  1  -1/5  -4/5  0  0   3/5 ]
```

### Paso 22. F4 ← (1/3) · F4

Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0  0   1    1   22/5  |  0  -6/5    1/5    0  0   8/5 ]
[ 0  1  0   1    0    8/5  |  0   1/5   -1/5    0  0   2/5 ]
[ 0  0  1  -1    0  -18/5  |  0   4/5    1/5    0  0  -7/5 ]
[ 0  0  0   1  1/3  -7/15  |  0  1/15  -1/15  1/3  0  -1/5 ]
[ 0  0  0   0    3   -1/5  |  0   3/5   -3/5    0  1  -4/5 ]
[ 0  0  0   1    0    7/5  |  1  -1/5   -4/5    0  0   3/5 ]
```

### Paso 23. F1 ← F1 + (-1) · F4

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0   0  2/3  73/15  |  0  -19/15   4/15  -1/3  0   9/5 ]
[ 0  1  0   1    0    8/5  |  0     1/5   -1/5     0  0   2/5 ]
[ 0  0  1  -1    0  -18/5  |  0     4/5    1/5     0  0  -7/5 ]
[ 0  0  0   1  1/3  -7/15  |  0    1/15  -1/15   1/3  0  -1/5 ]
[ 0  0  0   0    3   -1/5  |  0     3/5   -3/5     0  1  -4/5 ]
[ 0  0  0   1    0    7/5  |  1    -1/5   -4/5     0  0   3/5 ]
```

### Paso 24. F2 ← F2 + (-1) · F4

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0   0   2/3  73/15  |  0  -19/15   4/15  -1/3  0   9/5 ]
[ 0  1  0   0  -1/3  31/15  |  0    2/15  -2/15  -1/3  0   3/5 ]
[ 0  0  1  -1     0  -18/5  |  0     4/5    1/5     0  0  -7/5 ]
[ 0  0  0   1   1/3  -7/15  |  0    1/15  -1/15   1/3  0  -1/5 ]
[ 0  0  0   0     3   -1/5  |  0     3/5   -3/5     0  1  -4/5 ]
[ 0  0  0   1     0    7/5  |  1    -1/5   -4/5     0  0   3/5 ]
```

### Paso 25. F3 ← F3 + (1) · F4

El multiplicador es −(-1)/(1) = 1; así, -1 + (1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0   2/3   73/15  |  0  -19/15   4/15  -1/3  0   9/5 ]
[ 0  1  0  0  -1/3   31/15  |  0    2/15  -2/15  -1/3  0   3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0   13/15   2/15   1/3  0  -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0    1/15  -1/15   1/3  0  -1/5 ]
[ 0  0  0  0     3    -1/5  |  0     3/5   -3/5     0  1  -4/5 ]
[ 0  0  0  1     0     7/5  |  1    -1/5   -4/5     0  0   3/5 ]
```

### Paso 26. F6 ← F6 + (-1) · F4

El multiplicador es −(1)/(1) = -1; así, 1 + (-1)·(1) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0   2/3   73/15  |  0  -19/15    4/15  -1/3  0   9/5 ]
[ 0  1  0  0  -1/3   31/15  |  0    2/15   -2/15  -1/3  0   3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0   13/15    2/15   1/3  0  -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0    1/15   -1/15   1/3  0  -1/5 ]
[ 0  0  0  0     3    -1/5  |  0     3/5    -3/5     0  1  -4/5 ]
[ 0  0  0  0  -1/3   28/15  |  1   -4/15  -11/15  -1/3  0   4/5 ]
```

### Paso 27. F5 ← (1/3) · F5

Se divide toda la fila entre el pivote 3, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0  0  0   2/3   73/15  |  0  -19/15    4/15  -1/3    0    9/5 ]
[ 0  1  0  0  -1/3   31/15  |  0    2/15   -2/15  -1/3    0    3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0   13/15    2/15   1/3    0   -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0    1/15   -1/15   1/3    0   -1/5 ]
[ 0  0  0  0     1   -1/15  |  0     1/5    -1/5     0  1/3  -4/15 ]
[ 0  0  0  0  -1/3   28/15  |  1   -4/15  -11/15  -1/3    0    4/5 ]
```

### Paso 28. F1 ← F1 + (-2/3) · F5

El multiplicador es −(2/3)/(1) = -2/3; así, 2/3 + (-2/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0  221/45  |  0   -7/5     2/5  -1/3  -2/9  89/45 ]
[ 0  1  0  0  -1/3   31/15  |  0   2/15   -2/15  -1/3     0    3/5 ]
[ 0  0  1  0   1/3  -61/15  |  0  13/15    2/15   1/3     0   -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0   1/15   -1/15   1/3     0   -1/5 ]
[ 0  0  0  0     1   -1/15  |  0    1/5    -1/5     0   1/3  -4/15 ]
[ 0  0  0  0  -1/3   28/15  |  1  -4/15  -11/15  -1/3     0    4/5 ]
```

### Paso 29. F2 ← F2 + (1/3) · F5

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0  221/45  |  0   -7/5     2/5  -1/3  -2/9  89/45 ]
[ 0  1  0  0     0   92/45  |  0    1/5    -1/5  -1/3   1/9  23/45 ]
[ 0  0  1  0   1/3  -61/15  |  0  13/15    2/15   1/3     0   -8/5 ]
[ 0  0  0  1   1/3   -7/15  |  0   1/15   -1/15   1/3     0   -1/5 ]
[ 0  0  0  0     1   -1/15  |  0    1/5    -1/5     0   1/3  -4/15 ]
[ 0  0  0  0  -1/3   28/15  |  1  -4/15  -11/15  -1/3     0    4/5 ]
```

### Paso 30. F3 ← F3 + (-1/3) · F5

El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0   221/45  |  0   -7/5     2/5  -1/3  -2/9   89/45 ]
[ 0  1  0  0     0    92/45  |  0    1/5    -1/5  -1/3   1/9   23/45 ]
[ 0  0  1  0     0  -182/45  |  0    4/5     1/5   1/3  -1/9  -68/45 ]
[ 0  0  0  1   1/3    -7/15  |  0   1/15   -1/15   1/3     0    -1/5 ]
[ 0  0  0  0     1    -1/15  |  0    1/5    -1/5     0   1/3   -4/15 ]
[ 0  0  0  0  -1/3    28/15  |  1  -4/15  -11/15  -1/3     0     4/5 ]
```

### Paso 31. F4 ← F4 + (-1/3) · F5

El multiplicador es −(1/3)/(1) = -1/3; así, 1/3 + (-1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0     0   221/45  |  0   -7/5     2/5  -1/3  -2/9   89/45 ]
[ 0  1  0  0     0    92/45  |  0    1/5    -1/5  -1/3   1/9   23/45 ]
[ 0  0  1  0     0  -182/45  |  0    4/5     1/5   1/3  -1/9  -68/45 ]
[ 0  0  0  1     0     -4/9  |  0      0       0   1/3  -1/9    -1/9 ]
[ 0  0  0  0     1    -1/15  |  0    1/5    -1/5     0   1/3   -4/15 ]
[ 0  0  0  0  -1/3    28/15  |  1  -4/15  -11/15  -1/3     0     4/5 ]
```

### Paso 32. F6 ← F6 + (1/3) · F5

El multiplicador es −(-1/3)/(1) = 1/3; así, -1/3 + (1/3)·(1) = 0 en la columna 5. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0   221/45  |  0  -7/5   2/5  -1/3  -2/9   89/45 ]
[ 0  1  0  0  0    92/45  |  0   1/5  -1/5  -1/3   1/9   23/45 ]
[ 0  0  1  0  0  -182/45  |  0   4/5   1/5   1/3  -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |  0     0     0   1/3  -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |  0   1/5  -1/5     0   1/3   -4/15 ]
[ 0  0  0  0  0    83/45  |  1  -1/5  -4/5  -1/3   1/9   32/45 ]
```

### Paso 33. F6 ← (45/83) · F6

Se divide toda la fila entre el pivote 83/45, por eso el pivote se convierte en 1. Multiplicar una ecuación por un número distinto de cero produce una ecuación equivalente.

```text
[ 1  0  0  0  0   221/45  |      0   -7/5     2/5    -1/3  -2/9   89/45 ]
[ 0  1  0  0  0    92/45  |      0    1/5    -1/5    -1/3   1/9   23/45 ]
[ 0  0  1  0  0  -182/45  |      0    4/5     1/5     1/3  -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |      0      0       0     1/3  -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |      0    1/5    -1/5       0   1/3   -4/15 ]
[ 0  0  0  0  0        1  |  45/83  -9/83  -36/83  -15/83  5/83   32/83 ]
```

### Paso 34. F1 ← F1 + (-221/45) · F6

El multiplicador es −(221/45)/(1) = -221/45; así, 221/45 + (-221/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0        0  |  -221/83  -72/83  210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0    92/45  |        0     1/5    -1/5    -1/3     1/9   23/45 ]
[ 0  0  1  0  0  -182/45  |        0     4/5     1/5     1/3    -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |        0       0       0     1/3    -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |        0     1/5    -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0        1  |    45/83   -9/83  -36/83  -15/83    5/83   32/83 ]
```

### Paso 35. F2 ← F2 + (-92/45) · F6

El multiplicador es −(92/45)/(1) = -92/45; así, 92/45 + (-92/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0        0  |  -221/83  -72/83  210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0        0  |   -92/83   35/83   57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  -182/45  |        0     4/5     1/5     1/3    -1/9  -68/45 ]
[ 0  0  0  1  0     -4/9  |        0       0       0     1/3    -1/9    -1/9 ]
[ 0  0  0  0  1    -1/15  |        0     1/5    -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0        1  |    45/83   -9/83  -36/83  -15/83    5/83   32/83 ]
```

### Paso 36. F3 ← F3 + (182/45) · F6

El multiplicador es −(-182/45)/(1) = 182/45; así, -182/45 + (182/45)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0      0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0      0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0      0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0   -4/9  |        0       0        0     1/3    -1/9    -1/9 ]
[ 0  0  0  0  1  -1/15  |        0     1/5     -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0      1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 37. F4 ← F4 + (4/9) · F6

El multiplicador es −(-4/9)/(1) = 4/9; así, -4/9 + (4/9)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0      0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0      0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0      0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0      0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  -1/15  |        0     1/5     -1/5       0     1/3   -4/15 ]
[ 0  0  0  0  0      1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 38. F5 ← F5 + (1/15) · F6

El multiplicador es −(-1/15)/(1) = 1/15; así, -1/15 + (1/15)·(1) = 0 en la columna 6. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 39. [I | A⁻¹]: inversa obtenida

Aplicar las mismas operaciones elementales a [A | I] equivale a multiplicar ambos bloques por A⁻¹: A⁻¹A = I y A⁻¹I = A⁻¹.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 40. x1 = (-221/83)·(185) + (-72/83)·(200) + (210/83)·(280) + (46/83)·(150) + (-43/83)·(245) + (7/83)·(195) = 15

Producto fila 1 de A⁻¹ por la columna B. La suma de productos da la componente x1 de X = A⁻¹B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 41. x2 = (-92/83)·(185) + (35/83)·(200) + (57/83)·(280) + (3/83)·(150) + (-1/83)·(245) + (-23/83)·(195) = 20

Producto fila 2 de A⁻¹ por la columna B. La suma de productos da la componente x2 de X = A⁻¹B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 42. x3 = (182/83)·(185) + (30/83)·(200) + (-129/83)·(280) + (-33/83)·(150) + (11/83)·(245) + (4/83)·(195) = 25

Producto fila 3 de A⁻¹ por la columna B. La suma de productos da la componente x3 de X = A⁻¹B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 43. x4 = (20/83)·(185) + (-4/83)·(200) + (-16/83)·(280) + (21/83)·(150) + (-7/83)·(245) + (5/83)·(195) = 10

Producto fila 4 de A⁻¹ por la columna B. La suma de productos da la componente x4 de X = A⁻¹B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 44. x5 = (3/83)·(185) + (16/83)·(200) + (-19/83)·(280) + (-1/83)·(150) + (28/83)·(245) + (-20/83)·(195) = 15

Producto fila 5 de A⁻¹ por la columna B. La suma de productos da la componente x5 de X = A⁻¹B.

```text
[ 1  0  0  0  0  0  |  -221/83  -72/83   210/83   46/83  -43/83    7/83 ]
[ 0  1  0  0  0  0  |   -92/83   35/83    57/83    3/83   -1/83  -23/83 ]
[ 0  0  1  0  0  0  |   182/83   30/83  -129/83  -33/83   11/83    4/83 ]
[ 0  0  0  1  0  0  |    20/83   -4/83   -16/83   21/83   -7/83    5/83 ]
[ 0  0  0  0  1  0  |     3/83   16/83   -19/83   -1/83   28/83  -20/83 ]
[ 0  0  0  0  0  1  |    45/83   -9/83   -36/83  -15/83    5/83   32/83 ]
```

### Paso 45. x6 = (45/83)·(185) + (-9/83)·(200) + (-36/83)·(280) + (-15/83)·(150) + (5/83)·(245) + (32/83)·(195) = 20

Producto fila 6 de A⁻¹ por la columna B. La suma de productos da la componente x6 de X = A⁻¹B.

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
