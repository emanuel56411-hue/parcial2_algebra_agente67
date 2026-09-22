# Mapa de entregables y rúbrica

| Criterio | Puntos | Evidencia principal |
|---|---:|---|
| Dominio de Álgebra Lineal | 20 | `docs/informe_tecnico_ieee.tex`, apéndices completos y comparación exacta |
| Modelación Empresarial | 15 | Secciones II–III del informe e `docs/interpretacion_operaciones.md` |
| Implementación del Agente IA | 20 | `agent.py`, `exercise_parser.py`, `api/solve.py`, `api/tutor.py`, `web/` |
| Rigor Matemático | 15 | Tres trazas exactas, determinante por pivotes, rangos y pruebas |
| Pruebas y Extremos | 10 | `bitacora/BITACORA.md` y JSON completos por escenario |
| Interpretación | 10 | `docs/interpretacion_operaciones.md` |
| Documentación y Presentación | 10 | Informe IEEE, README, bitácora, interfaz y despliegue Vercel |

La comparación detallada con las seis fotos está en [`auditoria_guia_fotos.md`](auditoria_guia_fotos.md). El cálculo independiente de determinante y solución por Cramer puede repetirse con `python scripts/verify_photo_matrix.py`.

## Compilación del PDF IEEE

```bash
cd docs
pdflatex informe_tecnico_ieee.tex
pdflatex informe_tecnico_ieee.tex
```

La segunda ejecución actualiza referencias y numeración. Se requiere una distribución TeX que incluya `IEEEtran`, `babel`, `amsmath`, `booktabs`, `graphicx`, `hyperref` y fuentes T1.

## Identificación institucional incorporada

| Campo | Dato |
|---|---|
| Universidad | Universidad Francisco Gavidia |
| Docente | Exides Gamaliel Claros Velasquez |
| Grupo | 01 EO8 |
| Fecha de entrega | 23 de septiembre de 2026 |

## Datos por verificar antes de entregar

- Si la institución exige una variante específica de IEEE/ACM o portada separada.
- El B impreso es el caso oficial del paquete; el vector indicado se documenta como resultado incorrecto.
- Confirmación de que los coeficientes son consumos por mil módulos, no por módulo individual.
