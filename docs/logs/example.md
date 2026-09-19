# Ejemplo guiado · 3 × 3

TechChip Matrix Studio · procedimiento reproducible

Sistema pequeño con solución X = (2, 3, −1), útil para aprender el procedimiento.

## 1. Sistema de entrada

```text
[  2   1  -1  |    8 ]
[ -3  -1   2  |  -11 ]
[ -2   1   2  |   -3 ]
```

## 2. Diagnóstico

- Estado: Solución única
- det(A) = -1
- rango(A) = 3; rango([A|B]) = 3

## 3. Interpretación

- El sistema tiene una única solución y los tres métodos coinciden exactamente.
- Los valores negativos son soluciones matemáticas válidas; su interpretación depende del contexto del problema.
- La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

## 4. Solución y verificación

| Variable | Valor exacto | Aproximación |
|---|---:|---:|
| x1 | 2 | 2.000000 |
| x2 | 3 | 3.000000 |
| x3 | -1 | -1.000000 |

Los tres métodos coinciden: sí.
Error máximo por componente: 0; criterio exigido: < 10⁻⁶.

Fila 1: (2)·(2) + (1)·(3) + (-1)·(-1) = 8; B1 = 8; |AX − B| = 0
Fila 2: (-3)·(2) + (-1)·(3) + (2)·(-1) = -11; B2 = -11; |AX − B| = 0
Fila 3: (-2)·(2) + (1)·(3) + (2)·(-1) = -3; B3 = -3; |AX − B| = 0


## Procedimiento — Diagnóstico: determinante y rangos

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[  2   1  -1  |    8 ]
[ -3  -1   2  |  -11 ]
[ -2   1   2  |   -3 ]
```

### Paso 2. F1 ↔ F2

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ -3  -1   2  |  -11 ]
[  2   1  -1  |    8 ]
[ -2   1   2  |   -3 ]
```

### Paso 3. F2 ← F2 + (2/3) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ -3   -1    2  |  -11 ]
[  0  1/3  1/3  |  2/3 ]
[ -2    1    2  |   -3 ]
```

### Paso 4. F3 ← F3 + (-2/3) · F1

Se anula la entrada -2 en la columna 1; se opera sobre la fila completa.

```text
[ -3   -1    2  |   -11 ]
[  0  1/3  1/3  |   2/3 ]
[  0  5/3  2/3  |  13/3 ]
```

### Paso 5. F2 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 2.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0  1/3  1/3  |   2/3 ]
```

### Paso 6. F3 ← F3 + (-1/5) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```

### Paso 7. det(A) = -1

2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (-3) · (5/3) · (1/5) = -1.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```


## Procedimiento — Eliminación de Gauss

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[  2   1  -1  |    8 ]
[ -3  -1   2  |  -11 ]
[ -2   1   2  |   -3 ]
```

### Paso 2. F1 ↔ F2

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ -3  -1   2  |  -11 ]
[  2   1  -1  |    8 ]
[ -2   1   2  |   -3 ]
```

### Paso 3. F2 ← F2 + (2/3) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[ -3   -1    2  |  -11 ]
[  0  1/3  1/3  |  2/3 ]
[ -2    1    2  |   -3 ]
```

### Paso 4. F3 ← F3 + (-2/3) · F1

Se anula la entrada -2 en la columna 1; se opera sobre la fila completa.

```text
[ -3   -1    2  |   -11 ]
[  0  1/3  1/3  |   2/3 ]
[  0  5/3  2/3  |  13/3 ]
```

### Paso 5. F2 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 2.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0  1/3  1/3  |   2/3 ]
```

### Paso 6. F3 ← F3 + (-1/5) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```

### Paso 7. det(A) = -1

2 intercambio(s). Las sumas de filas conservan el determinante. det(A) = (-1)^2 · (-3) · (5/3) · (1/5) = -1.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```

### Paso 8. Matriz triangular superior U

Se resuelve U·X = C desde la última fila hacia la primera.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```

### Paso 9. x3 = (-1/5 − (0)) / (1/5) = -1

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```

### Paso 10. x2 = (13/3 − ((2/3)·(-1))) / (5/3) = 3

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```

### Paso 11. x1 = (-11 − ((-1)·(3) + (2)·(-1))) / (-3) = 2

