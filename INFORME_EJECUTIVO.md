# Monopolio del Suelo, Búsqueda de Rentas y Escasez Artificial
## Un Análisis Econométrico e Institucional del Urbanismo Discrecional en España

**Autor:** Jaime Pérez | *Business Operations, Strategy & Quantitative Analysis*  
**Enfoque:** Economía Institucional (*Public Choice*), Econometría de Panel (Two-Way Fixed Effects) y Microeconomía del Bienestar  
**Datos Analizados:** Panel de 52 Municipios representativos × 15 Años (2009–2023) | $N = 780$ observaciones  
**Calibración Empírica:** Registros oficiales de MITMA, INE, Banco de España, ASPRIMA y CGPJ / Fiscalía de Urbanismo

---

## 1. El Problema Institucional: ¿Por qué la vivienda es cara en España?

En el debate público suele achacarse el precio de la vivienda a la "especulación", a los fondos de inversión o a fallos del libre mercado. Sin embargo, el análisis económico e institucional (*Public Choice Theory*) demuestra que **el mercado del suelo en España no es un mercado libre, sino un monopolio político local**.

### El Cuello de Botella Legal (RDL 7/2015 y PGOU)
Bajo la Ley de Suelo estatal y las normativas autonómicas:
1. **Todo el suelo es no urbanizable por defecto:** A diferencia de países con derechos de propiedad plenos o sistemas *By-Right*, en España un propietario no puede edificar en su propio terreno salvo que el ayuntamiento, de forma arbitraria y discrecional, decida **"recalificarlo"** a través del Plan General de Ordenación Urbana (PGOU).
2. **Retrasos crónicos en licencias:** Una vez que el suelo es urbanizable, obtener una licencia municipal de obras tarda entre **12 y 24 meses** (frente a los 3 meses que marca la teoría).
3. **El "Pelotazo" y la Búsqueda de Rentas (Tullock Rent-Seeking):** Dado que la recalificación depende de una firma política, el valor del suelo se multiplica de media **24 veces** de la noche a la mañana. Esto no crea riqueza real; solo crea incentivos masivos para el *lobbying*, la corrupción, los convenios urbanísticos a medida y la litigación en tribunales.

```
       [ MARCO INSTITUCIONAL ACTUAL: STATUS QUO PGOU ]
   Tierra no protegida ──> Bloqueada por defecto (Rústico Común)
                                │
                                ▼  (Decisión política discrecional: PGOU)
                     Recalificación Municipal
                                │  (Salto de precio del suelo: x24 veces)
                                ▼
                   Colapso Administrativo de Licencias
                         (14 - 24 meses de espera)
                                │
                                ▼
             OFERTA RÍGIDA E INELÁSTICA (ε_s = 0.31)
                                │
                                ▼
         La subida de demanda se traduce 100% en PRECIO,
               NO en más viviendas para la gente.
```

---

## 2. Los Dos Regímenes Modelados

| Característica | Régimen 1: Monopolio Discrecional (Status Quo) | Régimen 2: Edificabilidad por Defecto (*By-Right*) |
| :--- | :--- | :--- |
| **Principio Legal** | Suelo NO edificable por defecto. Requiere permiso político. | Suelo edificable por defecto, salvo parques naturales protegidos. |
| **Tiempo de Licencia** | **14 – 24 meses** de atasco burocrático en ayuntamientos. | **2,5 meses** (declaración responsable y verificación técnica). |
| **Multiplicador de Suelo** | Salto de **~24x** en valor tras recalificación (*rent-seeking*). | Coste de construcción + suelo rústico competitivo (+15%). |
| **Elasticidad de Oferta** | **Rígida ($\epsilon_s \approx 0.31$ - $0.43$)**: No responde a la demanda. | **Elástica ($\epsilon_s \approx 1.20$ - $1.44$)**: Absorbe demanda con volumen. |
| **Efecto en Precios** | Inflación artificial y sobrecoste de hasta el **+32,4%**. | Precios anclados al coste marginal real de edificación. |

---

## 3. Hallazgos Econométricos Principales

Utilizando un modelo de regresión de panel con **Efectos Fijos Bidireccionales (Two-Way Fixed Effects, TWFE)** y errores estándar agrupados por municipio (*clustered errors*), aislamos el impacto puro de las trabas regulatorias manteniendo todo lo demás constante (*ceteris paribus*):

$$\ln(\text{Precio}_{it}) = \alpha_i + \lambda_t + \beta_1 \text{RetrasoLicencias}_{it} + \beta_2 \text{SueloCongelado}_{it} + \dots + u_{it}$$

