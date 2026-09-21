# Tutor IA contextual

El tutor toma matrices, fracciones, pivotes, rangos y residuos del análisis exacto de `agent.py`. OpenAI solo propone frases breves con marcadores. La API valida el esquema estricto y el texto; ante un fallo, el motor compone la explicación. Los botones de ayuda usan directamente los pasos calculados y no llaman al modelo.

## Ejemplos renderizados

Las capturas se hicieron en Chromium con un sistema de dos variables calculado por `TechChipAgent`. La respuesta del modelo en la última captura se simuló para probar los marcadores sin gastar cuota.

- [Explicación del motor en escritorio](screenshots/tutor-escritorio.png)
- [La misma vista en móvil](screenshots/tutor-movil.png)
- [Marcadores sustituidos por KaTeX y valores exactos](screenshots/tutor-marcadores.png)

En el ejemplo de marcadores, el texto `{{det}}` se muestra como una fracción apilada con aproximación gris; `{{matriz:paso1}}` se muestra con corchetes y barra de separación. La respuesta simulada no aporta ninguna cifra del sistema.

## Verificación

```bash
venv/bin/python -m unittest discover -s tests -q
cd web && npm run test && npm run lint && npm run build
```
