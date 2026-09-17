# Eslabón 5 — Validación de errores

## Cómo se blindó la entrada de datos

Streamlit obliga por diseño a que los campos numéricos solo acepten números (no se puede escribir texto en un `number_input`), y los límites `min_value`/`max_value` de cada campo ya impiden negativos y valores fuera de rango razonable. Esto cubre de raíz varios de los casos pedidos (texto en campo numérico, negativos, campo vacío — todos los campos tienen un valor por defecto). Sobre esa base, se añadieron validaciones de negocio que Streamlit no puede cubrir por sí solo.

| # | Caso de validación | Mecanismo | Mensaje al usuario |
|---|---|---|---|
| 1 | Litros/día negativo, cero o en texto | `st.number_input(min_value=1.0, max_value=2000.0)` | El campo simplemente no permite escribir un valor fuera de ese rango (feedback nativo de Streamlit). |
| 2 | % de grasa/proteína/sólidos/UFC negativos o absurdos | `min_value`/`max_value` en cada campo | Igual que arriba. |
| 3 | Campo numérico vacío | Todos los `number_input` tienen `value=` por defecto | No es posible dejar un campo vacío; siempre parte de un valor válido editable. |
| 4 | Composición físicamente inconsistente (grasa + proteína > sólidos totales) | Validación de negocio en `app.py` tras el envío del formulario | *"Revisa los porcentajes de calidad: la grasa más la proteína (X%) superan los sólidos totales que ingresaste (Y%), lo cual no es físicamente posible en la leche... El cálculo continúa, pero corrígelos si fue un error de digitación."* (advertencia, no bloquea) |
| 5 | Coordenadas fuera de la región | No aplica: el ganadero elige su municipio de una lista cerrada de los 10 municipios de la provincia; no ingresa coordenadas libres. | — |
| 6 | Archivo de datos (`tiendas_insumos.json` / `centros_acopio.json`) faltante | `DatosInvalidosError` en `src/datos.py`, capturado en `app.py` | *"⚠️ No se pudo iniciar el aplicativo: No se encontró el archivo de datos '...'. Verifica que la carpeta 'data' esté completa junto al aplicativo."* |
| 7 | Archivo de datos corrupto / JSON mal formado | `json.JSONDecodeError` capturado y relanzado como `DatosInvalidosError` | *"⚠️ ... El archivo de datos '...' está dañado o mal formado y no se pudo leer (línea X, columna Y). Restaura una copia válida del archivo."* |
| 8 | Registros con campos obligatorios faltantes | `_filtrar_registros_validos()` descarta el registro incompleto en vez de fallar | El registro corrupto se omite silenciosamente del cálculo; si TODOS los registros de un archivo están incompletos, se muestra: *"Ningún registro de '...' tiene los campos obligatorios completos. Revisa el archivo de datos."* |
| 9 | Ningún acopio cumple el volumen mínimo del ganadero | Verificado en `elegir_optima()` (retorna `None` si no hay factibles) | *"Con tu producción actual de X L/día, ningún centro de acopio de la región la acepta directamente. El volumen mínimo más bajo disponible es Y L/día, en [acopio]. Te faltan Z L/día. Considera asociarte con otros productores..."* |
| 10 | División por cero | No existe ninguna operación de división por un valor que pueda ser cero en el motor de cálculo (`src/modelo.py`); el único promedio (`factibles["margen_neto_mensual"].mean()`) solo se calcula cuando ya se confirmó que `factibles` no está vacío. | No aplica (prevenido estructuralmente). |
| 11 | Fallo de carga del mapa (sin internet, tiles no disponibles) | `try/except` alrededor de `construir_mapa()` y `st_folium()` | *"⚠️ No se pudo cargar el mapa (puede deberse a que no tienes conexión a internet en este momento...). El cálculo del margen y la tabla de resultados no se ven afectados."* |
| 12 | Error inesperado al leer los datos (cualquier otra excepción) | `except Exception` genérico en `app.py` alrededor de la carga de datos | *"⚠️ Ocurrió un problema inesperado leyendo los datos del aplicativo. Verifica que la carpeta 'data' esté completa..."* (nunca se muestra una traza técnica cruda). |

En ningún caso el usuario ve un traceback de Python en pantalla: todos los errores previstos se capturan y se traducen a un mensaje en español que explica qué pasó y cómo corregirlo.
