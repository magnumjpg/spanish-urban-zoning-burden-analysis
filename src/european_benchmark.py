"""
European Benchmark & Territorial Paradox Visualization Module (Clean & Minimalist)
===================================================================================
Project: Spanish Urban Zoning Burden Analysis
Author: Jaime Pérez | Quantitative Economics Portfolio

Renders Figure 7: Zero-clutter, publication-grade benchmark aligning with the
Banco de España Annual Report 2025/2026 (David López Salido, June 2026).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Configure clean aesthetic (Banco de España / FT style)
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
    "axes.edgecolor": "#CBD5E1",
    "axes.linewidth": 1.0,
    "grid.color": "#F1F5F9",
    "grid.linestyle": "--",
    "grid.alpha": 0.8,
    "axes.labelcolor": "#1E293B",
    "axes.labelsize": 10.0,
    "axes.titlesize": 11.0,
    "axes.titleweight": "bold",
    "xtick.color": "#475569",
    "ytick.color": "#475569",
    "figure.titlesize": 13.5,
    "figure.titleweight": "bold",
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def plot_figure_1_clean(output_path: str = "assets/figure_1_european_benchmark_paradox.png"):
    """
    Renders 4-panel clean benchmark (Figure 1):
    - Panel A: Inhabited 1km² Grid Cells (%) [Eurostat GEOSTAT]
    - Panel B: Effective Residential Density in Inhabited Areas (hab/km²) [Eurostat/BdE]
    - Panel C: Cumulative Housing Deficit 2021-2025 (% Average Households) [BdE Slide 29]
    - Panel D: Years of Net Household Income to Buy a Home (2024/2025) [BdE Slide 43]
    """
    fig, axes = plt.subplots(2, 2, figsize=(13, 8.5))
    axes = axes.flatten()

    # -------------------------------------------------------------
    # Panel A: Inhabited 1km² Population Grid Cells (%) - Eurostat GEOSTAT
    # -------------------------------------------------------------
    ax = axes[0]
    countries_a = ["España", "Portugal", "Italia", "Alemania", "Francia", "Países Bajos"]
    cells_pct = [13.0, 44.5, 57.2, 59.9, 67.8, 78.4]
    colors_a = ["#BE123C" if c == "España" else "#1E3A8A" for c in countries_a]

    bars_a = ax.barh(countries_a, cells_pct, color=colors_a, height=0.55, edgecolor="#0F172A", linewidth=0.6)
    for bar in bars_a:
        width = bar.get_width()
        ax.text(width + 1.2, bar.get_y() + bar.get_height() / 2, f"{width:.1f}%", va="center", fontsize=9.0, weight="bold", color="#1E293B")

    ax.set_xlim(0, 90)
    ax.set_xlabel("Celdas de 1 km² con Población Residente (%)", fontsize=10.0, labelpad=6)
    ax.set_title("A. Superficie Habitada en Mallas de 1 km² (Eurostat)", fontsize=11.0, weight="bold")

    # -------------------------------------------------------------
    # Panel B: Effective Residential Density in Inhabited Zones (hab/km²)
    # -------------------------------------------------------------
    ax = axes[1]
    densities = [737, 251, 348, 390, 175, 647]
    bars_b = ax.barh(countries_a, densities, color=colors_a, height=0.55, edgecolor="#0F172A", linewidth=0.6)
    for bar in bars_b:
        width = bar.get_width()
        ax.text(width + 12, bar.get_y() + bar.get_height() / 2, f"{width:,} hab/km²", va="center", fontsize=9.0, weight="bold", color="#1E293B")

    ax.set_xlim(0, 880)
    ax.set_xlabel("Densidad Demográfica Efectiva en Mallas Habitadas (hab/km²)", fontsize=10.0, labelpad=6)
    ax.set_title("B. Densidad Residencial Efectiva (Banco de España)", fontsize=11.0, weight="bold")

    # -------------------------------------------------------------
    # Panel C: Cumulative Housing Deficit 2021-2025 (% Households) - BdE Slide 29
    # -------------------------------------------------------------
    ax = axes[2]
    countries_c = ["Portugal", "Países Bajos", "España", "Italia", "Francia", "Alemania"]
    deficit_pct = [-7.0, -4.7, -3.9, -1.5, -0.02, 0.5]
    colors_c = ["#BE123C" if c == "España" else "#D97706" if v < 0 else "#0D9488" for c, v in zip(countries_c, deficit_pct)]

    bars_c = ax.bar(countries_c, deficit_pct, color=colors_c, width=0.55, edgecolor="#0F172A", linewidth=0.6)
    for bar in bars_c:
        height = bar.get_height()
        va_pos = "bottom" if height < 0 else "top"
        offset = -0.5 if height < 0 else 0.2
        val_str = f"{height:+.1f}%"
        if bar.get_x() == bars_c[2].get_x():  # Spain
            val_str = "-3.9% (-750k)"
        ax.text(bar.get_x() + bar.get_width() / 2, height + offset, val_str, ha="center", va=va_pos, fontsize=8.5, weight="bold", color="#1E293B")

    ax.axhline(0, color="#64748B", linewidth=1.0)
    ax.set_ylim(-8.5, 2.5)
    ax.set_ylabel("Déficit Acumulado (% Hogares Promedio)", fontsize=10.0)
    ax.set_title("C. Déficit de Vivienda vs. Hogares 2021-2025 (BdE Slide 29)", fontsize=11.0, weight="bold")

    # -------------------------------------------------------------
    # Panel D: Years of Net Income to Buy a Home (2024) - BdE Slide 43
    # -------------------------------------------------------------
    ax = axes[3]
    categories_d = ["Promedio Todos\nlos Hogares", "Inquilinos\nTotal Nacional", "Jóvenes en\nAlquiler", "Inquilinos Madrid,\nBCN y Málaga"]
    effort_years = [4.0, 6.8, 7.5, 10.0]
    colors_d = ["#0D9488", "#1E3A8A", "#D97706", "#BE123C"]

    bars_d = ax.bar(categories_d, effort_years, color=colors_d, width=0.55, edgecolor="#0F172A", linewidth=0.6)
    for bar in bars_d:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.25, f"{height:.1f} años", ha="center", fontsize=9.0, weight="bold", color="#1E293B")

    ax.axhline(4.5, color="#059669", linestyle=":", linewidth=1.2)
    ax.set_ylim(0, 11.8)
    ax.set_ylabel("Años de Renta Neta Familiar Necesarios", fontsize=10.0)
    ax.set_title("D. Años de Renta para Comprar Vivienda (BdE Slide 43)", fontsize=11.0, weight="bold")

    fig.suptitle(
        "Figure 1: Diagnóstico Territorial y de Oferta: Datos Oficiales Eurostat y Banco de España (Informe Anual 2025/2026)",
        fontsize=12.5, weight="bold", y=0.99
    )
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"[Clean Visualizer] Clean Figure 1 exported to: {output_path}")


if __name__ == "__main__":
    plot_figure_1_clean()