### Tabla Resumen de Modelos:
* **(1) Retraso en Licencias:** $\beta = +0.0153^{***}$ ($p < 0.001$).  
  **Cada mes adicional que un ayuntamiento tarda en otorgar licencias encarece el precio de la vivienda un +1,53%**. En municipios con atascos de 18 a 22 meses (Madrid, Barcelona, Palma, Marbella), la burocracia municipal explica entre el **+22% y el +26% del coste total de la vivienda**.
* **(2) Suelo Artificialmente Congelado:** $\beta = +0.2686^{**}$ ($p = 0.0056$).  
  Un incremento del 10% en el ratio de suelo retenido como rústico común encarece la vivienda un **+2,69%**.
* **(3) $R^2$ within:** **53,6%** de la variación intra-municipal del precio de la vivienda queda explicada exclusivamente por las restricciones de oferta e ingresos locales.

---

## 4. Evidencia Visual Demostrativa

### Gráfico 1: Impacto Marginal de las Trabas Burocráticas (Forest Plot)
Cada mes de retraso burocrático tiene un efecto positivo y estadísticamente significativo sobre el precio del metro cuadrado, mientras que el Euribor y la inflación general son absorbidos de manera no paramétrica por los efectos temporales.

![Figura 1: Coeficientes de Regresión TWFE](assets/figure_1_panel_regression_coefficients.png)

---

### Gráfico 2: La Elasticidad de la Oferta (PGOU vs. By-Right)
En las grandes capitales (Tier 1 Metros: Madrid, Barcelona, Valencia, Málaga), la elasticidad de oferta bajo el PGOU es raquítica ($\epsilon_s = 0.31$). Si se pasara a un sistema *By-Right*, la elasticidad se multiplicaría por **3,8x** (hasta 1,20) y en zonas costeras dinámicas por **6,4x** (hasta 1,44).

![Figura 2: Comparativa de Elasticidad por Estratos](assets/figure_2_supply_elasticity_by_tier.png)

---

### Gráfico 3: Pérdida Social y Despilfarro de Riqueza (€73.590 Millones)
El coste económico total generado por el urbanismo discrecional entre 2009 y 2023 en estos 52 municipios asciende a **73.590 millones de euros**:
* **29.130 M€ en Pérdida Irrecuperable de Eficiencia (Triángulo de Harberger):** Viviendas que jamás se llegaron a construir y familias que quedaron expulsadas del mercado.
* **44.460 M€ en Disipación de Rentas de Tullock:** Dinero transferido de los compradores a costes de espera financiera, abogados, especuladores de suelo y trámites municipales.
* **Impacto por habitante:** Representa un coste acumulado de **4.382 € por cada ciudadano** de la muestra.

![Figura 3: Pérdida de Bienestar y Rent Seeking](assets/figure_3_welfare_deadweight_loss_breakdown.png)

---

### Gráfico 4: Evolución Temporal del "Impuesto Regulatorio" (2009–2023)
La brecha entre el precio real (rojo) y el precio competitivo contrafactual (verde) muestra cómo a partir de la recuperación de 2015 el suelo se convirtió en un cuello de botella absoluto, encareciendo el $m^2$ entre **800 € y 1.700 €/m² de sobrecoste artificial** en Madrid, Barcelona, Ibiza o Málaga.

![Figura 4: Divergencia Temporal de Precios](assets/figure_4_longitudinal_price_divergence.png)

---

### Gráfico 5: Matriz de Esclerosis Institucional
Relación entre los meses de retraso municipal en licencias y el multiplicador de recalificación del suelo. Las grandes capitales y zonas turísticas se sitúan en el cuadrante de máxima extracción de rentas y retrasos administrativos.

![Figura 5: Matriz de Retraso vs Recalificación](assets/figure_5_scarcity_matrix_heatmap.png)

---

## 5. Conclusiones Ejecutivas para Dirección y Estrategia

1. **La vivienda en España no es un problema de falta de suelo físico:** España tiene el 85% de su territorio deshabitado. El problema es la **escasez jurídica y artificial** impuesta por los ayuntamientos mediante el monopolio del PGOU.
2. **Las subvenciones y controles de precios atacan el síntoma, no la causa:** Si la oferta es inelástica ($\epsilon_s = 0.31$), cualquier ayuda a la compra o al alquiler solo sirve para inflar el precio sin generar una sola vivienda adicional.
3. **La solución de alta eficiencia (*By-Right*):** Desregularizar el suelo no protegido (permitir edificar por defecto a quien cumpla normas técnicas) y sustituir la licencia previa por una declaración responsable con visado técnico aumentaría la oferta de vivienda en un 40% y rebajaría los precios entre un 25% y un 35% en las principales áreas metropolitanas **sin gastar un solo euro de dinero público**.
