"""AgroUbaté AI — encuentra la combinación óptima de tienda de insumos
y centro de acopio de leche para un ganadero de la provincia de Ubaté.
"""

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from src.datos import DatosInvalidosError, MUNICIPIOS_COORDS, cargar_acopios, cargar_tiendas
from src.modelo import calcular_combinaciones, elegir_optima

st.set_page_config(page_title="AgroUbaté AI", page_icon="🐄", layout="wide")


@st.cache_data
def obtener_datos():
    return cargar_tiendas(), cargar_acopios()


def construir_mapa(tiendas_df, acopios_df, finca=None, tienda_optima_id=None, acopio_optimo_id=None):
    centro = finca if finca else (5.35, -73.82)
    mapa = folium.Map(location=centro, zoom_start=10, tiles="OpenStreetMap")

    if finca:
        folium.Marker(
            finca,
            tooltip="Tu finca",
            icon=folium.Icon(color="red", icon="home", prefix="fa"),
        ).add_to(mapa)

    for _, t in tiendas_df.iterrows():
        color = "green" if t["id"] == tienda_optima_id else "blue"
        folium.Marker(
            [t["latitud"], t["longitud"]],
            tooltip=f"🛒 {t['nombre']} ({t['municipio']})",
            icon=folium.Icon(color=color, icon="shopping-cart", prefix="fa"),
        ).add_to(mapa)

    for _, a in acopios_df.iterrows():
        color = "green" if a["id"] == acopio_optimo_id else "orange"
        folium.Marker(
            [a["latitud"], a["longitud"]],
            tooltip=f"🥛 {a['nombre']} ({a['municipio']})",
            icon=folium.Icon(color=color, icon="tint", prefix="fa"),
        ).add_to(mapa)

    return mapa


st.title("🐄 AgroUbaté AI")
st.caption(
    "Encuentra la combinación de tienda de insumos y centro de acopio que "
    "maximiza tu margen neto mensual, en la provincia de Ubaté."
)

try:
    tiendas_df, acopios_df = obtener_datos()
except DatosInvalidosError as e:
    st.error(f"⚠️ No se pudo iniciar el aplicativo: {e}")
    st.stop()
except Exception:
    st.error(
        "⚠️ Ocurrió un problema inesperado leyendo los datos del aplicativo. "
        "Verifica que la carpeta 'data' esté completa y no haya sido modificada, "
        "y vuelve a intentarlo."
    )
    st.stop()

