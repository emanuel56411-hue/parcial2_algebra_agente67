# Mapa de entregables y rúbrica

| Criterio | Puntos | Evidencia principal |
|---|---:|---|
| Dominio de Álgebra Lineal | 20 | `docs/informe_tecnico_ieee.tex`, apéndices completos y comparación exacta |
| Modelación Empresarial | 15 | Secciones II–III del informe e `docs/interpretacion_operaciones.md` |
| Implementación del Agente IA | 20 | `agent.py`, `api/solve.py`, `api/tutor.py`, `web/` |
| Rigor Matemático | 15 | Tres trazas exactas, determinante por pivotes, rangos y pruebas |
| Pruebas y Extremos | 10 | `bitacora/BITACORA.md` y JSON completos por escenario |
| Interpretación | 10 | `docs/interpretacion_operaciones.md` |
| Documentación y Presentación | 10 | Informe IEEE, README, bitácora, interfaz y despliegue Vercel |

## Compilación del PDF IEEE

```bash
cd docs
pdflatex informe_tecnico_ieee.tex
pdflatex informe_tecnico_ieee.tex
```

La segunda ejecución actualiza referencias y numeración. Se requiere una distribución TeX que incluya `IEEEtran`, `babel`, `amsmath`, `booktabs`, `graphicx`, `hyperref` y fuentes T1.

## Datos por verificar antes de entregar

- Nombre completo, carné, docente, grupo, universidad y fecha institucional.
- Si la institución exige una variante específica de IEEE/ACM o portada separada.
- Confirmación docente de cuál vector B debe considerarse oficial.
- Confirmación de que los coeficientes son consumos por mil módulos, no por módulo individual.
