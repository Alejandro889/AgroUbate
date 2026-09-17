# AgroUbaté AI

Aplicativo web que ayuda a un ganadero de la provincia de Ubaté (Cundinamarca) a
encontrar la combinación de **tienda de insumos** y **centro de acopio de leche**
que maximiza su margen neto mensual.

Construido con Python + Streamlit. Corre 100% en local, sin servicios pagos ni
claves de API obligatorias.

**Hay dos formas de verlo funcionar:**

1. **`agroubate.html`** — versión de un solo archivo, sin instalar nada. Haz doble
   clic y se abre en tu navegador. Tiene el mismo formulario, el mismo motor de
   cálculo (portado a JavaScript) y el mismo mapa, con los datos ya incluidos
   dentro del archivo. Ideal para verla rápido o mostrarla sin configurar un entorno.
2. **`app.py`** (Streamlit) — la versión completa del proyecto, con el código en
   Python tal como se documentó en los Eslabones 1 a 6. Requiere instalar
   dependencias (ver abajo).

## Estructura de carpetas

```
AgroUbate/
├── agroubate.html          # Versión de un solo archivo (abrir con doble clic)
├── app.py                  # Interfaz Streamlit (formulario, resultados, mapa)
├── requirements.txt        # Dependencias del proyecto (para app.py)
├── src/
│   ├── datos.py             # Carga de datos y coordenadas de municipios
│   └── modelo.py            # Fórmulas económicas (Eslabón 3)
├── data/
│   ├── tiendas_insumos.json
│   ├── centros_acopio.json
│   └── fuentes.md            # Citas de las fuentes reales usadas
├── docs/                     # Entregables de cada eslabón del proceso
├── bitacora_prompts.md       # Bitácora de prompts (entregable académico)
└── registro_errores.md       # Registro de errores (entregable académico)
```

## Opción rápida: `agroubate.html`

1. Descarga o clona el repositorio.
2. Haz doble clic en `agroubate.html` (o ábrelo con "Abrir con → tu navegador").
3. Completa el formulario y presiona **Calcular la mejor combinación**.

Necesitas internet solo para que carguen la librería del mapa (Leaflet, vía CDN)
y las imágenes de OpenStreetMap; el cálculo funciona igual sin conexión, y si el
mapa no carga verás un aviso claro en vez de un error, sin que se rompa el resto
de la página. Los datos de tiendas y centros de acopio están embebidos dentro
del propio archivo HTML, por eso no hace falta ningún servidor local.

## Requisitos

- Python 3.10 o superior instalado ([python.org/downloads](https://www.python.org/downloads/)).
- Conexión a internet solo para: (a) instalar las dependencias la primera vez, y
  (b) cargar las teselas del mapa (OpenStreetMap, gratuitas, sin clave de API).
  El cálculo y la lógica del aplicativo funcionan sin internet.

## Instrucciones de ejecución

### Windows

```
cd AgroUbate
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```
cd AgroUbate
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit abrirá automáticamente el navegador en `http://localhost:8501`. Si no
se abre solo, copia esa dirección en tu navegador.

Para cerrar la app, vuelve a la terminal y presiona `Ctrl + C`.

## Uso

1. Completa el formulario con la producción diaria de tu finca, la calidad de tu
   leche y los insumos que compras al mes.
2. Presiona **Calcular la mejor combinación**.
3. Verás la combinación óptima de tienda + centro de acopio, el margen neto
   mensual, la comparación contra la peor opción viable y contra el promedio de
   la región, la tabla completa de combinaciones y el mapa de la provincia.
