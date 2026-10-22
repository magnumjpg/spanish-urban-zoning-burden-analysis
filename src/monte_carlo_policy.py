"""
Monte Carlo Policy Simulation Module
====================================
Project: Zoning Monopoly, Rent-Seeking, and Artificial Scarcity in Spain
Agent: Policy & Simulation Engineer

Simulates 10,000 stochastic Monte Carlo iterations across 3 concrete institutional reform scenarios:
1. Scenario A: "Fast-Track Licensing" (Declaración Responsable + 3-month positive silence)
2. Scenario B: "Targeted Peri-Urban Rezoning" (Freeing 60% of non-protected frozen rustic land)
3. Scenario C: "Comprehensive By-Right Reform" (Presumption of buildability + structural supply elasticity shift)

Quantifies:
- Expected price relief (%)
- Cumulative annual financial savings for Spanish households (€ Billions)
- New annual housing units unlocked
- 95% Empirical Confidence Intervals
"""

import os
import sys
from typing import Dict, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure local imports work
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from econometric_models import SpanishZoningEconometrics


class MonteCarloPolicySimulator:
    """Runs stochastic policy simulations using estimated econometric parameters."""

    def __init__(self, data_path: str = "data/spanish_municipalities_panel.csv", n_sims: int = 10000, seed: int = 42):
        self.n_sims = n_sims
        self.rng = np.random.default_rng(seed)
        self.econ = SpanishZoningEconometrics(data_path)
        self.df_2023 = self.econ.flat_df[self.econ.flat_df["year"] == 2023].copy()
        
        # Pull empirical econometric parameter distributions from TWFE model
        reg_results = self.econ.run_price_panel_models()
        twfe = reg_results["TWFE_Benchmark"]
        
        self.beta_delay_mean = float(twfe.params["licensing_delay_months"])  # ~0.0153
        self.beta_delay_se = float(twfe.std_errors["licensing_delay_months"])  # ~0.0025
        
        self.beta_frozen_mean = float(twfe.params["frozen_land_ratio"])     # ~0.2686
        self.beta_frozen_se = float(twfe.std_errors["frozen_land_ratio"])     # ~0.0970

    def run_simulations(self) -> Dict[str, Any]:
        """Executes 10,000 draws for each reform scenario."""
        # Draw parameter vectors from asymptotic normality
        beta_delay_draws = self.rng.normal(self.beta_delay_mean, self.beta_delay_se, self.n_sims)
        beta_frozen_draws = self.rng.normal(self.beta_frozen_mean, self.beta_frozen_se, self.n_sims)

        current_avg_delay = float(self.df_2023["licensing_delay_months"].mean())
        current_avg_frozen = float(self.df_2023["frozen_land_ratio"].mean())
        total_households_units = float(self.df_2023["new_housing_units"].sum())
        avg_price = float(self.df_2023["housing_price_sqm"].mean())
        avg_sqm = 95.0

        # Scenario 1: Fast-Track Licensing (Delay drops from ~14m to 2.5m)
        delay_reduction_s1 = current_avg_delay - 2.5
        price_drop_pct_s1 = (1.0 - np.exp(-beta_delay_draws * delay_reduction_s1)) * 100.0
        annual_savings_b_s1 = (avg_price * (price_drop_pct_s1 / 100.0) * total_households_units * avg_sqm) / 1e9

        # Scenario 2: Peri-Urban Land Unfreezing (Frozen ratio drops by 60%)
        frozen_reduction_s2 = current_avg_frozen * 0.60
        price_drop_pct_s2 = (1.0 - np.exp(-beta_frozen_draws * frozen_reduction_s2)) * 100.0
        annual_savings_b_s2 = (avg_price * (price_drop_pct_s2 / 100.0) * total_households_units * avg_sqm) / 1e9

        # Scenario 3: Comprehensive By-Right Reform (Combined effect + Supply Elasticity Expansion)
        total_log_reduction_s3 = (beta_delay_draws * delay_reduction_s1) + (beta_frozen_draws * frozen_reduction_s2)
        price_drop_pct_s3 = (1.0 - np.exp(-total_log_reduction_s3)) * 100.0
        # Volume expansion under elastic regime (+42% construction units unlocked)
        volume_multiplier = self.rng.normal(1.42, 0.05, self.n_sims)
        unlocked_units_s3 = total_households_units * (volume_multiplier - 1.0)
        annual_savings_b_s3 = (avg_price * (price_drop_pct_s3 / 100.0) * total_households_units * avg_sqm) / 1e9

        results = {
            "s1_licensing": {
                "name": "Scenario 1: Fast-Track Licensing (3 Months Max)",
                "price_drop_pct": price_drop_pct_s1,
                "savings_billions": annual_savings_b_s1,
                "median_drop": float(np.median(price_drop_pct_s1)),
                "ci_95_drop": (float(np.percentile(price_drop_pct_s1, 2.5)), float(np.percentile(price_drop_pct_s1, 97.5))),
                "median_savings": float(np.median(annual_savings_b_s1)),
                "ci_95_savings": (float(np.percentile(annual_savings_b_s1, 2.5)), float(np.percentile(annual_savings_b_s1, 97.5))),
            },
            "s2_land_unfreezing": {
                "name": "Scenario 2: Peri-Urban Land Unfreezing (-60% Frozen)",
                "price_drop_pct": price_drop_pct_s2,
                "savings_billions": annual_savings_b_s2,
                "median_drop": float(np.median(price_drop_pct_s2)),
                "ci_95_drop": (float(np.percentile(price_drop_pct_s2, 2.5)), float(np.percentile(price_drop_pct_s2, 97.5))),
                "median_savings": float(np.median(annual_savings_b_s2)),
                "ci_95_savings": (float(np.percentile(annual_savings_b_s2, 2.5)), float(np.percentile(annual_savings_b_s2, 97.5))),
            },
            "s3_comprehensive_byright": {
                "name": "Scenario 3: Comprehensive By-Right System (Full Reform)",
                "price_drop_pct": price_drop_pct_s3,
                "savings_billions": annual_savings_b_s3,
                "unlocked_units": unlocked_units_s3,
                "median_drop": float(np.median(price_drop_pct_s3)),
                "ci_95_drop": (float(np.percentile(price_drop_pct_s3, 2.5)), float(np.percentile(price_drop_pct_s3, 97.5))),
                "median_savings": float(np.median(annual_savings_b_s3)),
                "ci_95_savings": (float(np.percentile(annual_savings_b_s3, 2.5)), float(np.percentile(annual_savings_b_s3, 97.5))),
                "median_units": float(np.median(unlocked_units_s3)),
            },
        }
        return results

    def plot_monte_carlo_results(self, results: Dict[str, Any], output_path: str = "assets/figure_6_monte_carlo_policy_simulation.png"):
        """Renders publication-grade distribution plots for the Monte Carlo simulations."""
        plt.style.use("seaborn-v0_8-whitegrid")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

        # Consistent institutional color scheme
        colors = {
            "s1_licensing": "#0284C7",        # Sky Blue
            "s2_land_unfreezing": "#D97706",   # Amber
            "s3_comprehensive_byright": "#059669", # Emerald Green
        }

        # Panel 1: Price Reduction Density (% Drop)
        for key, res in results.items():
            sns.kdeplot(
                res["price_drop_pct"],
                ax=ax1,
                fill=True,
                color=colors[key],
                label=f"{res['name']}\nMedian: -{res['median_drop']:.1f}% [95% CI: {res['ci_95_drop'][0]:.1f}% to {res['ci_95_drop'][1]:.1f}%]",
                alpha=0.35,
                linewidth=2.2,
            )
            ax1.axvline(res["median_drop"], color=colors[key], linestyle="--", linewidth=1.4)

        ax1.set_xlabel("Simulated Housing Price Reduction (%)", fontsize=11, labelpad=8)
        ax1.set_ylabel("Probability Density", fontsize=11, labelpad=8)
        ax1.set_title("A. Distribution of Housing Price Reductions", fontsize=12, weight="bold")
        ax1.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=8.5)

        # Panel 2: Annual Household Financial Relief (€ Billions / Year)
        for key, res in results.items():
            sns.kdeplot(
                res["savings_billions"],
                ax=ax2,
                fill=True,
                color=colors[key],
                label=f"{res['name']}\nMedian: €{res['median_savings']:.2f}B/yr [95% CI: €{res['ci_95_savings'][0]:.2f}B - €{res['ci_95_savings'][1]:.2f}B]",
                alpha=0.35,
                linewidth=2.2,
            )
            ax2.axvline(res["median_savings"], color=colors[key], linestyle="--", linewidth=1.4)

        ax2.set_xlabel("Annual Household Financial Savings (€ Billions / Year)", fontsize=11, labelpad=8)
        ax2.set_ylabel("Probability Density", fontsize=11, labelpad=8)
        ax2.set_title("B. Distribution of Annual Economic Savings for Citizens", fontsize=12, weight="bold")
        ax2.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=8.5)

        fig.suptitle(
            "Figure 6: Monte Carlo Policy Simulation (10,000 Iterations): Expected Impact of Institutional Reforms",
            fontsize=13, weight="bold", y=0.98
        )
        plt.tight_layout()
        fig.savefig(output_path, dpi=300)
        plt.close(fig)
        print(f"[Monte Carlo Simulator] Simulation figure exported to: {output_path}")


if __name__ == "__main__":
    sim = MonteCarloPolicySimulator()
    res = sim.run_simulations()
    sim.plot_monte_carlo_results(res)
    print("\n--- MONTE CARLO SIMULATION RESULTS (10,000 RUNS) ---")
    for k, v in res.items():
        print(f"\n{v['name']}:")
        print(f"  Price Reduction:     -{v['median_drop']:.2f}% (95% CI: [{v['ci_95_drop'][0]:.2f}%, {v['ci_95_drop'][1]:.2f}%])")
        print(f"  Annual Savings:      €{v['median_savings']:.2f} Billion/year (95% CI: [€{v['ci_95_savings'][0]:.2f}B, €{v['ci_95_savings'][1]:.2f}B])")
        if "median_units" in v:
            print(f"  Unlocked New Homes:  +{v['median_units']:,.0f} units/year")
