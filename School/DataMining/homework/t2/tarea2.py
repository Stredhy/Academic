import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter
from pathlib import Path

# ============================================================
# TAREA 2 - FIGURAS
# ============================================================

# Busca automáticamente el CSV:
# 1) en la misma carpeta del .py
# 2) en la carpeta padre
# 3) en la carpeta padre de la carpeta padre
BASE = Path(__file__).resolve().parent

possible_files = [
    BASE / "industry_dataset_structured.csv",
    BASE / "industry_dataset_structured.xlsx - industry_dataset_structured.csv",
    BASE.parent / "industry_dataset_structured.csv",
    BASE.parent.parent / "industry_dataset_structured.csv",
]

INPUT = next((p for p in possible_files if p.exists()), None)

if INPUT is None:
    print("No encontré el archivo CSV automáticamente.")
    print("Coloca 'industry_dataset_structured.csv' en la misma carpeta que este .py")
    print("o cambia la variable INPUT por la ruta de tu CSV.")
    input("Presiona Enter para cerrar...")
    raise SystemExit

OUT = BASE / "figuras_tarea2"
OUT.mkdir(parents=True, exist_ok=True)

print(f"Dataset encontrado: {INPUT}")
print(f"Resultados: {OUT}")

df = pd.read_csv(INPUT)

# ---------------------------
# Estilos indicados por el profesor
# ---------------------------
LINE_STYLE = {
    "Line_A": {"color": "#1f77b4", "marker": "o"},
    "Line_B": {"color": "#ff7f0e", "marker": "s"},
    "Line_C": {"color": "#2ca02c", "marker": "^"},
}

SHIFT_STYLE = {
    "Morning": {"color": "#9467bd", "linestyle": "-"},
    "Evening": {"color": "#8c564b", "linestyle": "--"},
    "Night": {"color": "#d62728", "linestyle": "-."},
}

SHIFT_ORDER = ["Morning", "Evening", "Night"]
LINE_ORDER = ["Line_A", "Line_B", "Line_C"]


def format_ax(ax, percent_y=False):
    ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.6)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#222222")
        spine.set_linewidth(1.2)

    if percent_y:
        ax.yaxis.set_major_formatter(PercentFormatter(1.0))


