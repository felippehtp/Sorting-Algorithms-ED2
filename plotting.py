import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns

# Load benchmark data
df = pd.read_csv("benchmark_results.csv")

# Map array types to scenario labels
df["Cenário"] = df["Array Type"].map(
    {
        "Random": "Aleatório",
        "Inverse": "Inverso",
    }
)

# Visual configuration
sns.set_theme(style="whitegrid")
plt.rcParams.update(
    {
        "font.size": 10,
        "font.family": "serif",
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "grid.alpha": 0.4,
    }
)

# Color palette
cores_algoritmos = {
    "Quick Sort": "#C82828",
    "Heap Sort": "#15803D",
    "Radix Sort": "#1D4ED8",
}

# Unique geometric marker per algorithm
marcadores_algoritmos = {
    "Quick Sort": "o",
    "Heap Sort": "^",
    "Radix Sort": "s",
}

# Line style per scenario
estilos_linha = {
    "Aleatório": "-",
    "Inverso": "--",
}

# 3. Create 2x2 subplot layout
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

metrics = [
    (
        "Time",
        "Tempo (ms)",
        "(A) Tempo de Execução",
        axes[0, 0],
    ),
    (
        "Memory",
        "Memória (MB)",
        "(B) Consumo de Memória",
        axes[0, 1],
    ),
    (
        "Comparisons",
        "Comparações",
        "(C) Quantidade de Comparações",
        axes[1, 0],
    ),
    (
        "Changes",
        "Trocas",
        "(D) Quantidade de Trocas",
        axes[1, 1],
    ),
]

# Plotting loop
for y_col, y_label, title, ax in metrics:
    for algo, color in cores_algoritmos.items():
        for cenario, style in estilos_linha.items():
            sub_df = df[(df["Algorithm"] == algo) & (df["Cenário"] == cenario)]

            ax.plot(
                sub_df["Size"],
                sub_df[y_col],
                color=color,
                marker=marcadores_algoritmos[algo],
                linestyle=style,
                linewidth=1.8,
                markersize=6,
                markeredgecolor="white",
                markeredgewidth=0.5,
            )

    ax.set_title(title, fontweight="bold", pad=8)
    ax.set_xlabel("Tamanho (N)")
    ax.set_ylabel(y_label)

# Top legend
legend_elements = [
    Line2D(
        [0],
        [0],
        color="#C82828",
        marker="o",
        linewidth=1.8,
        label="Quick Sort",
    ),
    Line2D(
        [0],
        [0],
        color="#15803D",
        marker="^",
        linewidth=1.8,
        label="Heap Sort",
    ),
    Line2D(
        [0],
        [0],
        color="#1D4ED8",
        marker="s",
        linewidth=1.8,
        label="Radix Sort",
    ),
    Line2D(
        [0],
        [0],
        color="#444444",
        linestyle="-",
        linewidth=1.8,
        label="Aleatório",
    ),
    Line2D(
        [0],
        [0],
        color="#444444",
        linestyle="--",
        linewidth=1.8,
        label="Inverso",
    ),
]

fig.legend(
    handles=legend_elements,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.02),
    ncol=5,
    frameon=True,
    facecolor="white",
    edgecolor="none",
)

plt.tight_layout()

# Save output files
plt.savefig(
    "graficos_desempenho.pdf",
    format="pdf",
    bbox_inches="tight",
    dpi=300,
)
plt.savefig(
    "graficos_desempenho.png",
    format="png",
    bbox_inches="tight",
    dpi=300,
)
plt.show()
