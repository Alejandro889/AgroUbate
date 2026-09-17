# Eslabón 3 — Lógica de negocio

## 1. Variables de entrada (las ingresa el ganadero en el formulario)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `litros_dia` | Producción diaria de leche (L) | 80 |
| `ubicacion_finca` | Municipio (y opcionalmente coordenadas) de la finca | Cucunubá |
| `grasa_pct`, `proteina_pct`, `solidos_totales_pct` | Composición de la leche (%) | 3.6 / 3.2 / 12.5 |
| `ufc_ml` | Recuento bacteriano (UFC/mL) | 20.000 |
| `bultos_concentrado_mes`, `bultos_sal_mes` | Cantidad mensual de insumos a granel | 4 / 1 |
| `unidades_antiparasitario_mes`, `unidades_antibiotico_mes` | Cantidad mensual de estos insumos | 1 / 1 |
| `viajes_tienda_mes` | Veces que el ganadero viaja a comprar insumos en el mes | 1 |
| `costo_por_km` | Costo de transporte por kilómetro (combustible + desgaste) | $700 (valor por defecto, editable) |
| `dias_mes` | Días del mes a proyectar | 30 |

## 2. Variables que calcula el sistema

| Variable | Cómo se obtiene |
|---|---|
| `distancia_finca_tienda_km`, `distancia_finca_acopio_km` | Fórmula de Haversine entre las coordenadas de la finca y las de cada establecimiento del dataset |
| `precio_final_litro` | Precio base del acopio + bonificaciones/penalizaciones por calidad |
| `ingreso_mensual` | A partir de `litros_dia`, `dias_mes` y `precio_final_litro` |
| `costo_insumos_mensual` | Suma de precios de insumos con descuento por volumen, más transporte a la tienda |
| `costo_entrega_leche_mensual` | Solo si el acopio no recoge en finca |
| `margen_neto_mensual` | Ingreso − costo insumos − costo entrega de leche |

## 3. Fórmulas

**Distancia (Haversine)**, con R = 6.371 km:

```
d_km = 2R · arcsin( √( sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2) ) )
```

**Precio final por litro** (el sistema de pago por calidad colombiano es *marginal*: paga o penaliza la diferencia frente a una composición de referencia, no el contenido total — de lo contrario el bono superaría el precio base):

```
Δgrasa    = grasa_pct − grasa_ref
Δproteina = proteina_pct − proteina_ref
Δsolidos  = solidos_totales_pct − solidos_ref

precio_final_litro = precio_base_litro
                    + (Δgrasa    × 10 × precio_grasa_gramo)
                    + (Δproteina × 10 × precio_proteina_gramo)
                    + (Δsolidos  × 10 × precio_solidos_gramo)
                    + bonificacion_ufc_litro(ufc_ml)
```
*(el factor ×10 convierte % de composición a gramos por litro, asumiendo densidad ≈ 1.000 g/L)*

> **Supuesto a validar:** se usó como referencia de composición estándar grasa=3,0%, proteína=3,0%, sólidos totales=11,3% (valores típicos de la industria). La tabla oficial no publica estos valores de referencia de forma abierta en las fuentes consultadas en el Eslabón 2, así que este punto queda marcado como **ESTIMADO** — ver pregunta de validación 4.

**Ingreso mensual:**
```
ingreso_mensual = litros_dia × dias_mes × precio_final_litro
```

**Costo mensual de insumos:**
```
costo_insumos_bruto   = Σ (cantidad_i × precio_unitario_i)
costo_insumos_neto    = costo_insumos_bruto × (1 − %descuento_volumen si total_bultos ≥ umbral_tienda)
costo_transporte_insumos = distancia_finca_tienda_km × 2 (ida y vuelta) × costo_por_km × viajes_tienda_mes
costo_insumos_mensual = costo_insumos_neto + costo_transporte_insumos
```

**Costo de transporte (genérico, reutilizado para insumos y para entrega de leche):**
```
costo_transporte = distancia_km × numero_de_viajes_ida_y_vuelta_al_mes × costo_por_km
```

**Costo de entrega de leche** (solo si `recoge_en_finca = false`):
```
dias_entrega_mes = 30 si frecuencia_recoleccion = "Diaria"; 15 si = "Interdiaria"
costo_entrega_leche_mensual = distancia_finca_acopio_km × 2 × costo_por_km × dias_entrega_mes
```
Si `recoge_en_finca = true`, este costo es 0.

**Margen neto mensual:**
```
margen_neto_mensual = ingreso_mensual − costo_insumos_mensual − costo_entrega_leche_mensual
```

