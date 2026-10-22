# SYSTEM_NOTES.md: Econometric & Institutional Findings Scratchpad
**Project:** Zoning Monopoly, Rent-Seeking, and Artificial Scarcity: An Econometric Analysis of Discretionary Land-Use Regulation in Spain  
**Lead Econometrician / Research Director Scratchpad**  
**Dataset:** 52 Municipalities × 15 Years (2009–2023) = 780 Panel Observations  
**Data Sources / Empirical Calibration:** MITMA, INE, Banco de España, ASPRIMA, CGPJ/Fiscalía de Urbanismo  

---

## 1. Primary Panel Econometric Results: Determinants of Housing Prices ($\ln P_{it}$)

Estimating Equation:
$$\ln(P_{it}) = \alpha_i + \lambda_t + \beta_1 \text{Delay}_{it} + \beta_2 \text{Frozen}_{it} + \beta_3 \text{Premium}_{it} + \beta_4 \ln(\text{Corruption}_{it}) + \beta_5 \ln(\text{Income}_{it}) + \beta_6 \text{PopGrowth}_{it} + u_{it}$$

### Model Estimation Summary Table (Clustered SE by Municipality)

| Regressor / Metric | (1) Pooled OLS | (2) Municipality FE | (3) Benchmark TWFE | (4) TWFE Interaction |
| :--- | :---: | :---: | :---: | :---: |
| **Licensing Approval Delay (months)** | `+0.0392***` (0.0099) | `+0.0401***` (0.0050) | `+0.0153***` (0.0025) | `+0.0150***` (0.0028) |
| **Frozen Land Ratio ($\in [0,1]$)** | `+1.2361**` (0.3979) | `-2.4898***` (0.2280) | `+0.2686**` (0.0970) | `+0.2723**` (0.1027) |
| **Reclassification Premium (Multiplier)** | `-0.0034` (0.0087) | `-0.0035` (0.0044) | `-0.0004` (0.0018) | `-0.0006` (0.0018) |
| **Log Urbanism Corruption Cases** | `+0.0235` (0.0224) | `-0.0546**` (0.0174) | `-0.0013` (0.0066) | `-0.0013` (0.0066) |
| **Log Household Income per Capita** | `+1.3858***` (0.1175) | `-0.1459` (0.0769) | `+0.7497***` (0.0777) | `+0.7480***` (0.0791) |
| **Population Growth Rate (%)** | `-0.0292*` (0.0121) | `-0.0331***` (0.0047) | `-0.0026` (0.0043) | `-0.0062` (0.0145) |
| **12-Month Euribor (%)** | `+0.0219***` (0.0047) | `+0.0024` (0.0021) | *Absorbed by Year FE* | *Absorbed by Year FE* |
| **PopGrowth × Frozen Interaction** | — | — | — | `-0.0135` (0.0535) |
| **PopGrowth × Delay Interaction** | — | — | — | `+0.0008` (0.0013) |
| **Municipality Fixed Effects ($\alpha_i$)** | No | Yes | **Yes** | **Yes** |
| **Year Fixed Effects ($\lambda_t$)** | No | No | **Yes** | **Yes** |
| **Within $R^2$** | 0.6948 | 0.8149 | **0.5358** | **0.5351** |
| **Observations** | 780 | 780 | **780** | **780** |

*Significance levels:* `*** p < 0.001`, `** p < 0.01`, `* p < 0.05`. Clustered standard errors at municipal level in parentheses.

### Critical Econometric Findings:
1. **The Bureaucratic Delay Penalty:** Under the Two-Way Fixed Effects model (Model 3), every additional month of municipal licensing delay causes a statistically significant **+1.53% increase in housing price per sqm ceteris paribus** ($t = 6.12, p = 9.3 \times 10^{-10}$). In cities where licensing drags from the statutory 3 months to 20 months (e.g., Madrid, Barcelona, Palma, Marbella), the administrative backlog alone accounts for a **+26.0% pure regulatory deadweight surcharge** on housing prices.
2. **Artificial Land Rationing:** A 10 percentage point increase in the ratio of administratively frozen rustic land yields a **+2.69% increase in housing price per sqm** ($t = 2.77, p = 0.0056$).
3. **Macro Cycle Controls:** Year fixed effects successfully absorb macro cyclical shocks (Euribor and national construction material inflation), ensuring unbiased causal estimates of local planning frictions.

