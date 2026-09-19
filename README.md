# TechChip Matrix Studio

**Resuelve sistemas lineales. Entiende cada operación. Sustenta cada decisión.**

Autores: Henry Modesto Portillo Quintanilla (`PQ100126`), David Ernesto Quijada Vásquez (`QV100226`) y Josue Emanuel Cruz Fernandez (`CF100126`).

Universidad Francisco Gavidia · Docente: Exides Gamaliel Claros Velasquez · Grupo: `01 EO8` · Entrega: 23 de septiembre de 2026.

Aplicación web y agente de consola para Gauss, Gauss-Jordan y matriz inversa, con cálculo racional exacto, diagnóstico de singularidad y procedimientos exportables. Incluye el caso empresarial TechChip Systems y sistemas personalizados de **1 × 1 a 12 × 12**. Dispone de una interfaz completa en Streamlit y una versión responsive preparada para Vercel.

> **Hallazgo en la guía:** el vector esperado `(15,20,25,10,15,20)` requiere `B=(185,200,280,150,245,195)`. Las disponibilidades originales son `(155,160,225,140,215,175)` y producen una solución distinta con `x1<0`. La aplicación conserva ambos escenarios y no sustituye datos para forzar la respuesta.

## Qué puedes hacer

- Editar cualquier celda de A y B, pegar JSON o cargar un archivo.
- Introducir enteros, decimales, notación científica y fracciones como `"2/3"`.
- Comparar tres soluciones calculadas mediante algoritmos explícitos.
- Elegir Gauss, Gauss-Jordan o matriz inversa como método principal antes de resolver; los demás quedan como verificación cruzada.
- Recorrer pasos numerados con la operación de fila, su explicación y la matriz resultante; consultar todos los pasos en orden.
- Identificar en cada paso la fase algebraica, la razón por la que conserva soluciones, las celdas modificadas y la fila antes/después.
- Ver el cálculo del determinante, rangos, sustitución hacia atrás, construcción de la inversa y producto `A⁻¹B`.
- Diagnosticar solución única, incompatibilidad o una familia de soluciones con parámetros libres.
- Separar solución matemática y factibilidad de producción; consultar el balance por recurso.
- Descargar el procedimiento en Markdown, los datos/resultados en JSON y un informe HTML imprimible como PDF.
- Consultar un tutor opcional de OpenAI sobre el resultado o pedir una explicación del paso seleccionado.
- Alternar entre tema claro y oscuro; la preferencia queda guardada en el navegador.

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

La calculadora funciona localmente y no requiere cuentas ni claves de API. El motor es un agente determinista basado en reglas; sus operaciones son verificables. El **Tutor IA es opcional**: solo envía datos a OpenAI cuando pulsas su botón o envías una pregunta. La tipografía usa fuentes locales/sistema.

## Desplegar en Vercel

La raíz del repositorio contiene `vercel.json`, la interfaz en `web/` y las funciones Python en `api/`. La interfaz publicada usa **Vite + React + TypeScript + Tailwind CSS + shadcn/ui**; conserva los escenarios, matrices editables, diagnósticos, los tres procedimientos completos, la verificación, las exportaciones y el Tutor IA. Reutiliza `agent.py`, por lo que los resultados son los mismos que en Streamlit.

Para trabajar solo en la interfaz:

```bash
npm --prefix web ci
npm --prefix web run dev
npm --prefix web run build
```

`npm run dev` sirve el frontend; para probar también las funciones Python usa `npx vercel dev` desde la raíz.

```bash
npx vercel dev       # vista previa local
npx vercel           # despliegue de prueba
npx vercel --prod    # producción
```

También puedes importar el repositorio de GitHub desde el panel de Vercel. `vercel.json` instala y compila `web/` y publica `web/dist`; no hace falta repetir esa configuración en el panel. Para activar el tutor, configura `OPENAI_API_KEY` como secreto de producción. Opcionalmente define `OPENAI_MODEL` y `OPENAI_DAILY_REQUEST_LIMIT`. `.vercelignore` excluye las dependencias pesadas de Streamlit porque la función serverless usa la biblioteca estándar.

