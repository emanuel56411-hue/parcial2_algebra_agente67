# Auditoría de la guía del Parcial 2

## Hallazgos del código original

1. Solo estaba implementada la eliminación de Gauss. Faltaban Gauss-Jordan y la inversa.
2. No se mostraban las operaciones ni matrices intermedias.
3. B se calculaba a partir del vector esperado, sustituyendo silenciosamente las disponibilidades escritas en la guía.
4. El selector «Personalizado» no permitía introducir datos.
5. El determinante y los rangos dependían exclusivamente de funciones de NumPy; no había validación suficiente de forma, NaN/Infinity o dimensiones.
6. La singularidad se decidía por `abs(det)<1e-9`, criterio que puede confundir una matriz invertible escalada con una singular.
7. Se usaba «ÓPTIMO» sin función objetivo y se redondeaban unidades antes de discutir la naturaleza continua del modelo.
8. La batería imprimía resultados sin afirmaciones automatizadas ni comparación entre métodos.
9. Faltaban documentación de instalación, fuentes, reporte PDF y bitácora exportable.

## Estado tras la implementación

| Requisito / rúbrica | Evidencia | Estado |
|---|---|---|
| Modelo 6×6 y variables | `scenarios.py`, PDF, informe operacional | Implementado; unidades explicitadas |
| Dominio algebraico: determinante y equivalencia | `agent.py`, tests por permutaciones y comparación exacta | Implementado |
| Gauss + sustitución hacia atrás | Método `gauss`, matrices y expresiones numeradas | Implementado |
| Gauss-Jordan explícito | Método `gauss_jordan`, reducción `[A|B]→[I|X]` | Implementado |
| Inversa explícita | Reducción `[A|I]→[I|A⁻¹]`, producto fila-columna | Implementado |
| Entrada JSON o consola | `main.py`, formularios, editor, carga de archivo | Implementado |
| Validación dimensional y rangos | Validación anterior al cálculo; rango por pivotes | Implementado |
| Incompatible / infinitas soluciones | Rangos, contradicción y familia paramétrica | Implementado |
| Interpretación semántica | Agente de reglas y balance de recursos | Implementado; no es un modelo generativo |
| Vector esperado del enunciado | `examples/compatible.json` | Solo válido para B compatible; imposible con B original |
| Sustitución E<10⁻⁶ | Vector exacto de errores y prueba por cada fila | Implementado; E=0 en casos resueltos |
| Escasez B3=100 | Desde B original; dos variables negativas | Implementado |
| F6=2F1 | Casos incompatible e indeterminado | Implementado |
| Portabilidad | Núcleo sin dependencias; web instalable por pip | Implementado; pruebas locales en Python 3.14 |
| PDF técnico | `docs/informe_tecnico_ieee.tex` y `.pdf` | Clase oficial `IEEEtran`, cuerpo a dos columnas y 109 estados completos en anexos |
| Desarrollo manual | Cada operación y matriz del 6×6 en anexos | Desarrollo reproducible; no sustituye una entrega manuscrita si se exige |
| Bitácora | `bitacora/BITACORA.md` y JSON por escenario | Generada con ejecuciones reales; entrada, salida, diagnóstico y comparación |
| Capturas de la web | `scripts/browser_check.py`, `docs/screenshots/`, `docs/logs/browser.json` | 7 comprobaciones de navegador aprobadas; capturas reales conservadas en el repositorio |
| Hosting en Vercel | `web/`, `api/`, `vercel.json`, `.vercelignore` | Interfaz responsive, selector de método, procedimiento completo y Tutor IA serverless |
| Conclusiones cuantitativas | `docs/interpretacion_operaciones.md` | Implementado |

No se atribuye una calificación: la evaluación corresponde al docente.

## Ampliación: tutor opcional de OpenAI

Se incorporaron un chat sobre el sistema resuelto y una explicación del paso seleccionado mediante la API Responses. El tutor también recibe ecuaciones lineales, JSON o bloques A/B antes de usar la calculadora, los convierte de forma determinista y ejecuta el mismo motor exacto. El modelo generativo permanece independiente del cálculo: devuelve texto estructurado con marcadores y la API y el frontend descartan cifras inventadas o respuestas malformadas. Los cuatro botones contextuales, el saludo previo y la conversión de ejercicios responden sin llamar a OpenAI. La clave se configura como secreto del servidor y el historial libre no se reenvía.

La batería actual incluye **60 pruebas Python** y **5 pruebas Vitest** para el motor, la conversión segura de ejercicios escritos, el sustituidor de marcadores y el validador, además de build y ESLint. Las respuestas simuladas cubren JSON inválido, marcadores desconocidos, cifras inventadas, texto demasiado largo, tiempo límite y respaldo del motor. La comprobación de navegador cubre cálculo, procedimiento, Tutor IA y viewport móvil; también se comprobó que un saludo previo al cálculo no consume OpenAI.

## Inconsistencias que requieren aclaración académica

**Disponibilidades frente a respuesta esperada.** Con A de la guía:

```text
X esperado       = (15, 20, 25, 10, 15, 20)
A·X esperado     = (185, 200, 280, 150, 245, 195)
B original       = (155, 160, 225, 140, 215, 175)
A·X esperado − B = ( 30,  40,  55,  10,  30,  20)
```

La respuesta correcta para B original es `(-105,345,2430,1170,1130,2010)/83`. El programa no oculta que x1 es negativo. Se debe confirmar si se corrige B o la respuesta esperada; no es posible satisfacer ambos simultáneamente.

**Unidades.** Si x está en miles de módulos, los coeficientes deben estar expresados en consumo por mil módulos. Si realmente son consumos por módulo individual, debe cambiarse la escala. La interpretación adoptada se explica en el sistema y el informe.

**Singularidad.** Modificar solo F6 implica cero soluciones en estos datos porque 175≠310. Para mostrar infinitas soluciones se modifica también B6 a 310 en otro escenario claramente identificado.

**Optimización.** AX=B solo resuelve el balance. Sin una función objetivo y datos de costos/beneficios no puede justificarse un óptimo empresarial. El producto evita esa afirmación.

**Presentación académica.** El informe se genera con la clase `IEEEtran` en modalidad `conference`, cuerpo a dos columnas y apéndices completos. Incluye logotipo y nombre de la Universidad Francisco Gavidia, los tres autores y carnés, el docente Exides Gamaliel Claros Velasquez, el grupo `01 EO8` y la fecha de entrega del 23 de septiembre de 2026. Solo queda confirmar si la institución exige una variante propia de IEEE/ACM o una portada separada.
