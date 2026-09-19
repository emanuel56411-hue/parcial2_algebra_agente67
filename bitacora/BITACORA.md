# Bitácora de pruebas — TechChip Matrix Studio

Resultados regenerados el 19 de septiembre de 2026 mediante `main.py`; los JSON enlazados contienen la salida completa, incluidas todas las matrices intermedias.

| Escenario | det(A) | rangos A/[A|B] | Diagnóstico | Estado |
|---|---:|---:|---|---|
| Base consistente | -83 | 6/6 | Solución única | Cumple |
| B impreso en la guía | -83 | 6/6 | Solución única | Cumple: discrepancia demostrada |
| Escasez de resina | -83 | 6/6 | Solución única | Cumple |
| Singular incompatible | 0 | 5/6 | Cero soluciones | Cumple |
| Singular compatible indeterminado | 0 | 5/5 | Infinitas soluciones | Cumple |

## 1. Base consistente

### Entrada usada

```json
{
  "A": [
    [
      "2",
      "1",
      "3",
      "1",
      "2",
      "1"
    ],
    [
      "1",
      "3",
      "2",
      "2",
      "1",
      "2"
    ],
    [
      "3",
      "2",
      "4",
      "1",
      "3",
      "2"
    ],
    [
      "1",
      "1",
      "1",
      "4",
      "2",
      "1"
    ],
    [
      "2",
      "1",
      "2",
      "1",
      "5",
      "3"
    ],
    [
      "1",
      "2",
      "1",
      "2",
      "1",
      "4"
    ]
  ],
  "B": [
    "185",
    "200",
    "280",
    "150",
    "245",
    "195"
  ],
  "production": true
}
```

### Salida literal resumida

```text
status: unique
det(A): -83
rank(A): 6
rank([A|B]): 6
solution: (15, 20, 25, 10, 15, 20)
residual |AX-B|: (0, 0, 0, 0, 0, 0)
max_error: 0
methods_agree: True
```

Salida completa: [`compatible.json`](compatible.json).

### Diagnóstico

- Plan factible para el modelo continuo: todas las cantidades son no negativas y AX = B consume el 100 % de cada disponibilidad.
- X se expresa en miles de unidades; X·1000 se informa como cantidad continua, sin redondear a unidades enteras.
- La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

### Esperado frente a obtenido

- **Esperado:** X=(15,20,25,10,15,20), E=0.
- **Obtenido:** X = (15, 20, 25, 10, 15, 20), error máximo = 0.
- **Estado:** Cumple.

## 2. B impreso en la guía

### Entrada usada

```json
{
  "A": [
    [
      "2",
      "1",
      "3",
      "1",
      "2",
      "1"
    ],
    [
      "1",
      "3",
      "2",
      "2",
      "1",
      "2"
    ],
    [
      "3",
      "2",
      "4",
      "1",
      "3",
      "2"
    ],
    [
      "1",
      "1",
      "1",
      "4",
      "2",
      "1"
    ],
    [
      "2",
      "1",
      "2",
      "1",
      "5",
      "3"
    ],
    [
      "1",
      "2",
      "1",
      "2",
      "1",
      "4"
    ]
  ],
  "B": [
    "155",
    "160",
    "225",
    "140",
    "215",
    "175"
  ],
  "production": true
}
```

### Salida literal resumida

```text
status: unique
det(A): -83
rank(A): 6
rank([A|B]): 6
solution: (-105/83, 345/83, 2430/83, 1170/83, 1130/83, 2010/83)
residual |AX-B|: (0, 0, 0, 0, 0, 0)
max_error: 0
methods_agree: True
```

Salida completa: [`original.json`](original.json).

### Diagnóstico

- Plan de producción inalcanzable por restricción de materias primas.
- La solución de AX = B exige cantidades negativas: x1 = -105/83 (≈ -1.265060).
- No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa.
- La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

### Esperado frente a obtenido

- **Esperado:** La respuesta impresa no puede satisfacer este B; informar la discrepancia.
- **Obtenido:** X = (-105/83, 345/83, 2430/83, 1170/83, 1130/83, 2010/83), error máximo = 0.
- **Estado:** Cumple: discrepancia demostrada.

## 3. Escasez de resina

### Entrada usada

```json
{
  "A": [
    [
      "2",
      "1",
      "3",
      "1",
      "2",
      "1"
    ],
    [
      "1",
      "3",
      "2",
      "2",
      "1",
      "2"
    ],
    [
      "3",
      "2",
      "4",
      "1",
      "3",
      "2"
    ],
    [
      "1",
      "1",
      "1",
      "4",
      "2",
      "1"
    ],
    [
      "2",
      "1",
      "2",
      "1",
      "5",
      "3"
    ],
    [
      "1",
      "2",
      "1",
      "2",
      "1",
      "4"
    ]
  ],
  "B": [
    "155",
    "160",
    "100",
    "140",
    "215",
    "175"
  ],
  "production": true
}
```

### Salida literal resumida

```text
status: unique
det(A): -83
rank(A): 6
rank([A|B]): 6
solution: (-26355/83, -6780/83, 18555/83, 3170/83, 3505/83, 6510/83)
residual |AX-B|: (0, 0, 0, 0, 0, 0)
max_error: 0
methods_agree: True
```

Salida completa: [`scarcity.json`](scarcity.json).

### Diagnóstico

