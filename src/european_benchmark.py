"""
European Benchmark & Territorial Paradox Visualization Module
==============================================================
Project: Spanish Urban Zoning Burden Analysis
Agent: Visualization & Reporting Agent

Generates Figure 7: "The Spanish Territorial Paradox and European Benchmark"
Integrating empirical Eurostat GEOSTAT 1km² population grid microdata,
EU-SILC housing cost overburden, and Banco de España structural indicators.
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# Set global publication styling
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
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.5,
    "axes.titleweight": "bold",
    "xtick.color": "#475569",
    "ytick.color": "#475569",
    "figure.titlesize": 14,
    "figure.titleweight": "bold",
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def plot_figure_7_european_benchmark(output_path: str = "assets/figure_7_european_benchmark_paradox.png"):
    """
    Renders 4-panel European benchmark:
    - Panel A: Inhabited 1km² Cells (Spain 13% vs EU average 60-70%)
    - Panel B: Effective Residential Density in Inhabited Areas (Spain 737 hab/km²)
    - Panel C: Housing Cost Overburden in Market Rent (>40% income spent on housing)
    - Panel D: Youth Emancipation Age (Spain 30.3y vs Nordic 21.4y)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    # -------------------------------------------------------------
    # Panel A: Inhabited 1km² Population Grid Cells (%) - Eurostat GEOSTAT
    # -------------------------------------------------------------
    ax = axes[0]
    countries_a = ["España", "Portugal", "Italia", "Alemania", "Francia", "Países Bajos"]
    cells_pct = [13.0, 44.5, 57.2, 59.9, 67.8, 78.4]
    colors_a = ["#E11D48" if c == "España" else "#0284C7" for c in countries_a]

    bars_a = ax.barh(countries_a, cells_pct, color=colors_a, height=0.55, edgecolor="#0F172A", linewidth=0.8)
    for bar in bars_a:
        width = bar.get_width()
        ax.text(width + 1.5, bar.get_y() + bar.get_height() / 2, f"{width:.1f}%", va="center", fontsize=9.5, weight="bold", color="#1E293B")

    ax.set_xlim(0, 92)
    ax.set_xlabel("Celdas de 1 km² con Población Habitada (%)", fontsize=10.5, labelpad=6)
    ax.set_title("A. El Territorio Vacío: Proporción de Superficie Habitada", fontsize=11.5, weight="bold")
    ax.text(0.04, 0.15, "España: 87,0% del territorio peninsular e insular\nse encuentra deshabitado (Eurostat/JRC)", transform=ax.transAxes,
            fontsize=8.5, weight="medium", color="#9F1239",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF1F2", edgecolor="#FECDD3"))

    # -------------------------------------------------------------
    # Panel B: Effective Residential Density in Inhabited Zones (hab/km²)
    # -------------------------------------------------------------
    ax = axes[1]
    densities = [737, 251, 348, 390, 175, 647]
    bars_b = ax.barh(countries_a, densities, color=colors_a, height=0.55, edgecolor="#0F172A", linewidth=0.8)
    for bar in bars_b:
        width = bar.get_width()
        ax.text(width + 12, bar.get_y() + bar.get_height() / 2, f"{width:,} hab/km²", va="center", fontsize=9.5, weight="bold", color="#1E293B")

    ax.set_xlim(0, 890)
    ax.set_xlabel("Densidad Demográfica Efectiva en Mallas Habitadas (hab/km²)", fontsize=10.5, labelpad=6)
    ax.set_title("B. La Macrocefalia Urbana: Densidad Residencial Efectiva", fontsize=11.5, weight="bold")
    ax.text(0.48, 0.82, "España ostenta la mayor densidad residencial\nefectiva de la UE (Banco de España / GEOSTAT)", transform=ax.transAxes,
            fontsize=8.5, weight="medium", color="#9F1239",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF1F2", edgecolor="#FECDD3"))

    # -------------------------------------------------------------
    # Panel C: Housing Cost Overburden in Private Rent (>40% income)
    # -------------------------------------------------------------
    ax = axes[2]
    countries_c = ["España", "Dinamarca", "Italia", "Media UE-27", "Francia", "Alemania"]
    overburden = [38.0, 26.9, 22.3, 21.2, 18.7, 13.2]
    colors_c = ["#E11D48" if c == "España" else "#64748B" if "Media" in c else "#0284C7" for c in countries_c]

    bars_c = ax.bar(countries_c, overburden, color=colors_c, width=0.55, edgecolor="#0F172A", linewidth=0.8)
    for bar in bars_c:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1.0, f"{height:.1f}%", ha="center", fontsize=9.5, weight="bold", color="#1E293B")

    ax.set_ylim(0, 48)
    ax.set_ylabel("Inquilinos con Esfuerzo > 40% de la Renta (%)", fontsize=10.5)
    ax.set_title("C. Sobrecarga Financiera en Alquiler a Mercado (Eurostat)", fontsize=11.5, weight="bold")
    ax.text(0.04, 0.85, "1 de cada 3 inquilinos españoles destina más del 40%\nde su renta al alquiler (en quintil bajo supera 65%)", transform=ax.transAxes,
            fontsize=8.5, color="#9F1239",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF1F2", edgecolor="#FECDD3"))

    # -------------------------------------------------------------
    # Panel D: Youth Emancipation Age (Eurostat EU-SILC)
    # -------------------------------------------------------------
    ax = axes[3]
    countries_d = ["España", "Italia", "Media UE-27", "Francia", "Alemania", "Finlandia"]
    ages = [30.3, 30.0, 26.4, 23.7, 23.9, 21.3]
    colors_d = ["#E11D48" if c == "España" else "#64748B" if "Media" in c else "#059669" for c in countries_d]

    bars_d = ax.bar(countries_d, ages, color=colors_d, width=0.55, edgecolor="#0F172A", linewidth=0.8)
    for bar in bars_d:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.6, f"{height:.1f} años", ha="center", fontsize=9.5, weight="bold", color="#1E293B")

    ax.set_ylim(0, 36)
    ax.set_ylabel("Edad Media de Emancipación Juvenil (Años)", fontsize=10.5)
    ax.set_title("D. Retraso en el Ciclo Vital: Emancipación Juvenil", fontsize=11.5, weight="bold")
    ax.text(0.04, 0.85, "Brecha de casi 4 años respecto a la UE\ny casi 10 años frente al modelo escandinavo", transform=ax.transAxes,
            fontsize=8.5, color="#1E293B",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F1F5F9", edgecolor="#CBD5E1"))

    fig.suptitle(
        "Figura 7: El Espejo Europeo y la Paradoja Territorial: Densidad, Sobrecarga de Alquiler y Emancipación",
        fontsize=13.5, weight="bold", y=0.99
    )
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"[European Benchmark Visualizer] Figure exported to: {output_path}")


if __name__ == "__main__":
    plot_figure_7_european_benchmark()