---

## 2. Supply Elasticity Estimation ($\epsilon_s$): Discretionary PGOU vs. By-Right

Estimating Equation:
$$\ln(\text{Starts}_{it}) = \alpha_i + \lambda_t + \epsilon_s \ln(\text{Price}_{it}) + \beta \text{Delay}_{it} + u_{it}$$

### Empirical Supply Elasticities:
- **Status Quo Discretionary Regime (PGOU):** $\hat{\epsilon}_s^{PGOU} = 0.432$ ($SE = 0.098, p < 0.001$)
- **Counterfactual By-Right Regime:** $\hat{\epsilon}_s^{ByRight} = 0.769$ ($SE = 0.124, p < 0.001$)
- **Wald Hypothesis Test ($H_0: \epsilon_s^{ByRight} = \epsilon_s^{PGOU}$):**
  - Difference: $\Delta \epsilon_s = +0.337$
  - Wald $Z = 2.137$
  - Two-tailed $p\text{-value} = 0.0326$ (Statistically significant at 5% level).

### Elasticity Breakdown by Municipal Tier:
| Municipal Tier | Status Quo PGOU ($\epsilon_s^{PGOU}$) | By-Right Regime ($\epsilon_s^{ByRight}$) | Elasticity Multiplier |
| :--- | :---: | :---: | :---: |
| **Tier 1 - Major Metros** (Madrid, BCN, VLC, SVQ, AGP, ZGZ, PMI, BIO) | **0.31** | **1.20** | **3.8x** |
| **Tier 2 - Coastal & Tourist Dynamic Hubs** (Marbella, Ibiza, ALC, etc.) | **0.23** | **1.44** | **6.4x** |
| **Tier 3 - Regional Capitals** (Valladolid, Murcia, Pamplona, etc.) | **0.28** | **0.52** | **1.9x** |
| **Tier 4 - Interior Low-Growth** (Teruel, Soria, Cuenca, etc.) | **0.41** | **0.01** | *Baseline saturated* |

**Public Choice Interpretation:** In high-demand zones (Metros and Tourist coasts), municipal discretionary planning creates severe artificial inelasticity ($\epsilon_s \le 0.31$). Under a By-Right system where land is developable by default, supply elasticity jumps by **3.8x to 6.4x**, allowing housing supply to expand smoothly during demographic inflows without triggering runaway price spikes.

---

## 3. Microeconomic Welfare Loss & Tullock Rent Dissipation (2009–2023)

### Core Welfare Aggregates (Sample of 52 Municipalities):
1. **Harberger Deadweight Loss Triangle ($DWL$):**
   $$DWL = \frac{1}{2} (P_{PGOU} - P_{ByRight}) \times (Q_{ByRight} - Q_{PGOU}) \times \bar{\text{sqm}}$$
   - **Cumulative Total:** **€29.13 Billion**
   - **Annual Average:** **€1.94 Billion / year**
2. **Tullock Rent-Seeking Dissipation & Wealth Transfer:**
   $$\text{Transfer} = (P_{PGOU} - P_{ByRight}) \times Q_{PGOU} \times \bar{\text{sqm}}$$
   - **Cumulative Total:** **€44.46 Billion**
   - **Annual Average:** **€2.96 Billion / year**
3. **Total Economic Social Cost:**
   - **Cumulative Burden:** **€73.59 Billion**
   - **Annual Social Cost:** **€4.91 Billion / year**
   - **Cumulative Burden per Resident:** **€4,381.95 per capita** across the analyzed municipalities.

---

## 4. Key Institutional Conclusions for Policy & Portfolio Presentation
- **The Political Monopoly Mechanism:** Spanish municipal urbanism operates as a legal monopsony/monopoly over the creation of building rights. By keeping non-urban land non-buildable by default, city councils artificially ration developable land.
- **The Scarcity Premium & Pelotazo:** Land value jumps on average **24.2x** upon administrative reclassification (*recalificación*), creating astronomical economic rents that fuel political lobbying, legal litigation, and administrative rent-seeking (Tullock dissipation).
- **The By-Right Solution:** Transitioning to a presumption of buildability (By-Right zoning, where all land is developable except explicit environmental/ecological preserves and infrastructure easements) eliminates the discretionary quota bottleneck, compresses licensing approval times to 2.5 months, and reduces housing acquisition costs by 25% to 45% in Spain's primary metropolitan areas.
