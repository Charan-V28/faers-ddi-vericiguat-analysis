import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def generate_forest_plot():
    project_root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
    csv_path = project_root / "data" / "processed" / "ddi_signals_summary.csv"

    if not csv_path.exists():
        print(f"File not found: {csv_path}. Please run src/statistics.py first.")
        return

    df = pd.read_csv(csv_path)

    # Sort so strongest ROR appears at top
    df = df.sort_values(by="ROR", ascending=True)

    plt.figure(figsize=(10, 6), dpi=300)
    
    # Calculate error bar distances from center ROR
    left_err = df["ROR"] - df["ROR_CI_Lower"]
    right_err = df["ROR_CI_Upper"] - df["ROR"]
    xerr = [left_err.values, right_err.values]

    # Plot error bars (fixed keyword formatting)
    plt.errorbar(
        x=df["ROR"], 
        y=df["Concomitant_Drug"], 
        xerr=xerr, 
        fmt='o', 
        color='#1f77b4', 
        ecolor='#1f77b4', 
        capsize=5, 
        markersize=8,
        label='ROR (95% CI)'
    )

    # Add vertical null hypothesis threshold line at ROR = 1.0
    plt.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, label='Null Line (ROR = 1.0)')

    plt.xlabel('Reporting Odds Ratio (ROR)', fontsize=12, fontweight='bold')
    plt.ylabel('Concomitant Drug (Co-administered with Vericiguat)', fontsize=12, fontweight='bold')
    plt.title('Disproportionality Forest Plot: Hypotension Risk in FAERS', fontsize=14, fontweight='bold', pad=15)
    plt.grid(axis='x', linestyle=':', alpha=0.6)
    plt.legend(loc='lower right')
    plt.tight_layout()

    output_fig = project_root / "data" / "processed" / "forest_plot_ror.png"
    plt.savefig(output_fig)
    print(f"Saved Forest Plot figure to {output_fig}")
    plt.show()

if __name__ == "__main__":
    generate_forest_plot()