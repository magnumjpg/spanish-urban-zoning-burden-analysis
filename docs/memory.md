# Memoria Continua del Proyecto

## Lecciones Aprendidas (Mejora Continua)
- *2026-10-22*: Inicialización del proyecto de econometría urbana y análisis institucional. Mantener modularidad estricta en `/src`, estándares PEP8, sin dependencias no declaradas y asegurar reproducibilidad estadística.
- Regla de Fuentes Oficiales Más Recientes (Banco de España Informe Anual 2025/2026): El déficit acumulado de vivienda según la última presentación oficial de David López Salido (18 de junio de 2026) asciende exactamente a **750.000 viviendas** (diferencial acumulado 2021-2025 de -3,9% de hogares promedio). Nunca usar estimaciones preliminares obsoletas (450k) cuando existe el dato consolidado oficial de 750k.
- Regla de Gráficos Limpios (Zero-Clutter Visuals): NUNCA colocar cajas de texto flotantes (`bbox`) sobre el área de datos de los gráficos, ya que tapan barras, líneas y etiquetas. Las explicaciones deben residir exclusivamente en el texto del informe. El gráfico debe ser autoexplicativo, diáfano y minimalista (estilo gráfico del Banco de España / Financial Times).
- Regla del Esfuerzo de Compra (BdE Diapositiva 43): El esfuerzo salarial en Málaga, Madrid y Barcelona para hogares en alquiler alcanza los **10 años de renta neta** (frente al promedio nacional de 4 años para propietarios).
- Regla del Parque Público (BdE Diapositiva 48): El parque público en España es de solo el **1,5%** (1 de cada 65 viviendas), frente al 34,1% de Países Bajos o 14,0% de Francia.
- Metodología de Déficit BdE (Slide 29): Suma 2021-2025 de la diferencia acumulada entre viviendas residenciales terminadas y creación neta de hogares.

## Actualidad (Estado y Roadmap Activo)
- [x] **Calibración a Cifras Oficiales Banco de España 2025/2026**: Integrado el dato oficial definitivo de **750.000 viviendas** de déficit acumulado 2021-2025 (-3,9% de los hogares promedio) y los 10 años de esfuerzo salarial para inquilinos en grandes ciudades (David López Salido, 18 de junio de 2026).
- [x] **Limpieza Integral de Visualizaciones (Zero Clutter)**:
  - `figure_1_panel_regression_coefficients.png`: Eliminado el banner flotante `bbox`, trasladando la nota técnica a pie de figura discreto.
  - `figure_2_supply_elasticity_by_tier.png`: Eliminada la caja flotante del test de Wald; barras y etiquetas nítidas.
  - `figure_5_scarcity_matrix_heatmap.png`: Eliminados textos flotantes de cuadrante para no tapar burbujas de municipios.
  - `figure_7_european_benchmark_paradox.png`: Rediseñado a 4 paneles limpios y minimalistas, alineados con Eurostat y diapositivas 29 y 43 del Banco de España, sin cajas superpuestas.
- [x] **Sincronización de Documentos**: `INFORME_EJECUTIVO.md` y `README.md` sincronizados y actualizados con el rigor empírico demandado.