Sustitución hacia atrás: se usan las incógnitas ya calculadas.

```text
[ -3   -1    2  |   -11 ]
[  0  5/3  2/3  |  13/3 ]
[  0    0  1/5  |  -1/5 ]
```


## Procedimiento — Gauss-Jordan

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[  2   1  -1  |    8 ]
[ -3  -1   2  |  -11 ]
[ -2   1   2  |   -3 ]
```

### Paso 2. F1 ↔ F2

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ -3  -1   2  |  -11 ]
[  2   1  -1  |    8 ]
[ -2   1   2  |   -3 ]
```

### Paso 3. F1 ← (-1/3) · F1

Se convierte el pivote -3 en 1.

```text
[  1  1/3  -2/3  |  11/3 ]
[  2    1    -1  |     8 ]
[ -2    1     2  |    -3 ]
```

### Paso 4. F2 ← F2 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[  1  1/3  -2/3  |  11/3 ]
[  0  1/3   1/3  |   2/3 ]
[ -2    1     2  |    -3 ]
```

### Paso 5. F3 ← F3 + (2) · F1

Se anula la entrada -2 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/3  -2/3  |  11/3 ]
[ 0  1/3   1/3  |   2/3 ]
[ 0  5/3   2/3  |  13/3 ]
```

### Paso 6. F2 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 2.

```text
[ 1  1/3  -2/3  |  11/3 ]
[ 0  5/3   2/3  |  13/3 ]
[ 0  1/3   1/3  |   2/3 ]
```

### Paso 7. F2 ← (3/5) · F2

Se convierte el pivote 5/3 en 1.

```text
[ 1  1/3  -2/3  |  11/3 ]
[ 0    1   2/5  |  13/5 ]
[ 0  1/3   1/3  |   2/3 ]
```

### Paso 8. F1 ← F1 + (-1/3) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1    0  -4/5  |  14/5 ]
[ 0    1   2/5  |  13/5 ]
[ 0  1/3   1/3  |   2/3 ]
```

### Paso 9. F3 ← F3 + (-1/3) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1  0  -4/5  |  14/5 ]
[ 0  1   2/5  |  13/5 ]
[ 0  0   1/5  |  -1/5 ]
```

### Paso 10. F3 ← (5) · F3

Se convierte el pivote 1/5 en 1.

```text
[ 1  0  -4/5  |  14/5 ]
[ 0  1   2/5  |  13/5 ]
[ 0  0     1  |    -1 ]
```

### Paso 11. F1 ← F1 + (4/5) · F3

Se anula la entrada -4/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0    0  |     2 ]
[ 0  1  2/5  |  13/5 ]
[ 0  0    1  |    -1 ]
```

### Paso 12. F2 ← F2 + (-2/5) · F3

Se anula la entrada 2/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0  0  |   2 ]
[ 0  1  0  |   3 ]
[ 0  0  1  |  -1 ]
```

### Paso 13. [I | X]: lectura de la solución

Cada fila contiene una incógnita con coeficiente 1; la última columna es X.

```text
[ 1  0  0  |   2 ]
[ 0  1  0  |   3 ]
[ 0  0  1  |  -1 ]
```


## Procedimiento — Matriz inversa

### Paso 1. Matriz inicial

El bloque a la derecha también participa en cada operación de fila.

```text
[  2   1  -1  |  1  0  0 ]
[ -3  -1   2  |  0  1  0 ]
[ -2   1   2  |  0  0  1 ]
```

### Paso 2. F1 ↔ F2

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 1.

```text
[ -3  -1   2  |  0  1  0 ]
[  2   1  -1  |  1  0  0 ]
[ -2   1   2  |  0  0  1 ]
```

### Paso 3. F1 ← (-1/3) · F1

Se convierte el pivote -3 en 1.

```text
[  1  1/3  -2/3  |  0  -1/3  0 ]
[  2    1    -1  |  1     0  0 ]
[ -2    1     2  |  0     0  1 ]
```

### Paso 4. F2 ← F2 + (-2) · F1

Se anula la entrada 2 en la columna 1; se opera sobre la fila completa.

```text
[  1  1/3  -2/3  |  0  -1/3  0 ]
[  0  1/3   1/3  |  1   2/3  0 ]
[ -2    1     2  |  0     0  1 ]
```

