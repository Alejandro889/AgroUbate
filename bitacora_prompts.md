# Bitácora de prompts — AgroUbaté AI

Registro cronológico de cada prompt recibido y cada respuesta entregada durante la construcción del aplicativo, aplicando cadena de pensamiento, prompt chaining y ReAct.

---

## Entrada 1

- **Eslabón:** 0 → 1 (mensaje de arranque general del proyecto + primer entregable del Eslabón 1)
- **Técnica aplicada:** Prompt chaining (definición del método completo de 6 eslabones y puerta de aprobación) + ReAct (ejecutado en el Eslabón 1)
- **Objetivo del prompt:** Establecer el rol, el contexto de negocio (ganaderos de la provincia de Ubaté), el método de trabajo obligatorio (cadena de pensamiento, prompt chaining, ReAct), la puerta de aprobación por eslabón, y arrancar formalmente el Eslabón 1 (selección de herramientas).
- **Resultado obtenido:** Se creó la estructura de repositorio inicial, el archivo `docs/eslabon-1-seleccion-herramientas.md` con el ciclo ReAct completo (Pensamiento → Acción → Observación → Acción), una tabla comparativa de 4 stacks puntuados 1-5 en cinco criterios, y la recomendación del stack ganador: **Streamlit (Python) + pandas + streamlit-folium/Leaflet + JSON/CSV**.
- **Decisión tomada:** Presentar el entregable del Eslabón 1 y las preguntas de validación obligatorias, y **esperar** la aprobación explícita del usuario antes de avanzar al Eslabón 2, tal como exige la puerta de aprobación. No se adelantó trabajo de los eslabones 2 a 6 pese a que el mensaje original ya contenía sus instrucciones completas; esa información se guardó para usarse cuando corresponda.

---

## Entrada 2

- **Eslabón:** 1 (respuesta a las preguntas de validación)
- **Técnica aplicada:** ReAct (cierre del ciclo iniciado en la Entrada 1)
- **Objetivo del prompt:** El usuario respondió las 3 preguntas de validación del Eslabón 1: (a) especificaciones del equipo (captura de pantalla: HP ProOne 440 G9, Intel Core i7-12700T, 32,0 GB RAM, 477 GB de almacenamiento, Windows 11 Pro), (b) el docente no exige un lenguaje específico pero se usará Python, (c) prioridad: equilibrio entre buena interfaz y buen funcionamiento (ni solo simplicidad, ni solo realismo).
- **Resultado obtenido:** Se confirmó que el hardware (32 GB RAM, i7 de 12.ª generación) elimina cualquier restricción de consumo de recursos, que Python coincide con el stack ya recomendado, y que Streamlit sigue siendo la opción correcta porque permite lograr una interfaz cuidada (columnas, pestañas, tema, mapas y gráficos interactivos) sin necesitar HTML/CSS/JS manual. No se detectaron contradicciones ni ambigüedades en las respuestas.
- **Decisión tomada:** Mantener el stack recomendado (Streamlit + pandas + streamlit-folium/Leaflet + JSON/CSV) y solicitar la confirmación explícita ("aprobado") para cerrar formalmente el Eslabón 1 antes de iniciar el Eslabón 2 (datos de la región).

---

<!-- Se añade una nueva entrada al cerrar cada eslabón (cuando el usuario escriba "aprobado" o equivalente) y cada vez que el usuario reporte un error o dé retroalimentación relevante. -->