- Plan de producción inalcanzable por restricción de materias primas.
- La solución de AX = B exige cantidades negativas: x1 = -26355/83 (≈ -317.530120); x2 = -6780/83 (≈ -81.686747).
- No se puede consumir exactamente el 100 % de todos los recursos con X ≥ 0. Esto no demuestra que sea imposible producir con capacidad ociosa.
- La resolución de igualdades no maximiza beneficios ni minimiza costos. Para optimizar se necesita una función objetivo y restricciones adicionales.

### Esperado frente a obtenido

- **Esperado:** Detectar producciones negativas y plan inalcanzable.
- **Obtenido:** X = (-26355/83, -6780/83, 18555/83, 3170/83, 3505/83, 6510/83), error máximo = 0.
- **Estado:** Cumple.

## 4. Singular incompatible

### Entrada usada

```json
{
  "A": [
    [
      "2",
      "1",
      "3",
      "1",
      "2",
      "1"
    ],
    [
      "1",
      "3",
      "2",
      "2",
      "1",
      "2"
    ],
    [
      "3",
      "2",
      "4",
      "1",
      "3",
      "2"
    ],
    [
      "1",
      "1",
      "1",
      "4",
      "2",
      "1"
    ],
    [
      "2",
      "1",
      "2",
      "1",
      "5",
      "3"
    ],
    [
      "4",
      "2",
      "6",
      "2",
      "4",
      "2"
    ]
  ],
  "B": [
    "155",
    "160",
    "225",
    "140",
    "215",
    "175"
  ],
  "production": true
}
```

### Salida literal resumida

```text
status: inconsistent
det(A): 0
rank(A): 5
rank([A|B]): 6
solution: No aplica
residual |AX-B|: No aplica
max_error: None
methods_agree: False
```

Salida completa: [`singular.json`](singular.json).

### Diagnóstico

- Las restricciones se contradicen: no existe un vector X que cumpla todas las igualdades.
- Revisa las ecuaciones dependientes y sus disponibilidades antes de proponer un plan.

### Esperado frente a obtenido

- **Esperado:** det(A)=0 y cero soluciones porque B6≠2B1.
- **Obtenido:** rango(A)=5 < rango([A|B])=6.
- **Estado:** Cumple.

## 5. Singular compatible indeterminado

### Entrada usada

```json
{
  "A": [
    [
      "2",
      "1",
      "3",
      "1",
      "2",
      "1"
    ],
    [
      "1",
      "3",
      "2",
      "2",
      "1",
      "2"
    ],
    [
      "3",
      "2",
      "4",
      "1",
      "3",
      "2"
    ],
    [
      "1",
      "1",
      "1",
      "4",
      "2",
      "1"
    ],
    [
      "2",
      "1",
      "2",
      "1",
      "5",
      "3"
    ],
    [
      "4",
      "2",
      "6",
      "2",
      "4",
      "2"
    ]
  ],
  "B": [
    "155",
    "160",
    "225",
    "140",
    "215",
    "310"
  ],
  "production": true
}
```

### Salida literal resumida

```text
status: infinite
det(A): 0
rank(A): 5
rank([A|B]): 5
solution: No aplica
residual |AX-B|: No aplica
max_error: None
methods_agree: False
```

Salida completa: [`infinite.json`](infinite.json).

### Diagnóstico

- Hay 1 variable(s) libre(s): los datos no determinan una solución única.
- La familia X = Xₚ + t₁v₁ + … describe todas las soluciones reales; hacen falta restricciones independientes para reducir la ambigüedad.
- La viabilidad de esta familia bajo X ≥ 0 requiere un análisis adicional; no se declara un plan de producción viable.

### Esperado frente a obtenido

- **Esperado:** det(A)=0 e infinitas soluciones cuando B6=2B1.
- **Obtenido:** Xₚ = (-105/16, 345/16, 105/4, 165/16, 115/4, 0); columnas libres (base cero): 5.
- **Estado:** Cumple.

## Evidencia visual

- Inicio y entrada Streamlit: [`docs/screenshots/01_inicio.png`](../docs/screenshots/01_inicio.png)
- Caso base compatible: [`docs/screenshots/02_plan_compatible.png`](../docs/screenshots/02_plan_compatible.png)
- Procedimiento Streamlit: [`docs/screenshots/03_procedimiento.png`](../docs/screenshots/03_procedimiento.png)
- Escasez: [`docs/screenshots/04_escasez.png`](../docs/screenshots/04_escasez.png)
- Singular incompatible: [`docs/screenshots/05_singular.png`](../docs/screenshots/05_singular.png)
- Infinitas soluciones: [`docs/screenshots/06_infinitas.png`](../docs/screenshots/06_infinitas.png)
- Portada profesional en Vercel: [`docs/screenshots/08_vercel_profesional.png`](../docs/screenshots/08_vercel_profesional.png)
- Procedimiento completo en Vercel: [`docs/screenshots/09_vercel_procedimiento.png`](../docs/screenshots/09_vercel_procedimiento.png)
- Tutor IA en Vercel: [`docs/screenshots/10_vercel_tutor.png`](../docs/screenshots/10_vercel_tutor.png)
- Vista móvil en Vercel: [`docs/screenshots/11_vercel_movil.png`](../docs/screenshots/11_vercel_movil.png)
- Entregables públicos en Vercel: [`docs/screenshots/12_vercel_entregables.png`](../docs/screenshots/12_vercel_entregables.png)