**Restricción de factibilidad:**
Una combinación (tienda, acopio) solo es válida si `litros_dia ≥ volumen_minimo_litros_dia` del acopio. Las combinaciones que no cumplen se excluyen del ranking de "óptimas" pero se listan aparte con el mensaje: *"No disponible: [acopio] exige mínimo X L/día y tu producción es de Y L/día (te faltan Z L/día)."*

**Combinación óptima:**
```
combinacion_optima = argmax(margen_neto_mensual) entre todas las combinaciones factibles
```

**Regla de desempate** — se aplica si `|margen_A − margen_B| < max($20.000, 1% del mayor margen)`:
1. Menor `plazo_pago_dias` del acopio (mejor flujo de caja).
2. Menor distancia total (`distancia_finca_tienda_km + distancia_finca_acopio_km`).
3. Preferir `recoge_en_finca = true` sobre `false`.

## 4. Ejemplo numérico resuelto (perfil: finca en Cucunubá, 80 L/día)

**Datos de entrada:** litros_dia=80, dias_mes=30, grasa=3,6%, proteína=3,2%, sólidos totales=12,5%, UFC=20.000, insumos mensuales: 4 bultos concentrado + 1 bulto sal + 1 antiparasitario + 1 antibiótico, 1 viaje/mes a la tienda, costo_por_km=$700.

**Combinación A (candidata a óptima): Tienda T05 (Contrigran, Cucunubá) + Acopio A07 (Centro de Acopio Cucunubá, recoge en finca, mínimo 40 L/día → factible)**

- Costo insumos bruto = 4×101.000 + 1×94.500 + 39.000 + 46.000 = **$583.500** (5 bultos, no alcanza el umbral de descuento de T05 de 25 bultos → sin descuento)
- Distancia finca–tienda ≈ 1 km → costo transporte insumos = 1×2×700×1 = **$1.400**
- **Costo insumos mensual = $584.900**
- Bonificación por calidad: Δgrasa=0,6→6g×14,40=$86,40; Δproteína=0,2→2g×43,22=$86,44; Δsólidos=1,2→12g×15,28=$183,36; UFC (tramo 0-25.000)=$174 → **bonificación total = $530,20/L**
- Precio final = 1.745 + 530,20 = **$2.275,20/L**
- **Ingreso mensual = 80 × 30 × 2.275,20 = $5.460.480**
- Costo entrega leche = $0 (recoge en finca)
- **Margen neto mensual = 5.460.480 − 584.900 − 0 = $4.875.580**

**Combinación excluida por infactibilidad: Tienda T01 (Ubaté) + Acopio A01 (Doña Leche, Ubaté, mínimo 150 L/día)** → *"No disponible: Doña Leche exige mínimo 150 L/día y tu producción es de 80 L/día (te faltan 70 L/día)."*

**Combinación B (peor opción viable, para comparar): Tienda T09 (Carmen de Carupa) + Acopio A10 (Carmen de Carupa, no recoge en finca, interdiaria, mínimo 25 L/día → factible)**

- Costo insumos bruto = 4×100.000 + 103.000 + 37.500 + 45.500 = **$586.000**
- Distancia finca–tienda ≈ 18 km → transporte insumos = 18×2×700×1 = **$25.200**
- **Costo insumos mensual = $611.200**
- Misma calidad de leche → misma bonificación $530,20/L. Precio final = 1.705 + 530,20 = **$2.235,20/L**
- **Ingreso mensual = 80 × 30 × 2.235,20 = $5.364.480**
- No recoge en finca, interdiaria → 15 viajes/mes. Distancia finca–acopio ≈ 18 km → costo entrega = 18×2×700×15 = **$378.000**
- **Margen neto mensual = 5.364.480 − 611.200 − 378.000 = $4.375.280**

**Comparativo:** la Combinación A (óptima) supera a la Combinación B en **$500.300/mes**. El "promedio de la región" que mostrará la app se calcula promediando el margen neto de **todas** las combinaciones factibles del dataset (hasta 11×12=132, menos las excluidas por volumen mínimo); en este ejemplo reducido de 2 combinaciones, el promedio ilustrativo es (4.875.580+4.375.280)/2 = **$4.625.430/mes**.

## 5. Manejo del caso "ningún acopio cumple el volumen mínimo"

Si `litros_dia` es menor al volumen mínimo de **todos** los acopios disponibles, la app no debe fallar ni mostrar una tabla vacía sin explicación: debe mostrar el mensaje *"Con tu producción actual de X L/día, ningún centro de acopio de la región la acepta directamente. El volumen mínimo más bajo disponible es Y L/día, en [nombre del acopio]. Te faltan Z L/día."* y sugerir la opción de asociarse con otros productores para alcanzar el mínimo (mención informativa, sin cálculo adicional en esta versión).
