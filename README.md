# AgroUbaté AI

Aplicativo web que ayuda a un ganadero de la provincia de Ubaté (Cundinamarca) a
encontrar la combinación de **tienda de insumos** y **centro de acopio de leche**
que maximiza su margen neto mensual.

Construido con Python + Streamlit. Corre 100% en local, sin servicios pagos ni
claves de API obligatorias.

## Estructura de carpetas

```
AgroUbate/
├── app.py                 # Interfaz Streamlit (formulario, resultados, mapa)
├── requirements.txt       # Dependencias del proyecto
├── src/
│   ├── datos.py            # Carga de datos y coordenadas de municipios
│   └── modelo.py           # Fórmulas económicas (Eslabón 3)
├── data/
│   ├── tiendas_insumos.json
│   ├── centros_acopio.json
│   └── fuentes.md           # Citas de las fuentes reales usadas
├── docs/                    # Entregables de cada eslabón del proceso
├── bitacora_prompts.md      # Bitácora de prompts (entregable académico)
└── registro_errores.md      # Registro de errores (entregable académico)
```

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
