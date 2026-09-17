"""Carga de los datos de tiendas de insumos y centros de acopio (Eslabón 2)."""

import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Coordenadas aproximadas del centro urbano de cada municipio de la
# provincia de Ubaté. Se usan como ubicación de la finca cuando el
# ganadero no ingresa coordenadas exactas (dato de referencia geográfica
# pública, no ligado a ningún establecimiento comercial).
MUNICIPIOS_COORDS = {
    "Villa de San Diego de Ubaté": (5.3059, -73.8155),
    "Lenguazaque": (5.3126, -73.7156),
    "Guachetá": (5.3219, -73.6835),
    "Cucunubá": (5.2571, -73.7664),
    "Sutatausa": (5.2672, -73.8774),
    "Tausa": (5.2019, -73.8974),
    "Carmen de Carupa": (5.3406, -73.9086),
    "Fúquene": (5.4067, -73.7652),
    "Simijaca": (5.5083, -73.8437),
    "Susa": (5.4544, -73.8231),
}


class DatosInvalidosError(Exception):
    """Error de datos que debe mostrarse al usuario en español, sin traza técnica."""


def _cargar_json(nombre_archivo: str) -> list:
    ruta = DATA_DIR / nombre_archivo
    if not ruta.exists():
        raise DatosInvalidosError(
            f"No se encontró el archivo de datos '{nombre_archivo}'. "
            "Verifica que la carpeta 'data' esté completa junto al aplicativo."
        )
    try:
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
    except json.JSONDecodeError as e:
        raise DatosInvalidosError(
            f"El archivo de datos '{nombre_archivo}' está dañado o mal formado y no se pudo leer "
            f"(línea {e.lineno}, columna {e.colno}). Restaura una copia válida del archivo."
        ) from e
    if not isinstance(datos, list) or len(datos) == 0:
        raise DatosInvalidosError(
            f"El archivo de datos '{nombre_archivo}' no contiene registros válidos."
        )
    return datos


_CAMPOS_OBLIGATORIOS_TIENDA = {"id", "nombre", "municipio", "latitud", "longitud", "precios"}
_CAMPOS_OBLIGATORIOS_ACOPIO = {
    "id",
    "nombre",
    "municipio",
    "latitud",
    "longitud",
    "precio_base_litro",
    "bonificaciones_calidad",
    "volumen_minimo_litros_dia",
    "frecuencia_recoleccion",
    "plazo_pago_dias",
    "recoge_en_finca",
}


def _filtrar_registros_validos(datos: list, campos_obligatorios: set, nombre_archivo: str) -> list:
    validos = []
    for registro in datos:
        if campos_obligatorios.issubset(registro.keys()):
            validos.append(registro)
    if not validos:
        raise DatosInvalidosError(
            f"Ningún registro de '{nombre_archivo}' tiene los campos obligatorios completos. "
            "Revisa el archivo de datos."
        )
    return validos


def cargar_tiendas() -> pd.DataFrame:
    datos = _cargar_json("tiendas_insumos.json")
    datos = _filtrar_registros_validos(datos, _CAMPOS_OBLIGATORIOS_TIENDA, "tiendas_insumos.json")
    return pd.json_normalize(datos)


def cargar_acopios() -> pd.DataFrame:
    datos = _cargar_json("centros_acopio.json")
    datos = _filtrar_registros_validos(datos, _CAMPOS_OBLIGATORIOS_ACOPIO, "centros_acopio.json")
    return pd.json_normalize(datos)
