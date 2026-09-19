# Tres métodos para resolver AX = B

## Operaciones elementales

Intercambiar dos filas, multiplicar una fila por un escalar no nulo y sumar un múltiplo de otra fila conservan las soluciones. Todas las operaciones se aplican también al bloque derecho de la matriz aumentada.

## Eliminación de Gauss

Se forma `[A|B]`, se eligen pivotes y se eliminan las entradas inferiores hasta `[U|C]`. Después se calcula, desde la última fila:

`xi = (ci − Σ(j>i) uij·xj) / uii`.

La app muestra el pivote, cada modificación de fila y cada sustitución. El intercambio evita dividir por un pivote cero cuando hay otra fila utilizable. Véase [MIT OCW: Elimination with Matrices](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/0903b4b404284cd14b66ecccea103fd4_MIT18_06SCF11_Ses1.2sum.pdf).

## Gauss-Jordan

Se normaliza el pivote a 1 y se eliminan las entradas por encima y por debajo. Para una matriz invertible se llega a `[I|X]`, de donde se lee la solución. La reducción también permite encontrar variables libres o una contradicción. Véase [MIT OCW: Multiplication and Inverse Matrices](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf).

## Matriz inversa

Se trabaja con `[A|I]` y se reduce hasta `[I|A⁻¹]`. Después se multiplica `X=A⁻¹B`, componente por componente. La app conserva ambos momentos; B no participa en la construcción de la inversa. Si A es singular, esta vía no se ejecuta. La misma [lección del MIT sobre inversas](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/1963da71c4d96e5d14e7939780f79bcc_MIT18_06SCF11_Ses1.3sum.pdf) desarrolla la relación con las operaciones elementales.

## Rangos y soluciones

| Condición | Interpretación |
|---|---|
| rango(A) = rango([A|B]) = n | Solución única |
| rango(A) = rango([A|B]) < n | Infinitas soluciones con n−r variables libres |
| rango(A) < rango([A|B]) | Ninguna solución |

La familia compatible se escribe `X=Xp+Σ ti·vi`, con `A·Xp=B` y `A·vi=0`. Véase [MIT OCW: Solving AX=B, Row Reduced Form R](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/solving-ax-b-row-reduced-form-r/).

## Decisiones de implementación

El programa calcula el determinante con el producto de pivotes de Gauss y el signo de los intercambios. Utiliza `Fraction`, no un umbral arbitrario para decidir si un determinante es cero. La equivalencia entre métodos se prueba sobre los vectores exactos y se verifica cada componente de `|AX−B|`. Esta implementación prioriza la claridad y los sistemas pequeños, no el rendimiento de matrices industriales de gran tamaño.

### Por qué el residual puede ser exactamente cero

El motor convierte cada entrada finita a [`fractions.Fraction`](https://docs.python.org/3/library/fractions.html), que representa aritmética racional. Por eso no redondea durante la eliminación: si el sistema racional tiene solución única, la sustitución `A·X` reproduce `B` componente por componente y `E=max|A·X−B|=0`. Las aproximaciones decimales de la interfaz son informativas y nunca se reutilizan como entrada del algoritmo.

Para entradas de punto flotante convencionales, el residual suele ser pequeño pero no necesariamente cero debido a la representación binaria. La [documentación oficial de Python sobre punto flotante](https://docs.python.org/3/tutorial/floatingpoint.html) explica esa diferencia. La referencia [NIST DLMF §3.2](https://dlmf.nist.gov/3.2) fundamenta la eliminación, la sustitución hacia atrás, el pivoteo parcial y el uso del vector residual como comprobación.

Fuentes primarias consultadas el 19 de septiembre de 2026. Las explicaciones de este documento son resúmenes originales; no se incorporaron páginas del material docente al repositorio.
