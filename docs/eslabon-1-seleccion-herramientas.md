# Eslabón 1 — Selección de herramientas (ReAct)

## Ciclo ReAct

**Pensamiento:**
El aplicativo "AgroUbaté AI" necesita cuatro capacidades funcionales: (1) persistencia de datos de tiendas de insumos y centros de acopio, (2) un motor de cálculo que aplique fórmulas económicas (ingresos, costos, márgenes), (3) una visualización geográfica (mapa) de los establecimientos, y (4) un mecanismo de despliegue simple. Las restricciones del proyecto son más determinantes que las capacidades: el usuario final (o quien evalúe el trabajo) no tiene experiencia en programación, la entrega debe ser una carpeta comprimida autocontenida con sus dependencias, y la app debe ejecutarse en local sin servicios pagos ni claves de API obligatorias (esto descarta Google Maps API, bases de datos en la nube, hosting pago, etc.). Esto orienta la búsqueda hacia stacks que minimicen pasos de instalación, no requieran build tools complejos, y usen mapas basados en OpenStreetMap/Leaflet (gratuitos, sin API key).

**Acción:**
Se evaluaron 4 alternativas viables para este caso, cubriendo el espectro desde "sin backend" hasta "stack profesional con backend en Node":

1. **Streamlit (Python)** — framework para apps de datos, formularios y tablas con pocas líneas de Python, con soporte nativo o vía librerías (`streamlit-folium`, `pydeck`) para mapas con capas de OpenStreetMap sin clave de API.
2. **Flask + SQLite + Leaflet.js** — backend clásico en Python que sirve páginas HTML con plantillas Jinja2, base de datos SQLite local (un solo archivo), y Leaflet.js para el mapa.
3. **HTML/CSS/JavaScript estático (vanilla) + Leaflet.js** — sin servidor ni backend; toda la lógica corre en el navegador, los datos se cargan desde un archivo JSON local, y el mapa usa Leaflet con teselas de OpenStreetMap.
4. **React + Vite + Node/Express + Leaflet** — stack moderno de frontend con build tool (Vite), backend en Node/Express, y mapa con react-leaflet.

**Observación:**
A continuación la tabla comparativa puntuada de 1 (peor) a 5 (mejor) en cada criterio.

### Criterio de puntuación

- **Facilidad de implementación (1-5):** qué tan directo es traducir los requisitos (formulario, cálculo, tabla, mapa) en código funcional, sin pasos intermedios de configuración.
- **Consumo de recursos de hardware (1-5):** más alto = más liviano (menos RAM/CPU/disco necesarios para correr la app en un computador modesto).
- **Velocidad de desarrollo (1-5):** cuánto código y tiempo toma llegar a una versión funcional completa (los 6 eslabones).
- **Facilidad de empaquetado y entrega (1-5):** qué tan simple es comprimir la carpeta y que otra persona sin experiencia la ejecute (instalación, comandos requeridos).
- **Curva de aprendizaje (1-5):** más alto = más fácil de entender y modificar para alguien sin experiencia en programación (menos lenguajes/tecnologías simultáneas).

| Stack | Facilidad de implementación | Consumo de recursos | Velocidad de desarrollo | Facilidad de empaquetado y entrega | Curva de aprendizaje | **Puntaje total (máx. 25)** |
|---|---|---|---|---|---|---|
| **Streamlit (Python)** | 5 | 4 | 5 | 4 | 5 | **23** |
| HTML/CSS/JS estático + Leaflet.js | 4 | 5 | 3 | 5 | 3 | 20 |
| Flask + SQLite + Leaflet.js | 3 | 3 | 3 | 3 | 3 | 15 |
| React + Vite + Node/Express + Leaflet | 2 | 2 | 2 | 2 | 1 | 9 |

**Justificación breve por fila:**
- *Streamlit* concentra formulario, cálculo, tabla y mapa en un único lenguaje (Python), se ejecuta con un solo comando (`streamlit run app.py`) y no exige entender HTML/CSS/JS ni configurar un servidor manualmente.
- *HTML/JS estático* es el más liviano y el más fácil de entregar (abrir `index.html` en el navegador, cero instalación), pero exige escribir a mano la lógica de validación y renderizado, lo que sube el esfuerzo de desarrollo y la dificultad de mantenimiento para alguien sin experiencia.
- *Flask* añade una capa de servidor y rutas que no aporta valor frente a Streamlit para este alcance, y complica la entrega (hay que dejar el servidor corriendo).
- *React + Node* es el stack más "profesional" pero also el más pesado de instalar (node_modules puede pesar cientos de MB), el más lento de arrancar desde cero, y el más difícil de leer/modificar sin experiencia previa en JavaScript.

**Acción (recomendación):**
Stack ganador: **Streamlit (Python) + pandas (motor de cálculo) + streamlit-folium/Leaflet (mapa con OpenStreetMap, sin API key) + JSON/CSV como almacenamiento de datos**.

Gana porque es el único stack que resuelve las cuatro necesidades (formulario, cálculo, tabla, mapa) en un solo lenguaje simple de leer, se empaqueta con `requirements.txt` y se ejecuta con un único comando, sin necesidad de servicios pagos ni claves de API.
