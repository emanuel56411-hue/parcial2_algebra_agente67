# TechChip Matrix Studio

**Resuelve sistemas lineales. Entiende cada operación. Sustenta cada decisión.**

Aplicación web y agente de consola para Gauss, Gauss-Jordan y matriz inversa, con cálculo racional exacto, diagnóstico de singularidad y procedimientos exportables. Incluye el caso empresarial TechChip Systems y sistemas personalizados de **1 × 1 a 12 × 12**.

> **Hallazgo en la guía:** el vector esperado `(15,20,25,10,15,20)` requiere `B=(185,200,280,150,245,195)`. Las disponibilidades originales son `(155,160,225,140,215,175)` y producen una solución distinta con `x1<0`. La aplicación conserva ambos escenarios y no sustituye datos para forzar la respuesta.

## Qué puedes hacer

- Editar cualquier celda de A y B, pegar JSON o cargar un archivo.
- Introducir enteros, decimales, notación científica y fracciones como `"2/3"`.
- Comparar tres soluciones calculadas mediante algoritmos explícitos.
- Recorrer pasos numerados con la operación de fila, su explicación y la matriz resultante; consultar todos los pasos en orden.
- Ver el cálculo del determinante, rangos, sustitución hacia atrás, construcción de la inversa y producto `A⁻¹B`.
- Diagnosticar solución única, incompatibilidad o una familia de soluciones con parámetros libres.
- Separar solución matemática y factibilidad de producción; consultar el balance por recurso.
- Descargar el procedimiento en Markdown, los datos/resultados en JSON y un informe HTML imprimible como PDF.

## Iniciar la web

Requiere **Python 3.11 o superior**. Windows, Linux y macOS:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abre **http://localhost:8501**. En el entorno existente del proyecto también puedes usar:

```bash
venv/bin/python -m streamlit run app.py
```

La página funciona localmente y no requiere cuentas ni claves de API. No se envían matrices a servicios de IA. El motor es un agente determinista basado en reglas; las explicaciones proceden de operaciones verificables. La tipografía usa fuentes locales/sistema.

## Consola sin dependencias

La CLI y el motor solo necesitan la biblioteca estándar de Python. La salida predeterminada incluye el procedimiento completo:

```bash
python main.py                                    # Datos originales + todos los pasos
python main.py --scenario compatible              # B que corresponde al vector esperado
python main.py --scenario scarcity --summary      # Resina a 100 kg
python main.py --scenario singular                # Sin solución
python main.py --scenario infinite                # Familia de soluciones
python main.py --interactive                      # Introducir filas por consola
python main.py --input examples/example.json
python main.py --input examples/example.json --format json --output resultado.json
python main.py --scenario original --format html --output informe.html
python main.py --validate                         # Batería, salida JSON y código de estado
```

`--input -` lee JSON desde la entrada estándar. `--production` aplica interpretación de producción a entradas propias, con X en miles de unidades y A/B no negativos. Sin esa opción, los números negativos son soluciones matemáticas válidas. Códigos de salida: 0 = análisis completado (incluye sistemas sin solución), 1 = falla en la batería, 2 = entrada/archivo inválido.

### Formato de entrada

```json
{
  "A": [[2, 1], [1, -1]],
  "B": [5, 1]
}
```

El resultado es `X=(2,1)`. Se acepta B como `[5,1]` o `[[5],[1]]`. Para exactitud, los decimales JSON se leen con `Decimal` y después con `Fraction`. Las fracciones deben ir entre comillas. A debe ser cuadrada y B tener la misma cantidad de filas.

Límites: hasta 12 incógnitas, 100 kB por JSON, 64 caracteres por literal, exponentes de −50 a 50 y numeradores/denominadores de hasta 256 bits en la entrada. No se admiten NaN, infinito, booleanos, celdas vacías ni divisiones entre cero. No se evalúa código introducido por el usuario.

El JSON de salida codifica números exactos como cadenas (`"-105/83"`), además de operaciones estructuradas (`kind`, `target`, `source`, `factor`). Los índices internos de fila empiezan en 0; la presentación empieza en F1. Las aproximaciones de pantalla nunca intervienen en el cálculo.

## Escenarios verificados

