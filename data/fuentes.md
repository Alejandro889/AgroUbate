# Fuentes de datos — Eslabón 2

Este documento respalda el campo `fuente` y `fuente_cita` de `tiendas_insumos.json` y `centros_acopio.json`, y explica exactamente qué parte de cada dato es verificable y cuál es una estimación.

## Regla de honestidad aplicada

El campo `fuente` de cada registro (REAL / SIMULADO) se refiere **únicamente a si el establecimiento existe y está ubicado donde se indica** (nombre, municipio, y en algunos casos dirección/teléfono), según una fuente pública citada abajo.

**Los precios unitarios, descuentos, bonificaciones no reguladas, horarios, volúmenes mínimos, frecuencias de recolección y plazos de pago son ESTIMACIONES realistas para TODOS los registros (reales y simulados)**, porque esa información comercial granular no está publicada por ninguno de estos negocios (ni los reales ni obviamente los simulados). La única excepción son las bonificaciones por componente (proteína, grasa, sólidos totales) y por recuento bacteriano de baja carga (0-25.000 UFC/mL), que sí corresponden a una tabla oficial vigente y se aplicaron igual en todos los centros de acopio por estar todos en la misma región regulatoria.

## Fuentes reales citadas

1. **Resolución 017 de 2012 (Ministerio de Agricultura y Desarrollo Rural), actualización marzo 2025 - febrero 2026, Región 1 (Trópico Alto, incluye Cundinamarca):** proteína $43,22/gramo, grasa $14,40/gramo, sólidos totales $15,28/gramo, bonificación por calidad higiénica $174/litro para 0-25.000 UFC/mL.
   Fuente: [Actualizado el precio base de pago de leche cruda por calidad – Minagricultura](https://www.minagricultura.gov.co/noticias/Paginas/Actualizado-el-precio-base-de-pago-de-leche-cruda-por-calidad-.aspx), [Precio base de la leche subirá 5,36% – CONtexto Ganadero](https://www.contextoganadero.com/economia/precio-base-de-la-leche-subira-5-36-por-ciento-desde-el-1-de-marzo). Los demás tramos de UFC (25.001-100.000, 100.001-300.000, más de 300.000) son una extensión ESTIMADA y decreciente del tramo real, no figuran verificados en las fuentes consultadas.
   Nota importante: se confirmó también que Colombia **no** fija un "precio base por litro" único en pesos a nivel nacional — cada comprador lo negocia sobre la base de estos componentes — por lo que el campo `precio_base_litro` de cada centro de acopio es una ESTIMACIÓN realista (rango $1.700-$1.950/litro, agosto-septiembre 2025) y no un dato oficial.

2. **Doña Leche Alimentos S.A. / "Acopio de Leche Ubaté":** empresa láctea del Valle de Ubaté, planta de enfriamiento construida en 1984. Dirección: Vía Lenguazaque Km 1, Ubaté. Tel. 601-7468290.
   Fuentes: [donaleche.com](https://donaleche.com/), directorios empresariales (informacolombia.com, empresite.eleconomistaamerica.co, paginasamarillas.com.co).

3. **Lácteos Villa de Ubaté:** fábrica de lácteos en Ubaté desde 1992. Dirección: Km 5 vía Ubaté-Chiquinquirá, sector Puente del Río. Tel. 313 492 8867 / 321 346 2175.
   Fuente: [lacteosvilladeubate.com](https://www.lacteosvilladeubate.com/).

4. **Federación de Productores Lecheros de la Provincia de Ubaté y Áreas Circunvecinas:** asociación de productores. Dirección: Cra 5 # 14A-21, Ubaté. Tel. 311 514 2155.
   Fuente: directorio empresarial (ICBF - listado de asociaciones productoras Bogotá y Cundinamarca; informacolombia.com).

5. **Alquería:** presencia confirmada como comprador industrial en la cuenca lechera Ubaté-Chiquinquirá-Simijaca.
   Fuentes: [CONtexto Ganadero – Algarra, Alpina, Alquería y Parmalat disminuyen el acopio de leche](https://www.contextoganadero.com/economia/algarra-alpina-alqueria-y-parmalat-disminuyen-el-acopio-de-leche), [La República – Empresas líderes en compra de leche](https://www.larepublica.co/empresas/empresas-que-lideran-la-compra-de-leche-3988541).

6. **Cooperativa Agropecuaria del Valle de Ubaté:** Calle 7 # 9-85, Ubaté.
   Fuente: directorio empresarial (informacolombia.com).

7. **COOPALAC (Cooperativa de Productores Agropecuarios de Lenguazaque, El Valle de Ubaté y Municipios Circunvecinos):** Carrera 5 # 2-09, Lenguazaque Centro. Tel. 320 963 0180.
   Fuente: directorio empresarial (einforma.co, empresite.eleconomistaamerica.co).

8. **Serviagrofinca:** comercializadora de insumos agropecuarios con sede principal en Chiquinquirá (Boyacá) y puntos de venta confirmados en Ubaté y Simijaca (además de Duitama).
   Fuente: [serviagrofinca.com](https://serviagrofinca.com/), direccion.com.co.

9. **Contrigran:** planta productora de sal mineralizada, línea "Sal Bovimex leche Ubaté" formulada para la región. Ubicación: Km 1 vía Ubaté-Cucunubá.
   Fuente: [contrigran.co](https://www.contrigran.co/sal-bovimex-leche-ubate/).

## Referencias de mercado usadas para estimar precios de insumos (no ligadas a una tienda específica)

- Concentrado lechero, bulto de 40 kg: referencia $97.000-$98.900 (Solla), $72.692 (Italcol Super Terneras). Fuente: [La República – costos de concentrados suben 5%](https://www.larepublica.co/empresas/costos-de-los-concentrados-y-alimentos-para-animales-subieron-5-en-el-ultimo-mes-3320264), fichas de producto tierragro.com, croper.com.
- Sal mineralizada, bulto de 40 kg: referencia $95.299-$112.283 (Finca), $104.950 (Agroforr 8%). Fuente: fichas de producto y comparadores citados arriba.
- Antiparasitario (ivermectina): referencia $32.000 (Next Platino) a $77.200 (Ivomec Gold 3,15%). Fuente: lares.com.co.
- Antibiótico (oxitetraciclina): referencia $22.000-$60.000 según presentación. Fuente: lares.com.co, vecol.com.co.

## Resumen de proporción REAL vs. SIMULADO

| Dataset | Total registros | REAL (existencia/ubicación verificada) | SIMULADO |
|---|---|---|---|
| Tiendas de insumos | 11 | 5 (45,5%) | 6 (54,5%) |
| Centros de acopio | 12 | 4 (33,3%) | 8 (66,7%) |
| **Total combinado** | **23** | **9 (39,1%)** | **14 (60,9%)** |

Recordatorio: incluso en los 9 registros REALES, los precios/condiciones comerciales específicas son estimaciones (excepto las bonificaciones por componente y por UFC bajo, que sí son la tabla oficial vigente).
