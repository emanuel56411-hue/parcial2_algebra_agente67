# Singular · sin solución

TechChip Matrix Studio · procedimiento reproducible

F₆ = 2F₁, conservando B₆ = 175. La fila 1 exigiría B₆ = 310. La guía contiene una inconsistencia: el vector esperado (15, 20, 25, 10, 15, 20) requiere B = (185, 200, 280, 150, 245, 195). No resuelve el B original (155, 160, 225, 140, 215, 175). Ambos casos se conservan por separado.

## 1. Sistema de entrada

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 4  2  6  2  4  2  |  175 ]
```

## 2. Diagnóstico

- Estado: Sin solución
- det(A) = 0
- rango(A) = 5; rango([A|B]) = 6

## 3. Interpretación

- Las restricciones se contradicen: no existe un vector X que cumpla todas las igualdades.
- Revisa las ecuaciones dependientes y sus disponibilidades antes de proponer un plan.

## Procedimiento — Diagnóstico: determinante y rangos

### Paso 1. Matriz aumentada inicial

Punto de partida: [A | B]. La barra separa los coeficientes del bloque derecho, pero cada operación elemental se aplica a la fila completa para conservar un sistema equivalente.

```text
[ 2  1  3  1  2  1  |  155 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 4  2  6  2  4  2  |  175 ]
```

### Paso 2. F1 ↔ F6

Pivoteo parcial en la columna 1: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 4  2  6  2  4  2  |  175 ]
[ 1  3  2  2  1  2  |  160 ]
[ 3  2  4  1  3  2  |  225 ]
[ 1  1  1  4  2  1  |  140 ]
[ 2  1  2  1  5  3  |  215 ]
[ 2  1  3  1  2  1  |  155 ]
```

### Paso 3. F2 ← F2 + (-1/4) · F1

El multiplicador es −(1)/(4) = -1/4; así, 1 + (-1/4)·(4) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2    6    2  4    2  |    175 ]
[ 0  5/2  1/2  3/2  0  3/2  |  465/4 ]
[ 3    2    4    1  3    2  |    225 ]
[ 1    1    1    4  2    1  |    140 ]
[ 2    1    2    1  5    3  |    215 ]
[ 2    1    3    1  2    1  |    155 ]
```

### Paso 4. F3 ← F3 + (-3/4) · F1

El multiplicador es −(3)/(4) = -3/4; así, 3 + (-3/4)·(4) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  375/4 ]
[ 1    1     1     4  2    1  |    140 ]
[ 2    1     2     1  5    3  |    215 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 5. F4 ← F4 + (-1/4) · F1

El multiplicador es −(1)/(4) = -1/4; así, 1 + (-1/4)·(4) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  375/4 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  385/4 ]
[ 2    1     2     1  5    3  |    215 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 6. F5 ← F5 + (-1/2) · F1

El multiplicador es −(2)/(4) = -1/2; así, 2 + (-1/2)·(4) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  375/4 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  385/4 ]
[ 0    0    -1     0  3    2  |  255/2 ]
[ 2    1     3     1  2    1  |    155 ]
```

### Paso 7. F6 ← F6 + (-1/2) · F1

El multiplicador es −(2)/(4) = -1/2; así, 2 + (-1/2)·(4) = 0 en la columna 1. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0  1/2  -1/2  -1/2  0  1/2  |  375/4 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  385/4 ]
[ 0    0    -1     0  3    2  |  255/2 ]
[ 0    0     0     0  0    0  |  135/2 ]
```

### Paso 8. F3 ← F3 + (-1/5) · F2

El multiplicador es −(1/2)/(5/2) = -1/5; así, 1/2 + (-1/5)·(5/2) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0    0  -3/5  -4/5  0  1/5  |  141/2 ]
[ 0  1/2  -1/2   7/2  1  1/2  |  385/4 ]
[ 0    0    -1     0  3    2  |  255/2 ]
[ 0    0     0     0  0    0  |  135/2 ]
```

### Paso 9. F4 ← F4 + (-1/5) · F2