with st.form("formulario_ganadero"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tu finca")
        municipio = st.selectbox("Municipio de tu finca", list(MUNICIPIOS_COORDS.keys()))
        litros_dia = st.number_input(
            "Producción diaria de leche (litros/día)", min_value=1.0, max_value=2000.0, value=80.0, step=1.0
        )
        dias_mes = st.number_input("Días del mes a proyectar", min_value=28, max_value=31, value=30)

        st.subheader("Calidad de tu leche")
        grasa_pct = st.number_input("Grasa (%)", min_value=0.0, max_value=10.0, value=3.6, step=0.1)
        proteina_pct = st.number_input("Proteína (%)", min_value=0.0, max_value=10.0, value=3.2, step=0.1)
        solidos_pct = st.number_input("Sólidos totales (%)", min_value=0.0, max_value=20.0, value=12.5, step=0.1)
        ufc = st.number_input(
            "Recuento bacteriano (UFC/mL)", min_value=0, max_value=2_000_000, value=20_000, step=1000
        )

    with col2:
        st.subheader("Insumos que compras al mes")
        bultos_concentrado = st.number_input(
            "Bultos de concentrado lechero (40 kg)", min_value=0, max_value=100, value=4
        )
        bultos_sal = st.number_input("Bultos de sal mineralizada (40 kg)", min_value=0, max_value=100, value=1)
        unidades_antiparasitario = st.number_input(
            "Unidades de antiparasitario", min_value=0, max_value=50, value=1
        )
        unidades_antibiotico = st.number_input("Unidades de antibiótico", min_value=0, max_value=50, value=1)

        st.subheader("Transporte")
        viajes_tienda_mes = st.number_input(
            "Viajes al mes a la tienda de insumos", min_value=1, max_value=30, value=1
        )
        costo_por_km = st.number_input(
            "Costo de transporte por km, ida ($ COP)", min_value=0, max_value=10_000, value=700, step=50
        )

    with st.expander("Configuración avanzada: composición de referencia de la leche"):
        st.caption(
            "El bono por calidad se calcula sobre la diferencia frente a estos valores de "
            "referencia (estimación de la industria). Ajústalos si tu comprador usa otros."
        )
        grasa_ref = st.number_input("Grasa de referencia (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
        proteina_ref = st.number_input(
            "Proteína de referencia (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1
        )
        solidos_ref = st.number_input(
            "Sólidos totales de referencia (%)", min_value=0.0, max_value=20.0, value=11.3, step=0.1
        )

    enviado = st.form_submit_button("Calcular la mejor combinación", use_container_width=True)

if enviado and (grasa_pct + proteina_pct) > solidos_pct:
    st.warning(
        "⚠️ Revisa los porcentajes de calidad: la grasa más la proteína "
        f"({grasa_pct + proteina_pct:.1f}%) superan los sólidos totales que ingresaste "
        f"({solidos_pct:.1f}%), lo cual no es físicamente posible en la leche (los sólidos "
        "totales incluyen la grasa y la proteína, más lactosa y minerales). "
        "El cálculo continúa con los valores ingresados, pero corrígelos si fue un error de digitación."
    )

if enviado:
    finca_lat, finca_lon = MUNICIPIOS_COORDS[municipio]
    cantidades = {
        "bultos_concentrado": bultos_concentrado,
        "bultos_sal": bultos_sal,
        "unidades_antiparasitario": unidades_antiparasitario,
        "unidades_antibiotico": unidades_antibiotico,
    }

    df = calcular_combinaciones(
        tiendas_df,
        acopios_df,
        finca_lat,
        finca_lon,
        litros_dia,
        dias_mes,
        grasa_pct,
        proteina_pct,
        solidos_pct,
        ufc,
        cantidades,
        viajes_tienda_mes,
        costo_por_km,
        grasa_ref,
        proteina_ref,
        solidos_ref,
    )
    mejor, factibles = elegir_optima(df)

    if mejor is None:
        min_vol = acopios_df["volumen_minimo_litros_dia"].min()
        acopio_min = acopios_df.loc[acopios_df["volumen_minimo_litros_dia"].idxmin(), "nombre"]
        st.error(
            f"Con tu producción actual de {litros_dia:.0f} L/día, ningún centro de acopio de la "
            f"región la acepta directamente. El volumen mínimo más bajo disponible es "
            f"{min_vol:.0f} L/día, en **{acopio_min}**. Te faltan {min_vol - litros_dia:.0f} L/día. "
            "Considera asociarte con otros productores de tu vereda para alcanzar el mínimo."
        )
    else:
        st.success(
            f"**Combinación óptima:** compra insumos en **{mejor['tienda_nombre']}** "
            f"({mejor['tienda_municipio']}) y vende tu leche en **{mejor['acopio_nombre']}** "
            f"({mejor['acopio_municipio']})."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Margen neto mensual", f"${mejor['margen_neto_mensual']:,.0f}")
        c2.metric("Ingreso mensual", f"${mejor['ingreso_mensual']:,.0f}")
        c3.metric(
            "Costo insumos + entrega",
            f"${mejor['costo_insumos_mensual'] + mejor['costo_entrega_mensual']:,.0f}",
        )

        peor = factibles.sort_values("margen_neto_mensual").iloc[0]
        promedio = factibles["margen_neto_mensual"].mean()
        c4, c5 = st.columns(2)
        c4.metric(
            "Vs. la peor opción viable",
            f"+${mejor['margen_neto_mensual'] - peor['margen_neto_mensual']:,.0f} / mes",
        )
        c5.metric(
            "Vs. el promedio de la región",
            f"+${mejor['margen_neto_mensual'] - promedio:,.0f} / mes",
        )

        st.subheader("Todas las combinaciones factibles, ordenadas por margen neto")
        tabla = factibles.sort_values("margen_neto_mensual", ascending=False)[
            [
                "tienda_nombre",
                "acopio_nombre",
                "distancia_tienda_km",
                "distancia_acopio_km",
                "precio_final_litro",
                "ingreso_mensual",
                "costo_insumos_mensual",
                "costo_entrega_mensual",
                "margen_neto_mensual",
                "plazo_pago_dias",
            ]
        ].rename(
            columns={
                "tienda_nombre": "Tienda de insumos",
                "acopio_nombre": "Centro de acopio",
                "distancia_tienda_km": "Dist. tienda (km)",
                "distancia_acopio_km": "Dist. acopio (km)",
                "precio_final_litro": "Precio/L ($)",
                "ingreso_mensual": "Ingreso/mes ($)",
                "costo_insumos_mensual": "Costo insumos/mes ($)",
                "costo_entrega_mensual": "Costo entrega/mes ($)",
                "margen_neto_mensual": "Margen neto/mes ($)",
                "plazo_pago_dias": "Plazo de pago (días)",
            }
        )
        st.dataframe(tabla, use_container_width=True, hide_index=True)

        no_factibles = df[~df["factible"]].drop_duplicates("acopio_id")
        if not no_factibles.empty:
            with st.expander(f"⚠️ {len(no_factibles)} centro(s) de acopio no disponibles por volumen mínimo"):
                for _, fila in no_factibles.iterrows():
                    st.write(
                        f"- **{fila['acopio_nombre']}** exige mínimo {fila['volumen_minimo']:.0f} L/día "
                        f"(te faltan {fila['volumen_minimo'] - litros_dia:.0f} L/día)"
                    )

        st.subheader("Mapa de la región")
        try:
            mapa = construir_mapa(
                tiendas_df, acopios_df, finca=(finca_lat, finca_lon), tienda_optima_id=mejor["tienda_id"],
                acopio_optimo_id=mejor["acopio_id"],
            )
            st_folium(mapa, use_container_width=True, height=500, key="mapa_resultado")
        except Exception:
            st.warning(
                "⚠️ No se pudo cargar el mapa (puede deberse a que no tienes conexión a internet "
                "en este momento, ya que el mapa usa imágenes de OpenStreetMap). "
                "El cálculo del margen y la tabla de resultados no se ven afectados."
            )
else:
    st.info("Completa el formulario y presiona **Calcular la mejor combinación** para ver tu resultado.")
    st.subheader("Mapa de establecimientos en la provincia de Ubaté")
    try:
        mapa = construir_mapa(tiendas_df, acopios_df)
        st_folium(mapa, use_container_width=True, height=500, key="mapa_inicial")
    except Exception:
        st.warning(
            "⚠️ No se pudo cargar el mapa (puede deberse a que no tienes conexión a internet en "
            "este momento). Puedes seguir usando el formulario con normalidad."
        )