def save_fig(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ============================================================
# FIGURA 1
# ============================================================
print("Generando Figura 1...")

fig, ax = plt.subplots(figsize=(8, 5.5))

for line in LINE_ORDER:
    sub = df[df["Production_Line"] == line]

    ax.scatter(
        sub["Units_Produced"],
        sub["Defect_Rate"],
        color=LINE_STYLE[line]["color"],
        marker=LINE_STYLE[line]["marker"],
        edgecolor="black",
        linewidth=0.5,
        alpha=0.75,
        label=line
    )

ax.set_title("Fig. 1: Units_Produced vs Defect_Rate")
ax.set_xlabel("Units_Produced")
ax.set_ylabel("Defect_Rate")
format_ax(ax, percent_y=True)
ax.legend(title="Production_Line")

save_fig(fig, "Figura_01.png")


# ============================================================
# FIGURA 2
# ============================================================
print("Generando Figura 2...")

x = df["Energy_Consumption_kWh"].to_numpy()
y = df["Revenue_USD"].to_numpy()

r = np.corrcoef(x, y)[0, 1]

coef = np.polyfit(x, y, 1)
xx = np.linspace(x.min(), x.max(), 200)
yy = coef[0] * xx + coef[1]

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.scatter(
    x, y,
    color="#90c97a",
    edgecolor="black",
    linewidth=0.5,
    alpha=0.75,
    label="Observaciones"
)

ax.plot(
    xx, yy,
    "--",
    color="#333333",
    linewidth=2,
    label="Tendencia (OLS)"
)

ax.set_title(f"Fig. 2: Energía vs Ingresos (r = {r:.2f})")
ax.set_xlabel("Energy_Consumption_kWh")
ax.set_ylabel("Revenue_USD")
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
format_ax(ax)
ax.legend()

save_fig(fig, "Figura_02.png")


# ============================================================
# FIGURA 3
# ============================================================
print("Generando Figura 3...")

mean_def = df["Defect_Rate"].mean()
median_def = df["Defect_Rate"].median()

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.hist(
    df["Defect_Rate"],
    bins=20,
    color="#9ecae1",
    edgecolor="#1f4e79",
    linewidth=1
)

ax.axvline(
    mean_def,
    color="green",
    linestyle="--",
    linewidth=2,
    label=f"Media = {mean_def:.2%}"
)

ax.axvline(
    median_def,
    color="red",
    linestyle="-.",
    linewidth=2,
    label=f"Mediana = {median_def:.2%}"
)

ax.set_title("Fig. 3: Distribución de Defect_Rate")
ax.set_xlabel("Defect_Rate")
ax.set_ylabel("Frecuencia")
ax.xaxis.set_major_formatter(PercentFormatter(1.0))
format_ax(ax)
ax.legend()

save_fig(fig, "Figura_03.png")


# ============================================================
# FIGURA 4
# ============================================================
print("Generando Figura 4...")

p90 = df["Downtime_Minutes"].quantile(0.90)
p95 = df["Downtime_Minutes"].quantile(0.95)

counts, edges = np.histogram(
    df["Downtime_Minutes"],
    bins=15
)

mode_bin = int(np.argmax(counts))
mode_center = (edges[mode_bin] + edges[mode_bin + 1]) / 2

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.hist(
    df["Downtime_Minutes"],
    bins=15,
    color="#f28e2b",
    edgecolor="#1a1a1a",
    linewidth=1.2,
    label="Frecuencia"
)

ax.axvline(
    mode_center,
    color="green",
    linestyle="--",
    linewidth=2,
    label=f"Moda (bin) = {mode_center:.1f}"
)

ax.axvline(
    p90,
    color="blue",
    linestyle=":",
    linewidth=2,
    label=f"P90 = {p90:.1f}"
)

ax.axvline(
    p95,
    color="red",
    linestyle="-.",
    linewidth=2,
    label=f"P95 = {p95:.1f}"
)

ax.axvspan(
    p95,
    df["Downtime_Minutes"].max(),
    color="red",
    alpha=0.15,
    label="Cola derecha"
)

ax.set_title("Fig. 4: Distribución de Downtime_Minutes")
ax.set_xlabel("Downtime_Minutes")
ax.set_ylabel("Frecuencia")
format_ax(ax)
ax.legend()

save_fig(fig, "Figura_04.png")


# ============================================================
# FIGURA 5
# ============================================================
print("Generando Figura 5...")

stats = df.groupby("Production_Line")["Units_Produced"].agg(
    ["mean", "std", "count"]
)

stats["se"] = stats["std"] / np.sqrt(stats["count"])
stats = stats.sort_values("mean")

fig, ax = plt.subplots(figsize=(8, 5.5))

bars = ax.bar(
    stats.index,
    stats["mean"],
    yerr=stats["se"],
    capsize=5,
    color=[LINE_STYLE[x]["color"] for x in stats.index],
    edgecolor="black"
)

ax.set_title("Fig. 5: Productividad promedio por línea (±EE)")
ax.set_xlabel("Production_Line")
ax.set_ylabel("Units_Produced (promedio)")
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
format_ax(ax)

for bar, value in zip(bars, stats["mean"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:,.1f}",
        ha="center",
        va="bottom"
    )

save_fig(fig, "Figura_05.png")


# ============================================================
# FIGURA 6
# ============================================================
print("Generando Figura 6...")

stats = df.groupby("Shift")["Revenue_USD"].agg(
    ["mean", "std", "count"]
)

stats["se"] = stats["std"] / np.sqrt(stats["count"])
stats = stats.reindex(SHIFT_ORDER)

fig, ax = plt.subplots(figsize=(8, 5.5))

bars = ax.bar(
    stats.index,
    stats["mean"],
    yerr=stats["se"],
    capsize=5,
    color=[SHIFT_STYLE[x]["color"] for x in stats.index],
    edgecolor="black"
)

ax.set_title("Fig. 6: Ingresos promedio por turno (±EE)")
ax.set_xlabel("Shift")
ax.set_ylabel("Revenue_USD (promedio)")
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
format_ax(ax)

for bar, value in zip(bars, stats["mean"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:,.0f}",
        ha="center",
        va="bottom"
    )

save_fig(fig, "Figura_06.png")


# ============================================================
# FIGURA 7
# ============================================================
print("Generando Figura 7...")

data = [
    df.loc[df["Shift"] == shift, "Cost_per_Unit"]
    for shift in SHIFT_ORDER
]

fig, ax = plt.subplots(figsize=(8, 5.5))

bp = ax.boxplot(
    data,
    tick_labels=SHIFT_ORDER,
    notch=True,
    patch_artist=True,
    showfliers=True
)

for patch, shift in zip(bp["boxes"], SHIFT_ORDER):
    patch.set_facecolor(SHIFT_STYLE[shift]["color"])
    patch.set_alpha(0.45)

for median in bp["medians"]:
    median.set_color("black")
    median.set_linewidth(2)

ax.set_title("Fig. 7: Cost_per_Unit por Shift (Boxplot)")
ax.set_xlabel("Shift")
ax.set_ylabel("Cost_per_Unit")
format_ax(ax)

save_fig(fig, "Figura_07.png")


# ============================================================
# FIGURA 8
# ============================================================
print("Generando Figura 8...")

fig, ax = plt.subplots(figsize=(9, 5.8))

data = []
positions = []
labels = []

for i, line in enumerate(LINE_ORDER, start=1):

    for j, shift in enumerate(SHIFT_ORDER):

        values = df.loc[
            (df["Production_Line"] == line)
            & (df["Shift"] == shift),
            "Defect_Rate"
        ]

        data.append(values)
        positions.append(i + (j - 1) * 0.22)
        labels.append((line, shift))

bp = ax.boxplot(
    data,
    positions=positions,
    widths=0.18,
    patch_artist=True,
    showfliers=True
)

for patch, (_, shift) in zip(bp["boxes"], labels):
    patch.set_facecolor(SHIFT_STYLE[shift]["color"])
    patch.set_alpha(0.55)

for median in bp["medians"]:
    median.set_color("black")
    median.set_linewidth(1.8)

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(LINE_ORDER)

ax.set_title("Fig. 8: Defect_Rate por línea y turno (Boxplots)")
ax.set_xlabel("Production_Line")
ax.set_ylabel("Defect_Rate")
ax.yaxis.set_major_formatter(PercentFormatter(1.0))

format_ax(ax)

handles = [
    plt.Line2D(
        [0], [0],
        color=SHIFT_STYLE[s]["color"],
        lw=6,
        alpha=0.55,
        label=s
    )
    for s in SHIFT_ORDER
]

ax.legend(handles=handles, title="Shift")

save_fig(fig, "Figura_08.png")


# ============================================================
# FIGURA 9 - KDE
# ============================================================
print("Generando Figura 9...")

values = df["Energy_Consumption_kWh"].dropna().to_numpy()

grid = np.linspace(values.min(), values.max(), 300)

n = len(values)
std = values.std(ddof=1)
h = 1.06 * std * n ** (-1 / 5)

if h <= 0:
    h = 1.0

density = np.exp(
    -0.5 * ((grid[:, None] - values[None, :]) / h) ** 2
).sum(axis=1)

density /= n * h * np.sqrt(2 * np.pi)

mean_energy = values.mean()
median_energy = np.median(values)

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.plot(
    grid,
    density,
    color="#555555",
    linewidth=2,
    label="KDE"
)

ax.fill_between(
    grid,
    density,
    alpha=0.18
)

ax.axvline(
    mean_energy,
    color="green",
    linestyle="--",
    linewidth=2,
    label=f"Media = {mean_energy:.2f}"
)

ax.axvline(
    median_energy,
    color="red",
    linestyle="-.",
    linewidth=2,
    label=f"Mediana = {median_energy:.2f}"
)

ax.set_title("Fig. 9: Densidad de Energy_Consumption_kWh")
ax.set_xlabel("Energy_Consumption_kWh")
ax.set_ylabel("Densidad")

format_ax(ax)
ax.legend()

save_fig(fig, "Figura_09.png")


# ============================================================
# FIGURA 10 - HEATMAP
# ============================================================
print("Generando Figura 10...")

numeric_cols = [
    "Units_Produced",
    "Defect_Rate",
    "Energy_Consumption_kWh",
    "Worker_Count",
    "Downtime_Minutes",
    "Temperature_C",
    "Pressure_Bar",
    "Cost_per_Unit",
    "Revenue_USD"
]

corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(
    corr,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))