El multiplicador es −(1/2)/(5/2) = -1/5; así, 1/2 + (-1/5)·(5/2) = 0 en la columna 2. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0    0  -3/5  -4/5  0  1/5  |  141/2 ]
[ 0    0  -3/5  16/5  1  1/5  |     73 ]
[ 0    0    -1     0  3    2  |  255/2 ]
[ 0    0     0     0  0    0  |  135/2 ]
```

### Paso 10. F3 ↔ F5

Pivoteo parcial en la columna 3: se coloca arriba el mayor valor absoluto disponible. Intercambiar ecuaciones solo cambia su orden, no el conjunto de soluciones; además evita dividir entre cero.

```text
[ 4    2     6     2  4    2  |    175 ]
[ 0  5/2   1/2   3/2  0  3/2  |  465/4 ]
[ 0    0    -1     0  3    2  |  255/2 ]
[ 0    0  -3/5  16/5  1  1/5  |     73 ]
[ 0    0  -3/5  -4/5  0  1/5  |  141/2 ]
[ 0    0     0     0  0    0  |  135/2 ]
```

### Paso 11. F4 ← F4 + (-3/5) · F3

El multiplicador es −(-3/5)/(-1) = -3/5; así, -3/5 + (-3/5)·(-1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2     6     2     4    2  |    175 ]
[ 0  5/2   1/2   3/2     0  3/2  |  465/4 ]
[ 0    0    -1     0     3    2  |  255/2 ]
[ 0    0     0  16/5  -4/5   -1  |   -7/2 ]
[ 0    0  -3/5  -4/5     0  1/5  |  141/2 ]
[ 0    0     0     0     0    0  |  135/2 ]
```

### Paso 12. F5 ← F5 + (-3/5) · F3

El multiplicador es −(-3/5)/(-1) = -3/5; así, -3/5 + (-3/5)·(-1) = 0 en la columna 3. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2    6     2     4    2  |    175 ]
[ 0  5/2  1/2   3/2     0  3/2  |  465/4 ]
[ 0    0   -1     0     3    2  |  255/2 ]
[ 0    0    0  16/5  -4/5   -1  |   -7/2 ]
[ 0    0    0  -4/5  -9/5   -1  |     -6 ]
[ 0    0    0     0     0    0  |  135/2 ]
```

### Paso 13. F5 ← F5 + (1/4) · F4

El multiplicador es −(-4/5)/(16/5) = 1/4; así, -4/5 + (1/4)·(16/5) = 0 en la columna 4. Sumar a una ecuación un múltiplo de otra es reversible y conserva exactamente las soluciones.

```text
[ 4    2    6     2     4     2  |    175 ]
[ 0  5/2  1/2   3/2     0   3/2  |  465/4 ]
[ 0    0   -1     0     3     2  |  255/2 ]
[ 0    0    0  16/5  -4/5    -1  |   -7/2 ]
[ 0    0    0     0    -2  -5/4  |  -55/8 ]
[ 0    0    0     0     0     0  |  135/2 ]
```

### Paso 14. Columna 6: sin pivote

Desde la fila activa hacia abajo todas las entradas de esta columna son cero. No se puede crear un pivote aquí; la columna corresponderá a una variable libre si no aparece un pivote después.

```text
[ 4    2    6     2     4     2  |    175 ]
[ 0  5/2  1/2   3/2     0   3/2  |  465/4 ]
[ 0    0   -1     0     3     2  |  255/2 ]
[ 0    0    0  16/5  -4/5    -1  |   -7/2 ]
[ 0    0    0     0    -2  -5/4  |  -55/8 ]
[ 0    0    0     0     0     0  |  135/2 ]
```

### Paso 15. det(A) = 0

No hay n pivotes independientes; det(A) = 0. No existe A⁻¹.

```text
[ 4    2    6     2     4     2  |    175 ]
[ 0  5/2  1/2   3/2     0   3/2  |  465/4 ]
[ 0    0   -1     0     3     2  |  255/2 ]
[ 0    0    0  16/5  -4/5    -1  |   -7/2 ]
[ 0    0    0     0    -2  -5/4  |  -55/8 ]
[ 0    0    0     0     0     0  |  135/2 ]
```

### Paso 16. Contradicción: 0 = 135/2

La fila 6 demuestra que rango(A) = 5 < rango([A|B]) = 6. Se detienen los métodos de solución única.

```text
[ 4    2    6     2     4     2  |    175 ]
[ 0  5/2  1/2   3/2     0   3/2  |  465/4 ]
[ 0    0   -1     0     3     2  |  255/2 ]
[ 0    0    0  16/5  -4/5    -1  |   -7/2 ]
[ 0    0    0     0    -2  -5/4  |  -55/8 ]
[ 0    0    0     0     0     0  |  135/2 ]
```

## Referencias

- [MIT OpenCourseWare · Eliminación con matrices](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/0903b4b404284cd14b66ecccea103fd4_MIT18_06SCF11_Ses1.2sum.pdf)
- [MIT OpenCourseWare · Multiplicación, Gauss-Jordan e inversa](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf)
- [MIT OpenCourseWare · AX = B y variables libres](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/solving-ax-b-row-reduced-form-r/)

Cálculo racional exacto respecto de los datos introducidos. Los decimales de presentación son aproximados.