### Paso 5. F3 ← F3 + (2) · F1

Se anula la entrada -2 en la columna 1; se opera sobre la fila completa.

```text
[ 1  1/3  -2/3  |  0  -1/3  0 ]
[ 0  1/3   1/3  |  1   2/3  0 ]
[ 0  5/3   2/3  |  0  -2/3  1 ]
```

### Paso 6. F2 ↔ F3

Pivoteo parcial: se elige el mayor valor absoluto disponible en la columna 2.

```text
[ 1  1/3  -2/3  |  0  -1/3  0 ]
[ 0  5/3   2/3  |  0  -2/3  1 ]
[ 0  1/3   1/3  |  1   2/3  0 ]
```

### Paso 7. F2 ← (3/5) · F2

Se convierte el pivote 5/3 en 1.

```text
[ 1  1/3  -2/3  |  0  -1/3    0 ]
[ 0    1   2/5  |  0  -2/5  3/5 ]
[ 0  1/3   1/3  |  1   2/3    0 ]
```

### Paso 8. F1 ← F1 + (-1/3) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1    0  -4/5  |  0  -1/5  -1/5 ]
[ 0    1   2/5  |  0  -2/5   3/5 ]
[ 0  1/3   1/3  |  1   2/3     0 ]
```

### Paso 9. F3 ← F3 + (-1/3) · F2

Se anula la entrada 1/3 en la columna 2; se opera sobre la fila completa.

```text
[ 1  0  -4/5  |  0  -1/5  -1/5 ]
[ 0  1   2/5  |  0  -2/5   3/5 ]
[ 0  0   1/5  |  1   4/5  -1/5 ]
```

### Paso 10. F3 ← (5) · F3

Se convierte el pivote 1/5 en 1.

```text
[ 1  0  -4/5  |  0  -1/5  -1/5 ]
[ 0  1   2/5  |  0  -2/5   3/5 ]
[ 0  0     1  |  5     4    -1 ]
```

### Paso 11. F1 ← F1 + (4/5) · F3

Se anula la entrada -4/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0    0  |  4     3   -1 ]
[ 0  1  2/5  |  0  -2/5  3/5 ]
[ 0  0    1  |  5     4   -1 ]
```

### Paso 12. F2 ← F2 + (-2/5) · F3

Se anula la entrada 2/5 en la columna 3; se opera sobre la fila completa.

```text
[ 1  0  0  |   4   3  -1 ]
[ 0  1  0  |  -2  -2   1 ]
[ 0  0  1  |   5   4  -1 ]
```

### Paso 13. [I | A⁻¹]: inversa obtenida

Las operaciones que convierten A en I convierten I en A⁻¹.

```text
[ 1  0  0  |   4   3  -1 ]
[ 0  1  0  |  -2  -2   1 ]
[ 0  0  1  |   5   4  -1 ]
```

### Paso 14. x1 = (4)·(8) + (3)·(-11) + (-1)·(-3) = 2

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  |   4   3  -1 ]
[ 0  1  0  |  -2  -2   1 ]
[ 0  0  1  |   5   4  -1 ]
```

### Paso 15. x2 = (-2)·(8) + (-2)·(-11) + (1)·(-3) = 3

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  |   4   3  -1 ]
[ 0  1  0  |  -2  -2   1 ]
[ 0  0  1  |   5   4  -1 ]
```

### Paso 16. x3 = (5)·(8) + (4)·(-11) + (-1)·(-3) = -1

Producto fila por columna en X = A⁻¹·B.

```text
[ 1  0  0  |   4   3  -1 ]
[ 0  1  0  |  -2  -2   1 ]
[ 0  0  1  |   5   4  -1 ]
```

## Referencias

- [MIT OpenCourseWare · Eliminación con matrices](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/0903b4b404284cd14b66ecccea103fd4_MIT18_06SCF11_Ses1.2sum.pdf)
- [MIT OpenCourseWare · Multiplicación, Gauss-Jordan e inversa](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf)
- [MIT OpenCourseWare · AX = B y variables libres](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/solving-ax-b-row-reduced-form-r/)

Cálculo racional exacto respecto de los datos introducidos. Los decimales de presentación son aproximados.
