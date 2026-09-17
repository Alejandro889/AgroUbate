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

## Entrada 3

- **Eslabón:** 1 → 2 (cierre formal del Eslabón 1)
- **Técnica aplicada:** Prompt chaining (transición de fase)
- **Objetivo del prompt:** El usuario escribió "continua", que se interpreta como confirmación equivalente a "aprobado" para el Eslabón 1, dado que ya había respondido conforme a las 3 preguntas de validación sin objeciones ni solicitudes de cambio.
- **Resultado obtenido:** Se cierra el Eslabón 1 con el stack definitivo: Streamlit (Python) + pandas + streamlit-folium/Leaflet + JSON/CSV. Se inicia el Eslabón 2 (datos de la región): investigación de centros de acopio de leche y tiendas de insumos agropecuarios en la provincia de Ubaté.
- **Decisión tomada:** Avanzar al Eslabón 2 aplicando prompt chaining (la salida de este eslabón — el stack aprobado — es insumo para construir el dataset y, luego, la app). Se usará búsqueda web para maximizar la proporción de datos REALES antes de recurrir a datos SIMULADOS, respetando la regla de honestidad de datos.

---

## Entrada 4

- **Eslabón:** 2 (datos de la región)
- **Técnica aplicada:** Prompt chaining (la salida del Eslabón 1 — Streamlit/Python/JSON — define el formato de datos usado) + cadena de pensamiento (para decidir qué buscar y cómo clasificar REAL vs. SIMULADO antes de escribir el dataset)
- **Objetivo del prompt:** Construir el dataset base de tiendas de insumos agropecuarios y centros de acopio de leche en la provincia de Ubaté, aplicando la regla de honestidad de datos.
- **Resultado obtenido:** Se realizaron 12 búsquedas web dirigidas y se identificaron 9 establecimientos/organizaciones reales verificables (Doña Leche Alimentos S.A., Lácteos Villa de Ubaté, Federación de Productores Lecheros de la Provincia de Ubaté, Alquería, Cooperativa Agropecuaria del Valle de Ubaté, COOPALAC, Serviagrofinca en Ubaté y Simijaca, Contrigran), además de la tabla oficial vigente de bonificaciones por calidad de leche (Resolución 017 de 2012 actualizada, Minagricultura, Región 1) y referencias reales de precios de mercado (Solla, Italcol, Finca, Agroforr, Lares, Vecol). Se generaron `data/tiendas_insumos.json` (11 registros: 5 reales, 6 simulados), `data/centros_acopio.json` (12 registros: 4 reales, 8 simulados) y `data/fuentes.md` con la cita exacta de cada fuente real y la aclaración de qué campos son estimaciones incluso dentro de los registros reales.
- **Decisión tomada:** Etiquetar el campo `fuente` de cada registro únicamente respecto a la existencia/ubicación del establecimiento (nunca respecto a precios comerciales específicos, que siempre son estimados por no ser información pública), y dejarlo explícito en `fuentes.md` para no presentar ningún dato simulado como si fuera real. Se presenta el entregable con el resumen de proporciones (39,1% real / 60,9% simulado combinado) y se solicitan las 3 preguntas de validación del Eslabón 2 antes de cerrarlo.

---

## Entrada 5

- **Eslabón:** 2 → 3
- **Técnica aplicada:** Prompt chaining (cierre y transición de fase)
- **Objetivo del prompt:** El usuario respondió "si, si, si" a las 3 preguntas de validación del Eslabón 2 (cobertura geográfica, insumos relevantes, esquema de bonificaciones), lo que se interpreta como aprobación explícita.
- **Resultado obtenido:** Se cierra el Eslabón 2 con el dataset definitivo (`data/tiendas_insumos.json`, `data/centros_acopio.json`, `data/fuentes.md`). Se inicia el Eslabón 3 (lógica de negocio).
- **Decisión tomada:** Avanzar al Eslabón 3 usando el dataset aprobado como insumo directo (prompt chaining).

---

## Entrada 6

- **Eslabón:** 3 (lógica de negocio)
- **Técnica aplicada:** Prompt chaining (usa el dataset del Eslabón 2 como entrada) + cadena de pensamiento (para decidir cómo modelar el precio por calidad de forma realista)
- **Objetivo del prompt:** Formular las fórmulas de ingreso, costo de insumos, costo de transporte, costo de entrega de leche y margen neto, definir variables de entrada/calculadas, reglas de desempate, manejo de volumen mínimo no alcanzado, y resolver un ejemplo numérico con cifras del dataset ya aprobado.
- **Resultado obtenido:** Se detectó que aplicar el precio por gramo de proteína/grasa/sólidos al contenido TOTAL de la leche (en vez de a la diferencia frente a una composición de referencia) generaría bonificaciones irrealmente altas (>$500 extra por litro sobre un precio base de ~$1.750). Se corrigió el modelo a un esquema marginal (diferencia sobre referencia), consistente con cómo opera en la práctica el sistema de pago por calidad colombiano, dejando explícitamente marcada como ESTIMADA la composición de referencia usada (grasa 3,0%, proteína 3,0%, sólidos totales 11,3%) porque no se encontró publicada en las fuentes del Eslabón 2. Se escribió `docs/eslabon-3-logica-negocio.md` con todas las fórmulas, la tabla de variables, las reglas de desempate, el manejo del caso "ningún acopio cumple el volumen mínimo", y un ejemplo numérico resuelto paso a paso (finca en Cucunubá, 80 L/día) comparando una combinación óptima ($4.875.580/mes) contra una peor opción viable ($4.375.280/mes) y una combinación excluida por no alcanzar el volumen mínimo.
- **Decisión tomada:** Presentar el entregable y solicitar 4 preguntas de validación (transporte, plazo de pago, perfil de litros/día, y la composición de referencia estimada) antes de cerrar el Eslabón 3.

---

<!-- Se añade una nueva entrada al cerrar cada eslabón (cuando el usuario escriba "aprobado" o equivalente) y cada vez que el usuario reporte un error o dé retroalimentación relevante. -->
