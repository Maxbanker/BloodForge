"""
BloodForge v6.0 Visualization Module
Generates high-quality, publication-ready plots for cognitive-narrative stability,
entropy dynamics, collapse events, and action behavior.

Compatible with BF-CCSF v6.0 + Street/Prison Scrap Mod (SPSM v1.1)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple

sns.set_style("whitegrid")
plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12
})

class BloodForgeVisualizer:
    """Helper class for consistent BloodForge visualizations"""

    @staticmethod
    def plot_cognitive_timeline(
        df: pd.DataFrame,
        fighter_a_name: str,
        fighter_b_name: str,
        title: Optional[str] = None,
        save_path: Optional[str] = None,
        show_collapse: bool = True
    ):
        """
        Main timeline plot showing the five core operators + panic and collapse events.
        """
        fig, axs = plt.subplots(4, 1, figsize=(13, 11), sharex=True, 
                                height_ratios=[1.2, 1, 1.1, 0.7])

        # 1. Coherence Ω (most important stability metric)
        axs[0].plot(df["exchange"], df["a_omega"], label=f"{fighter_a_name} Ω", 
                    linewidth=2.5, color="#1f77b4")
        axs[0].plot(df["exchange"], df["b_omega"], label=f"{fighter_b_name} Ω", 
                    linewidth=2.5, color="#ff7f0e")
        axs[0].set_ylabel("Coherence (Ω)")
        axs[0].set_ylim(0, 1.05)
        axs[0].legend(loc="upper right")
        axs[0].grid(True, alpha=0.3)

        # 2. Drift Γ
        axs[1].plot(df["exchange"], df["a_gamma"], label=f"{fighter_a_name} Γ", 
                    linewidth=2.2, color="#1f77b4")
        axs[1].plot(df["exchange"], df["b_gamma"], label=f"{fighter_b_name} Γ", 
                    linewidth=2.2, color="#ff7f0e")
        axs[1].set_ylabel("Drift (Γ)")
        axs[1].set_ylim(0, 1.05)
        axs[1].legend(loc="upper left")
        axs[1].grid(True, alpha=0.3)

        # 3. Cognitive Veil V^cn + Panic
        axs[2].plot(df["exchange"], df["a_veil"], label=f"{fighter_a_name} Veil V^cn", 
                    linewidth=2.2, color="#1f77b4")
        axs[2].plot(df["exchange"], df["b_veil"], label=f"{fighter_b_name} Veil V^cn", 
                    linewidth=2.2, color="#ff7f0e")
        axs[2].plot(df["exchange"], df["a_panic"], '--', label=f"{fighter_a_name} Panic", 
                    alpha=0.75, color="#d62728")
        axs[2].plot(df["exchange"], df["b_panic"], '--', label=f"{fighter_b_name} Panic", 
                    alpha=0.75, color="#e377c2")
        axs[2].set_ylabel("Veil & Panic")
        axs[2].set_ylim(0, 1.05)
        axs[2].legend(loc="upper right", ncol=2)
        axs[2].grid(True, alpha=0.3)

        # 4. Collapse Events
        if show_collapse:
            collapses_a = df[df["a_collapse"] == True]
            collapses_b = df[df["b_collapse"] == True]

            if not collapses_a.empty:
                axs[3].scatter(collapses_a["exchange"], [1.0] * len(collapses_a),
                              label=f"{fighter_a_name} Collapse", color="#d62728", 
                              s=80, marker="x", linewidth=2)
            if not collapses_b.empty:
                axs[3].scatter(collapses_b["exchange"], [0.0] * len(collapses_b),
                              label=f"{fighter_b_name} Collapse", color="#e377c2", 
                              s=80, marker="x", linewidth=2)

            axs[3].set_yticks([0, 1])
            axs[3].set_yticklabels([fighter_b_name, fighter_a_name])
            axs[3].set_ylabel("Collapse Events")
            axs[3].legend(loc="upper right")
            axs[3].grid(True, alpha=0.2)

        fig.suptitle(title or f"BloodForge v6.0 — Cognitive-Narrative Dynamics\n{fighter_a_name} vs {fighter_b_name}", 
                     fontsize=15, y=0.98)
        plt.xlabel("Exchange")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")

        plt.show()

    @staticmethod
    def plot_action_distribution(
        df: pd.DataFrame,
        fighter_name: str,
        fighter_letter: str = "a"  # "a" or "b"
    ):
        """Bar chart showing action usage frequency"""
        action_col = f"action_{fighter_letter}"
        if action_col not in df.columns:
            print(f"Column {action_col} not found.")
            return

        actions = df[action_col].value_counts().sort_values(ascending=True)

        plt.figure(figsize=(11, 6))
        actions.plot(kind='barh', color="#2ca02c")
        plt.title(f"Action Distribution — {fighter_name}")
        plt.xlabel("Number of Times Used")
        plt.ylabel("Action")
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_regime_timeline(df: pd.DataFrame, title: Optional[str] = None):
        """Show how fight regimes evolved over time"""
        plt.figure(figsize=(12, 5))
        regime_map = {reg: i for i, reg in enumerate(df["regime"].unique())}
        numeric_regime = df["regime"].map(regime_map)

        plt.plot(df["exchange"], numeric_regime, linewidth=2, color="#9467bd", marker='o', markersize=4)
        plt.yticks(list(regime_map.values()), list(regime_map.keys()))
        plt.title(title or "Fight Regime Evolution")
        plt.xlabel("Exchange")
        plt.ylabel("Tempo Regime")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def compare_spsm_vs_base(df_spsm: pd.DataFrame, df_base: pd.DataFrame,
                             fighter_a_name: str, fighter_b_name: str):
        """Compare two runs (with vs without SPSM)"""
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # Coherence comparison
        axs[0].plot(df_spsm["exchange"], df_spsm["a_omega"], label=f"{fighter_a_name} (SPSM)", linewidth=2)
        axs[0].plot(df_base["exchange"], df_base["a_omega"], '--', label=f"{fighter_a_name} (Base)", linewidth=2)
        axs[0].set_ylabel("Coherence Ω (Fighter A)")
        axs[0].legend()

        # Collapse count summary
        collapses_spsm = len(df_spsm[df_spsm["a_collapse"]])
        collapses_base = len(df_base[df_base["a_collapse"]])
        axs[1].bar(["With SPSM", "Base Mode"], [collapses_spsm, collapses_base], color=["#d62728", "#1f77b4"])
        axs[1].set_ylabel("Collapse Events (Fighter A)")
        axs[1].set_title("Impact of Street/Prison Scrap Mod")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def save_all_plots(df: pd.DataFrame, fighter_a_name: str, fighter_b_name: str, prefix: str = "bloodforge"):
        """Convenience method to save multiple plots"""
        BloodForgeVisualizer.plot_cognitive_timeline(
            df, fighter_a_name, fighter_b_name,
            save_path=f"{prefix}_timeline.png"
        )
        BloodForgeVisualizer.plot_action_distribution(df, fighter_a_name, "a")
        BloodForgeVisualizer.plot_action_distribution(df, fighter_b_name, "b")
        BloodForgeVisualizer.plot_regime_timeline(df)