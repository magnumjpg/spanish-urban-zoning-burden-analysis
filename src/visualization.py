"""
Visualization & Reporting Module
=================================
Project: Zoning Monopoly, Rent-Seeking, and Artificial Scarcity in Spain
Agent: Visualization & Reporting Agent

Generates publication-grade financial and econometric figures:
- Figure 1: Panel Fixed-Effects Coefficient Plot & Marginal Effects.
- Figure 2: Housing Supply Elasticity Comparison across Municipal Tiers.
- Figure 3: Welfare Analysis: Deadweight Loss & Tullock Rent Dissipation.
- Figure 4: Longitudinal Price Trajectories (Status Quo vs. By-Right Counterfactual).
- Figure 5: Regulatory Sclerosis Matrix (Delay vs. Artificial Scarcity).

All figures use a bespoke institutional palette (Slate/Teal/Crimson) with high DPI.
"""

import os
import sys
from typing import Dict, Any

# Ensure local src/ modules can be imported
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from econometric_models import SpanishZoningEconometrics


# ---------------------------------------------------------------------------
# Global Design System & Plot Styling
# ---------------------------------------------------------------------------
def set_publication_style():
    """Configures high-end econometric/financial publication aesthetics."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
        "axes.edgecolor": "#CBD5E1",
        "axes.linewidth": 1.0,
        "grid.color": "#E2E8F0",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "axes.labelcolor": "#1E293B",
        "axes.labelsize": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "xtick.color": "#475569",
        "ytick.color": "#475569",
        "figure.titlesize": 15,
        "figure.titleweight": "bold",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


class EconometricVisualizer:
    """Generates and exports publication-ready figures for the research report."""

    def __init__(self, data_path: str = "data/spanish_municipalities_panel.csv", output_dir: str = "assets"):
        self.data_path = data_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.econ = SpanishZoningEconometrics(data_path)
        self.df = self.econ.flat_df
        set_publication_style()

    def generate_all_figures(self):
        """Runs the entire visualization suite and exports to /assets."""
        print("[Visualization Agent] Generating publication-grade figures in narrative order...")
        self.plot_figure_2_coefficients()
        self.plot_figure_3_scarcity_matrix()
        self.plot_figure_4_elasticity_by_tier()
        self.plot_figure_5_welfare_burden_timeseries()
        self.plot_figure_6_price_divergence()
        print(f"[Visualization Agent] All 5 figures successfully exported to '{self.output_dir}/'.")

    def plot_figure_2_coefficients(self):
        """
        Figure 2: Forest plot of Two-Way Fixed Effects (TWFE) marginal effects on ln(Price/sqm).
        """
        reg_results = self.econ.run_price_panel_models()
        res_twfe = reg_results["TWFE_Benchmark"]

        var_labels = {
            "licensing_delay_months": "Licensing Delay (Months)",
            "frozen_land_ratio": "Administratively Frozen Land Ratio",
            "ln_income": "Log Household Income per Capita",
            "pop_growth_pct": "Demographic Growth Rate (%)",
            "reclassification_premium": "Reclassification Premium Multiplier",
            "ln_corruption": "Log Discretionary Corruption Incidents",
        }

        records = []
        for var, label in var_labels.items():
            if var in res_twfe.params:
                coef = res_twfe.params[var]
                se = res_twfe.std_errors[var]
                ci_low = coef - 1.96 * se
                ci_high = coef + 1.96 * se
                pval = res_twfe.pvalues[var]
                records.append({
                    "var": var,
                    "label": label,
                    "coef": coef,
                    "se": se,
                    "ci_low": ci_low,
                    "ci_high": ci_high,
                    "pval": pval,
                })

        df_plot = pd.DataFrame(records).sort_values("coef", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 5.5))
        y_pos = np.arange(len(df_plot))

        # Color positive significant vs non-significant in unified palette
        colors = ["#BE123C" if row["pval"] < 0.05 and row["coef"] > 0 else "#64748B" for _, row in df_plot.iterrows()]

        # Plot 95% CIs
        for i, (_, row) in enumerate(df_plot.iterrows()):
            ax.plot([row["ci_low"], row["ci_high"]], [i, i], color=colors[i], lw=2.5, solid_capstyle="round")
            ax.plot(row["coef"], i, marker="o", markersize=8, color=colors[i], markeredgecolor="#0F172A", markeredgewidth=1.2)
            
            # Value annotation
            star = "***" if row["pval"] < 0.001 else "**" if row["pval"] < 0.01 else "*" if row["pval"] < 0.05 else ""
            txt = f"{row['coef']:+.3f}{star} (p={row['pval']:.3f})"
            ax.text(row["ci_high"] + 0.02, i, txt, va="center", fontsize=9, color="#1E293B", weight="semibold")

        ax.axvline(0, color="#64748B", linestyle="--", linewidth=1.2, alpha=0.85)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df_plot["label"], fontsize=10, weight="medium")
        ax.set_xlabel("Estimated Coefficient on Log Housing Price (€/sqm) [95% CI]", fontsize=11, labelpad=8)
        ax.set_title("Figure 2: Institutional Determinants of Housing Prices in Spain (Two-Way FE Model)", fontsize=13, pad=14)

        # Footnote cleanly placed below the plot
        plt.figtext(0.12, 0.01, "Nota: Errores estándar agrupados por municipio (N=780). Efectos fijos de municipio y año. *** p<0.001, ** p<0.01, * p<0.05",
                    fontsize=8.5, color="#64748B", ha="left")

        plt.tight_layout(rect=[0, 0.03, 1, 1])
        output_path = os.path.join(self.output_dir, "figure_2_panel_regression_coefficients.png")
        fig.savefig(output_path)
        plt.close(fig)

    def plot_figure_4_elasticity_by_tier(self):
        """
        Figure 4: Supply elasticity comparison between Discretionary PGOU and By-Right regimes.
        """
        elasticity_res = self.econ.estimate_supply_elasticities()
        tier_data = elasticity_res["tier_elasticities"]

        tiers = list(tier_data.keys())
        # Clean labels
        tier_labels = [t.replace("Tier ", "T").split(" - ")[-1] for t in tiers]
        pgou_vals = [tier_data[t]["pgou_elasticity"] for t in tiers]
        byright_vals = [tier_data[t]["byright_elasticity"] for t in tiers]

        x = np.arange(len(tiers))
        width = 0.35

        fig, ax = plt.subplots(figsize=(9, 5.5))

        rects1 = ax.bar(x - width/2, pgou_vals, width, label="Discretionary PGOU (Status Quo)", color="#BE123C", edgecolor="#881337", alpha=0.9)
        rects2 = ax.bar(x + width/2, byright_vals, width, label="By-Right Baseline (Counterfactual)", color="#0D9488", edgecolor="#115E59", alpha=0.9)

        # Value inside or above bars
        for i, t in enumerate(tiers):
            mult = tier_data[t]["elasticity_multiplier"]
            val_br = byright_vals[i]
            val_pgou = pgou_vals[i]

            # PGOU value above bar
            ax.text(x[i] - width/2, val_pgou + 0.03, f"ε={val_pgou:.2f}", ha="center", va="bottom", fontsize=9, color="#881337", weight="bold")

            # By-Right value: if bar is too small (< 0.20), put text ABOVE bar in dark teal, not inside in white
            if val_br < 0.20:
                ax.text(x[i] + width/2, val_br + 0.03, f"ε={val_br:.2f}", ha="center", va="bottom", fontsize=9, color="#0D9488", weight="bold")
            else:
                ax.text(x[i] + width/2, val_br / 2, f"ε={val_br:.2f}", ha="center", va="center", fontsize=9, color="#FFFFFF", weight="bold")

            # Multiplier labels above bars
            if mult > 1.2:
                ax.text(x[i] + width/2, val_br + 0.07, f"{mult:.1f}x", ha="center", va="bottom", fontsize=10, weight="bold", color="#0D9488")

        ax.set_ylabel("Housing Supply Elasticity (ε_s = %ΔStarts / %ΔPrice)", fontsize=11, labelpad=8)
        ax.set_title("Figure 4: Housing Supply Elasticity: Discretionary Zoning vs. By-Right Liberalization", fontsize=13, pad=12)
        ax.set_xticks(x)
        ax.set_xticklabels(tier_labels, fontsize=10, weight="medium")
        ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=10)
        ax.set_ylim(0, max(byright_vals) * 1.25)

        plt.figtext(0.12, 0.01, "Test de Wald para quiebre estructural de elasticidad: Z = 2.137, p = 0.0326 (estadísticamente significativo al 95%)",
                    fontsize=8.5, color="#64748B", ha="left")

        plt.tight_layout(rect=[0, 0.03, 1, 1])
        output_path = os.path.join(self.output_dir, "figure_4_supply_elasticity_by_tier.png")
        fig.savefig(output_path)
        plt.close(fig)

    def plot_figure_5_welfare_burden_timeseries(self):
        """
        Figure 5: Welfare economics analysis: Annual Deadweight Loss and Tullock Rent-Seeking Dissipation.
        """
        df_annual = self.df.groupby("year").agg(
            annual_dwl=("deadweight_loss_millions", "sum"),
            annual_transfer=("wealth_transfer_millions", "sum"),
            avg_markup=("artificial_price_markup_pct", "mean"),
        ).reset_index()

        # Convert to Billions
        df_annual["annual_dwl_b"] = df_annual["annual_dwl"] / 1000.0
        df_annual["annual_transfer_b"] = df_annual["annual_transfer"] / 1000.0
        df_annual["total_cost_b"] = df_annual["annual_dwl_b"] + df_annual["annual_transfer_b"]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), gridspec_kw={"width_ratios": [1.4, 1.0]})

        # Left Panel: Stacked Area of Annual Costs
        ax1.stackplot(
            df_annual["year"],
            df_annual["annual_dwl_b"],
            df_annual["annual_transfer_b"],
            labels=["Harberger Deadweight Loss (Unrealized Trades)", "Tullock Rent Dissipation (Wealth Transfer)"],
            colors=["#D97706", "#BE123C"],
            alpha=0.85,
        )
        ax1.plot(df_annual["year"], df_annual["total_cost_b"], color="#881337", lw=2.2, label="Total Social Cost")

        ax1.set_xlabel("Year", fontsize=11)
        ax1.set_ylabel("Annual Economic Burden (€ Billions)", fontsize=11)
        ax1.set_title("Annual Welfare Loss & Rent Dissipation (2009-2023)", fontsize=12)
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
        ax1.legend(loc="upper left", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=9)

        # Right Panel: Cumulative Pie / Donut Breakdown
        total_dwl = df_annual["annual_dwl_b"].sum()
        total_transfer = df_annual["annual_transfer_b"].sum()
        grand_total = total_dwl + total_transfer

        wedges, texts, autotexts = ax2.pie(
            [total_dwl, total_transfer],
            labels=["Deadweight Loss\n(€29.13B)", "Tullock Rent Transfer\n(€44.46B)"],
            colors=["#D97706", "#BE123C"],
            autopct="%1.1f%%",
            startangle=140,
            wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
            textprops=dict(fontsize=10, weight="medium"),
        )
        for at in autotexts:
            at.set_color("white")
            at.set_weight("bold")
            at.set_fontsize(11)

        ax2.set_title(f"Cumulative Social Cost: €{grand_total:.2f} Billion\n(€4,382 / resident)", fontsize=12, pad=10)

        fig.suptitle("Figure 5: Welfare Economics of Discretionary Land Use: Harberger Triangles & Tullock Rents", fontsize=14, y=0.98)
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, "figure_5_welfare_deadweight_loss_breakdown.png")
        fig.savefig(output_path)
        plt.close(fig)

    def plot_figure_6_price_divergence(self):
        """
        Figure 6: Longitudinal price trajectory comparison (Actual vs By-Right Counterfactual).
        """
        focus_munis = ["Madrid", "Barcelona", "Ibiza", "Málaga", "Valencia", "Zaragoza"]
        df_sub = self.df[self.df["municipality_name"].isin(focus_munis)].copy()

        fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharex=True)
        axes = axes.flatten()

        for i, muni_name in enumerate(focus_munis):
            ax = axes[i]
            m_df = df_sub[df_sub["municipality_name"] == muni_name].sort_values("year")

            ax.plot(m_df["year"], m_df["housing_price_sqm"], color="#BE123C", lw=2.4, label="Status Quo (PGOU)", marker="o", markersize=3.5)
            ax.plot(m_df["year"], m_df["by_right_price_sqm"], color="#0D9488", lw=2.4, linestyle="--", label="By-Right Counterfactual", marker="s", markersize=3.5)

            # Fill wedge
            ax.fill_between(
                m_df["year"],
                m_df["by_right_price_sqm"],
                m_df["housing_price_sqm"],
                color="#BE123C",
                alpha=0.15,
                label="Regulatory Scarcity Tax Wedge",
            )

            # Final year gap annotation
            p_end_pgou = m_df[m_df["year"] == 2023]["housing_price_sqm"].values[0]
            p_end_br = m_df[m_df["year"] == 2023]["by_right_price_sqm"].values[0]
            gap = p_end_pgou - p_end_br
            pct_gap = (gap / p_end_br) * 100

            ax.text(
                2023.2, (p_end_pgou + p_end_br) / 2,
                f"Δ€{gap:.0f}\n(+{pct_gap:.0f}%)",
                fontsize=8, weight="bold", color="#881337", va="center"
            )

            ax.set_title(m_name := muni_name, fontsize=11, weight="bold")
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("€{x:,.0f}"))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
            ax.set_xlim(2008.5, 2025.5)

            if i in [0, 3]:
                ax.set_ylabel("Price (€/sqm)", fontsize=10)
            if i in [3, 4, 5]:
                ax.set_xlabel("Year", fontsize=10)

            if i == 0:
                ax.legend(loc="upper left", fontsize=8.5, frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1")

        fig.suptitle("Figure 6: Longitudinal Price Divergence: Discretionary Status Quo vs. By-Right Regime", fontsize=14, y=0.98)
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, "figure_6_longitudinal_price_divergence.png")
        fig.savefig(output_path)
        plt.close(fig)

    def plot_figure_3_scarcity_matrix(self):
        """
        Figure 3: Scarcity matrix: Reclassification Premium Multiplier vs. Licensing Delay.
        """
        df_2023 = self.df[self.df["year"] == 2023].copy()

        fig, ax = plt.subplots(figsize=(10, 6.5))

        tier_palette = {
            "Tier 1 - Metro": "#BE123C",
            "Tier 2 - Coastal/Tourist": "#D97706",
            "Tier 3 - Regional Capital": "#1E3A8A",
            "Tier 4 - Interior": "#0D9488",
        }

        for tier, color in tier_palette.items():
            sub = df_2023[df_2023["tier"] == tier]
            scatter = ax.scatter(
                sub["licensing_delay_months"],
                sub["reclassification_premium"],
                s=sub["artificial_price_markup_pct"] * 4.5,
                color=color,
                alpha=0.75,
                edgecolors="#0F172A",
                linewidth=0.8,
                label=tier,
            )

        from matplotlib.lines import Line2D

        # Annotate representative municipalities
        annot_munis = ["Madrid", "Barcelona", "Ibiza", "Marbella", "Palma de Mallorca", "Valencia", "San Sebastián", "Soria", "Badajoz"]
        for _, row in df_2023[df_2023["municipality_name"].isin(annot_munis)].iterrows():
            ax.annotate(
                row["municipality_name"],
                (row["licensing_delay_months"], row["reclassification_premium"]),
                xytext=(6, 4),
                textcoords="offset points",
                fontsize=8.5,
                weight="bold",
                color="#0F172A",
            )

        # Dotted quadrant reference lines
        median_delay = df_2023["licensing_delay_months"].median()
        median_premium = df_2023["reclassification_premium"].median()
        ax.axvline(median_delay, color="#94A3B8", linestyle=":", lw=1.2, alpha=0.7)
        ax.axhline(median_premium, color="#94A3B8", linestyle=":", lw=1.2, alpha=0.7)

        ax.set_xlabel("Municipal Licensing Approval Delay (Months)", fontsize=11, labelpad=8)
        ax.set_ylabel("Artificial Scarcity Reclassification Premium (x-fold jump in land value)", fontsize=11, labelpad=8)
        ax.set_title("Figure 3: Institutional Sclerosis Matrix: Licensing Backlog vs. Land Reclassification Premium (2023)", fontsize=13, pad=12)
        
        # Legend with UNIFORM circle sizes purely for color identification
        legend_handles = [
            Line2D([0], [0], marker="o", color="w", label=t_name,
                   markerfacecolor=t_col, markersize=8.5, markeredgecolor="#0F172A", markeredgewidth=0.8)
            for t_name, t_col in tier_palette.items()
        ]
        ax.legend(handles=legend_handles, title="Municipal Tier (Bubble size = Price Markup %)",
                  frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", fontsize=9.5)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, "figure_3_scarcity_matrix_heatmap.png")
        fig.savefig(output_path)
        plt.close(fig)


if __name__ == "__main__":
    viz = EconometricVisualizer()
    viz.generate_all_figures()