Streamlit no se ejecuta dentro de Vercel: su sesión necesita una conexión WebSocket persistente. Por eso la versión alojada usa una aplicación React estática y una función Python por solicitud. El Tutor IA de Vercel vuelve a ejecutar el sistema en el servidor antes de construir el contexto; la respuesta generativa nunca tiene autoridad sobre los números exactos.

## Tutor IA opcional con OpenAI

Resuelve primero un sistema. La pestaña **Tutor IA** permite preguntar sobre ese resultado; en **Procedimiento → Paso a paso → Ayuda de IA para este paso** encontrarás **Explicar este paso con IA**. El motor matemático conserva la autoridad sobre los resultados; el texto generado se presenta como orientación y puede contener errores.

1. Instala las dependencias de `requirements.txt`.
2. Copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml` y completa `OPENAI_API_KEY` en tu editor local. Si ya existe el archivo, edítalo sin sobrescribir sus valores.
3. Reinicia Streamlit después de configurar los secretos. En Streamlit Community Cloud, añade las mismas claves en **Settings → Secrets**.

También se aceptan las variables de entorno `OPENAI_API_KEY`, `OPENAI_MODEL` y `OPENAI_DAILY_REQUEST_LIMIT`; tienen prioridad sobre el archivo. La clave se usa únicamente en el servidor y el archivo privado está excluido de Git. No la pegues en el chat del tutor ni la publiques en el repositorio.

El modelo inicial es `gpt-4.1-mini`, configurable por el administrador. Usa la [API Responses y el SDK oficial de Python](https://developers.openai.com/es-419/api/docs/quickstart). Cada consulta envía las matrices A/B, diagnóstico, solución e interpretación; el chat añade hasta seis mensajes anteriores y la explicación de pasos añade las matrices anterior y actual. No se envían archivos del equipo ni el PDF completo. Se solicita `store=False`; esto no equivale a una garantía de retención cero por el proveedor.

Controles de consumo: preguntas de hasta 1500 caracteres, contexto matemático de hasta 24000 caracteres, respuestas de hasta 1000 tokens, historial limitado y ningún reintento automático. La interfaz muestra los tokens reportados por OpenAI. Resolver, cambiar de pestaña o navegar entre pasos no genera llamadas a la API.

En Streamlit, el límite predeterminado es de **50 consultas por día UTC para todo el servidor**, compartido entre chat y explicación de pasos. La reserva es atómica y se guarda en `.tutor/usage.sqlite3`, excluido de Git. En Vercel existe además un límite preventivo por conexión e instancia, configurable con `OPENAI_DAILY_REQUEST_LIMIT`; por la naturaleza serverless no sustituye los límites y presupuesto del proyecto OpenAI.

Este límite controla solicitudes en una instalación, **no es un presupuesto en dólares de la cuenta**: otras aplicaciones, réplicas o la pérdida del disco pueden alterar el consumo total. Revisa también los límites de tu proyecto OpenAI. El costo depende del modelo y los tokens; consulta sus [tarifas oficiales](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

Las pruebas del tutor simulan las respuestas de OpenAI y no consumen saldo. La validación real requiere una clave con acceso al modelo; los errores de autenticación, cuota o conexión no impiden usar la calculadora.

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
- [Informe técnico IEEEtran en PDF](docs/informe_tecnico_ieee.pdf) y [fuente LaTeX](docs/informe_tecnico_ieee.tex): cuerpo a dos columnas y anexos completos con los tres métodos.
- [Interpretación de operaciones](docs/interpretacion_operaciones.md).
- [Bitácora de validación](bitacora/BITACORA.md), con JSON completos de cada escenario.
- [Mapa de entregables y rúbrica](docs/MAPA_ENTREGABLES.md).
- [Gauss, Gauss-Jordan e inversa: fundamentos y fuentes](docs/metodos.md).
- [Guía para un piloto empresarial](docs/piloto_empresarial.md).
- [Ejemplos de entrada](examples/).

Los anexos son desarrollos algebraicos computados y verificables a mano. No se presentan como trabajo manuscrito independiente. Antes de entregar: revisar la discrepancia con el docente y confirmar si pide resolución manuscrita o una variante IEEE/ACM específica.

## Verificación reproducible

```bash
# Solo núcleo / CLI, sin instalar paquetes:
python -m unittest discover -s tests -p test_solver.py -v
# Núcleo y recorridos Streamlit, después de instalar requirements.txt:
python -m unittest discover -s tests -v
# Frontend React: tipos, compilación y optimización de producción:
npm --prefix web ci
npm --prefix web run build
# Regenerar el PDF y los demás entregables:
python -m pip install -r requirements-dev.txt
python scripts/build_deliverables.py
# Regenerar LaTeX/bitácora desde las ejecuciones guardadas:
python scripts/build_academic_deliverables.py
```

Las pruebas comprueban soluciones conocidas, determinantes por una definición independiente, identidades de la inversa, familias paramétricas, reproducción de cada operación de fila, pivoteo, entradas inválidas y recorridos de los formularios web. La automatización de GitHub ejecuta las pruebas al recibir cambios.

La comprobación visual es un paso separado de AppTest. Con el servidor ya iniciado y Playwright instalado, `python scripts/browser_check.py` prueba la página y guarda capturas en `docs/screenshots/`. Se puede indicar `--browser /ruta/al/ejecutable` para usar un Chromium o Brave instalado. Se incluyen capturas reales y el resultado de **7 comprobaciones aprobadas** en `docs/logs/browser.json`, incluida la interfaz del tutor sin realizar llamadas a OpenAI.

## Arquitectura

```text
agent.py                  Validación, Gauss, Gauss-Jordan, inversa, explicación
scenarios.py              Datos originales y variantes independientes
reporting.py              Formato de matrices, guías y exportaciones
main.py                   Consola, JSON y batería de escenarios
app.py                    Interfaz Streamlit
web/                      React/TypeScript, Tailwind y componentes shadcn/ui
api/solve.py              API Python serverless para Vercel
api/tutor.py              Tutor IA serverless mediante Responses API
ai_tutor.py               Contexto matemático, API Responses y cuota diaria
tutor_ui.py               Chat y explicación opcional de pasos
scripts/build_deliverables.py  Ejemplos, bitácora y documento técnico
scripts/build_academic_deliverables.py  IEEEtran y entregables de la rúbrica
bitacora/                 Ejecuciones completas y bitácora académica
examples/                 Entradas reutilizables
tests/                    Pruebas de resultados y recorridos de interfaz
```

El motor no utiliza `numpy.linalg.solve`, `inv`, `det` ni `matrix_rank`. Gauss-Jordan y la inversa comparten el algoritmo de operaciones de fila, aplicado respectivamente a `[A|B]` y `[A|I]`; la inversa se multiplica por B después. El determinante se calcula antes de resolver, mediante los pivotes y la paridad de los intercambios. La aritmética exacta evita confundir determinantes pequeños con cero.

## Alcance de negocio

Este proyecto es un **prototipo funcional para demostración y piloto**, con trazabilidad como principal valor. No se afirma que una solución positiva sea óptima: no hay función objetivo, costos ni demanda en la guía. Para optimización real hacen falta esos datos y posiblemente `AX≤B`, restricciones enteras u otras condiciones. Autenticación, persistencia multiusuario, integraciones ERP y despliegue administrado no están implementados.

X está en miles de unidades: los coeficientes se interpretan como consumo **por mil módulos** para mantener coherencia dimensional. El 100% corresponde al modelo de igualdades, no a una garantía sobre operaciones reales.