| Escenario | Datos | Diagnóstico |
|---|---|---|
| `original` | A y B de la guía | Solución única; x1 negativo; plan no viable bajo AX=B, X≥0 |
| `compatible` | B = A·(15,20,25,10,15,20) | Vector esperado; caso identificado como variante |
| `scarcity` | B original con B3=100 | x1 y x2 negativos |
| `singular` | F6=2F1; B6 original=175 | det=0, rangos 5 y 6: incompatible |
| `infinite` | F6=2F1 y B6=2B1=310 | det=0, rangos 5 y 5: una variable libre |
| `example` | Sistema didáctico 3×3 | X=(2,3,−1) |

Para los casos invertibles de TechChip, `det(A)=-83`. Los tres métodos coinciden y el error exacto por componente `|AX−B|` es cero, por lo que satisface `<10⁻⁶`. La prueba base de la guía es contradictoria con B original: eso se informa como un hallazgo, no como una prueba numérica exitosa del vector incorrecto.

## Entregables y documentación

- [Auditoría de cumplimiento del parcial](docs/cumplimiento.md).
- [Informe técnico PDF y desarrollo completo](docs/informe_tecnico.pdf): artículo de dos columnas y anexos, estilo académico inspirado en IEEE; revisar la plantilla exigida por el docente.
- [Interpretación de operaciones](docs/interpretacion_operaciones.md).
- [Bitácora de validación](docs/logs/validation.json) y [procedimiento original](docs/logs/original.md).
- [Gauss, Gauss-Jordan e inversa: fundamentos y fuentes](docs/metodos.md).
- [Guía para un piloto empresarial](docs/piloto_empresarial.md).
- [Ejemplos de entrada](examples/).

Los anexos son desarrollos algebraicos computados y verificables a mano. No se presentan como trabajo manuscrito independiente. Antes de entregar: completar identificación académica, revisar la discrepancia con el docente y confirmar si pide resolución manuscrita o una plantilla IEEE/ACM específica.

## Verificación reproducible

```bash
# Solo núcleo / CLI, sin instalar paquetes:
python -m unittest discover -s tests -p test_solver.py -v
# Núcleo y recorridos Streamlit, después de instalar requirements.txt:
python -m unittest discover -s tests -v
# Regenerar el PDF y los demás entregables:
python -m pip install -r requirements-dev.txt
python scripts/build_deliverables.py
```

Las pruebas comprueban soluciones conocidas, determinantes por una definición independiente, identidades de la inversa, familias paramétricas, reproducción de cada operación de fila, pivoteo, entradas inválidas y recorridos de los formularios web. La automatización de GitHub ejecuta las pruebas al recibir cambios.

## Arquitectura

```text
agent.py                  Validación, Gauss, Gauss-Jordan, inversa, explicación
scenarios.py              Datos originales y variantes independientes
reporting.py              Formato de matrices, guías y exportaciones
main.py                   Consola, JSON y batería de escenarios
app.py                    Interfaz Streamlit
scripts/build_deliverables.py  Ejemplos, bitácora y documento técnico
examples/                 Entradas reutilizables
tests/                    Pruebas de resultados y recorridos de interfaz
```

El motor no utiliza `numpy.linalg.solve`, `inv`, `det` ni `matrix_rank`. Gauss-Jordan y la inversa comparten el algoritmo de operaciones de fila, aplicado respectivamente a `[A|B]` y `[A|I]`; la inversa se multiplica por B después. El determinante se calcula antes de resolver, mediante los pivotes y la paridad de los intercambios. La aritmética exacta evita confundir determinantes pequeños con cero.

## Alcance de negocio

Este proyecto es un **prototipo funcional para demostración y piloto**, con trazabilidad como principal valor. No se afirma que una solución positiva sea óptima: no hay función objetivo, costos ni demanda en la guía. Para optimización real hacen falta esos datos y posiblemente `AX≤B`, restricciones enteras u otras condiciones. Autenticación, persistencia multiusuario, integraciones ERP y despliegue administrado no están implementados.

X está en miles de unidades: los coeficientes se interpretan como consumo **por mil módulos** para mantener coherencia dimensional. El 100% corresponde al modelo de igualdades, no a una garantía sobre operaciones reales.
