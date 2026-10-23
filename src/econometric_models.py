"""
Econometric Modeling Module
===========================
Project: Zoning Monopoly, Rent-Seeking, and Artificial Scarcity in Spain
Author: Jaime Pérez | Quantitative Economics Portfolio

This module implements rigorous econometric estimators for:
1. Two-Way Fixed Effects (TWFE) Panel Regressions isolating the ceteris paribus price impact
   of discretionary licensing delays, administratively frozen land, and rent-seeking proxies.
2. Empirical Housing Supply Elasticity (epsilon_s) under Discretionary PGOU vs By-Right regimes.
3. Microeconomic Welfare Quantification: Harberger Deadweight Loss (DWL) and Tullock Rent-Seeking Dissipation.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS


class SpanishZoningEconometrics:
    """
    Econometric analyzer for municipal land-use panel data.
    Implements panel fixed-effects estimation with municipality-clustered standard errors.
    """

    def __init__(self, data_path: str = "data/spanish_municipalities_panel.csv"):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self._prepare_panel_data()

    def _prepare_panel_data(self) -> None:
        """Sets up log transformations and multi-index for linearmodels PanelOLS."""
        df = self.df.copy()
        df["ln_price"] = np.log(df["housing_price_sqm"])
        df["ln_by_right_price"] = np.log(df["by_right_price_sqm"])
        df["ln_income"] = np.log(df["income_per_capita"])
        df["ln_cost"] = np.log(df["construction_cost_sqm"])
        df["ln_starts"] = np.log(df["housing_starts_per_1000"])
        df["ln_by_right_starts"] = np.log(df["by_right_starts_per_1000"])
        df["ln_corruption"] = np.log1p(df["corruption_cases_cum"])
        
        # Interaction between demographic growth and land rationing
        df["pop_growth_x_frozen"] = df["pop_growth_pct"] * df["frozen_land_ratio"]
        df["pop_growth_x_delay"] = df["pop_growth_pct"] * df["licensing_delay_months"]

        # Multi-index for panel analysis (entity = municipality_id, time = year)
        df_panel = df.set_index(["municipality_id", "year"])
        self.panel_df = df_panel
        self.flat_df = df

    def run_price_panel_models(self) -> Dict[str, Any]:
        """
        Runs a battery of panel regressions:
        Model 1: Pooled OLS
        Model 2: Municipality Fixed Effects (Entity FE)
        Model 3: Two-Way Fixed Effects (Entity FE + Time FE) - Primary Specification
        Model 4: Two-Way Fixed Effects with Demand-Regulation Interaction Terms
        """
        exog_base = [
            "licensing_delay_months",
            "frozen_land_ratio",
            "reclassification_premium",
            "ln_corruption",
            "ln_income",
            "ln_cost",
            "pop_growth_pct",
            "euribor_12m",
        ]

        # Model 1: Pooled OLS (Cluster robust)
        pols = PooledOLS(
            self.panel_df["ln_price"],
            sm.add_constant(self.panel_df[exog_base]),
        )
        res_pols = pols.fit(cov_type="clustered", cluster_entity=True)

        # Model 2: Municipality FE
        mfe = PanelOLS(
            self.panel_df["ln_price"],
            self.panel_df[exog_base],
            entity_effects=True,
            time_effects=False,
            drop_absorbed=True,
        )
        res_mfe = mfe.fit(cov_type="clustered", cluster_entity=True)

        # In TWFE, time-invariant macro shocks (Euribor, national cost index) are absorbed by Year FE
        exog_twfe = [
            "licensing_delay_months",
            "frozen_land_ratio",
            "reclassification_premium",
            "ln_corruption",
            "ln_income",
            "pop_growth_pct",
        ]

        # Model 3: Two-Way Fixed Effects (Benchmark TWFE)
        twfe = PanelOLS(
            self.panel_df["ln_price"],
            self.panel_df[exog_twfe],
            entity_effects=True,
            time_effects=True,
        )
        res_twfe = twfe.fit(cov_type="clustered", cluster_entity=True)

        # Model 4: TWFE with Interaction Terms
        exog_interact = exog_twfe + ["pop_growth_x_frozen", "pop_growth_x_delay"]
        twfe_interact = PanelOLS(
            self.panel_df["ln_price"],
            self.panel_df[exog_interact],
            entity_effects=True,
            time_effects=True,
        )
        res_twfe_interact = twfe_interact.fit(cov_type="clustered", cluster_entity=True)

        results = {
            "Pooled_OLS": res_pols,
            "Municipality_FE": res_mfe,
            "TWFE_Benchmark": res_twfe,
            "TWFE_Interaction": res_twfe_interact,
        }
        return results

    def estimate_supply_elasticities(self) -> Dict[str, Any]:
        """
        Estimates Housing Supply Elasticity (epsilon_s) under both regimes:
        ln(Starts_it) = alpha_i + lambda_t + epsilon_s * ln(Price_it) + beta * Delay_it + u_it
        """
        # Regime 1: Discretionary Status Quo (PGOU)
        mod_pgou = PanelOLS(
            self.panel_df["ln_starts"],
            self.panel_df[["ln_price", "licensing_delay_months"]],
            entity_effects=True,
            time_effects=True,
            drop_absorbed=True,
        )
        res_pgou = mod_pgou.fit(cov_type="clustered", cluster_entity=True)

        # Regime 2: Liberalized By-Right Counterfactual
        mod_byright = PanelOLS(
            self.panel_df["ln_by_right_starts"],
            self.panel_df[["ln_by_right_price"]],
            entity_effects=True,
            time_effects=True,
            drop_absorbed=True,
        )
        res_byright = mod_byright.fit(cov_type="clustered", cluster_entity=True)

        # Elasticity breakdown by municipal tier
        tier_elasticities = {}
        for tier in self.flat_df["tier"].unique():
            sub = self.flat_df[self.flat_df["tier"] == tier].set_index(["municipality_id", "year"])
            
            # Status Quo
            m_p = PanelOLS(sub["ln_starts"], sub[["ln_price"]], entity_effects=True, time_effects=True, drop_absorbed=True)
            r_p = m_p.fit(cov_type="clustered", cluster_entity=True)
            
            # By-Right
            m_b = PanelOLS(sub["ln_by_right_starts"], sub[["ln_by_right_price"]], entity_effects=True, time_effects=True, drop_absorbed=True)
            r_b = m_b.fit(cov_type="clustered", cluster_entity=True)

            tier_elasticities[tier] = {
                "pgou_elasticity": float(r_p.params["ln_price"]),
                "pgou_se": float(r_p.std_errors["ln_price"]),
                "pgou_pval": float(r_p.pvalues["ln_price"]),
                "byright_elasticity": float(r_b.params["ln_by_right_price"]),
                "byright_se": float(r_b.std_errors["ln_by_right_price"]),
                "byright_pval": float(r_b.pvalues["ln_by_right_price"]),
                "elasticity_multiplier": float(r_b.params["ln_by_right_price"] / r_p.params["ln_price"]),
            }

        # Wald hypothesis test: Difference between by-right and PGOU elasticity
        eps_pgou = float(res_pgou.params["ln_price"])
        se_pgou = float(res_pgou.std_errors["ln_price"])
        eps_byright = float(res_byright.params["ln_by_right_price"])
        se_byright = float(res_byright.std_errors["ln_by_right_price"])
        diff = eps_byright - eps_pgou
        se_diff = np.sqrt(se_pgou**2 + se_byright**2)
        z_stat = diff / se_diff
        p_val_diff = 2.0 * (1.0 - stats.norm.cdf(abs(z_stat)))

        return {
            "res_pgou": res_pgou,
            "res_byright": res_byright,
            "overall_pgou_elasticity": eps_pgou,
            "overall_byright_elasticity": eps_byright,
            "difference_z_stat": float(z_stat),
            "difference_p_value": float(p_val_diff),
            "tier_elasticities": tier_elasticities,
        }

    def quantify_welfare_and_rent_seeking(self) -> Dict[str, Any]:
        """
        Quantifies the cumulative microeconomic burden of discretionary land-use:
        1. Harberger Deadweight Loss Triangle (Unrealized trades from artificial rationing).
        2. Tullock Rent Dissipation (Wealth extracted/dissipated from buyers to bureaucratic frictions).
        3. Total Social Cost and per-capita burden.
        """
        df = self.flat_df

        total_dwl = df["deadweight_loss_millions"].sum()
        total_transfer = df["wealth_transfer_millions"].sum()
        total_social_cost = df["total_economic_cost_millions"].sum()

        # Annual averages
        annual_dwl = total_dwl / df["year"].nunique()
        annual_transfer = total_transfer / df["year"].nunique()
        annual_social_cost = total_social_cost / df["year"].nunique()

        # Breakdown by municipal tier
        tier_summary = df.groupby("tier").agg(
            total_dwl_millions=("deadweight_loss_millions", "sum"),
            total_transfer_millions=("wealth_transfer_millions", "sum"),
            total_cost_millions=("total_economic_cost_millions", "sum"),
            avg_price_markup_pct=("artificial_price_markup_pct", "mean"),
            avg_delay_months=("licensing_delay_months", "mean"),
            avg_frozen_ratio=("frozen_land_ratio", "mean"),
            avg_reclass_premium=("reclassification_premium", "mean"),
        ).reset_index()

        # Per capita cumulative burden (EUR per resident across the 52 municipalities)
        total_pop_2023 = df[df["year"] == 2023]["population"].sum()
        cumulative_burden_per_capita = (total_social_cost * 1e6) / total_pop_2023

        return {
            "cumulative_deadweight_loss_billions": float(total_dwl / 1000.0),
            "cumulative_wealth_transfer_billions": float(total_transfer / 1000.0),
            "cumulative_total_social_cost_billions": float(total_social_cost / 1000.0),
            "annual_deadweight_loss_billions": float(annual_dwl / 1000.0),
            "annual_wealth_transfer_billions": float(annual_transfer / 1000.0),
            "annual_total_social_cost_billions": float(annual_social_cost / 1000.0),
            "cumulative_burden_per_capita_eur": float(cumulative_burden_per_capita),
            "tier_summary": tier_summary,
        }


def format_regression_table(results: Dict[str, Any]) -> str:
    """Formats panel models into an publication-grade comparative ASCII table."""
    models = ["Pooled_OLS", "Municipality_FE", "TWFE_Benchmark", "TWFE_Interaction"]
    vars_to_show = [
        "licensing_delay_months",
        "frozen_land_ratio",
        "reclassification_premium",
        "ln_corruption",
        "ln_income",
        "pop_growth_pct",
        "euribor_12m",
        "pop_growth_x_frozen",
        "pop_growth_x_delay",
    ]

    out = []
    out.append("=" * 95)
    out.append(f"{'Variable':<28} | {'(1) Pooled OLS':<14} | {'(2) Muni FE':<14} | {'(3) TWFE':<14} | {'(4) TWFE Inter':<14}")
    out.append("-" * 95)

    for var in vars_to_show:
        line_coef = f"{var:<28} | "
        line_se = f"{'':<28} | "
        for m in models:
            res = results[m]
            if var in res.params:
                coef = res.params[var]
                se = res.std_errors[var]
                pval = res.pvalues[var]
                stars = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
                line_coef += f"{coef:8.4f}{stars:<4}  | "
                line_se += f"({se:7.4f})      | "
            else:
                line_coef += f"{'--':^14} | "
                line_se += f"{'':^14} | "
        out.append(line_coef)
        out.append(line_se)

    out.append("-" * 95)
    out.append(f"{'Municipality FE':<28} | {'No':^14} | {'Yes':^14} | {'Yes':^14} | {'Yes':^14}")
    out.append(f"{'Year FE':<28} | {'No':^14} | {'No':^14} | {'Yes':^14} | {'Yes':^14}")
    out.append(f"{'Clustered SE (Muni)':<28} | {'Yes':^14} | {'Yes':^14} | {'Yes':^14} | {'Yes':^14}")
    
    r2_line = f"{'Within R-squared':<28} | "
    for m in models:
        res = results[m]
        r2_val = getattr(res, "rsquared_within", res.rsquared)
        r2_line += f"{r2_val:12.4f}  | "
    out.append(r2_line)

    n_line = f"{'Observations':<28} | "
    for m in models:
        n_line += f"{results[m].nobs:^14} | "
    out.append(n_line)
    out.append("=" * 95)
    out.append("Standard errors clustered at municipality level in parentheses. * p<0.05, ** p<0.01, *** p<0.001")
    return "\n".join(out)


if __name__ == "__main__":
    econ = SpanishZoningEconometrics()
    reg_results = econ.run_price_panel_models()
    print("\n--- PANEL DATA REGRESSION RESULTS: IMPACT ON LN(PRICE/SQM) ---")
    print(format_regression_table(reg_results))

    print("\n--- SUPPLY ELASTICITY COMPARISON (DISCRETIONARY vs BY-RIGHT) ---")
    elasticity_res = econ.estimate_supply_elasticities()
    print(f"Overall PGOU Supply Elasticity:      {elasticity_res['overall_pgou_elasticity']:.3f}")
    print(f"Overall By-Right Supply Elasticity:  {elasticity_res['overall_byright_elasticity']:.3f}")
    print(f"Difference Wald Z-Stat:              {elasticity_res['difference_z_stat']:.3f} (p-value: {elasticity_res['difference_p_value']:.4e})")
    print("\nTier Elasticity Breakdown:")
    for tier, data in elasticity_res["tier_elasticities"].items():
        print(f"  {tier:<26}: PGOU eps = {data['pgou_elasticity']:.2f} | By-Right eps = {data['byright_elasticity']:.2f} (x{data['elasticity_multiplier']:.1f} higher)")

    print("\n--- WELFARE ECONOMICS & RENT-SEEKING QUANTIFICATION ---")
    welfare = econ.quantify_welfare_and_rent_seeking()
    print(f"Cumulative Deadweight Loss (2009-2023):   €{welfare['cumulative_deadweight_loss_billions']:.2f} Billion")
    print(f"Cumulative Tullock Wealth Transfer:       €{welfare['cumulative_wealth_transfer_billions']:.2f} Billion")
    print(f"Total Cumulative Social Cost:             €{welfare['cumulative_total_social_cost_billions']:.2f} Billion")
    print(f"Annual Total Social Cost:                 €{welfare['annual_total_social_cost_billions']:.2f} Billion / year")
    print(f"Cumulative Burden per Capita (Sample):    €{welfare['cumulative_burden_per_capita_eur']:,.2f} / person")
