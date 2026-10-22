# Contexto del Proyecto: Zoning Monopoly & Artificial Scarcity in Spain

## Título del Proyecto
**Zoning Monopoly, Rent-Seeking, and Artificial Scarcity: An Econometric Analysis of Discretionary Land-Use Regulation in Spain**

## Objetivo General
Desarrollar un proyecto de investigación institucional y econométrica de alto nivel para un portfolio internacional de Business & Data Analysis / Econometría Cuantitativa.
El estudio analiza el impacto del marco regulatorio del suelo en España (Ley del Suelo, Planes Generales de Ordenación Urbana - PGOU, y discrecionalidad municipal en recalificaciones) sobre el encarecimiento de la vivienda, la pérdida de bienestar (Deadweight Loss) y el rent-seeking / corrupción urbanística, comparándolo con un régimen contrafactual de "By-Right" (edificabilidad por defecto con zonas protegidas explícitas).

## Arquitectura del Proyecto
1. `src/`
   - `data_simulation.py`: Generador y validación del panel empírico/sintético de municipios españoles a 15 años (50 municipios representativos, variables macroeconómicas, demográficas y regulatorias calibradas con estadísticas MITMA/INE/BdE).
   - `econometric_models.py`: Modelos econométricos modulares (Panel Data Fixed Effects, Two-Way FE, Estimación de Elasticidad de Oferta $\epsilon_s$, Cuantificación de Deadweight Loss y Rent-Seeking).
   - `visualization.py`: Módulo de visualizaciones con estética financiera minimalista y pulcra (exportación a `assets/`).
2. `analysis_report.ipynb`: Notebook Jupyter maestro interactivo y reproducible.
3. `SYSTEM_NOTES.md`: Registro continuo de hallazgos empíricos, coeficientes, $R^2$, p-valores y métricas de elasticidad.
4. `README.md`: Resumen ejecutivo de nivel profesional para reclutadores y directores de investigación.
5. `data/`: Datos generados del panel.
6. `assets/`: Gráficos de alta resolución generados.