ax.set_xticklabels(numeric_cols, rotation=90)
ax.set_yticklabels(numeric_cols)

for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        ax.text(
            j,
            i,
            f"{corr.iloc[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=7
        )

cbar = fig.colorbar(im, ax=ax)
cbar.set_label("Correlation (r)")

ax.set_title("Fig. 10: Heatmap de correlación")

fig.tight_layout()
fig.savefig(
    OUT / "Figura_10.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close(fig)


# ============================================================
# FIGURA 11
# ============================================================
print("Generando Figura 11...")

group = df.groupby(
    ["Batch", "Production_Line"]
)["Units_Produced"].agg(
    ["mean", "std", "count"]
)

group["se"] = group["std"] / np.sqrt(group["count"])

fig, ax = plt.subplots(figsize=(9, 5.8))

for line in LINE_ORDER:

    sub = group.xs(line, level="Production_Line").reset_index()
    sub = sub.sort_values("Batch")

    ax.plot(
        sub["Batch"],
        sub["mean"],
        color=LINE_STYLE[line]["color"],
        marker=LINE_STYLE[line]["marker"],
        linewidth=1.8,
        label=line
    )

    ax.fill_between(
        sub["Batch"],
        sub["mean"] - sub["se"],
        sub["mean"] + sub["se"],
        color=LINE_STYLE[line]["color"],
        alpha=0.12
    )

    last = sub.iloc[-1]

    ax.annotate(
        f"{line}: {last['mean']:.0f}",
        (last["Batch"], last["mean"]),
        xytext=(6, 0),
        textcoords="offset points",
        fontsize=8
    )

ax.set_title("Fig. 11: Tendencias Units_Produced por Línea (±EE)")
ax.set_xlabel("Batch")
ax.set_ylabel("Units_Produced (media)")

format_ax(ax)
ax.legend(title="Production_Line")

save_fig(fig, "Figura_11.png")


# ============================================================
# FIGURAS 12-15 EN UN SOLO LIENZO 2x2
# ============================================================
print("Generando Figuras 12-15...")

fig, axes = plt.subplots(
    2,
    2,
    figsize=(14, 10)
)


# ------------------------------------------------------------
# FIGURA 12
# ------------------------------------------------------------
ax = axes[0, 0]

for shift in SHIFT_ORDER:

    values = df.loc[
        df["Shift"] == shift,
        "Temperature_C"
    ].dropna().to_numpy()

    grid = np.linspace(values.min(), values.max(), 250)

    n = len(values)
    std = values.std(ddof=1)

    h = 1.06 * std * n ** (-1 / 5)

    if h <= 0:
        h = 0.1

    density = np.exp(
        -0.5 * ((grid[:, None] - values[None, :]) / h) ** 2
    ).sum(axis=1)

    density /= n * h * np.sqrt(2 * np.pi)

    ax.plot(
        grid,
        density,
        color=SHIFT_STYLE[shift]["color"],
        linestyle=SHIFT_STYLE[shift]["linestyle"],
        linewidth=2,
        label=shift
    )

ax.set_title("Fig. 12: Densidad de Temperature_C por Shift")
ax.set_xlabel("Temperature_C")
ax.set_ylabel("Densidad")

format_ax(ax)
ax.legend(title="Shift")


# ------------------------------------------------------------
# FIGURA 13
# ------------------------------------------------------------
ax = axes[0, 1]

pivot = df.pivot_table(
    index="Batch",
    columns="Shift",
    values="Units_Produced",
    aggfunc="sum"
).fillna(0)

pivot = pivot.reindex(columns=SHIFT_ORDER)

ax.stackplot(
    pivot.index,
    [pivot[s] for s in SHIFT_ORDER],
    labels=SHIFT_ORDER,
    colors=[SHIFT_STYLE[s]["color"] for s in SHIFT_ORDER],
    alpha=0.75
)

ax.set_title("Fig. 13: Área apilada Units_Produced por Shift (Batch)")
ax.set_xlabel("Batch")
ax.set_ylabel("Units_Produced (suma)")

format_ax(ax)
ax.legend(title="Shift", loc="upper left")


# ------------------------------------------------------------
# FIGURA 14
# ------------------------------------------------------------
ax = axes[1, 0]

counts = pd.crosstab(
    df["Production_Line"],
    df["Shift"]
).reindex(
    index=LINE_ORDER,
    columns=SHIFT_ORDER,
    fill_value=0
)

percentages = counts.div(
    counts.sum(axis=1),
    axis=0
) * 100

bottom = np.zeros(len(percentages))

for shift in SHIFT_ORDER:

    values = percentages[shift].to_numpy()

    ax.bar(
        percentages.index,
        values,
        bottom=bottom,
        color=SHIFT_STYLE[shift]["color"],
        label=shift,
        edgecolor="white",
        linewidth=0.6
    )

    for i, value in enumerate(values):

        if value >= 8:

            ax.text(
                i,
                bottom[i] + value / 2,
                f"{value:.0f}%",
                ha="center",
                va="center",
                fontsize=9
            )

    bottom += values

ax.set_title("Fig. 14: Composición de Turnos por Línea (%)")
ax.set_xlabel("Production_Line")
ax.set_ylabel("% de registros")
ax.set_ylim(0, 100)

format_ax(ax)
ax.legend(title="Shift")


# ------------------------------------------------------------
# FIGURA 15
# ------------------------------------------------------------
ax = axes[1, 1]

for line in LINE_ORDER:

    sub = df[df["Production_Line"] == line]

    ax.scatter(
        sub["Units_Produced"],
        sub["Revenue_USD"],
        color=LINE_STYLE[line]["color"],
        marker=LINE_STYLE[line]["marker"],
        edgecolor="black",
        linewidth=0.5,
        alpha=0.75,
        label=line
    )

ax.set_title("Fig. 15: Units_Produced vs Revenue_USD (por línea)")
ax.set_xlabel("Units_Produced")
ax.set_ylabel("Revenue_USD")

ax.yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

format_ax(ax)
ax.legend(title="Production_Line")


fig.tight_layout()

fig.savefig(
    OUT / "Figuras_12_15_2x2.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# RESULTADOS
# ============================================================

corr_prod_def = df["Units_Produced"].corr(
    df["Defect_Rate"]
)

corr_energy_rev = df["Energy_Consumption_kWh"].corr(
    df["Revenue_USD"]
)

corr_prod_rev = df["Units_Produced"].corr(
    df["Revenue_USD"]
)

print()
print("=" * 60)
print("TAREA 2 TERMINADA")
print("=" * 60)

print(f"Correlación producción-defectos: {corr_prod_def:.3f}")
print(f"Correlación energía-ingresos:    {corr_energy_rev:.3f}")
print(f"Correlación producción-ingresos: {corr_prod_rev:.3f}")

print()
print("Archivos generados en:")
print(OUT)

print()
print("Archivos:")
for file in sorted(OUT.iterdir()):
    print(" -", file.name)

input("\nPresiona Enter para cerrar...")
