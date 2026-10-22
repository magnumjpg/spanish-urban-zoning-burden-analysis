# Memoria Continua del Proyecto

## Lecciones Aprendidas (Mejora Continua)
- *2026-10-22*: Inicialización del proyecto de econometría urbana y análisis institucional. Mantener modularidad estricta en `/src`, estándares PEP8, sin dependencias no declaradas y asegurar reproducibilidad estadística.
- Regla: No hacer soluciones provisionales ni "hacky". Todos los modelos econométricos deben presentar tests de robustez, errores estándar clúster (HAC / Clustered by Municipality) y justificación institucional formal (Public Choice Theory - Buchanan, Tullock, Cheshire & Sheppard, Glaeser & Gyourko).
- Regla de Absorción en TWFE: En especificaciones con efectos fijos temporales (Year Fixed Effects $\lambda_t$), las variables macroeconómicas que solo varían en el tiempo (como Euribor o el índice general de inflación de costes de construcción) quedan absorbidas por los efectos fijos de año. Se deben manejar de forma explícita separando la especificación entre Pooled OLS/Entity FE y TWFE para evitar advertencias de colinealidad.
- Regla de Simulación Estocástica Heterogénea (Monte Carlo): Las simulaciones de Monte Carlo no pueden ser meras traslaciones gaussianas idénticas con igual varianza; deben incorporar asimetría (skewness), heterogeneidad espacial por estrato municipal (Madrid/BCN con atasco severo vs interior), orografía, elasticidades no lineales y distribución empírica de colas pesadas.
- Regla de Variables Socioeconómicas Clave: Para conectar la econometría con la realidad social sin sesgos políticos, incorporar métricas del Banco de España e INE:
  - Price-to-Income / Effort Ratio (años de salario necesarios para comprar vivienda).
  - Tasa de Hacinamiento y Emancipación (Eurostat).
  - Gap Estructural de Formación de Hogares vs Nuevas Viviendas (Net Household Formation vs Housing Completions).
- Regla de Riqueza Gráfica: Cada visualización debe poseer una identidad gráfica rica y dinámica con contraste nítido, sin rigideces cromáticas aburridas.

## Actualidad (Estado y Roadmap Activo)
- [x] **Configuración del entorno de trabajo**: Instalación y verificación de dependencias cuantitativas (`statsmodels`, `linearmodels`, `scipy`, `seaborn`, `nbconvert`, `ipykernel`).
- [x] **Sub-agente 1 (Data & Simulation Engineer)**: Implementado `/src/data_simulation.py`. Panel longitudinal de 52 municipios x 15 años (2009–2023, $N=780$) calibrado con estadísticas oficiales de MITMA, INE, Banco de España, ASPRIMA y CGPJ. Exportado a `data/spanish_municipalities_panel.csv`.
- [x] **Sub-agente 2 (Econometric Modeling)**: Implementado `/src/econometric_models.py`. Modelos Panel OLS, Entity FE y Two-Way Fixed Effects (TWFE) con errores estándar clúster por municipio. Estimación de elasticidades de oferta $\hat{\epsilon}_s^{PGOU} = 0.432$ vs $\hat{\epsilon}_s^{ByRight} = 0.769$ (test de Wald $Z=2.137, p=0.0326$). Cuantificación de Harberger DWL (€29.13B) y Tullock Rent Dissipation (€44.46B), con un coste social total de €73.59B (€4,381.95/habitante).
- [x] **Sub-agente 3 (Visualization & Reporting)**: Implementado `/src/visualization.py`. Cinco figuras publication-grade exportadas a `assets/` a 300 DPI:
  - `figure_1_panel_regression_coefficients.png`: Forest plot de coeficientes TWFE y CIs del 95%.
  - `figure_2_supply_elasticity_by_tier.png`: Elasticidades por estrato municipal (Metros 0.31 vs 1.20).
  - `figure_3_welfare_deadweight_loss_breakdown.png`: Pérdida de bienestar y rent dissipation acumulada (área apilada y donut).
  - `figure_4_longitudinal_price_divergence.png`: Trayectoria temporal de precios reales vs. contrafactual By-Right (Madrid, Barcelona, Ibiza, Málaga, Valencia, Zaragoza).
  - `figure_5_scarcity_matrix_heatmap.png`: Matriz de esclerosis regulatoria (meses de retraso de licencias vs. multiplicador de recalificación).
- [x] **Sub-agente 4 (Notebook Master & System Notes)**:
  - `SYSTEM_NOTES.md`: Scratchpad continuo con todas las tablas empíricas, coeficientes exactos, p-valores, $R^2$ within y matrices de elasticidad.
  - `analysis_report.ipynb`: Notebook Jupyter maestro generado y ejecutado in-place con outputs y gráficos renderizados.
- [x] **Sub-agente 5 (Executive Portfolio README & Informe Visual)**:
  - Redactado `README.md` exhaustivo y de nivel profesional para reclutadores de data analysis / quantitative economics, con diagramas institucionales, tablas de regresión comparadas, gráficos embebidos y referencias académicas.
  - Creado `INFORME_EJECUTIVO.md` en español con estilo ejecutivo, gráficos embebidos y formato legible para Jaime.
