"""Motor de cálculo económico de AgroUbaté AI (fórmulas del Eslabón 3)."""

import math

import pandas as pd

RADIO_TIERRA_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia en línea recta entre dos coordenadas geográficas."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * RADIO_TIERRA_KM * math.asin(math.sqrt(min(1.0, a)))


def _bonificacion_ufc(ufc: float, acopio: pd.Series) -> float:
    prefijo = "bonificaciones_calidad.bonificacion_calidad_higienica_ufc_ml."
    if ufc <= 25000:
        return acopio[prefijo + "0_25000"]
    if ufc <= 100000:
        return acopio[prefijo + "25001_100000"]
    if ufc <= 300000:
        return acopio[prefijo + "100001_300000"]
    return acopio[prefijo + "mas_300000"]


def precio_final_litro(
    acopio: pd.Series,
    grasa_pct: float,
    proteina_pct: float,
    solidos_pct: float,
    ufc: float,
    grasa_ref: float,
    proteina_ref: float,
    solidos_ref: float,
) -> tuple[float, float]:
    """Precio pagado por litro = precio base + bonificación/penalización por calidad.

    El bono se calcula sobre la DIFERENCIA frente a una composición de
    referencia (esquema marginal), no sobre el contenido total, tal como
    se documentó y corrigió en el Eslabón 3.
    """
    d_grasa = grasa_pct - grasa_ref
    d_proteina = proteina_pct - proteina_ref
    d_solidos = solidos_pct - solidos_ref
    bonificacion = (
        d_grasa * 10 * acopio["bonificaciones_calidad.grasa_por_gramo"]
        + d_proteina * 10 * acopio["bonificaciones_calidad.proteina_por_gramo"]
        + d_solidos * 10 * acopio["bonificaciones_calidad.solidos_totales_por_gramo"]
        + _bonificacion_ufc(ufc, acopio)
    )
    return acopio["precio_base_litro"] + bonificacion, bonificacion


def costo_insumos_mensual(
    tienda: pd.Series, cantidades: dict, distancia_km: float, costo_km: float, viajes_mes: int
) -> tuple[float, float, float]:
    bruto = (
        cantidades["bultos_concentrado"] * tienda["precios.concentrado_lechero_bulto_40kg"]
        + cantidades["bultos_sal"] * tienda["precios.sal_mineralizada_bulto_40kg"]
        + cantidades["unidades_antiparasitario"] * tienda["precios.antiparasitario_comun"]
        + cantidades["unidades_antibiotico"] * tienda["precios.antibiotico_comun"]
    )
    total_bultos = cantidades["bultos_concentrado"] + cantidades["bultos_sal"]
    descuento_pct = 0.0
    if total_bultos >= tienda["descuento_volumen.umbral_bultos"]:
        descuento_pct = tienda["descuento_volumen.porcentaje"] / 100.0
    neto = bruto * (1 - descuento_pct)
    transporte = distancia_km * 2 * costo_km * viajes_mes
    return neto + transporte, bruto, transporte


def costo_entrega_leche(acopio: pd.Series, distancia_km: float, costo_km: float) -> float:
    if bool(acopio["recoge_en_finca"]):
        return 0.0
    dias_mes_entrega = 30 if acopio["frecuencia_recoleccion"] == "Diaria" else 15
    return distancia_km * 2 * costo_km * dias_mes_entrega


def calcular_combinaciones(
    tiendas_df: pd.DataFrame,
    acopios_df: pd.DataFrame,
    finca_lat: float,
    finca_lon: float,
    litros_dia: float,
    dias_mes: int,
    grasa_pct: float,
    proteina_pct: float,
    solidos_pct: float,
    ufc: float,
    cantidades: dict,
    viajes_tienda_mes: int,
    costo_km: float,
    grasa_ref: float = 3.0,
    proteina_ref: float = 3.0,
    solidos_ref: float = 11.3,
) -> pd.DataFrame:
    filas = []
    for _, tienda in tiendas_df.iterrows():
        d_tienda = haversine_km(finca_lat, finca_lon, tienda["latitud"], tienda["longitud"])
        costo_ins, ins_bruto, transp_ins = costo_insumos_mensual(
            tienda, cantidades, d_tienda, costo_km, viajes_tienda_mes
        )
        for _, acopio in acopios_df.iterrows():
            d_acopio = haversine_km(finca_lat, finca_lon, acopio["latitud"], acopio["longitud"])
            factible = litros_dia >= acopio["volumen_minimo_litros_dia"]
            precio_l, bono = precio_final_litro(
                acopio, grasa_pct, proteina_pct, solidos_pct, ufc, grasa_ref, proteina_ref, solidos_ref
            )
            ingreso = litros_dia * dias_mes * precio_l
            costo_entrega = costo_entrega_leche(acopio, d_acopio, costo_km)
            margen = ingreso - costo_ins - costo_entrega
            filas.append(
                {
                    "tienda_id": tienda["id"],
                    "tienda_nombre": tienda["nombre"],
                    "tienda_municipio": tienda["municipio"],
                    "acopio_id": acopio["id"],
                    "acopio_nombre": acopio["nombre"],
                    "acopio_municipio": acopio["municipio"],
                    "factible": factible,
                    "volumen_minimo": acopio["volumen_minimo_litros_dia"],
                    "distancia_tienda_km": round(d_tienda, 1),
                    "distancia_acopio_km": round(d_acopio, 1),
                    "precio_final_litro": round(precio_l, 2),
                    "bonificacion_litro": round(bono, 2),
                    "ingreso_mensual": round(ingreso, 0),
                    "costo_insumos_mensual": round(costo_ins, 0),
                    "costo_entrega_mensual": round(costo_entrega, 0),
                    "margen_neto_mensual": round(margen, 0),
                    "plazo_pago_dias": acopio["plazo_pago_dias"],
                    "recoge_en_finca": bool(acopio["recoge_en_finca"]),
                }
            )
    return pd.DataFrame(filas)


def elegir_optima(df: pd.DataFrame):
    """Aplica la restricción de factibilidad y las reglas de desempate del Eslabón 3."""
    factibles = df[df["factible"]].copy()
    if factibles.empty:
        return None, factibles

    factibles = factibles.sort_values("margen_neto_mensual", ascending=False).reset_index(drop=True)
    margen_max = factibles.iloc[0]["margen_neto_mensual"]
    tolerancia = max(20000, 0.01 * abs(margen_max))
    empatados = factibles[(margen_max - factibles["margen_neto_mensual"]).abs() < tolerancia].copy()

    if len(empatados) > 1:
        empatados["distancia_total"] = empatados["distancia_tienda_km"] + empatados["distancia_acopio_km"]
        empatados = empatados.sort_values(
            by=["plazo_pago_dias", "distancia_total", "recoge_en_finca"],
            ascending=[True, True, False],
        )
        mejor = empatados.iloc[0]
    else:
        mejor = factibles.iloc[0]

    return mejor, factibles
